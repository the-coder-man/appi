**Appi \- your best virtual pal\!** 

Appi is a virtual desktop assistant designed to help you manage your Mac with simple, conversational commands. Built with Python and Tkinter, it provides a friendly, voice-enabled interface to perform various tasks on your computer. It aims to simplify your daily workflow by handling routine tasks with a simple text command, allowing you to stay focused on your work. The application's design prioritizes ease of use and accessibility, making it a great tool for users who prefer interacting with their computer through a command-line-like chat interface, enhanced with a voice. 

**Prerequisites** 

Before running the application, make sure you have a working Python 3 installation on your Mac. You don't need to install any additional Python libraries, as the application uses only standard, built-in modules like tkinter, os, and subprocess. 

**A Note on Compatibility:** This app is designed exclusively for macOS. While the core Python code is cross-platform, its functions for launching applications, managing files, and using text-to-speech rely on specific macOS commands and system calls that do not exist on other operating systems. 

**How to Use** 

1\. **Run the script:** Open your terminal and navigate to the directory where Appi.py is saved. Run the script using the following command: 

python3 Appi.py 

The application will launch and a small chat window will appear on your desktop. 2\. **Start a conversation:** The chat window is your primary interface with Appi. Simply type your commands or questions in the input box at the bottom and press "Send" or hit the Enter key. Appi's responses will appear in the chat history above. 

3\. **Explore the Settings:** Click the **Settings** button in the main window to open a separate dialog box. Here, you can customize Appi's behavior to your liking. This includes options for enabling or disabling its voice, controlling its access to your file system for enhanced privacy, and toggling certain personality features. You can also view more technical details about the application's current state. 

**Core Features** 

**Text-to-Speech (TTS)** 

Appi has a built-in voice that speaks its responses out loud, making it feel more like a personal assistant and less like a simple script. The TTS feature is a key part of the conversational experience, providing auditory feedback for every command. This can be especially useful for multitasking, as you don't have to constantly look at the chat window to know what Appi is doing. You can easily enable or disable this feature in the settings panel to suit your  
preferences, whether you're in a quiet environment or just prefer to read the responses. 

**Application Launcher** 

This feature allows you to quickly open applications on your Mac with a simple command. Appi can recognize a variety of trigger words, including open, run, launch, or start. This is a much faster alternative to navigating through the Finder or Launchpad, especially for frequently used apps. 

**Examples:** 

● open Safari: This will launch the Safari web browser. 

● launch Calculator: This will open the Calculator application. 

● start a game of Chess: This will launch the Chess.app. 

**File Management** 

Appi can help you manage your local files and folders directly from the chat interface. This feature is enabled by default to provide full functionality, but you can disable it in the settings for enhanced privacy or security if you prefer. This allows you to perform basic file operations without having to open a separate Finder window. 

**Commands:** 

● create folder \[folder name\]: Creates a new folder in the current directory where the script is being run. For example, create folder 'Project Alpha' will create a new directory named "Project Alpha." 

● delete \[item name\]: Deletes a specified file or folder. Appi will ask for confirmation before deleting to prevent accidental data loss. For example, delete old\_report.txt. ● search for \[query\]: Searches for files or folders matching a query within the current directory. This is useful for quickly locating a file you might have misplaced. ● properties of \[item name\]: Displays detailed information about a file or folder, such as its size, creation date, and last modified date. This is an efficient way to get a quick overview of a file's metadata. 

● list files: Lists all files and folders in the current directory. This command is a great way to orient yourself and see what's available for Appi to interact with. 

**Time and System Information** 

Ask Appi for the current time or for details about your Mac's operating system and hardware. This feature uses system commands to provide up-to-date and accurate information. It's a quick way to check the time or get a snapshot of your system's health without opening multiple windows or applications. 

**Commands:** 

● what's the time?: Appi will respond with the current time. 

● system info or about my mac: Appi will gather and display detailed information about your  
macOS version and hardware specifications. 

**Updates** 

Appi can check for available macOS software updates using the system's built-in command-line tools. It will report back whether your system is up to date or if there are any updates waiting to be installed. This is a convenient way to stay on top of your system's security and performance. 

**Commands:** 

● check for updates 

● Mac update 

● System update 

**Reminders** 

Set simple reminders with a specific time delay. Appi will send you a macOS notification when the time is up, so you don't miss important events or tasks. The reminders are processed in the background, allowing you to continue using your computer for other tasks. 

**Example:** 

● remind me in 5 minutes to call Jane: After five minutes, a notification will appear on your screen with the message "call Jane." 

**Troubleshooting** 

● If the application does not work, make sure you are running it on a macOS machine, as it is not cross-platform. 

● If you encounter a bug or an unexpected error, an error message will be displayed directly in the chat window, providing a hint about what went wrong. 

● If Appi's voice isn't working, check your system's volume and make sure the TTS feature is enabled in the settings. You can also test your system's say command in the terminal to ensure it's functioning correctly.
