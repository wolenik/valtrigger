import configparser
from ctypes import WinDLL
import time



(user32, kernel32, shcore) = (
    WinDLL('user32', use_last_error=True),
    WinDLL('kernel32', use_last_error=True),
    WinDLL('shcore', use_last_error=True),
)


shcore.SetProcessDpiAwareness(2)

class CONFIG:
    def __init__(self):
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)
        self.ZONE = 3
        self.GRAB_ZONE = (int(self.width / 2 - self.ZONE), int(self.height / 2 - self.ZONE),
                          int(self.width / 2 + self.ZONE), int(self.height / 2 + self.ZONE))
        self.detection_threshold = 3
        self.counterstrafe = False
        self.cooldowntime = 3.0
        self.hotkey_trigger = "shift"
        self.vandal_ht = "alt"
        self.initial_num = 0.015
        self.last_num = 0.018
        self.low_color = (139, 95, 188)  # Lower HSV:  (139, 95, 188) ##upper_color = 148,154,194 
        self.high_color = (156, 255, 255)  # Upper HSV:  (156, 255, 255)
        self.config = configparser.ConfigParser()
        self.shoot_key = 'k'
        self.target_fps = 60
        self.aim = False
        self.fov = False
        self.not1shot = False

        self.getconfig()

    def saveconfig(self):
        self.config['Config'] = {
            'ht': str(self.hotkey_trigger),
            'cs': str(self.counterstrafe),
            'cd': str(self.cooldowntime),
            'tf': str(self.target_fps),
            'zn': str(self.ZONE),
            'in': str(self.initial_num),
            'ln': str(self.last_num),
            'dt': str(self.detection_threshold),
            'ai': str(self.aim),
            'fv': str(self.fov),
            'nt': str(self.not1shot)
        }
        with open('test.ini', 'w') as configfile:
            self.config.write(configfile)

    def getconfig(self):
        try:
            config = configparser.ConfigParser()
            config.read('test.ini')
            self.hotkey_trigger = config['Config'].get('ht', 'shift')
            self.counterstrafe = config['Config'].getboolean('cs', False)
            self.cooldowntime = config['Config'].getfloat('cd', 3.0)
            self.target_fps = config['Config'].getint('tf', 60)
            self.ZONE = config['Config'].getint('zn', 3)
            self.initial_num = config['Config'].getfloat('in', 0.015)
            self.last_num = config['Config'].getfloat('ln', 0.018)
            self.detection_threshold = config['Config'].getint('dt', 3)
            self.aim = config['Config'].getboolean('ai', False)
            self.fov = config['Config'].getboolean('fv', False)
            self.not1shot = config['Config'].getboolean('nt', False)
        except Exception as e:
            self.saveconfig()
            time.sleep(2)
            self.getconfig()


#55cf7efbc3aa38d0ca402220a9f5a0d6
#9b61acf027f8aff5c07f890a96c44716
#7540614776de26fcd4dd8d6f0b9720e9
#2fbdf8e3fc54f762f837a18a0eb3d75c
#4cc411fa7cdaa1ffe4b58d30d36b80cb
#829eac2b4418ef0ba2529b0df7552e66
#8f5e2ba916bf059eb9aaaead5b589878
#d63ca1aa50dddb482b700e13d0511777
#d6c7a23ad3adeffffcb4d93697f89e2c
#85557977011df958b1bc53642ad99477
#688df6bfd10dc856b813ad338dcdeafc
#d8eb3a8b5702da2f8526dd5497785337
#e1cf8359399dfa90640f50fcf716d23a
#780107bfb1814028572a9b46bb914765
#be5bb48e677251251886a8e69514c99d
#7c72c02f2b5b3a6a5889be7371bd4b47
#33c6a63b7f7fe9ffa771e65c49669020
#f8b8e77a43a19a3a011797b2d85f94dc
#bb6a12179e5924b789fa38879c6363a7
#1078c83d0e0d2e95a72ab8fdba35d59a
#35a404b7ec87c5f0095a1da9cac354ca
#b4ba6cbcb2dda12482cf91d3a9ddcba3
#c397cf29aa550baa082423092684bc15
#7b596e7e4d2b08775adb7e5b7a8d10d0
#6097882a53c338a490e037587e6d91ea
#e4c692275756c6bb765f032c92f1f8c8
#a8f554ca6473be69158180b1ea4e4d0b
#33d211c363272f0454f891a2a0f52313
#86e325a0ba786ec3c9b6d750dc5c9244
#22ebe1eddcc22016864e5884a1a0d1f6
#746ed14050047057cd811b5124dc2db6
#e315e07ab0572cd31e66d032b30d7fc7
#4492fec4a61bf4ff456117e625cb1ff1
#aa0fb877b50a7204fa34338f32fb02a1
#60f154f00e1ae00a181c388c14fac579
#7c0d1386206a1de4e3a08ee7e976d9e4
#d9ef6b48d459d9205926cf62df29ac68
#8e9f19d4d46347f6e00fa42aea836770
#d9a4ddc7161811ab17da396328ff9499
#0afc9fd1e2d66c81293cc1f5ac523ee5