"""
Тренажёр слепой печати
Приложение для тренировки скорости и точности набора текста.
Яркий, запоминающийся интерфейс для молодых пользователей.
"""

import json
import sys
import time
import random
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Путь к данным: рядом с exe при сборке PyInstaller, иначе — папка скрипта
if getattr(sys, "frozen", False):
    _base_path = Path(sys.executable).parent
else:
    _base_path = Path(__file__).parent

import customtkinter as ctk
from tkinter import Text

# Импорт ассетов
try:
    from assets import ensure_assets
    _assets_dir = ensure_assets(_base_path)
except Exception:
    _assets_dir = _base_path / "assets"
    _assets_dir.mkdir(exist_ok=True)

# === РУССКАЯ РАСКЛАДКА ===
# Наборы фраз для тренировки
PHRASES = [
    "Слепая печать — это навык, который экономит время каждый день.",
    "Регулярные тренировки помогают развить мышечную память пальцев.",
    "Держите руки в правильной позиции: пальцы на клавишах ФЫВА и ОЛДЖ.",
    "Не смотрите на клавиатуру во время набора текста.",
    "Скорость приходит с практикой, не торопитесь в начале.",
    "Точность важнее скорости на первых этапах обучения.",
    "Каждый палец отвечает за определённую зону клавиатуры.",
    "Делайте короткие перерывы между сессиями тренировки.",
    "Современные программы помогают отслеживать прогресс.",
    "Клавиатура — основной инструмент для работы с компьютером.",
    "Текст набирается быстрее, когда руки не отрываются от клавиш.",
]

# Скороговорки
TONGUE_TWISTERS = [
    "Карл у Клары украл кораллы, а Клара у Карла украла кларнет.",
    "Шла Саша по шоссе и сосала сушку.",
    "Кукушка кукушонку купила капюшон.",
    "На дворе трава, на траве дрова.",
    "Грека шёл через реку, видит Грека в реке рак.",
    "Во дворе дрова, за двором дрова.",
    "Ехал Грека через реку.",
    "Мама мыла Раму, Рама мыл маму.",
]

# Цитаты и мотивация
QUOTES = [
    "Успех — это сумма небольших усилий, повторяемых изо дня в день.",
    "Не бойся идти медленно, бойся стоять на месте.",
    "Каждая минута тренировки приближает к цели.",
    "Лучше поздно, чем никогда. Лучше начать сейчас, чем завтра.",
    "Маленькие шаги каждый день приводят к большим результатам.",
    "Практика ведёт к совершенству.",
    "Ты справишься! Просто продолжай печатать.",
]

# Код для программистов
CODE_SNIPPETS = [
    "def main():",
    "for i in range(10):",
    "if x > 0:",
    "print('Hello')",
    "return True",
    "import json",
    "from pathlib import Path",
    "list.append(item)",
    "dict.get(key)",
    "try: except:",
]

# Слова для упражнений
WORDS = [
    "клавиатура", "монитор", "компьютер", "программа", "интернет",
    "память", "процессор", "мышь", "кнопка", "окно", "текст", "скорость",
    "упражнение", "символ", "пальцы", "клавиши", "файл", "папка",
    "экран", "браузер", "сообщение", "почта", "документ", "запись",
]

LETTERS = list("фывапролджэйцукенгшщзхъячсмитьбю")
DIGITS = "0123456789"
SYMBOLS = ".,!?:;-\"\'()[]{}@#$%"

# === АНГЛИЙСКАЯ РАСКЛАДКА ===
PHRASES_EN = [
    "Touch typing is a skill that saves time every single day.",
    "Regular practice helps develop muscle memory in your fingers.",
    "Keep your hands in the correct position: fingers on ASDF and JKL;",
    "Do not look at the keyboard while typing.",
    "Speed comes with practice, do not rush in the beginning.",
    "Accuracy is more important than speed in early stages.",
    "Each finger is responsible for a specific zone of the keyboard.",
    "Take short breaks between training sessions.",
    "Modern programs help track your progress.",
    "Text is typed faster when your hands stay on the keys.",
]

TONGUE_TWISTERS_EN = [
    "Peter Piper picked a peck of pickled peppers.",
    "How much wood would a woodchuck chuck.",
    "She sells seashells by the seashore.",
    "How can a clam cram in a clean cream can.",
    "I wish to wish the wish you wish to wish.",
    "Six sick hicks nick six slick bricks.",
]

QUOTES_EN = [
    "Success is the sum of small efforts repeated day in and day out.",
    "Do not fear going slowly, fear standing still.",
    "Every minute of practice brings you closer to your goal.",
    "Better late than never. Better start now than tomorrow.",
    "Small steps every day lead to big results.",
    "Practice makes perfect.",
    "You got this! Just keep typing.",
]

WORDS_EN = [
    "keyboard", "monitor", "computer", "program", "internet",
    "memory", "processor", "mouse", "button", "window", "text", "speed",
    "exercise", "symbol", "fingers", "keys", "file", "folder",
    "screen", "browser", "message", "email", "document", "record",
]

LETTERS_EN = list("qwertyuiopasdfghjklzxcvbnm")

MODE_LABELS = {
    "phrases": "Фразы",
    "words": "Слова",
    "letters": "Буквы",
    "numbers": "Цифры",
    "twisters": "Скороговорки",
    "quotes": "Цитаты",
    "code": "Код",
    "mixed": "Смешанный",
}

MODE_LABELS_EN = {
    "phrases": "Phrases",
    "words": "Words",
    "letters": "Letters",
    "numbers": "Numbers",
    "twisters": "Tongue twisters",
    "quotes": "Quotes",
    "code": "Code",
    "mixed": "Mixed",
}

MODE_HINTS = {
    "phrases": "Полные предложения для практики",
    "words": "Отдельные слова для скорости",
    "letters": "Случайные буквы, базовый уровень",
    "numbers": "Цифры и числа",
    "twisters": "Скороговорки для ловкости",
    "quotes": "Мотивирующие цитаты",
    "code": "Фрагменты кода для разработчиков",
    "mixed": "Слова + цифры + символы — как в жизни",
}

MODE_HINTS_EN = {
    "phrases": "Full sentences for practice",
    "words": "Individual words for speed",
    "letters": "Random letters, basic level",
    "numbers": "Digits and numbers",
    "twisters": "Tongue twisters for agility",
    "quotes": "Motivational quotes",
    "code": "Code snippets for developers",
    "mixed": "Words + numbers + symbols — like IRL",
}

# Подсказки для rotation
TIPS = [
    "Пальцы на ФЫВА и ОЛДЖ — не отрывай их!",
    "Не смотри на клавиатуру. Поначалу медленно — это норм.",
    "Точность важнее скорости. Лучше 50 без ошибок, чем 100 с косяками.",
    "Каждый день по 10 минут — лучше, чем раз в неделю час.",
    "Ошибся — не парься, продолжай печатать.",
    "Распрями спину, руки под углом 90°.",
]

TIPS_EN = [
    "Fingers on ASDF and JKL; — keep them there!",
    "Don't look at the keyboard. Slow at first is fine.",
    "Accuracy over speed. 50 correct beats 100 with errors.",
    "10 min every day beats 1 hour once a week.",
    "Made a mistake? No worries, keep typing.",
    "Sit straight, arms at 90 degrees.",
]

# Мотивационные сообщения при завершении
COMPLETION_MSGS = [
    "Красава! 🔥",
    "Ещё быстрее! ⚡",
    "Легко! 💪",
    "Убил! 🚀",
    "Красота! ✨",
    "Так держать! 👏",
    "Прёт! 💯",
]

COMPLETION_MSGS_EN = [
    "Awesome! 🔥",
    "Faster! ⚡",
    "Easy! 💪",
    "Killed it! 🚀",
    "Beautiful! ✨",
    "Keep it up! 👏",
    "Nailed it! 💯",
]

# Яркие цвета для зумеров
COLORS = {
    "header": "#6366f1",  # яркий индиго
    "header_text": "#ffffff",
    "sidebar": "#f8fafc",
    "sidebar_active": "#6366f1",
    "sidebar_hover": "#818cf8",
    "main_bg": "#ffffff",
    "card_bg": "#1e1b4b",  # тёмный фон для контраста
    "text_dark": "#1e293b",
    "text_muted": "#64748b",
    "correct": "#22c55e",   # яркий зелёный
    "wrong": "#ef4444",     # яркий красный
    "current": "#fbbf24",   # яркий жёлтый
}


class TypingTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Тренажёр слепой печати")
        self.geometry("1000x650")
        self.minsize(800, 550)

        ctk.set_appearance_mode("light")
        self.configure(fg_color=COLORS["main_bg"])

        self.data_path = _base_path / "progress.json"
        self.settings_path = _base_path / "settings.json"
        self.progress_data = self._load_progress()
        self.exercise_font_size = self._load_font_size()

        self.current_phrase = ""
        self.user_input = ""
        self.start_time = None
        self.is_typing = False
        self.exercise_done = False
        self.mode_key = "phrases"
        self.lang = "ru"  # "ru" | "en"
        self.timer_id = None

        self.total_exercises = len(self.progress_data)
        self.best_speed_overall = max(
            (p.get("speed_cpm", 0) for p in self.progress_data), default=0.0
        )

        self._build_ui()

    def _load_progress(self) -> list:
        if self.data_path.exists():
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def _load_font_size(self) -> int:
        """Загрузка размера шрифта из настроек."""
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    size = int(data.get("exercise_font_size", 28))
                    return max(14, min(48, size))
            except (json.JSONDecodeError, IOError, ValueError):
                pass
        return 28

    def _save_font_size(self):
        """Сохранение размера шрифта в настройки."""
        try:
            data = {}
            if self.settings_path.exists():
                try:
                    with open(self.settings_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    pass
            data["exercise_font_size"] = self.exercise_font_size
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _save_progress(self, speed: float, phrase_len: int, accuracy: float):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "speed_cpm": round(speed, 1),
            "chars": phrase_len,
            "accuracy": round(accuracy, 1),
            "mode": self.mode_key,
            "lang": self.lang,
        }
        self.progress_data.append(entry)
        self.total_exercises = len(self.progress_data)
        self.best_speed_overall = max(self.best_speed_overall, entry["speed_cpm"])
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.progress_data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Шапка
        header = ctk.CTkFrame(
            self,
            fg_color=COLORS["header"],
            height=52,
            corner_radius=0,
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        header_left = ctk.CTkFrame(header, fg_color="transparent")
        header_left.grid(row=0, column=0, padx=24, pady=14, sticky="w")
        try:
            from PIL import Image
            logo_path = _assets_dir / "logo.png"
            if logo_path.exists():
                pil_img = Image.open(logo_path).resize((40, 40))
                self.logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(40, 40))
                ctk.CTkLabel(header_left, image=self.logo_img, text="").pack(side="left", padx=(0, 12))
        except Exception:
            pass
        self.header_title = ctk.CTkLabel(
            header_left,
            text="⌨️ ТРЕНАЖЁР ПЕЧАТИ" if self.lang == "ru" else "⌨️ TYPING TRAINER",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["header_text"],
        )
        self.header_title.pack(side="left")

        nav = ctk.CTkFrame(header, fg_color="transparent")
        nav.grid(row=0, column=1, padx=16, sticky="e")
        ctk.CTkButton(nav, text="Прогресс", width=100, height=32, fg_color="transparent",
            border_width=1, border_color=COLORS["header_text"], text_color=COLORS["header_text"],
            hover_color="#818cf8", command=self._show_progress,
        ).pack(side="left", padx=4)
        ctk.CTkButton(nav, text="Статистика", width=100, height=32, fg_color="transparent",
            border_width=1, border_color=COLORS["header_text"], text_color=COLORS["header_text"],
            hover_color="#818cf8", command=self._show_stats,
        ).pack(side="left", padx=4)

        # Контейнер для двух экранов (меню и тренажёр)
        content = ctk.CTkFrame(self, fg_color=COLORS["main_bg"], corner_radius=0)
        content.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # === ЭКРАН МЕНЮ (полная страница) ===
        self.menu_frame = ctk.CTkFrame(content, fg_color=COLORS["main_bg"], corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure(2, weight=1)

        lang_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        lang_frame.grid(row=0, column=0, padx=24, pady=(24, 8), sticky="w")
        ctk.CTkLabel(lang_frame, text="Раскладка:" if self.lang == "ru" else "Layout:",
            font=ctk.CTkFont(size=12), text_color=COLORS["text_muted"]).pack(side="left", padx=(0, 8))
        self.btn_lang_ru = ctk.CTkButton(lang_frame, text="RU", width=50, height=32,
            fg_color=COLORS["sidebar_active"] if self.lang == "ru" else "transparent",
            hover_color=COLORS["sidebar_hover"], command=lambda: self._set_lang("ru"),
        )
        self.btn_lang_ru.pack(side="left", padx=(0, 6))
        self.btn_lang_en = ctk.CTkButton(lang_frame, text="EN", width=50, height=32,
            fg_color=COLORS["sidebar_active"] if self.lang == "en" else "transparent",
            hover_color=COLORS["sidebar_hover"], command=lambda: self._set_lang("en"),
        )
        self.btn_lang_en.pack(side="left")

        self.menu_title_label = ctk.CTkLabel(
            self.menu_frame,
            text="Выбери режим 👇" if self.lang == "ru" else "Choose a mode 👇",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_dark"],
        )
        self.menu_title_label.grid(row=1, column=0, padx=24, pady=(16, 24), sticky="nw")

        mode_labels = MODE_LABELS if self.lang == "ru" else MODE_LABELS_EN
        mode_grid = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        mode_grid.grid(row=2, column=0, padx=24, pady=(0, 24), sticky="nsew")
        for c in range(4):
            mode_grid.grid_columnconfigure(c, weight=1)
        mode_grid.grid_rowconfigure(tuple(range(4)), weight=1)

        self.mode_buttons = {}
        for i, (key, label) in enumerate(mode_labels.items()):
            row, col = divmod(i, 4)
            btn = ctk.CTkButton(
                mode_grid,
                text=label,
                font=ctk.CTkFont(size=16, weight="bold"),
                height=72,
                corner_radius=16,
                fg_color=COLORS["sidebar_active"],
                hover_color=COLORS["sidebar_hover"],
                text_color=COLORS["header_text"],
                command=lambda k=key: self._start_mode(k),
            )
            btn.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            self.mode_buttons[key] = btn

        # === ЭКРАН ТРЕНАЖЁРА ===
        self.training_frame = ctk.CTkFrame(content, fg_color=COLORS["main_bg"], corner_radius=0)
        self.training_frame.grid(row=0, column=0, sticky="nsew")
        self.training_frame.grid_columnconfigure(0, weight=1)
        self.training_frame.grid_rowconfigure(3, weight=1)

        # Кнопка «Назад в меню»
        top_bar = ctk.CTkFrame(self.training_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, padx=24, pady=(16, 8), sticky="ew")
        top_bar.grid_columnconfigure(1, weight=1)
        self.btn_back = ctk.CTkButton(
            top_bar,
            text="← Назад в меню" if self.lang == "ru" else "← Back to menu",
            width=160,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=COLORS["text_muted"],
            hover_color=COLORS["sidebar_hover"],
            text_color=COLORS["header_text"],
            command=self._back_to_menu,
        )
        self.btn_back.grid(row=0, column=0, sticky="w")

        # Регулировка размера шрифта
        font_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        font_frame.grid(row=0, column=1, sticky="e", padx=(0, 0))
        self.font_label = ctk.CTkLabel(font_frame, text="Шрифт:" if self.lang == "ru" else "Font:",
            font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"])
        self.font_label.pack(side="left", padx=(0, 8))
        ctk.CTkButton(font_frame, text="−", width=36, height=36,
            fg_color=COLORS["sidebar_active"], hover_color=COLORS["sidebar_hover"],
            command=lambda: self._change_font_size(-2)).pack(side="left", padx=(0, 4))
        self.font_size_label = ctk.CTkLabel(font_frame, text=str(self.exercise_font_size),
            font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["text_dark"], width=28)
        self.font_size_label.pack(side="left", padx=4)
        ctk.CTkButton(font_frame, text="+", width=36, height=36,
            fg_color=COLORS["sidebar_active"], hover_color=COLORS["sidebar_hover"],
            command=lambda: self._change_font_size(2)).pack(side="left")

        self.breadcrumb_label = ctk.CTkLabel(
            self.training_frame,
            text=f"{'Уроки' if self.lang == 'ru' else 'Lessons'} > {mode_labels[self.mode_key]}",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        )
        self.breadcrumb_label.grid(row=1, column=0, padx=24, pady=(0, 4), sticky="w")

        # Подсказка (ротация + подсказка по режиму) + картинка рук
        self.hint_frame = ctk.CTkFrame(self.training_frame, fg_color="#e0e7ff", corner_radius=10, height=60)
        self.hint_frame.grid(row=2, column=0, padx=24, pady=(0, 12), sticky="ew")
        self.hint_frame.grid_propagate(False)
        self.hint_frame.grid_columnconfigure(1, weight=1)
        try:
            from PIL import Image
            hands_path = _assets_dir / "hands.png"
            if hands_path.exists():
                pil_hands = Image.open(hands_path).resize((100, 55))
                hands_img = ctk.CTkImage(light_image=pil_hands, dark_image=pil_hands, size=(100, 55))
                ctk.CTkLabel(self.hint_frame, image=hands_img, text="").grid(row=0, column=0, padx=(16, 12), pady=8, sticky="w")
        except Exception:
            pass
        self.hint_label = ctk.CTkLabel(
            self.hint_frame,
            text="💡 " + (random.choice(TIPS) if self.lang == "ru" else random.choice(TIPS_EN)),
            font=ctk.CTkFont(size=16),
            text_color="#4338ca",
            wraplength=600,
        )
        self.hint_label.grid(row=0, column=1, padx=(0, 16), pady=12, sticky="w")
        self._rotate_hint()

        # Карточка с текстом (тёмная для контраста)
        card = ctk.CTkFrame(
            self.training_frame,
            fg_color=COLORS["card_bg"],
            corner_radius=16,
            border_width=0,
        )
        card.grid(row=3, column=0, padx=24, pady=(0, 12), sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        # Верх карточки: таймер и процент
        card_top = ctk.CTkFrame(card, fg_color="transparent")
        card_top.grid(row=0, column=0, padx=20, pady=(16, 8), sticky="ew")
        card_top.grid_columnconfigure(1, weight=1)

        self.timer_label = ctk.CTkLabel(
            card_top,
            text="⏱️ 00:00",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#a5b4fc",
        )
        self.timer_label.grid(row=0, column=0, sticky="w")

        self.accuracy_label = ctk.CTkLabel(
            card_top,
            text="🎯 0%",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#a5b4fc",
        )
        self.accuracy_label.grid(row=0, column=2, sticky="e")

        self.phrase_text = Text(
            card,
            font=("Consolas", self.exercise_font_size),
            wrap="word",
            height=4,
            relief="flat",
            padx=24,
            pady=16,
            state="disabled",
            cursor="arrow",
            bg=COLORS["card_bg"],
            fg="#e2e8f0",
            insertwidth=0,
        )
        self.phrase_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Яркие цвета: зелёный — правильно, красный — ошибка, жёлтый — текущий символ
        self.phrase_text.tag_configure("correct", foreground=COLORS["correct"], font=("Consolas", self.exercise_font_size, "bold"))
        self.phrase_text.tag_configure("wrong", foreground=COLORS["wrong"], font=("Consolas", self.exercise_font_size, "bold"))
        self.phrase_text.tag_configure("current", background=COLORS["current"], foreground="#1e1b4b", font=("Consolas", self.exercise_font_size, "bold"))

        # Поле ввода
        input_size = max(16, min(36, self.exercise_font_size - 6))  # чутко меньше текста
        self.input_entry = ctk.CTkEntry(
            self.training_frame,
            font=ctk.CTkFont(size=input_size, family="Consolas"),
            height=52,
            placeholder_text="Погнали! ⚡ Начни печатать сюда..." if self.lang == "ru" else "Let's go! ⚡ Start typing here...",
            corner_radius=12,
        )
        self.input_entry.grid(row=4, column=0, padx=24, pady=(0, 12), sticky="ew")
        self.input_entry.bind("<KeyRelease>", self._on_key)
        self.input_entry.bind("<Return>", lambda e: None)

        # Нижняя панель: скорость + кнопка
        bottom = ctk.CTkFrame(self.training_frame, fg_color="transparent")
        bottom.grid(row=5, column=0, padx=24, pady=(0, 20), sticky="ew")
        bottom.grid_columnconfigure(1, weight=1)

        self.speed_label = ctk.CTkLabel(
            bottom,
            text="⚡ Скорость: — зн/мин" if self.lang == "ru" else "⚡ Speed: — cpm",
            font=ctk.CTkFont(size=17),
            text_color=COLORS["text_muted"],
        )
        self.speed_label.grid(row=0, column=0, sticky="w")

        self.status_label = ctk.CTkLabel(
            bottom,
            text="",
            font=ctk.CTkFont(size=16),
            text_color="#22c55e",
        )
        self.status_label.grid(row=0, column=1, sticky="w", padx=(16, 0))

        self._apply_exercise_font()

        ctk.CTkButton(
            bottom,
            text="🔄 Новая фраза",
            width=150,
            height=40,
            fg_color=COLORS["sidebar_active"],
            hover_color=COLORS["sidebar_hover"],
            corner_radius=12,
            command=self._new_phrase,
        ).grid(row=0, column=2, sticky="e")

        # === ЭКРАН ПРОГРЕССА (полная страница) ===
        self.progress_frame = ctk.CTkFrame(content, fg_color=COLORS["main_bg"], corner_radius=0)
        self.progress_frame.grid(row=0, column=0, sticky="nsew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_rowconfigure(2, weight=1)
        self._build_progress_ui()

        # === ЭКРАН СТАТИСТИКИ (полная страница) ===
        self.stats_frame = ctk.CTkFrame(content, fg_color=COLORS["main_bg"], corner_radius=0)
        self.stats_frame.grid(row=0, column=0, sticky="nsew")
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.grid_rowconfigure(2, weight=1)
        self._build_stats_ui()

        # Показать меню, скрыть тренажёр до выбора режима
        self.training_frame.lower(self.menu_frame)
        self.stats_frame.lower(self.menu_frame)
        self.progress_frame.lower(self.menu_frame)
        self.menu_frame.tkraise()

        self._prev_frame = self.menu_frame
        self._current_screen = "menu"

    def _apply_exercise_font(self):
        """Применение размера шрифта к тексту упражнения и полю ввода."""
        sz = self.exercise_font_size
        self.phrase_text.configure(font=("Consolas", sz))
        self.phrase_text.tag_configure("correct", foreground=COLORS["correct"], font=("Consolas", sz, "bold"))
        self.phrase_text.tag_configure("wrong", foreground=COLORS["wrong"], font=("Consolas", sz, "bold"))
        self.phrase_text.tag_configure("current", background=COLORS["current"], foreground="#1e1b4b", font=("Consolas", sz, "bold"))
        input_sz = max(16, min(36, sz - 6))
        self.input_entry.configure(font=ctk.CTkFont(size=input_sz, family="Consolas"))
        if hasattr(self, "font_size_label"):
            self.font_size_label.configure(text=str(sz))

    def _change_font_size(self, delta: int):
        """Изменение размера шрифта в упражнениях."""
        self.exercise_font_size = max(14, min(48, self.exercise_font_size + delta))
        self._save_font_size()
        self._apply_exercise_font()
        self._update_phrase_display()

    def _rotate_hint(self):
        """Ротация подсказок каждые 8 секунд."""
        tips = TIPS if self.lang == "ru" else TIPS_EN
        hints = MODE_HINTS if self.lang == "ru" else MODE_HINTS_EN
        tip = random.choice(tips)
        mode_hint = hints.get(self.mode_key, "")
        full = f"💡 {tip}" + (f"  •  {mode_hint}" if mode_hint else "")
        self.hint_label.configure(text=full)
        self.after(8000, self._rotate_hint)

    def _set_lang(self, lang: str):
        """Переключение языка раскладки."""
        self.lang = lang
        self.btn_lang_ru.configure(fg_color=COLORS["sidebar_active"] if lang == "ru" else "transparent")
        self.btn_lang_en.configure(fg_color=COLORS["sidebar_active"] if lang == "en" else "transparent")
        self.header_title.configure(text="⌨️ ТРЕНАЖЁР ПЕЧАТИ" if lang == "ru" else "⌨️ TYPING TRAINER")
        self.menu_title_label.configure(text="Выбери режим 👇" if lang == "ru" else "Choose a mode 👇")
        self.btn_back.configure(text="← Назад в меню" if lang == "ru" else "← Back to menu")
        self.font_label.configure(text="Шрифт:" if lang == "ru" else "Font:")
        self.speed_label.configure(text="⚡ Скорость: — зн/мин" if lang == "ru" else "⚡ Speed: — cpm")
        labels = MODE_LABELS if lang == "ru" else MODE_LABELS_EN
        for key, btn in self.mode_buttons.items():
            btn.configure(text=labels[key])
        self.input_entry.configure(placeholder_text="Погнали! ⚡ Начни печатать сюда..." if lang == "ru" else "Let's go! ⚡ Start typing here...")
        self.breadcrumb_label.configure(text=f"{'Уроки' if lang == 'ru' else 'Lessons'} > {labels[self.mode_key]}")
        self._new_phrase()
        self._rotate_hint()

    def _start_mode(self, mode_key: str):
        """Переход в режим тренировки после выбора режима в меню."""
        self.mode_key = mode_key
        labels = MODE_LABELS if self.lang == "ru" else MODE_LABELS_EN
        self.breadcrumb_label.configure(text=f"{'Уроки' if self.lang == 'ru' else 'Lessons'} > {labels[mode_key]}")
        hints = MODE_HINTS if self.lang == "ru" else MODE_HINTS_EN
        tips = TIPS if self.lang == "ru" else TIPS_EN
        self.hint_label.configure(text=f"💡 {hints.get(mode_key, '')}  •  {random.choice(tips)}")
        self._current_screen = "training"
        self.training_frame.tkraise()
        self._new_phrase()
        self.input_entry.focus_set()

    def _back_to_menu(self):
        """Возврат в меню выбора режима."""
        self._current_screen = "menu"
        self.menu_frame.tkraise()

    def _update_timer(self):
        if not self.is_typing or self.start_time is None:
            return
        elapsed = int(time.time() - self.start_time)
        m, s = divmod(elapsed, 60)
        self.timer_label.configure(text=f"{m:02d}:{s:02d}")
        self.timer_id = self.after(500, self._update_timer)

    def _generate_text(self) -> str:
        if self.lang == "en":
            return self._generate_text_en()
        return self._generate_text_ru()

    def _generate_text_ru(self) -> str:
        if self.mode_key == "phrases":
            return random.choice(PHRASES)
        if self.mode_key == "words":
            return " ".join(random.choices(WORDS, k=8))
        if self.mode_key == "letters":
            seq = [random.choice(LETTERS) for _ in range(36)]
            return " ".join("".join(seq[i:i+3]) for i in range(0, 36, 3))
        if self.mode_key == "numbers":
            seq = [random.choice(DIGITS) for _ in range(30)]
            return " ".join("".join(seq[i:i+3]) for i in range(0, 30, 3))
        if self.mode_key == "twisters":
            return random.choice(TONGUE_TWISTERS)
        if self.mode_key == "quotes":
            return random.choice(QUOTES)
        if self.mode_key == "code":
            return "  ".join(random.choices(CODE_SNIPPETS, k=4))
        if self.mode_key == "mixed":
            parts = [random.choice(WORDS) for _ in range(4)]
            parts.append("".join(random.choices(DIGITS, k=4)))
            parts.append(random.choice(SYMBOLS))
            parts.append(random.choice(WORDS))
            return " ".join(parts)
        return random.choice(PHRASES)

    def _generate_text_en(self) -> str:
        if self.mode_key == "phrases":
            return random.choice(PHRASES_EN)
        if self.mode_key == "words":
            return " ".join(random.choices(WORDS_EN, k=8))
        if self.mode_key == "letters":
            seq = [random.choice(LETTERS_EN) for _ in range(36)]
            return " ".join("".join(seq[i:i+3]) for i in range(0, 36, 3))
        if self.mode_key == "numbers":
            seq = [random.choice(DIGITS) for _ in range(30)]
            return " ".join("".join(seq[i:i+3]) for i in range(0, 30, 3))
        if self.mode_key == "twisters":
            return random.choice(TONGUE_TWISTERS_EN)
        if self.mode_key == "quotes":
            return random.choice(QUOTES_EN)
        if self.mode_key == "code":
            return "  ".join(random.choices(CODE_SNIPPETS, k=4))
        if self.mode_key == "mixed":
            parts = [random.choice(WORDS_EN) for _ in range(4)]
            parts.append("".join(random.choices(DIGITS, k=4)))
            parts.append(random.choice(SYMBOLS))
            parts.append(random.choice(WORDS_EN))
            return " ".join(parts)
        return random.choice(PHRASES_EN)

    def _new_phrase(self):
        self.current_phrase = self._generate_text()
        self.user_input = ""
        self.input_entry.delete(0, "end")
        self.start_time = None
        self.is_typing = False
        self.exercise_done = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_label.configure(text="⏱️ 00:00")
        self.accuracy_label.configure(text="🎯 0%")
        self.speed_label.configure(text="⚡ Скорость: — зн/мин" if self.lang == "ru" else "⚡ Speed: — cpm")
        self.status_label.configure(text="")
        self._update_phrase_display()
        self.input_entry.focus_set()

    def _update_phrase_display(self):
        self.phrase_text.configure(state="normal")
        self.phrase_text.delete("1.0", "end")
        for i, char in enumerate(self.current_phrase):
            if i < len(self.user_input):
                tag = "correct" if self.user_input[i] == char else "wrong"
                self.phrase_text.insert("end", char, tag)
            else:
                tag = "current" if i == len(self.user_input) else None
                self.phrase_text.insert("end", char, tag or ())
        self.phrase_text.configure(state="disabled")

    def _on_key(self, event):
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"):
            return
        if self.exercise_done:
            return

        self.user_input = self.input_entry.get()

        if not self.is_typing and self.user_input:
            self.start_time = time.time()
            self.is_typing = True
            self._update_timer()

        if self.user_input:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                cpm = (len(self.user_input) / elapsed) * 60
                self.speed_label.configure(text=f"⚡ Скорость: {cpm:.0f} зн/мин" if self.lang == "ru" else f"⚡ Speed: {cpm:.0f} cpm")
            # Точность: правильные / введённые * 100
            correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.current_phrase) and c == self.current_phrase[i])
            total = len(self.user_input)
            acc = (correct / total * 100) if total else 0
            self.accuracy_label.configure(text=f"{acc:.0f}%")

        self._update_phrase_display()

        if len(self.user_input) >= len(self.current_phrase):
            self._finish_exercise()

    def _finish_exercise(self):
        if self.exercise_done:
            return
        self.exercise_done = True
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        if self.start_time is None:
            return
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            cpm = (len(self.user_input) / elapsed) * 60
            correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.current_phrase) and c == self.current_phrase[i])
            total = len(self.user_input)
            acc = (correct / total * 100) if total else 0
            self._save_progress(cpm, len(self.current_phrase), acc)
            msg = random.choice(COMPLETION_MSGS if self.lang == "ru" else COMPLETION_MSGS_EN)
            self.status_label.configure(text=f"{msg}  {cpm:.0f} зн/мин" if self.lang == "ru" else f"{msg}  {cpm:.0f} cpm")
        self.input_entry.configure(state="disabled")
        self.after(100, lambda: (self.input_entry.configure(state="normal"), self.input_entry.focus_set()))

    def _show_progress(self):
        self._prev_frame = self.training_frame if getattr(self, "_current_screen", None) == "training" else self.menu_frame
        self._current_screen = "progress"
        self._refresh_progress()
        self.progress_frame.tkraise()

    def _show_stats(self):
        self._prev_frame = self.training_frame if getattr(self, "_current_screen", None) == "training" else self.menu_frame
        self._current_screen = "stats"
        self._refresh_stats()
        self.stats_frame.tkraise()

    def _back_from_progress(self):
        self._prev_frame.tkraise()

    def _back_from_stats(self):
        self._prev_frame.tkraise()

    def _build_progress_ui(self):
        """Сборка интерфейса экрана прогресса."""
        top = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        top.grid(row=0, column=0, padx=24, pady=(24, 16), sticky="ew")
        top.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(top, text="← Назад" if self.lang == "ru" else "← Back",
            width=120, height=40, fg_color=COLORS["sidebar_active"], hover_color=COLORS["sidebar_hover"],
            command=self._back_from_progress).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(top, text="История тренировок" if self.lang == "ru" else "Training History",
            font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["text_dark"]).grid(row=0, column=1, sticky="w", padx=(24, 0))

        # Карточки с общей статистикой
        cards_row = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        cards_row.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="ew")
        cards_row.grid_columnconfigure((0, 1, 2), weight=1)
        self.progress_total_card = ctk.CTkFrame(cards_row, fg_color=COLORS["card_bg"], corner_radius=16, height=100)
        self.progress_total_card.grid(row=0, column=0, padx=(0, 12), pady=0, sticky="ew")
        self.progress_total_card.grid_propagate(False)
        self.progress_avg_card = ctk.CTkFrame(cards_row, fg_color=COLORS["header"], corner_radius=16, height=100)
        self.progress_avg_card.grid(row=0, column=1, padx=12, pady=0, sticky="ew")
        self.progress_avg_card.grid_propagate(False)
        self.progress_max_card = ctk.CTkFrame(cards_row, fg_color=COLORS["sidebar_active"], corner_radius=16, height=100)
        self.progress_max_card.grid(row=0, column=2, padx=(12, 0), pady=0, sticky="ew")
        self.progress_max_card.grid_propagate(False)
        self.progress_total_label = ctk.CTkLabel(self.progress_total_card, text="—", font=ctk.CTkFont(size=32, weight="bold"), text_color="#a5b4fc")
        self.progress_total_label.place(relx=0.5, rely=0.35, anchor="center")
        self.progress_total_sub = ctk.CTkLabel(self.progress_total_card, text="Упражнений" if self.lang == "ru" else "Exercises", font=ctk.CTkFont(size=13), text_color="#a5b4fc")
        self.progress_total_sub.place(relx=0.5, rely=0.7, anchor="center")
        self.progress_avg_label = ctk.CTkLabel(self.progress_avg_card, text="—", font=ctk.CTkFont(size=32, weight="bold"), text_color="white")
        self.progress_avg_label.place(relx=0.5, rely=0.35, anchor="center")
        self.progress_avg_sub = ctk.CTkLabel(self.progress_avg_card, text="Ср. скорость" if self.lang == "ru" else "Avg speed", font=ctk.CTkFont(size=13), text_color="#e2e8f0")
        self.progress_avg_sub.place(relx=0.5, rely=0.7, anchor="center")
        self.progress_max_label = ctk.CTkLabel(self.progress_max_card, text="—", font=ctk.CTkFont(size=32, weight="bold"), text_color="white")
        self.progress_max_label.place(relx=0.5, rely=0.35, anchor="center")
        self.progress_max_sub = ctk.CTkLabel(self.progress_max_card, text="Рекорд" if self.lang == "ru" else "Best", font=ctk.CTkFont(size=13), text_color="#e2e8f0")
        self.progress_max_sub.place(relx=0.5, rely=0.7, anchor="center")

        # Область для графика и таблицы
        main_area = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        main_area.grid(row=2, column=0, padx=24, pady=(0, 24), sticky="nsew")
        main_area.grid_columnconfigure(0, weight=1)
        main_area.grid_rowconfigure(0, weight=1)
        self.progress_chart_container = ctk.CTkFrame(main_area, fg_color="white", corner_radius=16, height=220)
        self.progress_chart_container.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        self.progress_chart_container.grid_propagate(False)
        self.progress_chart_container.grid_columnconfigure(0, weight=1)
        self.progress_chart_container.grid_rowconfigure(0, weight=1)
        self.progress_table = ctk.CTkScrollableFrame(main_area, fg_color="#f1f5f9", corner_radius=12, height=200)
        self.progress_table.grid(row=1, column=0, sticky="nsew")

    def _build_stats_ui(self):
        """Сборка интерфейса экрана статистики."""
        top = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        top.grid(row=0, column=0, padx=24, pady=(24, 16), sticky="ew")
        top.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(top, text="← Назад" if self.lang == "ru" else "← Back",
            width=120, height=40, fg_color=COLORS["sidebar_active"], hover_color=COLORS["sidebar_hover"],
            command=self._back_from_stats).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(top, text="Сводная статистика" if self.lang == "ru" else "Statistics Overview",
            font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["text_dark"]).grid(row=0, column=1, sticky="w", padx=(24, 0))

        self.stats_tabview = ctk.CTkTabview(self.stats_frame, corner_radius=12)
        self.stats_tabview.grid(row=2, column=0, padx=24, pady=(0, 24), sticky="nsew")
        for name, level in [("День", "day"), ("Месяц", "month"), ("Год", "year")]:
            self.stats_tabview.add(name)
        self.stats_chart_containers = {}
        for name, level in [("День", "day"), ("Месяц", "month"), ("Год", "year")]:
            tab = self.stats_tabview.tab(name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
            container = ctk.CTkFrame(tab, fg_color="white", corner_radius=12)
            container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)
            self.stats_chart_containers[level] = container

    def _refresh_progress(self):
        """Обновление данных и графика прогресса."""
        data = self.progress_data
        total = len(data)
        avg = sum(p["speed_cpm"] for p in data) / total if total else 0
        best = max((p["speed_cpm"] for p in data), default=0)
        self.progress_total_label.configure(text=str(total))
        self.progress_avg_label.configure(text=f"{avg:.0f}" + (" зн/мин" if self.lang == "ru" else " cpm"))
        self.progress_max_label.configure(text=f"{best:.0f}" + (" зн/мин" if self.lang == "ru" else " cpm"))
        for w in self.progress_chart_container.winfo_children():
            w.destroy()
        for w in self.progress_table.winfo_children():
            w.destroy()
        if data:
            try:
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                from matplotlib.figure import Figure
                fig = Figure(figsize=(7, 3), dpi=80, facecolor="#ffffff")
                ax = fig.add_subplot(111)
                recent = list(reversed(data[-30:]))
                x = list(range(len(recent)))
                y = [p["speed_cpm"] for p in recent]
                ax.fill_between(x, y, alpha=0.3, color=COLORS["header"])
                ax.plot(x, y, color=COLORS["header"], linewidth=2, marker="o", markersize=4)
                ax.set_facecolor("#ffffff")
                ax.set_xlabel("№" if self.lang == "ru" else "#", fontsize=10, color="#64748b")
                ax.set_ylabel("зн/мин" if self.lang == "ru" else "cpm", fontsize=10, color="#64748b")
                ax.tick_params(colors="#64748b")
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                fig.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=self.progress_chart_container)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)
                self._progress_canvas = canvas
            except Exception:
                ctk.CTkLabel(self.progress_chart_container, text="График недоступен" if self.lang == "ru" else "Chart unavailable",
                    font=ctk.CTkFont(size=14), text_color="gray").pack(expand=True, pady=40)
        else:
            ctk.CTkLabel(self.progress_chart_container, text="Нет данных для графика" if self.lang == "ru" else "No data for chart",
                font=ctk.CTkFont(size=14), text_color="gray").pack(expand=True, pady=40)
        labels = MODE_LABELS if self.lang == "ru" else MODE_LABELS_EN
        h = ctk.CTkFrame(self.progress_table, fg_color="transparent")
        h.pack(fill="x", pady=(8, 6))
        for t, w in [("Дата" if self.lang == "ru" else "Date", 90), ("Время" if self.lang == "ru" else "Time", 70), ("Скорость", 90), ("Точность" if self.lang == "ru" else "Accuracy", 70), ("Режим" if self.lang == "ru" else "Mode", 100)]:
            ctk.CTkLabel(h, text=t, font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["text_muted"], width=w, anchor="w").pack(side="left")
        for entry in reversed(data[-50:]):
            row = ctk.CTkFrame(self.progress_table, fg_color="transparent")
            row.pack(fill="x", pady=2)
            mode = labels.get(entry.get("mode", "phrases"), "Фразы" if self.lang == "ru" else "Phrases")
            for val, w in [(entry["date"], 90), (entry["time"], 70), (f"{entry['speed_cpm']:.1f}", 90), (f"{entry.get('accuracy', 0):.0f}%", 70), (mode, 100)]:
                ctk.CTkLabel(row, text=str(val), font=ctk.CTkFont(size=12), width=w, anchor="w").pack(side="left")

    def _refresh_stats(self):
        """Обновление графиков статистики."""
        data = self.progress_data
        for level in ["day", "month", "year"]:
            container = self.stats_chart_containers[level]
            for w in container.winfo_children():
                w.destroy()
        if not data:
            for level in ["day", "month", "year"]:
                ctk.CTkLabel(self.stats_chart_containers[level], text="Пока нет данных." if self.lang == "ru" else "No data yet.",
                    font=ctk.CTkFont(size=14), text_color="gray").pack(expand=True, pady=40)
            return
        for level in ["day", "month", "year"]:
            groups = defaultdict(lambda: {"speeds": [], "count": 0})
            for e in data:
                d = e.get("date", "")
                if not d:
                    continue
                k = d[:4] if level == "year" else (d[:7] if level == "month" else d)
                groups[k]["speeds"].append(e.get("speed_cpm", 0))
                groups[k]["count"] += 1
            container = self.stats_chart_containers[level]
            items = [(k, g) for k, g in groups.items() if g["speeds"]]
            items.sort(key=lambda x: x[0], reverse=True)
            items = items[:15]
            if not items:
                ctk.CTkLabel(container, text="Пока нет данных." if self.lang == "ru" else "No data yet.",
                    font=ctk.CTkFont(size=14), text_color="gray").pack(expand=True, pady=40)
                continue
            try:
                import matplotlib
                matplotlib.use("Agg")
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                from matplotlib.figure import Figure
                fig = Figure(figsize=(6, 3.5), dpi=80, facecolor="#ffffff")
                ax = fig.add_subplot(111)
                labels_list = [x[0] for x in reversed(items)]
                avg_speeds = [sum(x[1]["speeds"]) / len(x[1]["speeds"]) for x in reversed(items)]
                colors = [COLORS["header"] if i < len(avg_speeds) - 1 else COLORS["sidebar_active"] for i in range(len(avg_speeds))]
                bars = ax.bar(range(len(labels_list)), avg_speeds, color=colors, edgecolor="none")
                ax.set_xticks(range(len(labels_list)))
                ax.set_xticklabels(labels_list, rotation=45, ha="right")
                ax.set_facecolor("#ffffff")
                ax.set_ylabel("зн/мин" if self.lang == "ru" else "cpm", fontsize=10, color="#64748b")
                ax.tick_params(colors="#64748b")
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                fig.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=container)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)
            except Exception:
                ctk.CTkLabel(container, text="График недоступен" if self.lang == "ru" else "Chart unavailable",
                    font=ctk.CTkFont(size=14), text_color="gray").pack(expand=True, pady=40)


def main():
    app = TypingTrainerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
