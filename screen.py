import sys
sys.path.append("./dll/")
import time
import keyboard
import pydxshot
import cv2
import random
import string
import threading
from threading import Event
from ctypes import WinDLL
from utils import CONFIG
import numpy as np
import ctypes
import ctypes.wintypes as wintypes

class aim:
    
    WH_MOUSE_LL = 14
    WM_MOUSEMOVE = 0x0200
    
    LowLevelMouseProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
    
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    
    SetWindowsHookEx = user32.SetWindowsHookExW
    SetWindowsHookEx.argtypes = [ctypes.c_int, LowLevelMouseProc, wintypes.HINSTANCE, wintypes.DWORD]
    SetWindowsHookEx.restype = wintypes.HHOOK
    
    UnhookWindowsHookEx = user32.UnhookWindowsHookEx
    UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
    UnhookWindowsHookEx.restype = wintypes.BOOL
    
    CallNextHookEx = user32.CallNextHookEx
    CallNextHookEx.argtypes = [wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
    CallNextHookEx.restype = ctypes.c_int
    
    GetModuleHandle = kernel32.GetModuleHandleW
    GetModuleHandle.argtypes = [wintypes.LPCWSTR]
    GetModuleHandle.restype = wintypes.HINSTANCE
    
    hook = None
    
    def hook_callback(nCode, wParam, lParam):
        if nCode >= 0 and wParam == aim.WM_MOUSEMOVE:
            return 1  # Block mouse movement
        return aim.CallNextHookEx(hook, nCode, wParam, lParam)
    
    HookCallback = LowLevelMouseProc(hook_callback)
    
    def disable_mouse_movement():
        global hook
        h_module = aim.GetModuleHandle(None)
        hook = aim.SetWindowsHookEx(aim.WH_MOUSE_LL, aim.HookCallback, h_module, 0)

(user32, kernel32, shcore) = (
    WinDLL('user32', use_last_error=True),
    WinDLL('kernel32', use_last_error=True),
    WinDLL('shcore', use_last_error=True)
)

shcore.SetProcessDpiAwareness(2)

(WIDTH, HEIGHT) = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

KEY_MAPPING = {
    'a': 'd',
    'd': 'a',
    'w': 's',
    's': 'w'
}

class triggerbot:
    def __init__(self):
        self.config = self.start_config()
        self.previous_fps = self.config.target_fps
        self.previous_zone = self.config.GRAB_ZONE
        self.cam = pydxshot.create(output_color='BGR')
        self.adjusting = 1
        self.img = None
        self.yes = False
        self.trigger_times = 0
        self.filter_delay = 0.0
        self.real_one = 0.0
        self.stop_event = Event()
        
    def start_config(self):
        return CONFIG()

    def start_threads(self):
        self.stop_event.clear()
        self.thread1 = threading.Thread(target=self.lastandfilter, daemon=True)
        self.thread2 = threading.Thread(target=self.running, daemon=True)
        self.thread1.start()
        self.thread2.start()

    def stop_threads(self):
        self.stop_event.set()
        self.thread1.join()
        self.thread2.join()
        
    def restart_threads(self):
        self.stop_threads()
        self.start_threads()

    @staticmethod
    def randomgen(size=12, chars=string.ascii_uppercase + string.digits):
        return ''.join((random.choice(chars) for _ in range(size)))

    def lastframe(self):
        image = self.cam.get_latest_frame()
        if image is not None:
            self.img = image
            self.start = time.perf_counter()
            
    def filterimage(self):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.config.low_color, self.config.high_color)
        kernel = np.ones((3, 3), np.uint8)
        dilated_mask = cv2.dilate(mask, kernel, iterations=self.config.detection_threshold)
        self.yes = cv2.countNonZero(dilated_mask) != 0

    def is_pressed_excluding_tab(self, key):
        return keyboard.is_pressed(key) and not keyboard.is_pressed('tab')

    def lastandfilter(self):
        while not self.stop_event.is_set():
            if self.config.not1shot:
                while (self.is_pressed_excluding_tab(self.config.hotkey_trigger) or self.is_pressed_excluding_tab(self.config.vandal_ht)):
                    if not self.cam.is_capturing:
                        self.cam.start(target_fps=self.config.target_fps, video_mode=True, region=self.config.GRAB_ZONE)
                    if self.cam.is_capturing:
                        self.lastframe()
                        self.filterimage()
            else:
                while self.is_pressed_excluding_tab(self.config.hotkey_trigger):
                    if not self.cam.is_capturing:
                        self.cam.start(target_fps=self.config.target_fps, video_mode=True, region=self.config.GRAB_ZONE)
                    if self.cam.is_capturing:
                        self.lastframe()
                        self.filterimage()
            if self.cam.is_capturing:
                self.cam.stop()
            time.sleep(0.1)

    def apply_cooldown(self):
        self.real_one = time.perf_counter() - self.start
        if self.real_one < self.config.initial_num:
            additional_delay = self.randomizedelay() - self.real_one
            time.sleep(additional_delay)
            
    def searcherino(self):
        if self.yes:
            if self.config.aim:
                aim.disable_mouse_movement()
            held = []
            if self.config.counterstrafe:
                if self.is_pressed_excluding_tab('a') and not self.is_pressed_excluding_tab('d'):
                    keyboard.press('d')
                    held.append('d')
                    time.sleep(0.1)
                elif self.is_pressed_excluding_tab('s') and not self.is_pressed_excluding_tab('w'):
                    keyboard.press('w')
                    held.append('w')
                    time.sleep(0.1)
                elif self.is_pressed_excluding_tab('d') and not self.is_pressed_excluding_tab('a'):
                    keyboard.press('a')
                    held.append('a')
                    time.sleep(0.1)
                elif self.is_pressed_excluding_tab('w') and not self.is_pressed_excluding_tab('s'):
                    keyboard.press('s')
                    held.append('s')
                    time.sleep(0.1)
            self.apply_cooldown()
            keyboard.press(self.config.shoot_key)
            time.sleep(self.randomizedelaytoshoot())
            aim.UnhookWindowsHookEx(hook)
            keyboard.release(self.config.shoot_key)
            for cap in held:
                time.sleep(0.2)
                keyboard.release(cap)
            self.trigger_times += 1
            time.sleep(self.config.cooldowntime / 10)

    def hold(self):
        self.start_threads()
        
    def running(self):
        while not self.stop_event.is_set():
            if self.config.not1shot:
                while (self.is_pressed_excluding_tab(self.config.hotkey_trigger) or self.is_pressed_excluding_tab(self.config.vandal_ht)):
                    self.searcherino()
                    time.sleep(0.001)
            else:
                while self.is_pressed_excluding_tab(self.config.hotkey_trigger):
                    self.searcherino()
                    time.sleep(0.001)
            time.sleep(0.1)

    def randomizedelay(self):
        return random.uniform(self.config.initial_num, self.config.last_num)
    
    def randomizedelaytoshoot(self):
        if self.config.not1shot and self.is_pressed_excluding_tab(self.config.vandal_ht):
            return random.uniform(0.12, 0.17)
        else:
            return random.uniform(0.06, 0.08)
#610cb69f703a6aa8c04db9030d254580
#38f93e4ce3b151953a83b631d5f48cce
#269ab8531eb3991cb79ebb7df6136eaa
#c4362ca684a6230bbdc6009bb1669c58
#09f4e2209e007a1d4fc960342694cfda
#f5da1a0b5a5b7e5062b8282f31c204ad
#d38d2ad04f882007b71a758535b2d1b5
#88ded58ee1964891ca8db331575804b4
#125a4333fc4131e85f8f083c54d4f937
#3501308012b0848a5d5184d9a989ed2c
#81bbd398d54509be0d66994475e75018
#88823c6b86f4184f8d86bc4ff6be81d3
#e5eb686e5dd3749451a6e66a730ee672
#81eb57c51dc24dbae8122e72d6524661
#acda64531b437427421e4e4a050a7104
#b4a3e1872abb5a66d8ac750d9e10483b
#dede3eee09afe8980368dba8c85a1ebb
#44a37771ae44f91ce571a73a635e6f29
#338115094188453d7667d1bc59fce04a
#949b5ba846aea20194463ad05a328312
#3bf7538aa66be70c25410beb9d3c2196
#69d96dd9e9328fe81adf51559ecb10fc
#51865c0224ac888182abf5aded3bf2ff
#0060b96edb1ec4e3e766604a0248f587
#c8957661c266a2df154cdd8f6a87144e
#75ecc5a6c3e492eea85fc172c9481b62
#42e525ab5f16ae306b842a30fe4094cb
#6a9eef145716332750af033e52667226
#3934ba4f42065625c6d5f8bc890f45f9
#1c51e54c9b42840cf9a007b2f6d6dd08
#357f2c07fbff6a7c775a4c8bf1f3856c
#295b2fc18f372e99feeb5d585bb69c96
#2eca4cda5e80a4db2a7563535fb6b96b
#9956de783f09b9dd5527527c7e550838
#3dfc0511aa57fced54c2b1454d71cb89
#3802e0f5513261c8896be0bccb783407
#36b5c5c997da0e8e59155c385aaefc39
#db6160d265a071485e875c94ae2d65a2
#9b04912a89cb63dd6eb54bd4559347db
#c95bfa3c13549cc09bbd3bf2dcf2f84f