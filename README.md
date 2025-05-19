# KlarGespräch - AI Psychologist 

“Other bots just chat. This app actually leads to your feelings.”

---

🚀 What Is This?
-----------------
KlarGespräch is a fully local, privacy-first AI psychologist chat app powered by your own GGUF model (e.g. Nous Hermes 2 Mistral 7B).  
All conversations stay on your machine—no internet, no data leaks, no excuses.

If you’re paranoid, perfectionist, or just want to own your data—welcome home.

---

💎 Features
-----------
- Truly offline — No cloud, no tracking, no leaks.
- Bring your own GGUF model — Top-level local LLM (Nous Hermes 2, Mistral 7B, etc.)
- Modern UI — Custom themes, light/dark/system.
- Session management — Every chat is saved. Review, restart, or nuke your sessions anytime.
- Fast as your CPU allows — While web-based AIs are still loading, you’re already done.
- Configurable, hackable, yours — Don’t like something? It’s Python, change it.

---

🛠️ Installation
-----------------
1. Requirements:
   - Python 3.10+
   - llama-cpp-python (https://github.com/abetlen/llama-cpp-python)
   - customtkinter (https://github.com/TomSchimansky/CustomTkinter)
   - Your GGUF model (e.g. Nous Hermes 2 Mistral 7B DPO)

   Install the required packages by running:
   pip install llama-cpp-python customtkinter

2. Place your GGUF Model:
   Put your .gguf file here:
   klargesprach/model/YourModel/YourModel.gguf

   Change the model path in llm_engine.py if needed.

---

⚡ Usage
-------
Run the following command:
   python main.py

Start chatting in the Chat tab.
For a new conversation, hit “New Conversation” – your old session is autosaved.
Sessions are listed on the left; clicking on any session reloads that previous conversation.

---

🧩 Customization
----------------
- Model: Swap your GGUF model by changing the path in llm_engine.py.
- Prompt: Tweak your system prompt in make_prompt() if you want a sassier, smarter, or colder psychologist.
- UI Theme: Change light/dark/system in Settings.
- RAM/CPU: It depend's on system. The more bread, the more meatballs. 

---

🛑 Disclaimer
-------------
This project is for informational and personal support use only.
It is not a replacement for a real psychologist.
If you need urgent help, talk to a human. 
# KlarGesprach-AI-Psychologist
