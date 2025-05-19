import customtkinter as ctk
from threading import Thread
from datetime import datetime
from settings import load_settings, update_setting
import styles
from sessions import display_sessions, delete_sessions, save_session
from llm_engine import query_llm  # llm_engine.py: query_llm(user_message) function

ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("KlarGespräch - AI Psychologist")
app.geometry("1200x800")
app.minsize(900, 600)

settings = load_settings()
current_theme = styles.init_theme_from_settings(settings)
colors = styles.get_colors()
app.configure(fg_color=colors["primary_bg"])

tabview = ctk.CTkTabview(app, fg_color=colors["secondary_bg"])
tabview.pack(fill="both", expand=True, padx=10, pady=10)
chat_tab = tabview.add("Chat")
settings_tab = tabview.add("Settings")
about_tab = tabview.add("About")

# ==== CHAT TAB ====
chat_frame = ctk.CTkFrame(chat_tab, fg_color="transparent")
chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
chat_frame.grid_columnconfigure(0, weight=0, minsize=250)
chat_frame.grid_columnconfigure(1, weight=1)
chat_frame.grid_rowconfigure(0, weight=1)

sidebar = ctk.CTkFrame(chat_frame, fg_color="transparent")
sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 16), pady=0)

sessions_list = ctk.CTkScrollableFrame(
    sidebar, fg_color="transparent", width=220, height=500, corner_radius=8
)
sessions_list.pack(fill="both", expand=True, padx=8, pady=(0, 12), anchor="nw")

def reload_sessions():
    for widget in sessions_list.winfo_children():
        widget.destroy()
    display_sessions(sessions_list, messages_frame)

def new_conversation():
    transcript = ""
    for widget in messages_frame.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    text = child.cget("text")
                    if "You •" in text:
                        transcript += f"You: "
                    elif "AI •" in text:
                        transcript += f"Psychologist: "
                    if child.cget("wraplength") > 0 and child.cget("text"):
                        transcript += child.cget("text") + "\n"
    if transcript.strip():
        save_session(transcript)
    for widget in messages_frame.winfo_children():
        widget.destroy()
    show_welcome()
    reload_sessions()

new_conversation_button = ctk.CTkButton(
    sidebar,
    text="New Conversation",
    command=new_conversation,
    font=styles.FONTS["button"],
    fg_color=colors["accent"],
    hover_color=colors["button_hover"],
    width=190,
    height=36,
    corner_radius=8
)
new_conversation_button.pack(fill="x", pady=(12, 6), padx=6, anchor="nw")

delete_all_sessions_button = ctk.CTkButton(
    sidebar,
    text="Delete All Sessions",
    fg_color="#B91C1C",
    hover_color="#881C1C",
    font=styles.FONTS["button"],
    width=190,
    height=36,
    corner_radius=8,
    command=lambda: [delete_sessions(), reload_sessions()]
)
delete_all_sessions_button.pack(fill="x", pady=(0, 8), padx=6, anchor="nw")

main_chat_panel = ctk.CTkFrame(chat_frame, fg_color="transparent")
main_chat_panel.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
main_chat_panel.grid_rowconfigure(0, weight=1)
main_chat_panel.grid_rowconfigure(1, weight=0)
main_chat_panel.grid_columnconfigure(0, weight=1)

messages_frame = ctk.CTkScrollableFrame(
    main_chat_panel, fg_color=colors["secondary_bg"], corner_radius=12
)
messages_frame.grid(row=0, column=0, sticky="nsew", padx=(6, 6), pady=(6, 3))

input_frame = ctk.CTkFrame(main_chat_panel, fg_color="transparent", height=90)
input_frame.grid(row=1, column=0, sticky="ew", padx=(6, 6), pady=(3, 6))
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=0)

message_entry = ctk.CTkTextbox(
    input_frame,
    height=70,
    fg_color=colors["secondary_bg"],
    text_color=colors["text"],
    font=styles.FONTS["entry"],
    corner_radius=10,
    wrap="word"
)
message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
message_entry.focus_set()

# CTRL + A
def select_all(event):
    event.widget.tag_add("sel", "1.0", "end-1c")
    return "break"

message_entry.bind("<Control-a>", select_all)
message_entry.bind("<Control-A>", select_all)  # for all conditiongvndf


def add_message(text, is_user=True):
    message_frame = ctk.CTkFrame(
        messages_frame,
        fg_color=colors["user_message"] if is_user else colors["ai_message"],
        corner_radius=10
    )
    message_frame.pack(anchor="e" if is_user else "w", fill="x", padx=10, pady=5)
    messages_frame.update_idletasks()
    wraplen = max(messages_frame.winfo_width() - 60, 250)
    timestamp = datetime.now().strftime("%H:%M")
    sender = "You" if is_user else "AI"
    header_text = f"{sender} • {timestamp}"
    header_label = ctk.CTkLabel(
        message_frame,
        text=header_text,
        font=(styles.FONTS["main"][0], 10),
        text_color=colors["text"],
        justify="left" if not is_user else "right"
    )
    header_label.pack(anchor="w" if not is_user else "e", padx=10, pady=(5, 0))
    message_label = ctk.CTkLabel(
        message_frame,
        text=text,
        font=styles.FONTS["message"],
        wraplength=wraplen,
        justify="left",
        text_color=colors["text"]
    )
    message_label.pack(anchor="w", fill="x", padx=10, pady=(0, 5))
    messages_frame.update_idletasks()
    messages_frame._parent_canvas.yview_moveto(1.0)
    return message_frame  # Thinking... widget for the message

def show_welcome():
    welcome_message = ctk.CTkLabel(
        messages_frame,
        text="Welcome to KlarGespräch! I'm here to provide psychological support and conversation.\nHow are you feeling today?",
        font=styles.FONTS["message"],
        justify="left",
        wraplength=max(messages_frame.winfo_width() - 60, 300),
        fg_color=colors["ai_message"],
        text_color=colors["text"],
        corner_radius=10
    )
    welcome_message.pack(anchor="w", fill="x", padx=10, pady=10)

show_welcome()
reload_sessions()

def send_message():
    message_text = message_entry.get("0.0", "end").strip()
    if not message_text:
        return
    add_message(message_text, is_user=True)
    message_entry.delete("0.0", "end")

    def ai_reply():
        thinking_widget = add_message("Thinking...", is_user=False)
        try:
            response = query_llm(message_text)
            # Thinking delete
            if thinking_widget and thinking_widget.winfo_exists():
                thinking_widget.destroy()
            add_message(response, is_user=False)
        except Exception as e:
            if thinking_widget and thinking_widget.winfo_exists():
                thinking_widget.destroy()
            add_message(f"Error: {str(e)}", is_user=False)

    Thread(target=ai_reply).start()

send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    command=send_message,
    font=styles.FONTS["button"],
    fg_color=colors["button_bg"],
    hover_color=colors["button_hover"],
    width=100,
    height=70,
    corner_radius=10
)
send_button.grid(row=0, column=1, sticky="ns")

def on_enter(event):
    if not (event.state == 1 and event.keysym == "Return"):
        send_message()
        return "break"
message_entry.bind("<Return>", on_enter)

# ==== SETTINGS TAB ====
settings_frame = ctk.CTkScrollableFrame(settings_tab, fg_color="transparent")
settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

settings_header = ctk.CTkLabel(settings_frame, text="Application Settings", font=styles.FONTS["title"])
settings_header.pack(pady=10)

theme_label = ctk.CTkLabel(settings_frame, text="Theme:", font=styles.FONTS["main"])
theme_label.pack(pady=8)

def change_theme(new_theme):
    global colors
    styles.set_theme(new_theme)
    colors = styles.get_colors()
    update_setting("theme", new_theme)
    app.configure(fg_color=colors["primary_bg"])
    tabview.configure(fg_color=colors["secondary_bg"])
    messages_frame.configure(fg_color=colors["secondary_bg"])
    message_entry.configure(fg_color=colors["secondary_bg"], text_color=colors["text"])
    send_button.configure(fg_color=colors["button_bg"], hover_color=colors["button_hover"])
    new_conversation_button.configure(fg_color=colors["accent"], hover_color=colors["button_hover"])
    delete_all_sessions_button.configure(fg_color="#B91C1C", hover_color="#881C1C")
    reload_sessions()

theme_dropdown = ctk.CTkOptionMenu(
    settings_frame,
    values=["System", "Light", "Dark"],
    command=change_theme
)
theme_dropdown.set(settings.get("theme", "System").capitalize())
theme_dropdown.pack(pady=2)

def reset_settings():
    load_settings(reset=True)
    theme_dropdown.set("System")
    change_theme("system")

reset_button = ctk.CTkButton(
    settings_frame,
    text="Reset Settings",
    command=reset_settings,
    fg_color=colors["button_bg"],
    hover_color=colors["button_hover"],
    font=styles.FONTS["button"]
)
reset_button.pack(pady=10)

# ==== ABOUT TAB ====
about_frame = ctk.CTkFrame(about_tab, fg_color="transparent")
about_frame.pack(fill="both", expand=True, padx=20, pady=20)

about_title = ctk.CTkLabel(about_frame, text="KlarGespräch - AI Psychologist", font=styles.FONTS["title"])
about_title.pack(pady=20)

about_description = ctk.CTkLabel(about_frame,
    text="An AI-powered application for psychological support and conversation.",
    font=styles.FONTS["message"],
    wraplength=600
)
about_description.pack(pady=10)

about_details = ctk.CTkLabel(about_frame,
    text="KlarGespräch uses local LLMs (your GGUF model) for private conversations. No data is sent to external servers.\n\nThis application is for support and self-reflection, not a replacement for professional mental health services.",
    font=styles.FONTS["main"],
    wraplength=600,
    justify="left"
)
about_details.pack(pady=10)

version_label = ctk.CTkLabel(about_frame, text="Version 1.0.0", font=styles.FONTS["main"])
version_label.pack(pady=5)

disclaimer = ctk.CTkLabel(about_frame,
    text="DISCLAIMER: This is not a substitute for professional mental health treatment. If you're experiencing a crisis or need immediate help, please contact a mental health professional or crisis hotline.",
    font=styles.FONTS["main"],
    wraplength=600,
    text_color="red"
)
disclaimer.pack(pady=10)

if __name__ == "__main__":
    app.mainloop()
