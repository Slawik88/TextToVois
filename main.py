import customtkinter as ctk
import os
from gtts import gTTS
from tkinter import filedialog
import threading

# Настройка темы
ctk.set_appearance_mode("dark")  # Темная тема
ctk.set_default_color_theme("blue")  # Синие акценты

# Создание окна
root = ctk.CTk()
root.title("Создание аудиокниги")
root.geometry("700x550")

# Основной фрейм для элементов управления
control_frame = ctk.CTkFrame(root)
control_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Переменные
text_file_path = ctk.StringVar(value="example.txt")  # Путь к файлу
lang = ctk.StringVar(value="ru")  # Язык по умолчанию
speed = ctk.BooleanVar(value=False)  # Скорость речи

# Функция выбора файла
def select_file():
    file_path = filedialog.askopenfilename(
        title="Выберите текстовый файл",
        filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*"))
    )
    if file_path:
        text_file_path.set(file_path)

# Функция обновления статуса
def update_status(message):
    status_label.configure(text=message)
    root.update_idletasks()

# Функция создания аудиокниги в потоке
def create_audiobook_thread():
    try:
        text_file = text_file_path.get()
        selected_lang = lang.get()  # Получаем выбранный язык
        is_slow = speed.get()  # Получаем значение скорости

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        output_file = os.path.join(desktop, "audiobook.mp3")

        if not os.path.exists(text_file):
            raise FileNotFoundError(f"Файл '{text_file}' не найден.")

        with open(text_file, 'r', encoding='utf-8') as file:
            text = file.read()

        if not text.strip():
            raise ValueError("Файл пустой.")

        update_status("⏳ Создание аудиокниги...")

        tts = gTTS(text=text, lang=selected_lang, slow=is_slow)
        tts.save(output_file)

        update_status(f"✅ Аудиокнига сохранена как '{output_file}'")

        # Открытие файла в зависимости от ОС
        if os.name == 'nt':  # Windows
            os.system(f'start "{output_file}"')
        elif os.name == 'posix':  # MacOS/Linux
            if os.uname().sysname == 'Darwin':  # MacOS
                os.system(f'open "{output_file}"')
            else:  # Linux
                os.system(f'xdg-open "{output_file}"')

    except FileNotFoundError as e:
        update_status(f"❌ Ошибка: {e}")
    except ValueError as e:
        update_status(f"❌ Ошибка: {e}")
    except Exception as e:
        update_status(f"⚠️ Ошибка: {e}")

# Запуск создания в потоке
def start_audiobook_creation():
    thread = threading.Thread(target=create_audiobook_thread)
    thread.start()

# Виджеты в control_frame
# 1. Путь к файлу
file_label = ctk.CTkLabel(control_frame, text="Путь к файлу:", font=("Helvetica", 14))
file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

file_entry = ctk.CTkEntry(control_frame, textvariable=text_file_path, width=350)
file_entry.grid(row=0, column=1, padx=10, pady=10)

select_button = ctk.CTkButton(control_frame, text="Выбрать", command=select_file, width=100)
select_button.grid(row=0, column=2, padx=10, pady=10)

# 2. Выбор языка
lang_label = ctk.CTkLabel(control_frame, text="Язык:", font=("Helvetica", 14))
lang_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

lang_options = ["ru", "en", "fr", "de", "es"]  # Список языков
lang_menu = ctk.CTkOptionMenu(control_frame, variable=lang, values=lang_options, width=100)
lang_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# 3. Скорость речи
speed_checkbox = ctk.CTkCheckBox(control_frame, text="Медленная речь", variable=speed, font=("Helvetica", 14))
speed_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# 4. Кнопка создания
create_button = ctk.CTkButton(control_frame, text="Создать аудиокнигу", command=start_audiobook_creation, 
                              font=("Helvetica", 14), height=40)
create_button.grid(row=3, column=0, columnspan=3, pady=20)

# Метка статуса вне фрейма
status_label = ctk.CTkLabel(root, text="Ожидание действия...", font=("Helvetica", 12))
status_label.pack(pady=10)

# Запуск программы
root.mainloop()