# PlugNGrab

**PlugNGrab** is an educational and ethical testing tool designed to extract saved browser passwords, Wi-Fi credentials, and system information from a Windows machine. It is intended for use on devices you own or have explicit permission to test.

---

## ⚠️ Disclaimer

> This software is developed solely for educational and entertainment purposes.  
> The developer does **not** support or accept any responsibility for the misuse of this tool.  
> You are solely responsible for ensuring that your usage complies with all applicable laws and ethical guidelines.  
> Use only on systems you own or have explicit authorization to analyze.

---

## 🛠 Features

- Extracts saved passwords from major browsers (Chrome, Edge, Opera, Brave)
- Retrieves stored Wi-Fi passwords
- Captures clipboard contents
- Collects basic system information (hostname, IP, MAC)
- Runs silently in the background

---

## 🧪 For Educational Testing Only

You should only use this tool on **test systems** or **your own machines**.  
Never use it without explicit consent from the device owner.

---

## 🚀 Usage

### 1. Download the Script

Download `PlugNGrab.py` and place it in your desired folder.

### 2. Open Command Prompt

Open a Command Prompt in the folder where the script is located.

### 3. Convert to Executable (Optional)

If you'd like to convert the script into a `.exe` file that runs standalone:

```
pyinstaller --onefile --noconsole --icon=icon.ico --name=PlugNGrab PlugNGrab.py
```

This will create an executable in the `dist/` folder.

---

## ✏️ Customization

The code is fully open and can be modified to suit your needs.  
Feel free to change:

- Output directory names
- Logging format
- Additional data to collect (e.g. screenshots, browser history, etc.)

---

## 📁 Output

Collected data will be saved in a folder like this:

```
Bilgiler_
├── chrome_sifreler.txt
├── edge_sifreler.txt
├── wifi_sifreleri.txt
├── pano.txt
└── sistem_bilgisi.txt
```

---

## ✅ Requirements

- Python 3.x
- Windows OS
- Required packages:
  - `pycryptodome`
  - `pywin32`
  - `pyinstaller` (for compiling to `.exe`)

You can install them with:

```
pip install pycryptodome pywin32 pyinstaller
```

---

## 📚 License

This project is released under the MIT License.

---

## 🙋 Support

This project is for educational use only. No official support is provided.
