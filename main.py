"""
Тренажёр слепой печати
Приложение для тренировки скорости и точности набора текста.
"""

import json
import sys
import time
import random
from datetime import datetime
from pathlib import Path

# Путь к данным: рядом с exe при сборке PyInstaller, иначе — папка скрипта
if getattr(sys, "frozen", False):
    _base_path = Path(sys.executable).parent
else:
    _base_path = Path(__file__).parent

import customtkinter as ctk

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
    "Правильная осанка важна для комфортной работы за компьютером.",
    "Многие профессии требуют быстрого набора текста.",
    "Тренажёры печати доступны бесплатно в интернете.",
    "Постепенно увеличивайте сложность упражнений.",
]

# Слова и символы для разных типов упражнений
WORDS = [
    "клавиатура",
    "монитор",
    "компьютер",
    "программа",
    "интернет",
    "память",
    "процессор",
    "мышь",
    "кнопка",
    "окно",
    "текст",
    "скорость",
    "упражнение",
    "символ",
    "пальцы",
    "клавиши",
]

LETTERS = list("фывапролджэйцукенгшщзхъячсмитьбю")
DIGITS = "0123456789"

MODE_LABELS = {
    "phrases": "Фразы",
    "words": "Слова",
    "letters": "Буквы",
    "numbers": "Цифры",
}


class TypingTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Тренажёр слепой печати")
        self.geometry("900x600")
        self.minsize(700, 500)

        # Тема: мягкие нейтральные цвета
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=("#f5f5f5", "#2b2b2b"))
        self._configure_colors()

        self.data_path = _base_path / "progress.json"
        self.progress_data = self._load_progress()

        self.current_phrase = ""
        self.user_input = ""
        self.start_time = None
        self.is_typing = False
        self.exercise_done = False
        self.mode_key = "phrases"

        # Агрегированные показатели для декоративных карточек
        self.total_exercises = len(self.progress_data)
        self.best_speed_overall = (
            max((p.get("speed_cpm", 0) for p in self.progress_data), default=0.0)
        )

        self._build_ui()

    def _configure_colors(self):
        """Цветовая схема: спокойная, не вырвиглазная."""
        self.colors = {
            "bg": ("#f5f5f5", "#2b2b2b"),
            "card": ("#ffffff", "#3d3d3d"),
            "text": ("#333333", "#e0e0e0"),
            "accent": ("#4a90d9", "#5a9fd9"),
            "correct": ("#2e7d32", "#4caf50"),
            "wrong": ("#c62828", "#ef5350"),
            "muted": ("#757575", "#9e9e9e"),
        }

    def _load_progress(self) -> list:
        """Загрузка истории прогресса из JSON."""
        if self.data_path.exists():
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def _save_progress(self, speed: float, phrase_len: int):
        """Сохранение результата сессии."""
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "speed_cpm": round(speed, 1),
            "chars": phrase_len,
            "mode": self.mode_key,
        }
        self.progress_data.append(entry)
        # Обновляем агрегированные показатели
        self.total_exercises = len(self.progress_data)
        self.best_speed_overall = max(self.best_speed_overall, entry["speed_cpm"])
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.progress_data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _build_ui(self):
        """Построение интерфейса."""
        # Верхняя панель
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(16, 4))

        title_block = ctk.CTkFrame(top_frame, fg_color="transparent")
        title_block.pack(side="left")

        ctk.CTkLabel(
            title_block,
            text="Тренажёр слепой печати",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["text"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block,
            text="Тренируй скорость, точность и разные типы упражнений",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["muted"],
        ).pack(anchor="w", pady=(2, 0))

        # Правый блок: выбор режима + кнопки статистики
        right_top = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_top.pack(side="right")

        # Меню выбора режима упражнения
        import tkinter

        self.mode_var = tkinter.StringVar(value=MODE_LABELS[self.mode_key])
        self.mode_menu = ctk.CTkOptionMenu(
            right_top,
            variable=self.mode_var,
            values=list(MODE_LABELS.values()),
            command=self._on_mode_change,
            width=170,
        )
        self.mode_menu.pack(side="left", padx=(0, 8))

        self.btn_progress = ctk.CTkButton(
            right_top,
            text="Прогресс",
            width=110,
            command=self._show_progress,
            fg_color=self.colors["accent"],
        )
        self.btn_progress.pack(side="left", padx=(0, 4))

        self.btn_stats = ctk.CTkButton(
            right_top,
            text="Статистика",
            width=110,
            command=self._show_stats,
        )
        self.btn_stats.pack(side="left")

        # Декоративная цветная линия под заголовком
        ctk.CTkFrame(self, fg_color=self.colors["accent"], height=2).pack(
            fill="x", padx=20, pady=(0, 8)
        )

        # Карточки-обзор: сегодня, всего, лучший результат
        overview = ctk.CTkFrame(self, fg_color="transparent")
        overview.pack(fill="x", padx=20, pady=(0, 10))

        card_kwargs = dict(fg_color=self.colors["card"], corner_radius=12)

        self.card_today = ctk.CTkFrame(overview, **card_kwargs)
        self.card_total = ctk.CTkFrame(overview, **card_kwargs)
        self.card_best = ctk.CTkFrame(overview, **card_kwargs)

        self.card_today.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.card_total.pack(side="left", fill="x", expand=True, padx=6)
        self.card_best.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # Карточка "Сегодня"
        ctk.CTkLabel(
            self.card_today,
            text="Сегодня",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"],
        ).pack(anchor="w", padx=12, pady=(10, 0))
        self.card_today_value = ctk.CTkLabel(
            self.card_today,
            text="—",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.card_today_value.pack(anchor="w", padx=12, pady=(2, 10))

        # Карточка "Всего упражнений"
        ctk.CTkLabel(
            self.card_total,
            text="Всего упражнений",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"],
        ).pack(anchor="w", padx=12, pady=(10, 0))
        self.card_total_value = ctk.CTkLabel(
            self.card_total,
            text="0",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.card_total_value.pack(anchor="w", padx=12, pady=(2, 10))

        # Карточка "Лучший результат"
        ctk.CTkLabel(
            self.card_best,
            text="Лучший результат",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"],
        ).pack(anchor="w", padx=12, pady=(10, 0))
        self.card_best_value = ctk.CTkLabel(
            self.card_best,
            text="—",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.card_best_value.pack(anchor="w", padx=12, pady=(2, 10))

        # Область с фразой (tkinter.Text для подсветки символов)
        phrase_frame = ctk.CTkFrame(self, fg_color=self.colors["card"], corner_radius=12)
        phrase_frame.pack(fill="both", expand=True, padx=20, pady=10)

        from tkinter import Text
        # Цвета фона/текста в зависимости от темы
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg, fg = ("#ffffff", "#333333") if not is_dark else ("#3d3d3d", "#e0e0e0")
        self.phrase_text = Text(
            phrase_frame,
            font=("Consolas", 18),
            wrap="word",
            height=5,
            relief="flat",
            padx=16,
            pady=16,
            state="disabled",
            cursor="arrow",
            bg=bg,
            fg=fg,
            insertwidth=0,
        )
        self.phrase_text.pack(fill="both", expand=True, padx=16, pady=16)

        # Поле ввода
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.input_entry = ctk.CTkEntry(
            input_frame,
            font=ctk.CTkFont(size=18, family="Consolas"),
            height=50,
            placeholder_text="Начните печатать здесь...",
        )
        self.input_entry.pack(fill="x")
        self.input_entry.bind("<KeyRelease>", self._on_key)
        self.input_entry.bind("<Return>", lambda e: None)  # блокируем Enter

        # Нижняя панель: скорость и кнопки
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        left_panel = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        left_panel.pack(side="left")

        self.speed_label = ctk.CTkLabel(
            left_panel,
            text="Скорость: — зн/мин",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["muted"],
        )
        self.speed_label.pack(anchor="w")

        self.status_label = ctk.CTkLabel(
            left_panel,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["muted"],
        )
        self.status_label.pack(anchor="w")

        right_panel = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        right_panel.pack(side="right")

        ctk.CTkButton(
            right_panel,
            text="Новая фраза",
            width=140,
            command=self._new_phrase,
            fg_color=self.colors["accent"],
        ).pack(side="left", padx=(0, 8))

        self._new_phrase()
        self.input_entry.focus_set()
        self._update_overview_cards()

    def _on_mode_change(self, selected_label: str):
        """Переключение режима упражнения из меню."""
        for key, label in MODE_LABELS.items():
            if label == selected_label:
                self.mode_key = key
                break
        self._new_phrase()

        # Обновляем декоративные карточки (режим влияет на тренировки за сегодня)
        self._update_overview_cards()

    def _update_overview_cards(self):
        """Обновляет декоративные карточки со сводной информацией."""
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_speeds = [p.get("speed_cpm", 0) for p in self.progress_data if p.get("date") == today_str]
        today_avg = sum(today_speeds) / len(today_speeds) if today_speeds else 0.0

        self.card_today_value.configure(text=f"{today_avg:.1f} зн/мин" if today_speeds else "—")
        self.card_total_value.configure(text=str(self.total_exercises))
        self.card_best_value.configure(
            text=f"{self.best_speed_overall:.1f} зн/мин" if self.best_speed_overall > 0 else "—"
        )

    def _generate_text(self) -> str:
        """Генерация текста в зависимости от выбранного режима."""
        if self.mode_key == "phrases":
            return random.choice(PHRASES)
        if self.mode_key == "words":
            words = [random.choice(WORDS) for _ in range(6)]
            return " ".join(words)
        if self.mode_key == "letters":
            seq = [random.choice(LETTERS) for _ in range(36)]
            groups = ["".join(seq[i : i + 3]) for i in range(0, len(seq), 3)]
            return " ".join(groups)
        if self.mode_key == "numbers":
            seq = [random.choice(DIGITS) for _ in range(30)]
            groups = ["".join(seq[i : i + 3]) for i in range(0, len(seq), 3)]
            return " ".join(groups)
        return random.choice(PHRASES)

    def _new_phrase(self):
        """Выбор новой фразы для тренировки."""
        self.current_phrase = self._generate_text()
        self.user_input = ""
        self.input_entry.delete(0, "end")
        self.start_time = None
        self.is_typing = False
        self.exercise_done = False
        self._update_phrase_display()
        self.speed_label.configure(text="Скорость: — зн/мин")
        self.status_label.configure(text="")
        self.input_entry.focus_set()

    def _update_phrase_display(self):
        """Обновление отображения фразы с подсветкой правильных/неправильных символов."""
        self.phrase_text.configure(state="normal")
        self.phrase_text.delete("1.0", "end")

        self.phrase_text.tag_configure("correct", foreground="#2e7d32")
        self.phrase_text.tag_configure("wrong", foreground="#c62828")
        self.phrase_text.tag_configure("current", background="#e3f2fd", foreground="#1565c0")

        for i, char in enumerate(self.current_phrase):
            if i < len(self.user_input):
                if self.user_input[i] == char:
                    self.phrase_text.insert("end", char, "correct")
                else:
                    self.phrase_text.insert("end", char, "wrong")
            else:
                if i == len(self.user_input):
                    self.phrase_text.insert("end", char, "current")
                else:
                    self.phrase_text.insert("end", char)

        self.phrase_text.configure(state="disabled")

    def _on_key(self, event):
        """Обработка нажатия клавиши."""
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"):
            return
        if self.exercise_done:
            return

        self.user_input = self.input_entry.get()

        if not self.is_typing and self.user_input:
            self.start_time = time.time()
            self.is_typing = True

        if self.user_input:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                cpm = (len(self.user_input) / elapsed) * 60
                self.speed_label.configure(text=f"Скорость: {cpm:.0f} зн/мин")

        self._update_phrase_display()

        # Проверка завершения
        if len(self.user_input) >= len(self.current_phrase):
            self._finish_exercise()

    def _finish_exercise(self):
        """Завершение упражнения и сохранение результата."""
        if self.exercise_done:
            return
        self.exercise_done = True
        if self.start_time is None:
            return
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            cpm = (len(self.user_input) / elapsed) * 60
            self._save_progress(cpm, len(self.current_phrase))
            self.status_label.configure(
                text=f"Готово! Скорость: {cpm:.0f} зн/мин. Нажмите «Новая фраза» для продолжения."
            )
        self.input_entry.configure(state="disabled")
        self.after(100, lambda: (self.input_entry.configure(state="normal"), self.input_entry.focus_set()))

    def _show_progress(self):
        """Открытие окна прогресса."""
        ProgressWindow(self, self.progress_data)


    def _show_stats(self):
        """Открытие окна сводной статистики."""
        StatsWindow(self, self.progress_data)


class ProgressWindow(ctk.CTkToplevel):
    """Окно с историей прогресса."""

    def __init__(self, parent, progress_data: list):
        super().__init__(parent)
        self.title("Прогресс")
        self.geometry("500x450")
        self.transient(parent)

        self.progress_data = progress_data

        ctk.CTkLabel(
            self,
            text="История тренировок",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(20, 10))

        # Статистика
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)

        total = len(progress_data)
        avg_speed = sum(p["speed_cpm"] for p in progress_data) / total if total else 0

        ctk.CTkLabel(
            stats_frame,
            text=f"Всего упражнений: {total}",
            font=ctk.CTkFont(size=14),
        ).pack(anchor="w")
        ctk.CTkLabel(
            stats_frame,
            text=f"Средняя скорость: {avg_speed:.1f} зн/мин",
            font=ctk.CTkFont(size=14),
        ).pack(anchor="w")

        # Таблица
        table_frame = ctk.CTkScrollableFrame(self, height=280)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if not progress_data:
            ctk.CTkLabel(
                table_frame,
                text="Пока нет данных. Начните тренировку!",
                font=ctk.CTkFont(size=14),
                text_color="gray",
            ).pack(pady=20)
        else:
            # Заголовки
            header = ctk.CTkFrame(table_frame, fg_color="transparent")
            header.pack(fill="x", pady=(0, 5))
            ctk.CTkLabel(header, text="Дата", width=90, anchor="w").pack(side="left")
            ctk.CTkLabel(header, text="Время", width=70, anchor="w").pack(side="left")
            ctk.CTkLabel(header, text="Скорость (зн/мин)", width=140, anchor="w").pack(side="left")
            ctk.CTkLabel(header, text="Тип", width=120, anchor="w").pack(side="left")

            for entry in reversed(progress_data[-50:]):  # последние 50 записей
                row = ctk.CTkFrame(table_frame, fg_color="transparent")
                row.pack(fill="x", pady=2)
                mode_label = MODE_LABELS.get(entry.get("mode", "phrases"), "Фразы")
                ctk.CTkLabel(row, text=entry["date"], width=90, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=entry["time"], width=70, anchor="w").pack(side="left")
                ctk.CTkLabel(
                    row,
                    text=f"{entry['speed_cpm']:.1f}",
                    width=140,
                    anchor="w",
                ).pack(side="left")
                ctk.CTkLabel(row, text=mode_label, width=120, anchor="w").pack(side="left")

        ctk.CTkButton(
            self,
            text="Закрыть",
            width=120,
            command=self.destroy,
        ).pack(pady=20)


class StatsWindow(ctk.CTkToplevel):
    """Окно со сводной статистикой по дням, месяцам и годам."""

    def __init__(self, parent, progress_data: list):
        super().__init__(parent)
        self.title("Статистика")
        self.geometry("520x460")
        self.transient(parent)

        ctk.CTkLabel(
            self,
            text="Сводная статистика",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(20, 10))

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)

        tab_day = tabview.add("День")
        tab_month = tabview.add("Месяц")
        tab_year = tabview.add("Год")

        self._build_agg_tab(tab_day, progress_data, level="day")
        self._build_agg_tab(tab_month, progress_data, level="month")
        self._build_agg_tab(tab_year, progress_data, level="year")

        ctk.CTkButton(
            self,
            text="Закрыть",
            width=120,
            command=self.destroy,
        ).pack(pady=12)

    def _build_agg_tab(self, container, progress_data: list, level: str):
        """Строит агрегированную таблицу по выбранному уровню."""
        if not progress_data:
            ctk.CTkLabel(
                container,
                text="Пока нет данных для статистики.",
                font=ctk.CTkFont(size=14),
                text_color="gray",
            ).pack(pady=20)
            return

        # Группировка: по дню / месяцу / году
        groups: dict[str, dict[str, float | int | list[float]]] = {}
        for entry in progress_data:
            date_str = entry.get("date", "")
            if not date_str:
                continue
            if level == "day":
                key = date_str  # YYYY-MM-DD
            elif level == "month":
                key = date_str[:7]  # YYYY-MM
            else:
                key = date_str[:4]  # YYYY

            g = groups.setdefault(key, {"speeds": [], "count": 0})
            g["speeds"].append(entry.get("speed_cpm", 0))
            g["count"] += 1

        if not groups:
            ctk.CTkLabel(
                container,
                text="Нет корректных данных для отображения.",
                font=ctk.CTkFont(size=14),
                text_color="gray",
            ).pack(pady=20)
            return

        table = ctk.CTkScrollableFrame(container, height=320)
        table.pack(fill="both", expand=True, padx=4, pady=(5, 5))

        # Заголовок
        header = ctk.CTkFrame(table, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(header, text="Период", width=110, anchor="w").pack(side="left")
        ctk.CTkLabel(header, text="Упражнений", width=110, anchor="w").pack(side="left")
        ctk.CTkLabel(header, text="Ср. скорость", width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(header, text="Макс. скорость", width=120, anchor="w").pack(side="left")

        # Сортируем по возрастанию и показываем последние сначала
        for key in sorted(groups.keys(), reverse=True):
            g = groups[key]
            speeds = g["speeds"]
            count = g["count"]
            if not speeds or count == 0:
                continue
            avg_speed = sum(speeds) / count
            max_speed = max(speeds)

            row = ctk.CTkFrame(table, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=key, width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(count), width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"{avg_speed:.1f}", width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"{max_speed:.1f}", width=120, anchor="w").pack(side="left")


def main():
    app = TypingTrainerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
