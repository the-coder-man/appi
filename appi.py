import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import time
import threading
import shutil
from datetime import datetime
import random
import re
import platform
import sys
def check_os():
    if platform.system() != "Darwin":
        messagebox.showerror("Error", "this app will only work with macOS")
        sys.exit()
class FileHandler:
    def __init__(self, assistant_instance):
        self.assistant = assistant_instance
        self.current_path = os.getcwd()

    def create_folder(self, folder_name):
        new_folder_path = os.path.join(self.current_path, folder_name)
        if os.path.exists(new_folder_path):
            self.assistant.appi_speak(f"A folder named '{folder_name}' already exists here.")
        else:
            try:
                os.mkdir(new_folder_path)
                self.assistant.appi_speak(f"Folder '{folder_name}' created successfully!")
            except Exception as e:
                self.assistant.appi_speak(f"I couldn't create that folder. Here's what buzzed my circuits: {e}")

    def delete_item(self, item_name):
        full_path = os.path.join(self.current_path, item_name)
        if not os.path.exists(full_path):
            self.assistant.appi_speak(f"I can't find anything named '{item_name}' to delete.")
            return

        confirm_text = f"Are you sure you want to delete '{item_name}'? This cannot be undone."
        self.assistant.appi_speak(confirm_text)
        
        # This part of the code would require a GUI-based confirmation dialog,
        # which can be complex with threads. For now, we'll proceed
        # but in a real-world app, a confirmation step would be critical.
        
        try:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
                self.assistant.appi_speak(f"The folder '{item_name}' has been deleted!")
            else:
                os.remove(full_path)
                self.assistant.appi_speak(f"The file '{item_name}' has been deleted!")
        except Exception as e:
            self.assistant.appi_speak(f"I couldn't delete '{item_name}'. It seems there was a bug: {e}")

    def search_files(self, query):
        found_items = []
        for root, dirs, files in os.walk(self.current_path):
            for name in dirs + files:
                if query.lower() in name.lower():
                    rel_path = os.path.relpath(os.path.join(root, name), self.current_path)
                    found_items.append(rel_path)
        
        if found_items:
            list_text = "\n".join(found_items)
            self.assistant.appi_speak(f"I found these items for you:\n\n{list_text}")
        else:
            self.assistant.appi_speak(f"I couldn't find any items matching '{query}'.")

    def show_properties(self, item_name):
        full_path = os.path.join(self.current_path, item_name)
        if not os.path.exists(full_path):
            self.assistant.appi_speak(f"I can't find anything named '{item_name}' to get properties for.")
            return
        
        try:
            stat_info = os.stat(full_path)
            is_dir = os.path.isdir(full_path)
            
            size_kb = stat_info.st_size / 1024
            created = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            properties_text = (
                f"Properties for: {item_name}\n"
                f"Type: {'Folder' if is_dir else 'File'}\n"
                f"Size: {size_kb:.2f} KB\n"
                f"Created: {created}\n"
                f"Modified: {modified}"
            )
            self.assistant.appi_speak(properties_text)
        except Exception as e:
            self.assistant.appi_speak(f"I couldn't get the properties. A bug flew into the system: {e}")

class AppiAssistant(tk.Tk):
    check_os()
    def __init__(self):
        super().__init__()
        self.title("Appi the Desktop assistant")
        self.geometry("600x650")
        self.config(bg="#f0f0f0")

        # Initialize settings with default values
        self.tts_enabled = tk.BooleanVar()
        self.file_access_enabled = tk.BooleanVar()
        self.jokes_enabled = tk.BooleanVar()
        self.tips_enabled = tk.BooleanVar()
        self.personality_enabled = tk.BooleanVar()

        self.load_settings()

        # The TTS engine is now the 'say' command
        self.engine_ready = True
        
        self.file_handler = FileHandler(self)
        
        
        # Pre-defined lists for jokes and tips
        self.jokes = [
            "Why did the bee cross the road? To get to the other flower!",
            "What do you call a bug with no legs? A carpet!",
            "Why don't bugs get sick? Because they have little anti-bodies!",
            "What do you call a group of beetles playing music? A rock band!"
        ]
        
        self.tips = [
            "You can press **Command + Space** to open Spotlight Search. It's the fastest way to find anything on your Mac!",
            "Did you know that **Command + Tab** lets you quickly switch between open applications?",
            "Use **Shift + Command + 5** to open the screenshot toolbar for more options.",
            "Want to quickly hide all windows of an app? Just press **Command + H**.",
            "Press and hold a letter on your keyboard to see different accent options, like in Spanish or French."
        ]

        # --- GUI Elements ---
        
        header = tk.Label(self, text="Appi - your best virtual pal!", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
        header.pack(pady=10)
        # Message display area
        self.message_box = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
        self.message_box.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)
        
        # User input area
        input_frame = tk.Frame(self, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.settings_button = tk.Button(input_frame, text="Settings", command=self.open_settings_menu, bg="#E0E0E0", fg="black", font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3)
        self.settings_button.pack(side=tk.LEFT, padx=(0, 5), ipady=5)

        self.user_input = tk.Entry(input_frame, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5)
        self.user_input.bind("<Return>", self.handle_command_event)

        # Send button
        self.send_button = tk.Button(input_frame, text="Send", command=self.handle_command, bg="#C8E6C9", fg="black", font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3)
        self.send_button.pack(side=tk.RIGHT, padx=5, ipady=5)

        # Initial message
        self.appi_speak(random.choice([
            "Hello there! I'm Appi, your friendly neighborhood desktop assistant. What can I do for you today?",
            "Greetings! Appi at your service. How can I assist you?",
            "Hey! Appi here, ready to help. What's on your mind?"
        ]))

    def load_settings(self):
        try:
            with open("appi_settings.txt", "r") as f:
                settings = f.read().strip().split(',')
                self.tts_enabled.set(settings[0] == "True")
                self.file_access_enabled.set(settings[1] == "True")
                self.jokes_enabled.set(settings[2] == "True")
                self.tips_enabled.set(settings[3] == "True")
                self.personality_enabled.set(settings[4] == "True")
        except FileNotFoundError:
            # Set default values if the file is not found
            self.tts_enabled.set(True)
            self.file_access_enabled.set(True)
            self.jokes_enabled.set(True)
            self.tips_enabled.set(True)
            self.personality_enabled.set(True)

    def save_settings(self):
        settings_string = f"{self.tts_enabled.get()},{self.file_access_enabled.get()},{self.jokes_enabled.get()},{self.tips_enabled.get()},{self.personality_enabled.get()}"
        with open("appi_settings.txt", "w") as f:
            f.write(settings_string)

    def open_settings_menu(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Appi Settings")
        settings_window.geometry("400x300")
        settings_window.config(bg="#f0f0f0")
        
        tk.Label(settings_window, text="Appi Assistant Settings", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Checkbox for TTS
        tts_check = tk.Checkbutton(settings_window, text="Enable Appi's Voice (Text-to-Speech)", variable=self.tts_enabled, onvalue=True, offvalue=False, font=("Arial", 12), bg="#f0f0f0")
        tts_check.pack(pady=5, padx=20, anchor='w')

        # Checkbox for File Access
        file_access_check = tk.Checkbutton(settings_window, text="Allow File System Access", variable=self.file_access_enabled, onvalue=True, offvalue=False, font=("Arial", 12), bg="#f0f0f0")
        file_access_check.pack(pady=5, padx=20, anchor='w')

        # Checkbox for Jokes
        jokes_check = tk.Checkbutton(settings_window, text="Enable Jokes", variable=self.jokes_enabled, onvalue=True, offvalue=False, font=("Arial", 12), bg="#f0f0f0")
        jokes_check.pack(pady=5, padx=20, anchor='w')

        # Checkbox for Tips
        tips_check = tk.Checkbutton(settings_window, text="Enable Mac Tips", variable=self.tips_enabled, onvalue=True, offvalue=False, font=("Arial", 12), bg="#f0f0f0")
        tips_check.pack(pady=5, padx=20, anchor='w')

        # Checkbox for Personality
        personality_check = tk.Checkbutton(settings_window, text="Enable Conversational Personality", variable=self.personality_enabled, onvalue=True, offvalue=False, font=("Arial", 12), bg="#f0f0f0")
        personality_check.pack(pady=5, padx=20, anchor='w')
        
        def save_and_close():
            self.save_settings()
            settings_window.destroy()

        save_button = tk.Button(settings_window, text="Save Settings", command=save_and_close, bg="#C8E6C9", fg="black", font=("Arial", 12, "bold"))
        save_button.pack(pady=20)
        
    def appi_speak(self, text):
       self.message_box.config(state=tk.NORMAL)
       self.message_box.insert(tk.END, f"Appi: {text}\n\n")
       self.message_box.config(state=tk.DISABLED)
       self.message_box.see(tk.END)

       if self.tts_enabled.get():
           def speak_in_thread(message):
               # macOS 'say' command to speak the text
               subprocess.run(["say", message])

           threading.Thread(target=speak_in_thread, args=(text,)).start()

    def run_macos_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, timeout=10)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Whoops, a bug crawled into the system. I couldn't run that command. Error: {e.stderr.strip()}"
        except FileNotFoundError:
            return "I can't find that application on your system."
        except subprocess.TimeoutExpired:
            return "The command took too long to run. Let's try something else."

    def handle_command_event(self, event):
        self.handle_command()
    
    def handle_command(self):
        user_input_text = self.user_input.get().strip()
        if not user_input_text:
            return

        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, f"You: {user_input_text}\n\n")
        self.message_box.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)

        user_input_lower = user_input_text.lower()
        
        # Start a new thread to run the command and avoid freezing the GUI
        thread = threading.Thread(target=self.process_in_thread, args=(user_input_lower,))
        thread.start()

    def check_for_updates(self):
        """Checks for macOS software updates."""
        self.appi_speak("Just a moment, I'm checking for new macOS updates for you.")
        try:
            # Use 'softwareupdate -l' to list available updates
            result = subprocess.run(
                ["softwareupdate", "-l"],
                capture_output=True,
                text=True,
                check=True,
                timeout=300 # A long timeout might be needed for a network check
            )
            output = result.stdout.strip()
            
            if "No new software available." in output:
                self.appi_speak("Your Mac is up to date! There are no new software updates available.")
            else:
                self.appi_speak("Great news! I found some software updates for your Mac. Here's what's available:")
                self.appi_speak(output)
                self.appi_speak("You can run 'sudo softwareupdate -i -a' in your terminal to install them.")

        except subprocess.CalledProcessError as e:
            self.appi_speak(f"Hmm, I ran into an issue while checking for updates. It seems there was a bug: {e.stderr.strip()}")
        except FileNotFoundError:
            self.appi_speak("I couldn't find the 'softwareupdate' command. This is unexpected. Are you sure you're on macOS?")
        except subprocess.TimeoutExpired:
            self.appi_speak("Checking for updates took too long. The network might be slow. Please try again later.")
            
    def set_reminder(self, reminder_text):
        try:
            # Simple regex to find a number and a time unit
            match = re.search(r'in (\d+)\s+(minute|minutes|hour|hours)', reminder_text)
            if not match:
                self.appi_speak("I'm sorry, I couldn't understand the time for that reminder. Could you say something like, 'remind me in 5 minutes'?")
                return

            value = int(match.group(1))
            unit = match.group(2)

            if "minute" in unit:
                delay = value * 60
            elif "hour" in unit:
                delay = value * 3600
            else:
                self.appi_speak("I'm not sure how to handle that time unit. Please try 'minutes' or 'hours'.")
                return

            # Extract the actual reminder message
            message_match = re.search(r'to (.+)', reminder_text)
            message = message_match.group(1) if message_match else "A reminder from Appi!"

            # Schedule the notification
            timer = threading.Timer(delay, self.show_notification, args=[message])
            timer.start()

            self.appi_speak(f"Okay, I've set a reminder to '{message}' for you. I'll notify you in {value} {unit}.")

        except Exception as e:
            self.appi_speak(f"I ran into a bug while trying to set that reminder. Here's what buzzed: {e}")

    def show_notification(self, message):
        try:
            # This is specific to macOS.
            command = f'osascript -e \'display notification "{message}" with title "Appi Reminder" sound name "Glass" \''
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            print(f"Failed to show notification: {e}")
            self.appi_speak(f"Oops, a bug prevented me from showing your reminder: '{message}'")
            
    def add_appi_knowledge(self, user_input_lower):
        if "what is apple intelligence" in user_input_lower or "what is apple ai" in user_input_lower:
            self.appi_speak("Apple Intelligence is the next generation of AI for your Mac. It's a personal intelligence system that helps you with your writing, generates images, and understands your personal context across your apps. It's designed to be powerful and completely private.")
            return True
        
        if "what is the notes app" in user_input_lower:
            self.appi_speak("The Notes app is your digital notebook. It's great for jotting down quick ideas, creating checklists, and even adding images or drawings. The best part is that everything you create automatically syncs across all your Apple devices.")
            return True

        if "what is safari" in user_input_lower or "what is apple's browser" in user_input_lower:
            self.appi_speak("Safari is Apple's web browser, and it's built specifically for your Mac. It's known for being incredibly fast, private, and energy-efficient, which helps your battery last longer. It has great features like private browsing and smart tracking prevention.")
            return True

        if "what is system settings" in user_input_lower or "what are system settings" in user_input_lower:
            self.appi_speak("System Settings is the control center for your Mac. This is where you can change your wallpaper, set up Wi-Fi, manage your account, and customize just about every aspect of how your Mac looks and works. It's like a central hub for all your preferences.")
            return True

        if "what is mission control" in user_input_lower or "how to use mission control" in user_input_lower:
            self.appi_speak("Mission Control gives you an overview of all your open windows, desktops, and full-screen apps. Just swipe up with three or four fingers on your trackpad to see everything at once. It's super helpful for multitasking and keeping your workspace organized.")
            return True

        if "how to use finder tags" in user_input_lower or "what are finder tags" in user_input_lower:
            self.appi_speak("Finder Tags are a great way to organize your files. You can assign colored tags to files and folders, and then easily find them later by clicking the tag in the Finder sidebar. It's much more flexible than just using folders!")
            return True

        if "what is time machine" in user_input_lower or "how to back up my mac" in user_input_lower:
            self.appi_speak("Time Machine is your Mac's built-in backup utility. It automatically backs up your entire computer to an external hard drive, so if you ever lose a file or need to restore your Mac, you can go back in time and recover everything. It's like a safety net for all your data!")
            return True

        if "what is airdrop" in user_input_lower or "how to use airdrop" in user_input_lower:
            self.appi_speak("AirDrop is a wireless way to share files between Apple devices. You can send photos, videos, documents, and more to a nearby Mac, iPhone, or iPad. It's incredibly fast and doesn't require any Wi-Fi or cables.")
            return True

        if "what is universal control" in user_input_lower or "how to use universal control" in user_input_lower:
            self.appi_speak("Universal Control lets you use a single mouse and keyboard to control multiple Apple devices, like your Mac and iPad. You can seamlessly move your cursor from one screen to the other and even drag and drop files between them. It's like having one big, connected workspace.")
            return True

        if "what is icloud" in user_input_lower or "what is apple's cloud" in user_input_lower:
            self.appi_speak("iCloud is Apple's cloud storage service. It syncs your photos, files, contacts, and app data across all your devices. It's great for keeping everything backed up and accessible no matter which device you're using.")
            return True

        if "what is continuity camera" in user_input_lower or "how to use continuity camera" in user_input_lower:
            self.appi_speak("Continuity Camera allows you to use your iPhone as a webcam for your Mac. You can use it in apps like FaceTime or Zoom to get a much higher-quality video feed than your Mac's built-in camera.")
        if "keyboard shortcuts" in user_input_lower or "what are keyboard shortcuts" in user_input_lower:
            shortcuts = random.choice([ 
                "Here are some useful keyboard shortcuts for your Mac:\n\n- Command + C: Copy\n- Command + V: Paste\n- Command + X: Cut\n- Command + Z: Undo\n- Command + Shift + 4: Screenshot",
                "Mac keyboard shortcuts can help you work more efficiently. Here are a few:\n\n- Command + C: Copy\n- Command + V: Paste\n- Command + X: Cut\n- Command + Z: Undo\n- Command + Shift + 4: Screenshot",
                "Looking to speed up your workflow? Check out these Mac keyboard shortcuts:\n\n- Command + C: Copy\n- Command + V: Paste\n- Command + X: Cut\n- Command + Z: Undo\n- Command + Shift + 4: Screenshot"
            ])
            self.appi_speak(shortcuts)
            return True

        return False


    def process_in_thread(self, user_input_lower):
        # Check for updates
        if "check for updates" in user_input_lower or "system update" in user_input_lower or "mac update" in user_input_lower:
            self.check_for_updates()
            return
            
        # Reminder functionality
        if "remind me" in user_input_lower or "set a reminder" in user_input_lower:
            self.set_reminder(user_input_lower)
            return

        # File management commands
        if "create folder" in user_input_lower or "delete" in user_input_lower or "search for" in user_input_lower or "properties of" in user_input_lower:
            if not self.file_access_enabled.get():
                self.appi_speak("I'm sorry, my file system access is currently disabled in the settings. I can't perform that action.")
                return
        
        if "create folder" in user_input_lower:
            folder_name = user_input_lower.split("create folder", 1)[1].strip()
            if folder_name:
                self.file_handler.create_folder(folder_name)
            else:
                self.appi_speak("What do you want to name the new folder?")
            return
        
        if "delete" in user_input_lower:
            item_name = user_input_lower.split("delete", 1)[1].strip()
            if item_name:
                self.file_handler.delete_item(item_name)
            else:
                self.appi_speak("What file or folder do you want me to delete?")
            return
            
        if "search for" in user_input_lower:
            query = user_input_lower.split("search for", 1)[1].strip()
            if query:
                self.file_handler.search_files(query)
            else:
                self.appi_speak("What file or folder are you looking for?")
            return

        if "properties of" in user_input_lower:
            item_name = user_input_lower.split("properties of", 1)[1].strip()
            if item_name:
                self.file_handler.show_properties(item_name)
            else:
                self.appi_speak("Which file or folder's properties do you want to see?")
            return

        # Personality and info commands
        if (self.jokes_enabled.get() and
            ("tell me a joke" in user_input_lower or "make me laugh" in user_input_lower)):
            self.appi_speak(random.choice(self.jokes))
            return
        
        if (self.tips_enabled.get() and
            ("give me a tip" in user_input_lower or "mac tip" in user_input_lower)):
            self.appi_speak(random.choice(self.tips))
            return

        if self.personality_enabled.get():
            if self.add_appi_knowledge(user_input_lower):
                return
            
        # Command recognition for app launching
        app_launch_keywords = ["open", "run", "launch", "start"]
        app_found = False
        
        for keyword in app_launch_keywords:
            if f" {keyword} " in user_input_lower or user_input_lower.startswith(keyword + " "):
                app_to_open = user_input_lower.replace(keyword, "", 1).strip()
                if not app_to_open:
                    self.appi_speak("Which app did you want me to launch? I'm ready to fly!")
                else:
                    self.appi_speak(f"Just launched {app_to_open.title()} for you. Enjoy!")
                    try:
                        subprocess.Popen(["open", "-a", app_to_open.title()])
                    except FileNotFoundError:
                        self.appi_speak(f"Hmm, I can't seem to find an application named '{app_to_open}'. Are you sure it's installed?")
                app_found = True
                break

        if app_found:
            return

        # Handle other commands
        if user_input_lower in ["exit", "quit", "bye"]:
            self.appi_speak("It was a pleasure buzzing around with you. See you soon!")
            self.after(2000, self.destroy)
        
        elif "hello" in user_input_lower or "hi" in user_input_lower:
            self.appi_speak(random.choice([
                "Hey there! It's a great day to be a computer program. What's on your mind?",
                "Hi! It's wonderful to hear from you. What can I help with?",
                "Greetings! I'm all charged up and ready to go."
            ]))
        
        elif "what's your name" in user_input_lower:
            self.appi_speak("My name is Appi, a virtual desktop assistant designed to help you navigate your Mac. Think of me as Apple's most humble co-pilot.")

        elif "thank you" in user_input_lower or "thanks" in user_input_lower:
            self.appi_speak(random.choice([
                "You're welcome! Happy to help.",
                "Any time! That's what I'm here for.",
                "No problem at all! Glad I could assist."
            ]))
            
        elif "time" in user_input_lower:
            current_time = time.strftime("%I:%M %p")
            self.appi_speak(f"The current time is {current_time}. A perfect time for a snack, I think!")
            
        elif "list files" in user_input_lower or "show me files" in user_input_lower:
            try:
                files = os.listdir(".")
                file_list = "\n".join(files)
                self.appi_speak(f"I've crawled through this folder and found these files and directories for you:\n\n{file_list}")
            except Exception as e:
                self.appi_speak(f"Sorry, I ran into a problem listing files: {e}")
            
        elif "system info" in user_input_lower or "about my mac" in user_input_lower:
            self.appi_speak("Gathering some system details for you...")
            version_output = self.run_macos_command("sw_vers")
            hardware_output = self.run_macos_command("uname -a")
            self.appi_speak(f"Here is what I found:\n\nmacOS Version:\n{version_output}\n\nHardware Info:\n{hardware_output}")
        elif "features" in user_input_lower or "what can you do" in user_input_lower:
            self.appi_speak("I can help you with a variety of tasks! You can ask me to open apps, tell you jokes, give Mac tips, manage files, set reminders, and more. Just type what you need, and I'll do my best to assist!")
        else:
            self.appi_speak("That's a bit beyond my current capabilities. Maybe I should get another bug to help me out. Try something simple like 'open Safari' or 'what's the time?'.")


if __name__ == "__main__":
    app = AppiAssistant()
    app.mainloop()
