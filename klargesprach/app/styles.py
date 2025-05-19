import customtkinter as ctk

COLORS = {
    "light": {
        "primary_bg": "#F8FAFC",
        "secondary_bg": "#E3E8F0",
        "text": "#191D23",
        "accent": "#6366F1",
        "button_bg": "#6366F1",
        "button_hover": "#4F46E5",
        "user_message": "#DBEAFE",
        "ai_message": "#F5D0FE",
        "sidebar_bg": "#F1F5F9",
        "sidebar_button": "#6366F1",
        "sidebar_hover": "#818CF8",
        "danger": "#DC2626",
        "danger_hover": "#B91C1C"
    },
    "dark": {
        "primary_bg": "#181825",
        "secondary_bg": "#22223B",
        "text": "#FAF9FB",
        "accent": "#818CF8",
        "button_bg": "#6366F1",
        "button_hover": "#4F46E5",
        "user_message": "#312E81",
        "ai_message": "#713F93",
        "sidebar_bg": "#23253B",
        "sidebar_button": "#4F46E5",
        "sidebar_hover": "#6366F1",
        "danger": "#DC2626",
        "danger_hover": "#B91C1C"
    }
}

FONTS = {
    "main": ("Inter", 13),
    "title": ("Inter", 20, "bold"),
    "header": ("Inter", 16, "bold"),
    "button": ("Inter", 14, "bold"),
    "entry": ("Inter", 13),
    "message": ("Inter", 14),
    "sidebar": ("Inter", 12, "bold")
}

PADDINGS = {
    "xsmall": 4,
    "small": 8,
    "normal": 16,
    "large": 28,
}
RADIUS = 14

current_theme = "dark"

def set_theme(theme):
    global current_theme
    theme = theme.lower()
    if theme == "system":
        ctk.set_appearance_mode("System")
        current_theme = "dark"  # fallback default
    elif theme == "light":
        ctk.set_appearance_mode("Light")
        current_theme = "light"
    else:
        ctk.set_appearance_mode("Dark")
        current_theme = "dark"

def get_colors():
    return COLORS.get(current_theme, COLORS["dark"])

def init_theme_from_settings(settings):
    theme = settings.get("theme", "system").lower()
    set_theme(theme)
    return theme

def apply_theme_to_widgets(root):
    pass
