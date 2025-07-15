📖 Translator
Translator is a Windows app that captures a screen area, recognizes text using Tesseract OCR, and translates it between English and Russian with Google Translate. It features a minimalist, adaptive UI with automatic translation and customizable settings.

🚀 Installation
1. Install Tesseract-OCR

Download and install Tesseract-OCR: Tesseract Installer.
Ensure Tesseract is at C:\Program Files\Tesseract-OCR\tesseract.exe.
Verify eng.traineddata and rus.traineddata are in C:\Program Files\Tesseract-OCR\tessdata.

2. Run from Source

Install dependencies:pip install pytesseract==0.3.13 pyautogui==0.9.54 googletrans==4.0.0-rc1 pillow==11.2.1 pandas==2.2.2
Run the app
python screen_translator.py

🖥️ Usage

Launch the App:
Double-click Translator.exe or run python screen_translator.py.


Configure Settings (in the header):
Enable/disable automatic translation.
Select translation language: en (English) or ru (Russian).
Choose font size: 10, 12, 14, 16.


Capture Screen Area:
Click "Capture Area".
Hold the left mouse button to select an area (white rectangle on a darkened background).
Release to recognize and translate text (if auto-translation is enabled).


View and Save:
Original text appears in the top field, translated text in the bottom.
Click "Save Text" to save results to translated_text.txt.


Manual Translation (if auto-translation is off):
Click "Translate" to translate the text.



