import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import pyautogui
import pytesseract
from googletrans import Translator
import os

class ScreenTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Переводчик с экрана")
        self.root.geometry("700x500")
        self.root.configure(bg="#e0e0e0")
        self.root.minsize(500, 400)  # Минимальный размер окна
        
        # Путь к Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Инициализация переводчика
        self.translator = Translator()
        
        # Переменные для захвата области
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        
        # Переменные для настроек
        self.auto_translate_var = tk.BooleanVar(value=True)
        self.font_size_var = tk.StringVar(value="12")
        self.dest_lang_var = tk.StringVar(value="ru")
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Стиль для минимализма
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), background="#e0e0e0", foreground="#333333")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5, background="#333333", foreground="#ffffff")
        style.configure("TCheckbutton", font=("Arial", 10), background="#e0e0e0", foreground="#333333")
        style.configure("TCombobox", font=("Arial", 10))
        
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Шапка с настройками
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        main_frame.columnconfigure(0, weight=1)
        
        # Настройки в шапке
        ttk.Checkbutton(header_frame, text="Автоматический перевод", variable=self.auto_translate_var, 
                        command=self.toggle_translate_button).pack(side="left", padx=5)
        ttk.Label(header_frame, text="Язык:").pack(side="left", padx=5)
        ttk.Combobox(header_frame, textvariable=self.dest_lang_var, values=["ru", "en"], 
                     state="readonly", width=5).pack(side="left", padx=5)
        ttk.Label(header_frame, text="Шрифт:").pack(side="left", padx=5)
        ttk.Combobox(header_frame, textvariable=self.font_size_var, values=["10", "12", "14", "16"], 
                     state="readonly", width=5).pack(side="left", padx=5)
        
        # Кнопка захвата
        ttk.Button(main_frame, text="Захватить область", command=self.start_capture).grid(row=1, column=0, pady=10)
        
        # Поле исходного текста
        ttk.Label(main_frame, text="Исходный текст").grid(row=2, column=0, sticky="w", padx=5)
        self.original_text = tk.Text(main_frame, height=5, width=50, font=("Arial", int(self.font_size_var.get())), 
                                     bg="#ffffff", fg="#333333", borderwidth=1, relief="solid")
        self.original_text.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        main_frame.rowconfigure(3, weight=1)
        
        # Поле переведенного текста
        ttk.Label(main_frame, text="Переведенный текст").grid(row=4, column=0, sticky="w", padx=5)
        self.translated_text = tk.Text(main_frame, height=5, width=50, font=("Arial", int(self.font_size_var.get())), 
                                      bg="#ffffff", fg="#333333", borderwidth=1, relief="solid")
        self.translated_text.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        main_frame.rowconfigure(5, weight=1)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, pady=10)
        self.translate_button = ttk.Button(button_frame, text="Перевести", command=self.translate_text)
        self.translate_button.pack(side="left", padx=5)
        ttk.Button(button_frame, text="Сохранить текст", command=self.save_text).pack(side="left", padx=5)
        
        # Обновление состояния кнопки перевода
        self.font_size_var.trace("w", self.update_font_size)
        self.toggle_translate_button()
        
    def toggle_translate_button(self):
        # Включить/отключить кнопку "Перевести"
        self.translate_button.configure(state="disabled" if self.auto_translate_var.get() else "normal")
        
    def update_font_size(self, *args):
        # Обновить размер шрифта
        font_size = int(self.font_size_var.get())
        self.original_text.configure(font=("Arial", font_size))
        self.translated_text.configure(font=("Arial", font_size))
        
    def start_capture(self):
        # Скрыть окно приложения
        self.root.iconify()
        
        # Создать окно для выделения области
        self.capture_window = tk.Toplevel(self.root)
        self.capture_window.attributes('-fullscreen', True)
        self.capture_window.attributes('-alpha', 0.5)  # Темный фон
        self.capture_window.configure(bg='grey')
        
        # Создать холст для рисования
        self.canvas = tk.Canvas(self.capture_window, cursor="cross", bg='grey', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Привязка событий мыши
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        # Инициализация координат
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        
    def on_mouse_press(self, event):
        # Сохранить начальные координаты
        self.start_x = int(self.canvas.canvasx(event.x))
        self.start_y = int(self.canvas.canvasy(event.y))
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, 
                                                outline='white', width=3)
        
    def on_mouse_drag(self, event):
        if self.rect is None or self.start_x is None or self.start_y is None:
            return
        # Обновить конечные координаты
        self.end_x = int(self.canvas.canvasx(event.x))
        self.end_y = int(self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        
    def on_mouse_release(self, event):
        if self.start_x is None or self.start_y is None:
            self.capture_window.destroy()
            self.root.deiconify()
            messagebox.showwarning("Предупреждение", "Область не выделена!")
            return
        
        # Обновить конечные координаты
        self.end_x = int(self.canvas.canvasx(event.x))
        self.end_y = int(self.canvas.canvasy(event.y))
        
        # Закрыть окно захвата
        self.capture_window.destroy()
        self.root.deiconify()
        
        # Проверить валидность координат
        if self.end_x is None or self.end_y is None:
            messagebox.showwarning("Предупреждение", "Область не выделена корректно!")
            return
        
        # Захват выделенной области
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        
        # Убедиться, что область ненулевая
        if x2 - x1 <= 0 or y2 - y1 <= 0:
            messagebox.showwarning("Предупреждение", "Выделенная область слишком мала!")
            return
        
        # Сделать скриншот
        try:
            screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
            screenshot.save("temp_screenshot.png")
            
            # Распознавание текста
            text = pytesseract.image_to_string(Image.open("temp_screenshot.png"), lang='eng+rus')
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(tk.END, text.strip())
            
            # Удалить временный файл
            os.remove("temp_screenshot.png")
            
            # Автоматический перевод, если включен
            if self.auto_translate_var.get():
                self.translate_text()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось распознать текст: {str(e)}")
        
    def translate_text(self):
        text = self.original_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Нет текста для перевода!")
            return
        
        try:
            # Определение языка текста
            detected = self.translator.detect(text)
            src_lang = detected.lang
            
            # Использовать выбранный язык
            dest_lang = self.dest_lang_var.get()
            
            # Если язык совпадает, копировать текст
            if src_lang.startswith(dest_lang):
                self.translated_text.delete(1.0, tk.END)
                self.translated_text.insert(tk.END, text)
                return
            
            # Перевод текста
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
            self.translated_text.delete(1.0, tk.END)
            self.translated_text.insert(tk.END, translated.text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось перевести текст: {str(e)}")
            
    def save_text(self):
        # Сохранение текста
        original = self.original_text.get(1.0, tk.END).strip()
        translated = self.translated_text.get(1.0, tk.END).strip()
        if not original and not translated:
            messagebox.showwarning("Предупреждение", "Нет текста для сохранения!")
            return
        
        try:
            with open("translated_text.txt", "a", encoding="utf-8") as f:
                f.write("Исходный текст:\n")
                f.write(original + "\n")
                f.write("Переведенный текст:\n")
                f.write(translated + "\n")
                f.write("-" * 50 + "\n")
            messagebox.showinfo("Успех", "Текст сохранен в translated_text.txt")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить текст: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenTranslatorApp(root)
    root.mainloop()