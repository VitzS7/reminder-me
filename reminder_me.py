import customtkinter as ctk
from PIL import Image, ImageDraw
import pystray
import threading
from datetime import datetime, timedelta
import json
import os
from tkinter import messagebox

try:
    from winotify import Notification as WinNotify, audio as WinAudio
    _WINOTIFY = True
except ImportError:
    _WINOTIFY = False
    from plyer import notification as _plyer_notify

try:
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ReminderMe.App")
except Exception:
    pass

ctk.set_default_color_theme("blue")

APP_NAME = "Reminder Me"


def _app_base() -> str:
    import sys
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(exe_dir, "reminder-me")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


_BASE         = _app_base()
DATA_FILE     = os.path.join(_BASE, "reminders.json")
SETTINGS_FILE = os.path.join(_BASE, "settings.json")
COL_ERR       = "#E53935"
COL_OK        = "#43A047"
COL_WARN      = "#FB8C00"
COL_NEUTRAL   = "#777777"
ACCENT        = "#1565C0"
ACCENT_HOVER  = "#0D47A1"

LANGUAGES = {
    "English":            "en",
    "Português (Brasil)": "pt",
    "Español":            "es",
    "Русский":            "ru",
    "中文":               "zh",
}

TRANSLATIONS = {
    "en": {
        "title":            "Reminder Me",
        "desc_ph":          "What to remember…",
        "msg_ph":           "Extra message (optional)",
        "add":              "Add reminder",
        "edit":             "✏ Edit",
        "remove":           "🗑 Delete sel.",
        "clear_all":        "✕ Clear all",
        "your_reminders":   "Reminders",
        "no_reminders":     "No reminders yet.",
        "ready":            "Creator GitHub: VitzS7 | Instagram: @vitin_xzx",
        "language":         "Language",
        "repeat_types":     ["Once","Every hour","Daily","Every X minutes","Weekly","Monthly","Specific date"],
        "interval_min":     "min",
        "day_of_week":      "Day",
        "week_days":        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "day_of_month":     "Day (1–31)",
        "date_ph":          "YYYY-MM-DD",
        "tray_open":        "Open",
        "tray_quit":        "Quit",
        "clear_confirm":    "Remove ALL reminders?",
        "clear_title":      "Clear all",
        "notification_default": "Time for your reminder!",
        "edited_msg":       "Editing — press Add to save.",
        "removed_msg":      "Reminder removed.",
        "cleared_msg":      "All reminders removed.",
        "no_clear_msg":     "No reminders to remove.",
        "added_msg":        "'{}' added!",
        "sent_msg":         "🔔 {}",
        "notif_fail":       "Failed to send notification.",
        "err_desc":         "Description is required.",
        "err_time":         "Set a time for this reminder.",
        "err_time_fmt":     "Invalid time — use HH:MM.",
        "err_interval":     "Interval must be a positive integer.",
        "err_day_month":    "Day must be between 1 and 31.",
        "err_date":         "Enter the date (YYYY-MM-DD).",
        "err_date_time":    "Enter the time (HH:MM).",
        "err_date_fmt":     "Invalid date or time format.",
        "err_select_edit":  "Select a reminder to edit.",
        "err_select_del":   "Select a reminder to remove.",
        "time_dialog_title":"Set time",
        "confirm":          "Confirm",
        "emoji_title":      "Choose an emoji",
        "every_hour":       "Every hour",
        "every_x_min":      "Every {} min",
        "weekly_fmt":       "{} at {}",
        "monthly_fmt":      "Day {} at {}",
        "specific_fmt":     "{} {}",
        "time_lbl":         "🕐 Set time",
        "week_map": {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6},
    },
    "pt": {
        "title":            "Reminder Me",
        "desc_ph":          "O que lembrar…",
        "msg_ph":           "Mensagem extra (opcional)",
        "add":              "Adicionar lembrete",
        "edit":             "✏ Editar",
        "remove":           "🗑 Excluir sel.",
        "clear_all":        "✕ Limpar tudo",
        "your_reminders":   "Lembretes",
        "no_reminders":     "Nenhum lembrete ainda.",
        "ready":            "Criador GitHub: VitzS7 | Instagram: @vitin_xzx",
        "language":         "Idioma",
        "repeat_types":     ["Vez única","Cada hora","Diariamente","A cada X minutos","Semanalmente","Mensalmente","Data específica"],
        "interval_min":     "min",
        "day_of_week":      "Dia",
        "week_days":        ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"],
        "day_of_month":     "Dia (1–31)",
        "date_ph":          "AAAA-MM-DD",
        "tray_open":        "Abrir",
        "tray_quit":        "Sair",
        "clear_confirm":    "Remover TODOS os lembretes?",
        "clear_title":      "Limpar tudo",
        "notification_default": "Hora do seu lembrete!",
        "edited_msg":       "Editando — pressione Adicionar para salvar.",
        "removed_msg":      "Lembrete removido.",
        "cleared_msg":      "Todos os lembretes removidos.",
        "no_clear_msg":     "Nenhum lembrete para remover.",
        "added_msg":        "'{}' adicionado!",
        "sent_msg":         "🔔 {}",
        "notif_fail":       "Falha ao enviar notificação.",
        "err_desc":         "A descrição é obrigatória.",
        "err_time":         "Defina uma hora para este lembrete.",
        "err_time_fmt":     "Hora inválida — use HH:MM.",
        "err_interval":     "Intervalo deve ser um inteiro positivo.",
        "err_day_month":    "Dia deve ser entre 1 e 31.",
        "err_date":         "Informe a data (AAAA-MM-DD).",
        "err_date_time":    "Informe a hora (HH:MM).",
        "err_date_fmt":     "Data ou hora com formato inválido.",
        "err_select_edit":  "Selecione um lembrete para editar.",
        "err_select_del":   "Selecione um lembrete para remover.",
        "time_dialog_title":"Definir hora",
        "confirm":          "Confirmar",
        "emoji_title":      "Escolha um emoji",
        "every_hour":       "Toda hora",
        "every_x_min":      "A cada {} min",
        "weekly_fmt":       "{} às {}",
        "monthly_fmt":      "Dia {} às {}",
        "specific_fmt":     "{} {}",
        "time_lbl":         "🕐 Definir hora",
        "week_map": {"Segunda":0,"Terça":1,"Quarta":2,"Quinta":3,"Sexta":4,"Sábado":5,"Domingo":6},
    },
    "es": {
        "title":            "Reminder Me",
        "desc_ph":          "¿Qué recordar…?",
        "msg_ph":           "Mensaje extra (opcional)",
        "add":              "Agregar recordatorio",
        "edit":             "✏ Editar",
        "remove":           "🗑 Eliminar sel.",
        "clear_all":        "✕ Borrar todo",
        "your_reminders":   "Recordatorios",
        "no_reminders":     "Sin recordatorios aún.",
        "ready":            "Creador GitHub: VitzS7 | Instagram: @vitin_xzx",
        "language":         "Idioma",
        "repeat_types":     ["Una vez","Cada hora","Diariamente","Cada X minutos","Semanalmente","Mensualmente","Fecha específica"],
        "interval_min":     "min",
        "day_of_week":      "Día",
        "week_days":        ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"],
        "day_of_month":     "Día (1–31)",
        "date_ph":          "AAAA-MM-DD",
        "tray_open":        "Abrir",
        "tray_quit":        "Salir",
        "clear_confirm":    "¿Eliminar TODOS los recordatorios?",
        "clear_title":      "Borrar todo",
        "notification_default": "¡Es hora de tu recordatorio!",
        "edited_msg":       "Editando — pulsa Agregar para guardar.",
        "removed_msg":      "Recordatorio eliminado.",
        "cleared_msg":      "Todos los recordatorios eliminados.",
        "no_clear_msg":     "No hay recordatorios para eliminar.",
        "added_msg":        "'{}' agregado!",
        "sent_msg":         "🔔 {}",
        "notif_fail":       "Error al enviar notificación.",
        "err_desc":         "La descripción es obligatoria.",
        "err_time":         "Define una hora para este recordatorio.",
        "err_time_fmt":     "Hora inválida — usa HH:MM.",
        "err_interval":     "El intervalo debe ser un entero positivo.",
        "err_day_month":    "El día debe estar entre 1 y 31.",
        "err_date":         "Ingresa la fecha (AAAA-MM-DD).",
        "err_date_time":    "Ingresa la hora (HH:MM).",
        "err_date_fmt":     "Formato de fecha u hora inválido.",
        "err_select_edit":  "Selecciona un recordatorio para editar.",
        "err_select_del":   "Selecciona un recordatorio para eliminar.",
        "time_dialog_title":"Establecer hora",
        "confirm":          "Confirmar",
        "emoji_title":      "Elige un emoji",
        "every_hour":       "Cada hora",
        "every_x_min":      "Cada {} min",
        "weekly_fmt":       "{} a las {}",
        "monthly_fmt":      "Día {} a las {}",
        "specific_fmt":     "{} {}",
        "time_lbl":         "🕐 Establecer hora",
        "week_map": {"Lunes":0,"Martes":1,"Miércoles":2,"Jueves":3,"Viernes":4,"Sábado":5,"Domingo":6},
    },
    "ru": {
        "title":            "Reminder Me",
        "desc_ph":          "Что запомнить…",
        "msg_ph":           "Доп. сообщение (необязательно)",
        "add":              "Добавить напоминание",
        "edit":             "✏ Изменить",
        "remove":           "🗑 Удалить выбр.",
        "clear_all":        "✕ Очистить всё",
        "your_reminders":   "Напоминания",
        "no_reminders":     "Нет напоминаний.",
        "ready":            "Создатель GitHub: VitzS7 | Instagram: @vitin_xzx",
        "language":         "Язык",
        "repeat_types":     ["Один раз","Каждый час","Ежедневно","Каждые X минут","Еженедельно","Ежемесячно","Конкретная дата"],
        "interval_min":     "мин",
        "day_of_week":      "День",
        "week_days":        ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"],
        "day_of_month":     "День (1–31)",
        "date_ph":          "ГГГГ-ММ-ДД",
        "tray_open":        "Открыть",
        "tray_quit":        "Выход",
        "clear_confirm":    "Удалить ВСЕ напоминания?",
        "clear_title":      "Очистить всё",
        "notification_default": "Время вашего напоминания!",
        "edited_msg":       "Редактирование — нажмите Добавить.",
        "removed_msg":      "Напоминание удалено.",
        "cleared_msg":      "Все напоминания удалены.",
        "no_clear_msg":     "Нет напоминаний для удаления.",
        "added_msg":        "'{}' добавлено!",
        "sent_msg":         "🔔 {}",
        "notif_fail":       "Ошибка отправки уведомления.",
        "err_desc":         "Описание обязательно.",
        "err_time":         "Установите время для напоминания.",
        "err_time_fmt":     "Неверное время — используйте ЧЧ:ММ.",
        "err_interval":     "Интервал должен быть положительным целым.",
        "err_day_month":    "День должен быть от 1 до 31.",
        "err_date":         "Введите дату (ГГГГ-ММ-ДД).",
        "err_date_time":    "Введите время (ЧЧ:ММ).",
        "err_date_fmt":     "Неверный формат даты или времени.",
        "err_select_edit":  "Выберите напоминание для редактирования.",
        "err_select_del":   "Выберите напоминание для удаления.",
        "time_dialog_title":"Установить время",
        "confirm":          "Подтвердить",
        "emoji_title":      "Выберите эмодзи",
        "every_hour":       "Каждый час",
        "every_x_min":      "Каждые {} мин",
        "weekly_fmt":       "{} в {}",
        "monthly_fmt":      "{} числа в {}",
        "specific_fmt":     "{} {}",
        "time_lbl":         "🕐 Время",
        "week_map": {"Понедельник":0,"Вторник":1,"Среда":2,"Четверг":3,"Пятница":4,"Суббота":5,"Воскресенье":6},
    },
    "zh": {
        "title":            "提醒我",
        "desc_ph":          "提醒内容…",
        "msg_ph":           "附加消息（可选）",
        "add":              "添加提醒",
        "edit":             "✏ 编辑",
        "remove":           "🗑 删除选中",
        "clear_all":        "✕ 全部清除",
        "your_reminders":   "提醒列表",
        "no_reminders":     "暂无提醒。",
        "ready":            "作者 GitHub: VitzS7 | Instagram: @vitin_xzx",
        "language":         "语言",
        "repeat_types":     ["一次","每小时","每天","每X分钟","每周","每月","特定日期"],
        "interval_min":     "分钟",
        "day_of_week":      "星期",
        "week_days":        ["周一","周二","周三","周四","周五","周六","周日"],
        "day_of_month":     "日期（1–31）",
        "date_ph":          "YYYY-MM-DD",
        "tray_open":        "打开",
        "tray_quit":        "退出",
        "clear_confirm":    "删除所有提醒？",
        "clear_title":      "全部清除",
        "notification_default": "提醒时间到！",
        "edited_msg":       "编辑中 — 点击添加以保存。",
        "removed_msg":      "提醒已删除。",
        "cleared_msg":      "所有提醒已删除。",
        "no_clear_msg":     "没有提醒可删除。",
        "added_msg":        "'{}' 已添加！",
        "sent_msg":         "🔔 {}",
        "notif_fail":       "发送通知失败。",
        "err_desc":         "描述为必填项。",
        "err_time":         "请设置时间。",
        "err_time_fmt":     "时间格式无效，请使用 HH:MM。",
        "err_interval":     "间隔必须为正整数。",
        "err_day_month":    "日期必须在 1 到 31 之间。",
        "err_date":         "请输入日期（YYYY-MM-DD）。",
        "err_date_time":    "请输入时间（HH:MM）。",
        "err_date_fmt":     "日期或时间格式无效。",
        "err_select_edit":  "请选择要编辑的提醒。",
        "err_select_del":   "请选择要删除的提醒。",
        "time_dialog_title":"设置时间",
        "confirm":          "确认",
        "emoji_title":      "选择表情",
        "every_hour":       "每小时",
        "every_x_min":      "每 {} 分钟",
        "weekly_fmt":       "{} {}",
        "monthly_fmt":      "{} 日 {}",
        "specific_fmt":     "{} {}",
        "time_lbl":         "🕐 设置时间",
        "week_map": {"周一":0,"周二":1,"周三":2,"周四":3,"周五":4,"周六":5,"周日":6},
    },
}

TYPES_NO_TIME = {"Every hour", "Every X minutes"}
EN_TYPES      = TRANSLATIONS["en"]["repeat_types"]


def save_reminders(reminders):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)


def load_reminders():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.pop("theme", None)
            return data
    return {"language": "en"}


def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f)


def _setup_icons() -> tuple:
    import sys
    if getattr(sys, "frozen", False):
        base = os.path.join(os.path.dirname(sys.executable), "reminder-me")
    else:
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reminder-me")
    os.makedirs(base, exist_ok=True)
    ico = os.path.join(base, "icon.ico")
    png = os.path.join(base, "icon.png")

    def _make_bell(final_size=256):
        SS = 4
        s  = final_size * SS
        cx, cy, R = s//2, s//2, s//2 - 4
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d   = ImageDraw.Draw(img)

        # Radial gradient background
        for r in range(R, 0, -1):
            t  = r / R
            d.ellipse((cx-r, cy-r, cx+r, cy+r),
                      fill=(int(22+(55-22)*(1-t)),
                            int(32+(55-32)*(1-t)),
                            int(90+(130-90)*(1-t)), 255))

        bell_cx  = cx
        bell_top = int(cy - R * 0.22)
        bell_bot = int(cy + R * 0.32)
        w_top    = int(R * 0.30)
        w_bot    = int(R * 0.60)
        dome_r   = int(R * 0.44)
        dome_cy  = bell_top

        # Smooth scanline bell body
        for row in range(bell_top, bell_bot + 1):
            frac = (row - bell_top) / max(bell_bot - bell_top, 1)
            if frac < 0.55:
                w = w_top + (w_bot - w_top) * (frac / 0.55) ** 0.65
            else:
                w = w_bot - (w_bot - int(w_bot * 0.90)) * ((frac - 0.55) / 0.45)
            shade = int(25 * frac)
            d.line([(bell_cx - int(w), row), (bell_cx + int(w), row)],
                   fill=(245 - shade, 195 - shade, 28, 255))

        # Dome
        d.ellipse((bell_cx - dome_r, dome_cy - dome_r,
                   bell_cx + dome_r, dome_cy + dome_r),
                  fill=(245, 195, 28, 255))

        # Specular crescent highlight: bright ellipse carved by dome-coloured ellipse
        hi_r  = int(dome_r * 0.58)
        hi_ox = -int(dome_r * 0.24)
        hi_oy = -int(dome_r * 0.26)
        d.ellipse((bell_cx+hi_ox-hi_r, dome_cy+hi_oy-hi_r,
                   bell_cx+hi_ox+hi_r, dome_cy+hi_oy+hi_r),
                  fill=(255, 230, 130, 255))
        cr  = int(dome_r * 0.56)
        cox = int(dome_r * 0.14)
        coy = int(dome_r * 0.14)
        d.ellipse((bell_cx+cox-cr, dome_cy+coy-cr,
                   bell_cx+cox+cr, dome_cy+coy+cr),
                  fill=(245, 195, 28, 255))

        # Stem
        stem_w = int(R * 0.09)
        d.rounded_rectangle(
            (bell_cx - stem_w, dome_cy - dome_r - int(R * 0.18),
             bell_cx + stem_w, dome_cy - dome_r),
            radius=stem_w, fill=(245, 195, 28, 255))

        # Rim
        rim_h = int(R * 0.10)
        rim_w = w_bot + int(R * 0.06)
        d.rounded_rectangle(
            (bell_cx - rim_w, bell_bot - rim_h // 2,
             bell_cx + rim_w, bell_bot + rim_h // 2),
            radius=rim_h // 2, fill=(160, 115, 8, 255))

        # Clapper
        clap_r = int(R * 0.09)
        clap_y = bell_bot + rim_h // 2 + clap_r + 4
        d.ellipse((bell_cx - clap_r, clap_y - clap_r,
                   bell_cx + clap_r, clap_y + clap_r),
                  fill=(160, 115, 8, 255))

        # Badge depth shadow (opaque dark red, offset)
        bdg_cx = bell_cx + int(R * 0.38)
        bdg_cy = dome_cy - dome_r + int(R * 0.08)
        bdg_r  = int(R * 0.21)
        off    = max(3, int(bdg_r * 0.20))
        d.ellipse((bdg_cx - bdg_r + off, bdg_cy - bdg_r + off,
                   bdg_cx + bdg_r + off, bdg_cy + bdg_r + off),
                  fill=(130, 15, 15, 255))
        # Badge
        d.ellipse((bdg_cx - bdg_r, bdg_cy - bdg_r,
                   bdg_cx + bdg_r, bdg_cy + bdg_r),
                  fill=(215, 38, 38, 255))

        # Clip to circle
        mask = Image.new("L", (s, s), 0)
        ImageDraw.Draw(mask).ellipse((cx-R, cy-R, cx+R, cy+R), fill=255)
        img.putalpha(mask)
        return img.resize((final_size, final_size), Image.LANCZOS)

    try:
        if not os.path.exists(ico):
            base_img = _make_bell(256)
            szs      = [(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)]
            icons    = [base_img.resize(s, Image.LANCZOS) for s in szs]
            icons[0].save(ico, format="ICO",
                          sizes=[(s[0], s[1]) for s in szs],
                          append_images=icons[1:])
        if not os.path.exists(png):
            base_img = _make_bell(256)
            base_img.save(png, "PNG")
    except Exception:
        ico = png = ""

    return ico, png


def _register_app_id(png_path: str) -> None:
    try:
        import winreg
        key_path = r"SOFTWARE\Classes\AppUserModelId\ReminderMe.App"
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, key_path,
                                0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, "DisplayName", 0, winreg.REG_SZ, APP_NAME)
            if png_path and os.path.exists(png_path):
                winreg.SetValueEx(k, "IconUri", 0, winreg.REG_SZ, png_path)
    except Exception:
        pass


_ICON_ICO, _ICON_PNG = _setup_icons()
_register_app_id(_ICON_PNG)


def send_notification(title: str, message: str):
    if _WINOTIFY:
        toast = WinNotify(app_id="ReminderMe.App",
                          title=title, msg=message, duration="long")
        if _ICON_PNG and os.path.exists(_ICON_PNG):
            toast.icon = _ICON_PNG
        toast.set_audio(WinAudio.Default, loop=False)
        toast.show()
    else:
        _plyer_notify.notify(title=title, message=message,
                             app_name=APP_NAME, timeout=0)


class SpinField(ctk.CTkFrame):
    _SLOT_W = 66
    _SLOT_H = 50

    def __init__(self, parent, initial, min_val, max_val):
        super().__init__(parent, fg_color="transparent")
        self._val     = initial
        self._min     = min_val
        self._max     = max_val
        self._editing = False

        btn_kw = dict(width=self._SLOT_W, height=26,
                      fg_color="transparent", font=("Segoe UI", 13, "bold"))
        ctk.CTkButton(self, text="▲", **btn_kw, command=lambda: self._step(1)).pack()

        self._slot = ctk.CTkFrame(self, width=self._SLOT_W, height=self._SLOT_H,
                                  fg_color="transparent")
        self._slot.pack()
        self._slot.pack_propagate(False)

        self.lbl = ctk.CTkLabel(self._slot, text=f"{self._val:02d}",
                                font=("Segoe UI", 32, "bold"),
                                cursor="xterm", fg_color="transparent")
        self.lbl.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl.bind("<Button-1>", self._start_edit)

        ctk.CTkButton(self, text="▼", **btn_kw, command=lambda: self._step(-1)).pack()

    def _step(self, d):
        self._val = (self._val + d - self._min) % (self._max - self._min + 1) + self._min
        self.lbl.configure(text=f"{self._val:02d}")

    def _start_edit(self, _=None):
        if self._editing:
            return
        self._editing = True
        self.lbl.place_forget()
        self._entry = ctk.CTkEntry(self._slot, width=self._SLOT_W - 4,
                                   justify="center", font=("Segoe UI", 26, "bold"))
        self._entry.insert(0, f"{self._val:02d}")
        self._entry.select_range(0, "end")
        self._entry.place(relx=0.5, rely=0.5, anchor="center")
        self._entry.focus_set()
        self._entry.bind("<Return>",   self._end_edit)
        self._entry.bind("<FocusOut>", self._end_edit)
        self._entry.bind("<Escape>",   lambda _: self._cancel_edit())

    def _end_edit(self, _=None):
        if not self._editing:
            return
        try:
            v = int(self._entry.get().strip())
            self._val = max(self._min, min(self._max, v))
        except ValueError:
            pass
        self._entry.destroy()
        self.lbl.configure(text=f"{self._val:02d}")
        self.lbl.place(relx=0.5, rely=0.5, anchor="center")
        self._editing = False

    def _cancel_edit(self):
        if not self._editing:
            return
        self._entry.destroy()
        self.lbl.place(relx=0.5, rely=0.5, anchor="center")
        self._editing = False

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, v):
        self._val = max(self._min, min(self._max, int(v)))
        self.lbl.configure(text=f"{self._val:02d}")


class TimePicker(ctk.CTkToplevel):
    def __init__(self, parent, callback, current="12:00", tr=None):
        super().__init__(parent)
        self.callback = callback
        self.tr       = tr or TRANSLATIONS["en"]
        self.title(self.tr["time_dialog_title"])
        self.geometry("230x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        try:
            h, m = current.split(":")
            ih, im = int(h) % 24, int(m) % 60
        except Exception:
            ih, im = 12, 0

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(expand=True)

        self.spin_h = SpinField(row, ih, 0, 23)
        self.spin_h.grid(row=0, column=0, padx=10, pady=16)
        ctk.CTkLabel(row, text=":", font=("Segoe UI", 32, "bold")).grid(
            row=0, column=1, padx=2, pady=(0, 8))
        self.spin_m = SpinField(row, im, 0, 59)
        self.spin_m.grid(row=0, column=2, padx=10, pady=16)

        ctk.CTkButton(self, text=self.tr["confirm"], height=32,
                      command=self._confirm).pack(fill="x", padx=20, pady=(0, 16))

    def _confirm(self):
        self.callback(f"{self.spin_h.value:02d}:{self.spin_m.value:02d}")
        self.destroy()


class EmojiPicker(ctk.CTkToplevel):
    _CATS = {
        "😀": ["😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😜","🤪","😝","🤑","🤗","🤭","🤫","🤔","🤐","🤨","😐","😑","😶","😏","😒","🙄","😬","🤥","😔","😪","🤤","😴","😷","🤒","🤕","🤢","🤮","🤧","🥵","🥶","🥴","😵","🤯","🤠","🥳","😎","🤓","🧐","😕","😟","🙁","☹️","😮","😯","😲","😳","🥺","😦","😧","😨","😩","😰","😱","😖","😣","😞","😓","😢","😭","😤","😡","😠","🤬","😈","👿","💀","☠️","💩","🤡","👹","👺","👻","👽","👾","🤖"],
        "❤️": ["❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💔","💕","💞","💓","💗","💖","💘","💝","💟","❣️","💌"],
        "✋": ["✋","🤚","🖐️","👌","🤏","✌️","🤞","🤟","🤘","🤙","👈","👉","👆","🖕","👇","☝️","👍","👎","✊","👊","🤛","🤜","👏","🙌","👐","🤲","🙏","✍️","💅","🤳","💪","🦾","🦿","🦵","🦶","👂","👃"],
        "🎉": ["🎉","🎊","🎈","🎂","🎁","🎆","🎇","✨","🌟","⭐","🌠","🎃","🎄","🎋","🎍","🎎","🎏","🎐","🎑","🧧","🎀","🎫","🎟️","🎗️","🏆","🥇","🥈","🥉","🏅","🎖️","🏵️","🎯","🎲","🎮","🎰","🎱","🎳","🎴","🎵","🎶","🎷","🎸","🎹","🎺","🎻","🥁","🎼","🎤","🎧","🎩","🎬","🎭","🎪"],
        "🍕": ["🍕","🍔","🍟","🍩","🍦","🍉","🍓","🍇","🍈","🍒","🍑","🍍","🥭","🍌","🍎","🍏","🍐","🍊","🍋","🍖","🍗","🥩","🥓","🌭","🍿","🥚","🍳","🥞","🧇","🥯","🥨","🥐","🍞","🥖","🥪","🥗","🥘","🍲","🍛","🍜","🍝","🍠","🍢","🍣","🍤","🍥","🍧","🍨","🍪","🎂","🍰","🧁","🥧","🍫","🍬","🍭","🍮","🍯","🍼","🥛","☕","🍵","🧃","🥤","🍶","🍺","🍻","🥂","🍷","🥃","🍸","🍹","🍾","🥄","🍴","🍽️"],
        "🚗": ["🚗","🚕","🚙","🚌","🚎","🏎️","🚓","🚑","🚒","🚐","🚚","🚛","🚜","🛵","🏍️","🛺","🚲","🛴","🛹","🚏","🛣️","🛤️","🛢️","⛽","🚨","🚥","🚦","🛑","🚧","⚓","⛵","🛶","🚤","🛳️","⛴️","🛥️","🚢","✈️","🛩️","🛫","🛬","🪂","🚁","🚟","🚠","🚡","🛰️","🚀","🛸","🪐","🌠"],
    }

    def __init__(self, parent, callback, title="Choose an emoji"):
        super().__init__(parent)
        self.callback  = callback
        self.cat       = list(self._CATS.keys())[0]
        self._cat_btns = {}
        self.title(title)
        self.geometry("560x360")
        self.minsize(480, 320)
        self.transient(parent)
        self.grab_set()

        bar = ctk.CTkFrame(self, fg_color=("gray90", "#181818"),
                           corner_radius=0, height=48)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        for c in self._CATS:
            b = ctk.CTkButton(
                bar, text=c, width=54, height=38,
                font=("Segoe UI Emoji", 18), fg_color="transparent",
                hover_color=ACCENT, corner_radius=6,
                command=lambda x=c: self._switch(x))
            b.pack(side="left", padx=3, pady=5)
            self._cat_btns[c] = b

        self._set_active_btn(self.cat)
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=6, pady=6)
        self._render()

    def _set_active_btn(self, active_cat):
        for cat, btn in self._cat_btns.items():
            btn.configure(fg_color=ACCENT if cat == active_cat else "transparent")

    def _switch(self, cat):
        self.cat = cat
        self._set_active_btn(cat)
        self._render()

    def _render(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        for i, e in enumerate(self._CATS[self.cat]):
            ctk.CTkButton(
                self.scroll, text=e, width=46, height=46,
                font=("Segoe UI Emoji", 21),
                fg_color=("gray85", "#2b2b2b"),
                hover_color=ACCENT, corner_radius=8,
                command=lambda x=e: self._pick(x)
            ).grid(row=i // 10, column=i % 10, padx=2, pady=2)

    def _pick(self, emoji):
        self.callback(emoji)
        self.destroy()


class ReminderMe(ctk.CTk):
    def __init__(self):
        super().__init__()
        settings           = load_settings()
        self.lang          = settings.get("language", "en")
        self.tr            = TRANSLATIONS[self.lang]
        self.reminders     = load_reminders()
        self.threads: dict = {}
        self.current_emoji = "⏰"
        self.selected_id   = None
        self._time_var     = ctk.StringVar()
        self._settings     = settings

        ctk.set_appearance_mode("system")

        self.title(self._t("title"))
        self.geometry("780x480")
        self.minsize(620, 400)
        if _ICON_ICO:
            try:
                self.iconbitmap(_ICON_ICO)
            except Exception:
                pass

        self._build_ui()
        self._refresh_list()
        self.protocol("WM_DELETE_WINDOW", self._minimize_tray)

        for r in self.reminders:
            if r.get("active", True):
                self._start_thread(r["id"])

    def _t(self, key):
        return self.tr.get(key, TRANSLATIONS["en"].get(key, key))

    def _build_ui(self):
        SF = ("Segoe UI", 11)
        BF = ("Segoe UI", 12)

        self.columnconfigure(0, weight=0, minsize=290)
        self.columnconfigure(1, weight=0, minsize=1)
        self.columnconfigure(2, weight=1, minsize=260)
        self.rowconfigure(0, weight=1)

        left = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray95", "#1c1c1c"))
        left.grid(row=0, column=0, sticky="nsew")
        left.columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text=self._t("title"),
                     font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, sticky="w", padx=14, pady=(14, 6))

        lang_names   = list(LANGUAGES.keys())
        current_name = next(k for k, v in LANGUAGES.items() if v == self.lang)
        self.lang_menu = ctk.CTkOptionMenu(
            left, values=lang_names, height=28, font=SF,
            command=self._change_language)
        self.lang_menu.set(current_name)
        self.lang_menu.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 10))

        ctk.CTkFrame(left, height=1, fg_color=("gray80", "gray30")).grid(
            row=2, column=0, sticky="ew", padx=14, pady=(0, 10))

        self.e_desc = ctk.CTkEntry(left, placeholder_text=self._t("desc_ph"),
                                   height=34, font=BF)
        self.e_desc.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 6))

        te_row = ctk.CTkFrame(left, fg_color="transparent")
        te_row.grid(row=4, column=0, sticky="ew", padx=14, pady=(0, 6))
        te_row.columnconfigure(0, weight=1)

        self.btn_time = ctk.CTkButton(
            te_row, text=self._t("time_lbl"), height=32, font=SF,
            command=self._open_time)
        self.btn_time.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.btn_emoji = ctk.CTkButton(
            te_row, text=self.current_emoji,
            width=38, height=32, font=("Segoe UI Emoji", 15),
            fg_color=("gray80", "gray30"), text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray25"), command=self._open_emoji)
        self.btn_emoji.grid(row=0, column=1)

        self.combo_type = ctk.CTkOptionMenu(
            left, values=self._t("repeat_types"),
            command=self._on_type, height=32, font=SF)
        self.combo_type.set(self._t("repeat_types")[0])
        self.combo_type.grid(row=5, column=0, sticky="ew", padx=14, pady=(0, 6))

        self.frame_extra = ctk.CTkFrame(left, fg_color="transparent")

        self.e_msg = ctk.CTkEntry(left, placeholder_text=self._t("msg_ph"),
                                  height=32, font=SF)
        self.e_msg.grid(row=7, column=0, sticky="ew", padx=14, pady=(0, 10))

        ctk.CTkFrame(left, height=1, fg_color=("gray80", "gray30")).grid(
            row=8, column=0, sticky="ew", padx=14, pady=(0, 10))

        self.btn_add = ctk.CTkButton(
            left, text=self._t("add"), height=36, font=("Segoe UI", 12, "bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER, command=self._add)
        self.btn_add.grid(row=9, column=0, sticky="ew", padx=14, pady=(0, 6))

        sec = ctk.CTkFrame(left, fg_color="transparent")
        sec.grid(row=10, column=0, sticky="ew", padx=14, pady=(0, 10))
        sec.columnconfigure((0, 1, 2), weight=1)

        for col, (key, cmd, fc, hc) in enumerate([
            ("edit",      self._edit,      ("#E65100","#E65100"), ("#BF360C","#BF360C")),
            ("remove",    self._remove,    ("#C62828","#C62828"), ("#8B0000","#8B0000")),
            ("clear_all", self._clear_all, ("gray70",  "gray35"), ("gray60",  "gray25")),
        ]):
            ctk.CTkButton(sec, text=self._t(key), height=30, font=SF,
                          fg_color=fc, hover_color=hc, command=cmd).grid(
                row=0, column=col,
                padx=(0, 3) if col < 2 else (0, 0), sticky="ew")

        left.rowconfigure(11, weight=1)
        self.status_bar = ctk.CTkLabel(
            left, text=self._t("ready"), font=("Segoe UI", 10),
            text_color=COL_NEUTRAL, anchor="w")
        self.status_bar.grid(row=12, column=0, sticky="ew", padx=14, pady=(0, 10))

        ctk.CTkFrame(self, width=1, fg_color=("gray80", "gray28")).grid(
            row=0, column=1, sticky="ns")

        right = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        right.grid(row=0, column=2, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        list_hdr = ctk.CTkFrame(right, fg_color="transparent")
        list_hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 6))
        list_hdr.columnconfigure(0, weight=1)
        ctk.CTkLabel(list_hdr, text=self._t("your_reminders"),
                     font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w")
        self.lbl_count = ctk.CTkLabel(list_hdr, text="0", font=SF,
                                      text_color=COL_NEUTRAL)
        self.lbl_count.grid(row=0, column=1)

        self.list_frame = ctk.CTkScrollableFrame(right, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self._on_type()

    def _on_type(self, *_):
        loc_types = self._t("repeat_types")
        label     = self.combo_type.get()
        idx       = loc_types.index(label) if label in loc_types else 0
        internal  = EN_TYPES[idx]

        for w in self.frame_extra.winfo_children():
            w.destroy()

        uses_time = internal not in TYPES_NO_TIME and internal != "Specific date"
        self.btn_time.configure(
            state="normal" if uses_time else "disabled",
            fg_color=(ACCENT if uses_time else ("gray75", "gray35")))

        has_extra = internal in ("Every X minutes", "Weekly", "Monthly", "Specific date")
        if has_extra:
            self.frame_extra.grid(row=6, column=0, sticky="ew", padx=14, pady=(0, 6))
        else:
            self.frame_extra.grid_remove()

        SF2 = ("Segoe UI", 11)
        if internal == "Every X minutes":
            self.e_interval = ctk.CTkEntry(
                self.frame_extra, width=90, height=30,
                placeholder_text=f"30 {self._t('interval_min')}", font=SF2)
            self.e_interval.pack(fill="x")
        elif internal == "Weekly":
            self.combo_weekday = ctk.CTkOptionMenu(
                self.frame_extra, values=self._t("week_days"), height=30, font=SF2)
            self.combo_weekday.set(self._t("week_days")[0])
            self.combo_weekday.pack(fill="x")
        elif internal == "Monthly":
            self.e_day = ctk.CTkEntry(
                self.frame_extra, height=30,
                placeholder_text=self._t("day_of_month"), font=SF2)
            self.e_day.pack(fill="x")
        elif internal == "Specific date":
            r1 = ctk.CTkFrame(self.frame_extra, fg_color="transparent")
            r1.pack(fill="x")
            r1.columnconfigure((0, 1), weight=1)
            self.e_date = ctk.CTkEntry(r1, height=30,
                                       placeholder_text=self._t("date_ph"), font=SF2)
            self.e_date.grid(row=0, column=0, sticky="ew", padx=(0, 4))
            self.e_spec_time = ctk.CTkEntry(r1, height=30,
                                            placeholder_text="HH:MM", font=SF2)
            self.e_spec_time.grid(row=0, column=1, sticky="ew")

    def _open_time(self):
        TimePicker(self, self._set_time, self._time_var.get() or "12:00", self.tr)

    def _set_time(self, val):
        self._time_var.set(val)
        self.btn_time.configure(text=f"🕐  {val}")

    def _open_emoji(self):
        if hasattr(self, "_emoji_win") and self._emoji_win.winfo_exists():
            self._emoji_win.lift()
            return
        self._emoji_win = EmojiPicker(self, self._set_emoji, self._t("emoji_title"))

    def _set_emoji(self, emoji):
        self.current_emoji = emoji
        self.btn_emoji.configure(text=emoji)

    def _change_language(self, lang_name):
        self.lang                  = LANGUAGES[lang_name]
        self.tr                    = TRANSLATIONS[self.lang]
        self._settings["language"] = self.lang
        save_settings(self._settings)
        self._rebuild_ui()

    def _rebuild_ui(self):
        for w in self.winfo_children():
            w.destroy()
        self.title(self._t("title"))
        self._time_var     = ctk.StringVar()
        self.current_emoji = "⏰"
        self.selected_id   = None
        self._build_ui()
        self._refresh_list()

    def _internal_type(self):
        loc_types = self._t("repeat_types")
        label     = self.combo_type.get()
        idx       = loc_types.index(label) if label in loc_types else 0
        return EN_TYPES[idx]

    def _collect(self):
        desc     = self.e_desc.get().strip()
        internal = self._internal_type()
        errors   = []
        extras   = {}

        if not desc:
            errors.append(self._t("err_desc"))

        def need_time():
            t = self._time_var.get().strip()
            if not t:
                errors.append(self._t("err_time"))
                return
            try:
                datetime.strptime(t, "%H:%M")
                extras["time"] = t
            except ValueError:
                errors.append(self._t("err_time_fmt"))

        if internal == "Every X minutes":
            try:
                iv = int(self.e_interval.get().strip())
                if iv <= 0:
                    raise ValueError
                extras["interval_minutes"] = iv
            except ValueError:
                errors.append(self._t("err_interval"))
        elif internal == "Weekly":
            day_label               = self.combo_weekday.get()
            extras["weekday"]       = self._t("week_map").get(day_label, 0)
            extras["weekday_label"] = day_label
            need_time()
        elif internal == "Monthly":
            try:
                d = int(self.e_day.get().strip())
                if not 1 <= d <= 31:
                    raise ValueError
                extras["day_of_month"] = d
            except ValueError:
                errors.append(self._t("err_day_month"))
            need_time()
        elif internal == "Specific date":
            ds = self.e_date.get().strip()
            ts = self.e_spec_time.get().strip()
            if not ds:
                errors.append(self._t("err_date"))
            if not ts:
                errors.append(self._t("err_date_time"))
            if ds and ts:
                try:
                    datetime.strptime(ds, "%Y-%m-%d")
                    datetime.strptime(ts, "%H:%M")
                    extras["date"] = ds
                    extras["time"] = ts
                except ValueError:
                    errors.append(self._t("err_date_fmt"))
        elif internal not in TYPES_NO_TIME:
            need_time()

        if errors:
            self._status("  ".join(errors), COL_ERR)
            return None

        return {"description": desc, "type": internal, "emoji": self.current_emoji,
                "message": self.e_msg.get().strip(), "active": True, **extras}

    def _add(self):
        data = self._collect()
        if not data:
            return
        nid        = max((r["id"] for r in self.reminders), default=0) + 1
        data["id"] = nid
        self.reminders.append(data)
        save_reminders(self.reminders)
        self._start_thread(nid)
        self._refresh_list()
        self._clear_fields()
        self._status(self._t("added_msg").format(data["description"]), COL_OK)

    def _edit(self):
        if not self.selected_id:
            self._status(self._t("err_select_edit"), COL_ERR)
            return
        r = next((x for x in self.reminders if x["id"] == self.selected_id), None)
        if not r:
            return

        self.e_desc.delete(0, "end")
        self.e_desc.insert(0, r["description"])
        self.e_msg.delete(0, "end")
        self.e_msg.insert(0, r.get("message", ""))
        self.current_emoji = r["emoji"]
        self.btn_emoji.configure(text=r["emoji"])

        idx = EN_TYPES.index(r["type"]) if r["type"] in EN_TYPES else 0
        self.combo_type.set(self._t("repeat_types")[idx])
        self._on_type()

        if "time" in r:
            self._time_var.set(r["time"])
            self.btn_time.configure(text=f"🕐  {r['time']}")

        if r["type"] == "Every X minutes" and hasattr(self, "e_interval"):
            self.e_interval.insert(0, str(r.get("interval_minutes", "")))
        elif r["type"] == "Weekly" and hasattr(self, "combo_weekday"):
            wdays = self._t("week_days")
            wd    = r.get("weekday", 0)
            self.combo_weekday.set(wdays[wd] if wd < len(wdays) else wdays[0])
        elif r["type"] == "Monthly" and hasattr(self, "e_day"):
            self.e_day.insert(0, str(r.get("day_of_month", "")))
        elif r["type"] == "Specific date":
            if hasattr(self, "e_date"):
                self.e_date.insert(0, r.get("date", ""))
            if hasattr(self, "e_spec_time"):
                self.e_spec_time.insert(0, r.get("time", ""))

        self._stop_thread(self.selected_id)
        self.reminders   = [x for x in self.reminders if x["id"] != self.selected_id]
        save_reminders(self.reminders)
        self.selected_id = None
        self._refresh_list()
        self._status(self._t("edited_msg"), COL_WARN)

    def _remove(self):
        if not self.selected_id:
            self._status(self._t("err_select_del"), COL_ERR)
            return
        self._stop_thread(self.selected_id)
        self.reminders   = [r for r in self.reminders if r["id"] != self.selected_id]
        save_reminders(self.reminders)
        self.selected_id = None
        self._refresh_list()
        self._status(self._t("removed_msg"))

    def _clear_all(self):
        if not self.reminders:
            self._status(self._t("no_clear_msg"), COL_WARN)
            return
        if messagebox.askyesno(self._t("clear_title"), self._t("clear_confirm")):
            for r in self.reminders:
                self._stop_thread(r["id"])
            self.reminders   = []
            save_reminders(self.reminders)
            self.selected_id = None
            self._refresh_list()
            self._status(self._t("cleared_msg"))

    def _item_bg(self, selected):
        return ("#BBDEFB", "#1a4a8a") if selected else ("#e8e8e8", "#2a2a2a")

    def _refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        active = [r for r in self.reminders if r.get("active", True)]
        if hasattr(self, "lbl_count"):
            self.lbl_count.configure(text=str(len(active)))

        if not active:
            ctk.CTkLabel(self.list_frame, text=self._t("no_reminders"),
                         font=("Segoe UI", 11), text_color=COL_NEUTRAL).pack(pady=30)
            return

        for r in active:
            itype = r["type"]
            idx   = EN_TYPES.index(itype) if itype in EN_TYPES else 0
            tlbl  = self._t("repeat_types")[idx]

            if itype == "Specific date":
                sub = self._t("specific_fmt").format(r["date"], r.get("time", ""))
            elif itype == "Every X minutes":
                sub = self._t("every_x_min").format(r["interval_minutes"])
            elif itype == "Weekly":
                sub = self._t("weekly_fmt").format(
                    self._t("week_days")[r.get("weekday", 0)], r.get("time", ""))
            elif itype == "Monthly":
                sub = self._t("monthly_fmt").format(r["day_of_month"], r.get("time", ""))
            elif itype == "Every hour":
                sub = self._t("every_hour")
            else:
                sub = r.get("time", "")

            is_sel = r["id"] == self.selected_id
            card   = ctk.CTkFrame(self.list_frame,
                                  fg_color=self._item_bg(is_sel), corner_radius=8)
            card.pack(fill="x", pady=2, padx=4)
            card.columnconfigure(1, weight=1)
            card.reminder_id = r["id"]

            ctk.CTkLabel(card, text=r["emoji"],
                         font=("Segoe UI Emoji", 18), width=36).grid(
                row=0, column=0, rowspan=2, padx=(10, 4), pady=6)
            ctk.CTkLabel(card, text=r["description"],
                         font=("Segoe UI", 12, "bold"), anchor="w").grid(
                row=0, column=1, sticky="ew", padx=(0, 8), pady=(6, 0))
            ctk.CTkLabel(card, text=f"{tlbl}  ·  {sub}",
                         font=("Segoe UI", 10), text_color=COL_NEUTRAL, anchor="w").grid(
                row=1, column=1, sticky="ew", padx=(0, 8), pady=(0, 6))

            for w in card.winfo_children():
                w.bind("<Button-1>", lambda e, fid=r["id"]: self._select(fid))
            card.bind("<Button-1>", lambda e, fid=r["id"]: self._select(fid))

    def _select(self, fid):
        self.selected_id = fid
        for c in self.list_frame.winfo_children():
            if hasattr(c, "reminder_id"):
                c.configure(fg_color=self._item_bg(c.reminder_id == fid))

    def _stop_thread(self, rid):
        if rid in self.threads:
            _, ev = self.threads.pop(rid)
            ev.set()

    def _start_thread(self, rid):
        self._stop_thread(rid)
        ev = threading.Event()
        t  = threading.Thread(target=self._monitor, args=(rid, ev), daemon=True)
        self.threads[rid] = (t, ev)
        t.start()

    def _monitor(self, rid, stop: threading.Event):
        r = next((x for x in self.reminders if x["id"] == rid), None)
        if not r:
            return

        itype = r["type"]
        now   = datetime.now()

        def time_obj():
            return datetime.strptime(r["time"], "%H:%M").time()

        def next_occurrence(t):
            dt = datetime.combine(now.date(), t)
            return dt if dt > now else dt + timedelta(days=1)

        if itype == "Once":
            nxt = next_occurrence(time_obj())
        elif itype == "Every hour":
            nxt = now + timedelta(hours=1)
        elif itype == "Daily":
            nxt = next_occurrence(time_obj())
        elif itype == "Every X minutes":
            nxt = now + timedelta(minutes=r["interval_minutes"])
        elif itype == "Weekly":
            t         = time_obj()
            today     = now.date()
            delta     = (r["weekday"] - today.weekday()) % 7
            candidate = datetime.combine(today + timedelta(days=delta), t)
            if candidate <= now:
                delta     = delta + 7 if delta else 7
                candidate = datetime.combine(today + timedelta(days=delta), t)
            nxt = candidate
        elif itype == "Monthly":
            t = time_obj()
            try:
                candidate = datetime(now.year, now.month, r["day_of_month"], t.hour, t.minute)
            except ValueError:
                candidate = None
            if candidate is None or candidate <= now:
                y, m = (now.year + 1, 1) if now.month == 12 else (now.year, now.month + 1)
                try:
                    candidate = datetime(y, m, r["day_of_month"], t.hour, t.minute)
                except ValueError:
                    candidate = datetime(y, m, 1, t.hour, t.minute)
            nxt = candidate
        elif itype == "Specific date":
            d   = datetime.strptime(r["date"], "%Y-%m-%d").date()
            t   = datetime.strptime(r["time"], "%H:%M").time()
            nxt = datetime.combine(d, t)
            if nxt <= now:
                self.reminders = [x for x in self.reminders if x["id"] != rid]
                save_reminders(self.reminders)
                self.after(0, self._refresh_list)
                return
        else:
            return

        while not stop.is_set() and r.get("active", True):
            wait_secs = (nxt - datetime.now()).total_seconds()
            if wait_secs > 0:
                if stop.wait(timeout=wait_secs):
                    break
            if not r.get("active", True):
                break
            if (nxt - datetime.now()).total_seconds() > 2:
                continue
            try:
                self._fire(r)
            except Exception as e:
                print(f"Error firing reminder: {e}")

            if itype in ("Once", "Specific date"):
                self.reminders = [x for x in self.reminders if x["id"] != rid]
                save_reminders(self.reminders)
                self.after(0, self._refresh_list)
                break
            elif itype == "Every hour":
                nxt = datetime.now() + timedelta(hours=1)
            elif itype == "Daily":
                nxt += timedelta(days=1)
            elif itype == "Every X minutes":
                nxt = datetime.now() + timedelta(minutes=r["interval_minutes"])
            elif itype == "Weekly":
                nxt += timedelta(weeks=1)
            elif itype == "Monthly":
                y, m = (nxt.year + 1, 1) if nxt.month == 12 else (nxt.year, nxt.month + 1)
                try:
                    nxt = datetime(y, m, r["day_of_month"], nxt.hour, nxt.minute)
                except ValueError:
                    nxt = datetime(y, m, 1, nxt.hour, nxt.minute)

    def _fire(self, r):
        try:
            title = f"{r['emoji']} {r['description']}"
            body  = r["message"] if r["message"] else self._t("notification_default")
            send_notification(title, body)
            self.after(0, lambda: self._status(
                self._t("sent_msg").format(r["description"]), COL_OK))
        except Exception as e:
            print(f"Notification error: {e}")
            self.after(0, lambda: self._status(self._t("notif_fail"), COL_ERR))

    def _clear_fields(self):
        self.e_desc.delete(0, "end")
        self.e_msg.delete(0, "end")
        self._time_var.set("")
        self.btn_time.configure(text=self._t("time_lbl"))
        self.current_emoji = "⏰"
        self.btn_emoji.configure(text="⏰")
        self.combo_type.set(self._t("repeat_types")[0])
        self._on_type()

    def _status(self, msg, color=COL_NEUTRAL):
        self.status_bar.configure(text=msg, text_color=color)
        self.after(4500, lambda: self.status_bar.configure(
            text=self._t("ready"), text_color=COL_NEUTRAL))

    def _minimize_tray(self):
        self.withdraw()
        try:
            if _ICON_PNG and os.path.exists(_ICON_PNG):
                tray_img = Image.open(_ICON_PNG).convert("RGBA").resize((64, 64), Image.LANCZOS)
            else:
                tray_img = Image.new("RGB", (64, 64), (20, 20, 20))
                ImageDraw.Draw(tray_img).ellipse((8, 8, 56, 56), fill=(70, 130, 220))
            menu = pystray.Menu(
                pystray.MenuItem(self._t("tray_open"), self._restore),
                pystray.MenuItem(self._t("tray_quit"), self._quit_app),
            )
            self._tray = pystray.Icon(APP_NAME, tray_img, APP_NAME, menu)
            threading.Thread(target=self._tray.run, daemon=True).start()
        except Exception as e:
            print(f"Tray error: {e}")

    def _restore(self, *_):
        self.after(0, self.deiconify)
        if hasattr(self, "_tray"):
            self._tray.stop()

    def _quit_app(self, *_):
        if hasattr(self, "_tray"):
            self._tray.stop()
        self.quit()


if __name__ == "__main__":
    app = ReminderMe()
    app.mainloop()
