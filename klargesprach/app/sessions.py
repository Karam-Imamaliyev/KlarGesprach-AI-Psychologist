import os
import json
from datetime import datetime
import customtkinter as ctk

# Sessions directory (can set it according to project root)
SESSIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

def save_session(transcript):
    """Save a session transcript as a .json file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    title = "Untitled Session"
    try:
        if "You: " in transcript:
            first_msg = transcript.split("You: ")[1].split("\n")[0]
            title = first_msg[:30] + "..." if len(first_msg) > 30 else first_msg
    except Exception:
        pass

    session_data = {
        "title": title,
        "timestamp": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transcript": transcript
    }

    filepath = os.path.join(SESSIONS_DIR, f"session_{timestamp}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)

def load_session(filename):
    """Load a saved session by filename."""
    filepath = os.path.join(SESSIONS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_sessions():
    """Return all sessions (sorted by newest first)."""
    sessions = []
    for filename in os.listdir(SESSIONS_DIR):
        if filename.endswith(".json"):
            try:
                session = load_session(filename)
                session["filename"] = filename
                sessions.append(session)
            except Exception:
                continue
    sessions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return sessions

def display_sessions(sessions_frame, conversation_frame):
    """Display all saved sessions in sidebar. Click to load."""
    for widget in sessions_frame.winfo_children():
        widget.destroy()
    sessions = get_all_sessions()
    if not sessions:
        no_sessions = ctk.CTkLabel(sessions_frame, text="No saved sessions.", font=("Inter", 10, "italic"), text_color="gray")
        no_sessions.pack(pady=8)
        return

    def on_session_click(session):
        load_session_to_conversation(session, conversation_frame)

    for session in sessions:
        title = session.get("title", "Untitled")
        date = session.get("date", "Unknown")
        if len(title) > 25:
            title = title[:22] + "..."
        btn = ctk.CTkButton(
            sessions_frame,
            text=f"{title}\n{date}",
            font=("Inter", 11),
            width=180,
            height=40,
            corner_radius=8,
            fg_color="#232753",
            hover_color="#4b4f7d",
            anchor="w",
            command=lambda s=session: on_session_click(s)
        )
        btn.pack(fill="x", pady=3, padx=4, anchor="nw")

def load_session_to_conversation(session_data, conversation_frame):
    """Load messages into chat window."""
    for widget in conversation_frame.winfo_children():
        widget.destroy()
    transcript = session_data.get('transcript', '')
    lines = transcript.split('\n')
    current_speaker = None
    current_message = []
    from main import add_message  # import locally to avoid circular imports

    for line in lines:
        if line.startswith("You: "):
            if current_speaker and current_message:
                add_message('\n'.join(current_message), is_user=(current_speaker == "You"))
            current_speaker = "You"
            current_message = [line[5:]]
        elif line.startswith("Psychologist: "):
            if current_speaker and current_message:
                add_message('\n'.join(current_message), is_user=(current_speaker == "You"))
            current_speaker = "Psychologist"
            current_message = [line[14:]]
        elif line.strip() == "":
            continue
        else:
            if current_speaker:
                current_message.append(line)
    if current_speaker and current_message:
        add_message('\n'.join(current_message), is_user=(current_speaker == "You"))

def delete_sessions():
    """Delete all session files in the SESSIONS_DIR. Returns how many deleted."""
    count = 0
    if not os.path.exists(SESSIONS_DIR):
        return 0
    for filename in os.listdir(SESSIONS_DIR):
        if filename.endswith('.json'):
            try:
                os.remove(os.path.join(SESSIONS_DIR, filename))
                count += 1
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
    return count


# Quick test
if __name__ == "__main__":
    print("Found sessions:", len(get_all_sessions()))
