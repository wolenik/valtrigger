import dearpygui.dearpygui as dpg
import keyboard
import threading
import string
import random
from screen import triggerbot
import sys
import hashlib
import ctypes
from ctypes import c_int
import time
dwm = ctypes.windll.dwmapi
import win32gui
import win32con

class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", c_int),
                ("cxRightWidth", c_int),
                ("cyTopHeight", c_int),
                ("cyBottomHeight", c_int)
               ]

UNICODE_MAPPING = {
    dpg.mvKey_Tab: 'tab',
    dpg.mvKey_Capital: "capslock",
    dpg.mvKey_Shift: 'shift',
    dpg.mvKey_Control: 'control',
    dpg.mvKey_Alt: 'alt',
    dpg.mvKey_F1: 'f1',
    dpg.mvKey_F2: 'f2',
    dpg.mvKey_F3: 'f3',
    dpg.mvKey_F4: 'f4',
    dpg.mvKey_F5: 'f5',
    dpg.mvKey_F6: 'f6',
    dpg.mvKey_F7: 'f7',
    dpg.mvKey_F8: 'f8',
    dpg.mvKey_F9: 'f9',
    dpg.mvKey_F10: 'f10',
    dpg.mvKey_F11: 'f11',
    dpg.mvKey_F12: 'f12',
    dpg.mvKey_Insert: "insert"
}

viewport = None
title_bar_drag = False
shoot_key = False
trigger_key = False
vandal_key = False
aimkey = False
min_delay = 0
max_delay = 0
slider1 = None
slider2 = None
trigger = triggerbot()
config = trigger.config
previous_zone = config.ZONE
quad = None
key_press_handler_id = None
logged = False

def exit():
    sys.exit()

def change_hotkey(sender, app_data):
    global shoot_key, trigger_key, vandal_key, aimkey
    unregister_key_press_handler()
    key = UNICODE_MAPPING.get(app_data, chr(app_data))
    if key in {config.shoot_key, config.hotkey_trigger, config.vandal_ht}:
        dpg.configure_item(item=alreadykey, show=True)
        return
    if shoot_key:
        config.shoot_key = key
        dpg.set_value("shoot_hotkey", f"Shoot Key: {key}")
        shoot_key = False
    elif trigger_key:
        config.hotkey_trigger = key
        dpg.set_value("trigger_hotkey", f"Trigger Key: {key}")
        trigger_key = False
    elif vandal_key:
        config.vandal_ht = key
        dpg.set_value("vandal_ht", f"Vandal Key: {key}")
    elif aimkey:
        config.aimkey = key
        dpg.set_value("aimkey", f"Aim Key: {key}")
        aimkey = False
    
def handle_key_press(sender, app_data):
    change_hotkey(sender, app_data)

def register_key_press_handler():
    global key_press_handler_id
    with dpg.handler_registry():
        key_press_handler_id = dpg.add_key_press_handler(callback=handle_key_press)

def unregister_key_press_handler():
    if key_press_handler_id:
        dpg.delete_item(key_press_handler_id)

def trigger_key_callback():
    global trigger_key
    trigger_key = True
    register_key_press_handler()
    
def shoot_key_callback():
    global shoot_key
    shoot_key = True
    register_key_press_handler()

def vandal_key_callback():
    global vandal_key
    vandal_key = True
    register_key_press_handler()

def aim_key_callback():
    global aimkey
    aimkey = True
    register_key_press_handler()

def randomgen(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join((random.choice(chars) for _ in range(size)))

def update_zone_from_slider(sender, attribute):
    value = dpg.get_value(sender)
    setattr(config, attribute, value)
    config.GRAB_ZONE = (
        int(config.width / 2 - value),
        int(config.height / 2 - value),
        int(config.width / 2 + value),
        int(config.height / 2 + value)
    )
    if config.fov:
        show_fov(None, False)
        show_fov(None, True)

def update_config(sender, attribute):
    value = dpg.get_value(sender)
    setattr(config, attribute, value)
    
def login_callback(sender):
    global logged
    license_key = dpg.get_value("##license_input")
    logged = True
    if logged:
        dpg.set_value("##status_text", "Login successful")
        show_main_menu()
        trigger.hold()
    else:
        dpg.set_value("##status_text", "Login failed")

def show_fov(sender, data):
    global quad
    try:
        true = dpg.get_value(data)
    except:
        true = data
    zone = dpg.get_value(slider3)
    grab_zone = (
        int(config.width / 2 - zone), int(config.height / 2 - zone),
        int(config.width / 2 + zone), int(config.height / 2 + zone)
    )
    p1 = (grab_zone[0], grab_zone[1])
    p2 = (grab_zone[2], grab_zone[1])
    p3 = (grab_zone[2], grab_zone[3])
    p4 = (grab_zone[0], grab_zone[3])
    if data:
        quad = dpg.draw_quad(p1, p2, p3, p4, color=(255, 255, 255, 255), parent="FOV")
        config.fov = True
    elif ~data and dpg.does_item_exist(quad):
        dpg.delete_item(quad)
        config.fov = False

def show_main_menu():
    dpg.configure_item(win, show=True)
    dpg.configure_item(login_window, show=False)

def change_title():
    while True:
        time.sleep(1)
        dpg.configure_viewport(viewport, title=randomgen())

def restart_tg():
    trigger.restart_threads()

def set_config_legit():
    config.counterstrafe = True
    config.cooldowntime = 1.5
    config.target_fps = 165
    config.ZONE = 4
    config.initial_num = 0.017
    config.last_num = 0.019
    config.detection_threshold = 10
    config.slowaim = False
    config.shoot_key = 'l'
    show_fov(None, False)
    dpg.set_value("##counterstrafe_checkbox", config.counterstrafe)
    dpg.set_value("##cooldowntime_slider", config.cooldowntime)
    dpg.set_value("##target_fps_slider", config.target_fps)
    dpg.set_value("##zone_slider", config.ZONE)
    dpg.set_value("##initial_num_slider", config.initial_num)
    dpg.set_value("##last_num_slider", config.last_num)
    dpg.set_value("##detection_threshold_slider", config.detection_threshold)
    dpg.set_value("##slowaim_checkbox", config.slowaim)
    dpg.set_value("##fov_checkbox", config.fov)
    dpg.set_value("delay", f"Between {config.initial_num:.4f} and {config.last_num:.4f}")
    dpg.set_value("shoot_hotkey", f"Shoot Hotkey: {config.shoot_key}")

with dpg.theme() as container_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (150, 100, 100), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (100, 150, 100), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)


def run():
    global viewport, window_hidden, width, height, slider1, slider2, win, login_window, slider3, hwnd, ZONE, click_through, alreadykey
    width = 600
    height = 700
    context = dpg.create_context()
    viewport = dpg.create_viewport(title='steam', always_on_top=True, decorated=False, clear_color=[0.0, 0.0, 0.0, 0.0], resizable=False, disable_close=True)
    threading.Thread(target=change_title, daemon=True).start()
    dpg.set_viewport_always_top(True)
    dpg.create_context()
    dpg.setup_dearpygui()
    dpg.add_viewport_drawlist(front=False, tag="FOV")
    window_hidden = False
    # with dpg.window(label="Ethan's menu", width=width, height=height, no_collapse=True, no_resize=True, on_close=exit) as login_window:
    #     dpg.add_text("Enter your license:")
    #     dpg.add_input_text(tag="##license_input", width=200)
    #     with dpg.group(horizontal=True):    
    #         dpg.add_button(label="Login", callback=login_callback)
    #         dpg.add_button(label="Exit", callback=lambda: exit)  
    #     dpg.add_text(tag="##status_text", label="", color=(255, 255, 255))
        
    with dpg.window(label="Ethan's menu", width=width, height=height, no_collapse=True, no_resize=True, on_close=exit, show=False) as win:
        dpg.add_slider_int(label="Target FPS", default_value=config.target_fps, min_value=60, max_value=240, tag="##target_fps_slider", callback=lambda sender: update_config(sender, 'target_fps'))
        dpg.add_slider_int(label="Threshold", default_value=config.detection_threshold, min_value=1, max_value=10, tag="##detection_threshold_slider", callback=lambda sender: update_config(sender, 'detection_threshold'))
        slider3 = dpg.add_slider_int(label="Zone", default_value=config.ZONE, min_value=1, max_value=10, tag="##zone_slider", callback=lambda sender: update_zone_from_slider(sender, 'ZONE'))
        dpg.add_slider_float(label="Delay after shoot", default_value=config.cooldowntime, min_value=1.0001, max_value=5.0001, tag="##cooldowntime_slider", callback=lambda sender: update_config(sender, 'cooldowntime'), format="%.4f")
        
        with dpg.group(horizontal=True):    
            dpg.add_text("Delay range")  
            slider1 = dpg.add_slider_float(min_value=0.001, max_value=0.033, default_value=config.initial_num, tag="##initial_num_slider", callback=lambda sender: update_config(sender, 'initial_num'), width=100)
            slider2 = dpg.add_slider_float(min_value=0.002, max_value=0.036, default_value=config.last_num, tag="##last_num_slider", callback=lambda sender: update_config(sender, 'last_num'), width=100)

        dpg.add_checkbox(label="Counterstrafe on", default_value=config.counterstrafe, tag="##counterstrafe_checkbox", callback=lambda sender: update_config(sender, 'counterstrafe'))
        dpg.add_checkbox(label="Aim Assist(Stops aim when enemy is viewed)", default_value=config.aim, tag="##aim_checkbox", callback=lambda sender: update_config(sender, 'aim'))
        dpg.add_checkbox(label="FOV (not for in match)", default_value=config.fov, tag="##fov_checkbox", callback=show_fov)
        with dpg.group(horizontal=True):
            dpg.add_text(label="awp hotkey: ", tag="trigger_hotkey")
            dpg.set_value("trigger_hotkey", f"Trigger Hotkey: {config.hotkey_trigger}")
            dpg.add_button(label="Change", callback=trigger_key_callback)
        with dpg.group(horizontal=True):
            dpg.add_text(label="Shoot Hotkey: ", tag="shoot_hotkey")
            dpg.set_value("shoot_hotkey", f"Shoot Hotkey: {config.shoot_key}")
            dpg.add_button(label="Change", callback=shoot_key_callback)
        dpg.add_checkbox(label="not 1 shot", default_value=config.not1shot, tag="##not1shot", callback=lambda sender: update_config(sender, 'not1shot'))
        with dpg.group(horizontal=True):
            dpg.add_text(label="Vandal Hotkey: ", tag="vandal_ht")
            dpg.set_value("vandal_ht", f"Vandal Hotkey: {config.vandal_ht}")
            dpg.add_button(label="Change", callback=vandal_key_callback)
        with dpg.group(horizontal=True):
            dpg.add_text(label="aim hotkey: ", tag="aim_hotkey")
            dpg.set_value("aim_hotkey", f"Aim Hotkey: {config.hotkey_aim}")
            dpg.add_button(label="Change", callback=aim_key_callback)
        dpg.add_text("Delay (Legit = 0.017, Pro = 0.16, Rage = 0.14 to below): ")
        dpg.add_text(label="Between: ", tag="delay")
        dpg.set_value("delay", f"Between {config.initial_num:.4f} and {config.last_num:.4f}")
        dpg.add_button(label="LEGIT", callback=set_config_legit)
        dpg.add_button(label="RESTART in case of bugs", callback=restart_tg)
        alreadykey = dpg.add_text("Key already setted. please choose another.", show=False)

    dpg.show_viewport()
    dpg.toggle_viewport_fullscreen()
    hwnd = win32gui.FindWindow(None, 'steam')
    margins = MARGINS(-1, -1, -1, -1)
    ex_style = win32gui.GetWindowLong(hwnd, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE))
    dwm.DwmExtendFrameIntoClientArea(hwnd, margins)
    click_through = False

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        if keyboard.is_pressed('insert' or 'end'):
            click_through = not click_through
            dpg.configure_item(item=alreadykey, show=False)
            time.sleep(0.1)

        if click_through and logged:
            config.saveconfig()
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
            dpg.configure_item(win, show=False)
            config.getconfig()
        elif not click_through and logged:
            dpg.configure_item(win, show=True)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                ex_style & ~win32con.WS_EX_LAYERED & ~win32con.WS_EX_TRANSPARENT)

def start():
    run()
    dpg.destroy_context()

if __name__ == "__main__":
    start()

#9b8682101af833c55578c4962e6a9eaa
#a9b19d3858e18ab732b607d10b70eb3d
#e261d3e5868b21f22a6bbcec4807adb5
#cfdde22ed3b99af871ea42f54e5940e8
#69221a260c15ada8d02e6184f8dba63c
#52f53d0844626d824724361e66b3f5d4
#9779548379ac4446b0ae3fd1823835b2
#6fa7d34f0d41f826cfc03ed7ea88ab8e
#a80eb773d717bb35e12371025350cbff
#d8e58ea936434d7191e81d1671d2e6d8
#feef0e038648a5469ac6e70c5afe63f4
#bc34f58f6999ef6762feee29cd428328
#c2168c284645412d2fbe27033294a66c
#04888d586fe0b9e3c5bd8e37c80d3f78
#d436c9b68114c5871ceaa46a75b4977c
#b5e8939098b24d34868c715824892e1d
#71534e7422e9daa8bf683c1c1de3b4c6
#ab0750145b962b88c65d57af2c730b3a
#1252031a1a7221f3f82b639ba149470f
#576aeca1b1e5627b8831057c2d0660ab
#b5b0ad8ae3c6ae6306c3ac86213d5d43
#1f8ebc673fa021faedc51a6bdc33e279
#60fad4fd7356ec923634d31cf659ab15
#d6f9ed98d6808f148a3b85b3b840c296
#29c4724490674707bf2a4dfa6aeafdce
#0165397b126883b5f7b45bc346fe7f21
#ad384bd9d1f77a8f443eab4458253a08
#91a59e450cea8fd9f1386f63eb748212
#a36696a5ed943b1997daea31469ebe61
#e74fda3a89864187c20edaa686d837b8
#2483eefeadae43f7a7d4d15808dd8896
#2fc450f23afeb6ffb74a24eee3af4615
#27ae8036126178151200582354c4723f
#5a1dbaf68bca9e5eddbfe3e8f5653372
#954fe02f6f54fd2cdd0ae0593f150a08
#21c2fc2e6e78ea5502057d27c8480062
#c7667ba08db67642eb7bc89cf540de05
#79631425ca5898bbdef9d9906d163d33
#db14199680a0d5de16dbbd535a768b8f
#4f8423fb76dad0acea1ac834d8415c42
#35af17741695144d423557ca41c4fab2
#26aa2a84f5742588a600c95cb520e62d
#4498796f9d73ef64395b7644a0cc613e
#ea879c77e2938119690a6ee304875e0f
#218ce5d352be421e6a80cde3d41fb35d
#0a88009b8597b7510f2b3bdc253feb27
#032420b8c697dd806959c326dfbe81c3
#85a2ea0b3b49f31698159b62a52dd415
#4fc09b3c5866c50d90fcf0c16e5dd241
#524b032a0d51f2e834ec35f8d8eb0cf0
#7e226f848370e356abbf7ac351e830fa
#05d3b2bf887348ab67d355d840ee3573
#0779f4fb4ab7b714913eac249461a59c
#60fb4eb6ae72acc55d6ce26d9583a060
#58742bdc424b41d99499db7f19ae249b
#0368694e4266027c69f65d55e032f1ce
#a826792d7b165b27859ecd3b73037cef
#e259e11fd0ca6db5a8465d0131b9d990
#367c644be07a66f9c202ab7f93a6fa9c
#13af99e304c10fff24155aae217faf1f
#3ba846dde2f1333ef9a38304bd1135ff
#8cfadb0f2a59d4795bd67d658d99e493
#9ddcc8d8bffaea8a0c460a592fa23e61
#7f542ea126c32c48a7fd2b5d38a2ac34
#b0c44fd8876d9cc068895bfa66d23e2a
#752e0d3bc593938db12a9b751a937aa5
#af1d297f821820411f4684550b63cde8
#5d914485c53995eeead94c8d9a50e25d
#fa13fc1af0f7cd9fd8a51d6ffe500934
#458b5723579b3cd6daa312b7fcadd83f
#6f36ed25e45a35da926576da52bce51e
#cff4a7c60bf1480e9460d5a3d09601c5
#8d64004b027c5a49ade0ae086682204a
#e71f08d7c1545acd8e98d09f1a173088
#623578f2cec1dc1fe1e5071e350f82ff
#aeb6ac9fad81b90dbefd3b637982e8eb
#064feedead9b644502a67d30051b90e8
#efbc924074ae477d99822f6a35add16a
#3a1b671f6c2a89e01636fc0ceb6fe727
#6ebd7b5ecc7b297a5a6fd6702fa89bd0