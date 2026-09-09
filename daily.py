import os
from datetime import datetime

try:
    import pyttsx3
    engine = pyttsx3.init()
    def speak(text):
        engine.say(text)
        engine.runAndWait()
    has_voice = True
except:
    def speak(text):
        print("[Voice not installed, run pip install pyttsx3]")
    has_voice = False

if not os.path.exists("brain.md"):
    print("No brain.md found")
    exit()

lines = open("brain.md", "r", encoding="utf-8").readlines()
notes = []
for l in lines:
    if l.startswith("- ["):
        notes.append(l)

today = datetime.now().strftime('%Y-%m-%d')
today_notes = []
for l in notes:
    if today in l:
        today_notes.append(l)

print("")
print("=== DAILY SUMMARY ===")
print(today)
print("Total ideas: " + str(len(notes)))
print("Today: " + str(len(today_notes)))
print("")

for n in notes:
    print(n.strip())

filename = "summary-" + today + ".md"
open(filename, "w", encoding="utf-8").writelines(notes)
print("")
print("Saved to " + filename)

# SPEAKING PART
msg = "Good evening Bharat! You had " + str(len(today_notes)) + " ideas today, and " + str(len(notes)) + " ideas in total. Your second brain is updated. Keep building!"
print("")
print(msg)

if has_voice:
    speak(msg)

print("Done!")