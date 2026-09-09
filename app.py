import tkinter as tk
import datetime
import os

# FIXED - Save to Documents (never permission error)
DOCS_FOLDER = os.path.join(os.path.expanduser("~"), "Documents")
BRAIN_FILE = os.path.join(DOCS_FOLDER, "bharat-brain.md")

# Create file if not exists
if not os.path.exists(BRAIN_FILE):
    with open(BRAIN_FILE, "w", encoding="utf-8") as f:
        f.write("# My Second Brain - Bharat\n")

def save_idea():
    text = entry.get().strip()
    if not text:
        return
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(BRAIN_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n- [{now}] {text}")
        entry.delete(0, tk.END)
        listbox.insert(tk.END, f"[{now}] {text}")
        status.config(text=f"SAVED to Documents! ✅", fg="#00FF88")
        entry.focus()
    except Exception as e:
        status.config(text=f"Error: {e}", fg="red")

def add_idea(text):
    save_idea_text(text)

def save_idea_text(text):
    if not text: return
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(BRAIN_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n- [{now}] {text}")
    listbox.insert(tk.END, f"[{now}] {text}")

def view_all():
    listbox.delete(0, tk.END)
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines()[-100:]:
                if line.strip() and not line.startswith("#"):
                    listbox.insert(tk.END, line.strip())
    status.config(text=f"Loaded from: {BRAIN_FILE}", fg="white")

def search_ideas():
    q = search_entry.get().lower().strip()
    listbox.delete(0, tk.END)
    if not os.path.exists(BRAIN_FILE): return
    if not q:
        view_all()
        return
    with open(BRAIN_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if q in line.lower():
                listbox.insert(tk.END, line.strip())

def speak_idea():
    try:
        import speech_recognition as sr
        status.config(text="Listening... Speak now! 🎤", fg="#FF4081")
        root.update()
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5)
        text = r.recognize_google(audio)
        entry.delete(0, tk.END)
        entry.insert(0, text)
        status.config(text=f"Heard: {text}", fg="#00FF88")
    except Exception as e:
        status.config(text=f"Voice error: Install mic or type. {e}", fg="orange")

# UI
root = tk.Tk()
root.title("Second Brain - Bharat's JARVIS")
root.geometry("700x650")
root.configure(bg="#121212")

tk.Label(root, text="🧠 SECOND BRAIN", font=("Arial", 24, "bold"), fg="#00FF88", bg="#121212").pack(pady=15)
tk.Label(root, text="Your AI Memory - Built by Bharat", fg="white", bg="#121212").pack()

frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10, fill="x", padx=20)
entry = tk.Entry(frame, font=("Arial", 12), bg="#222", fg="white", insertbackground="white")
entry.pack(side="left", fill="x", expand=True, ipady=8)
entry.bind("<Return>", lambda e: save_idea())
tk.Button(frame, text="💾 Save", command=save_idea, bg="#00FF88", font=("Arial", 10, "bold"), padx=15, pady=5).pack(side="left", padx=5)

tk.Button(root, text="🎤 Speak Idea (Voice Input)", command=speak_idea, bg="#FF4081", fg="white", font=("Arial", 11, "bold"), padx=20, pady=8).pack(pady=10)

sframe = tk.Frame(root, bg="#121212")
sframe.pack(fill="x", padx=20, pady=5)
search_entry = tk.Entry(sframe, font=("Arial", 10), bg="#222", fg="white", insertbackground="white")
search_entry.insert(0, "Search ideas...")
search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) if search_entry.get()=="Search ideas..." else None)
search_entry.pack(side="left", fill="x", expand=True, ipady=5)
tk.Button(sframe, text="🔍 Search", command=search_ideas, bg="#333", fg="white").pack(side="left", padx=2)
tk.Button(sframe, text="📋 View All", command=view_all, bg="#333", fg="white").pack(side="left", padx=2)

listbox = tk.Listbox(root, bg="#1E1E1E", fg="white", font=("Arial", 10), height=18)
listbox.pack(fill="both", expand=True, padx=20, pady=10)

status = tk.Label(root, text=f"Ready! Saving to Documents/bharat-brain.md", fg="#00FF88", bg="#121212", font=("Arial", 8))
status.pack(pady=5)

view_all()
entry.focus()
root.mainloop()