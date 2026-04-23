import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import time
import pyautogui
import subprocess

# 🔑 API KEY
API_KEY = "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"

# 🔊 Voice Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

if voices:
    engine.setProperty('voice', voices[0].id)
else:
    print("No voice found!")

engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)

# 🔊 Speak
def speak(text):
    print("Jarvis:", text)
    engine.say(str(text))
    engine.runAndWait()

# 🎤 Listen
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

# 🤖 AI
def ask_ai(prompt):
    try:
        speak("Thinking...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        if "choices" in data:
            return data['choices'][0]['message']['content']
        return None
    except:
        return None

# 🧠 Fallback
def fallback_response(command):
    if "how are you" in command:
        return "I am functioning perfectly, Aninda!"
    return "Sorry, I couldn't connect to the internet."

# ⚠️ Confirm Dangerous Actions
def confirm_action(action):
    speak(f"Do you want me to {action}?")
    ans = listen()
    return "yes" in ans

# 🖥️ Open App
def open_application(app_name):
    try:
        speak(f"Opening {app_name}")
        subprocess.Popen(app_name)
    except:
        speak("I couldn't open that application")

# 🟢 Wake Word
def wait_for_wake_word():
    while True:
        command = listen()
        if "hey jarvis" in command:
            speak("Yes Aninda, I am listening")
            return

# 🧠 Main
def run_jarvis():
    speak("System ready. Say Hey Jarvis to start.")

    while True:
        wait_for_wake_word()
        time.sleep(0.5)

        while True:
            command = listen()

            if command == "":
                continue

            # ⏰ Time
            elif "time" in command:
                current_time = datetime.datetime.now().strftime("%H:%M")
                speak(f"The time is {current_time}")

            # 🌐 Search
            elif "search" in command:
                query = command.replace("search", "")
                speak(f"Searching for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")

            # 🌐 Open Website
            elif "open website" in command:
                site = command.replace("open website", "").strip()
                speak(f"Opening {site}")
                webbrowser.open(f"https://{site}.com")

            # 🖥️ Specific Apps
            elif "open chrome" in command:
                speak("Opening Chrome")
                os.system("start chrome")

            elif "open notepad" in command:
                speak("Opening Notepad")
                os.system("notepad")

            # 🧠 Dynamic Open (keep AFTER specific)
            elif command.startswith("open"):
                app = command.replace("open", "").strip()
                open_application(app)

            # ❌ Close App
            elif "close" in command:
                app = command.replace("close", "").strip()
                os.system(f"taskkill /f /im {app}.exe")
                speak(f"Closing {app}")

            # 🔊 Volume
            elif "volume up" in command:
                pyautogui.press("volumeup")

            elif "volume down" in command:
                pyautogui.press("volumedown")

            elif "mute" in command:
                pyautogui.press("volumemute")

            # ⌨️ Type
            elif "type" in command:
                text = command.replace("type", "")
                speak("Typing now")
                pyautogui.write(text)

            # 📸 Screenshot
            elif "screenshot" in command:
                img = pyautogui.screenshot()
                img.save("screenshot.png")
                speak("Screenshot taken")

            # 🔴 Shutdown
            elif "shutdown" in command:
                if confirm_action("shutdown the system"):
                    os.system("shutdown /s /t 5")

            # 🔁 Restart
            elif "restart" in command:
                if confirm_action("restart the system"):
                    os.system("shutdown /r /t 5")

            # ❌ Cancel Shutdown
            elif "cancel shutdown" in command:
                os.system("shutdown /a")
                speak("Shutdown cancelled")

            # 🔐 Lock
            elif "lock computer" in command:
                os.system("rundll32.exe user32.dll,LockWorkStation")
                speak("Computer locked")

            # 🌙 Sleep Mode
            elif "sleep computer" in command:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                speak("Going to sleep")

            # 🛑 Stop
            elif "stop" in command:
                speak("Goodbye Aninda")
                exit()
            elif "who made you" in command or "your creator" in command:
                speak(
                    "I was designed and developed by Aninda Nath, a B Tech Computer Science student from KIIT University.")

            # 😴 Jarvis Sleep
            elif "sleep" in command:
                speak("Going to sleep")
                break

            # 🤖 AI fallback
            else:
                answer = ask_ai(command)
                if answer:
                    speak(answer)
                else:
                    speak(fallback_response(command))

# ▶️ Run
if __name__ == "__main__":
    run_jarvis()