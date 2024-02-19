import tkinter as tk
import tkinter.messagebox as messagebox
import os
import shutil
import sys
import subprocess

class Downloader:
    def __init__(self, download_directory, installation_directory):
        self.download_directory = download_directory
        self.installation_directory = installation_directory

    def install_dependencies(self):
        commands = [
            "cd ~/.NLU-Application && mkdir -p Virtual_Environment",
            "cd ~/.NLU-Application/Virtual_Environment && python3 -m venv NLU_VE",
            "python3 ~/.NLU-Application/Virtual_Environment/NLU_VE/bin/pip install -r ~/.NLU-Application/Setup/requirements.txt"
        ]

        # Execute the commands
        for cmd in commands:
            subprocess.run(cmd, shell=True, executable="/bin/bash")
    
    def create_desktop_entry(self):
        os.system("cd ~ && wget https://github.com/ChronoByte404/NLU-Application/raw/main/Installers/Launcher.program")
        subprocess.run(f"sudo chmod +x ~/.NLU-Application/Installers/Launcher.program", shell=True, check=True)
        desktop_entry = f'''[Desktop Entry]
Name=NLU Assistant
Exec="~/.NLU-Application/Installers/Launcher.program"
Icon={os.path.join(self.installation_directory, 'images', 'icon.png')}
Type=Application
Categories=Utility;'''

        desktop_path = os.path.join(os.environ['HOME'], '.local', 'share', 'applications', 'NLU-Application.desktop')

        with open(desktop_path, 'w') as desktop_file:
            desktop_file.write(desktop_entry)

        print(f"Desktop entry created at: {desktop_path}")

    def download_and_extract(self):
        try:
            print("Removing existing installation (excluding Settings folder).")
            if os.path.exists(self.installation_directory):
                shutil.rmtree(self.installation_directory)

            print("Downloading zip.")
            os.system(f"cd {self.download_directory} && wget https://github.com/ChronoByte404/NLU-Application/archive/refs/heads/main.zip -O NLU-Application.zip")

            print("Extracting zip.")
            os.system(f"unzip -o {self.download_directory}/NLU-Application.zip -d ~/ && cd ~/ && mv -f ./NLU-Application-main ./.NLU-Application")

            print("Creating executable.")

            NLUAssistantInfo = ""

            print("Installing dependencies and configuring virtual environment.")
            self.install_dependencies()

            messagebox.showinfo("Installation Complete", "NLU Personal Assistant has been installed successfully!")
            self.create_desktop_entry()  # Call to create desktop entry
            sys.exit()
        except Exception as e:
            messagebox.showerror("Installation Failed", f"An error occurred during installation: {str(e)}")


class App:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("NLU Personal Assistant - Installer")
        width, height = 324, 228
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

    def create_widgets(self):
        # Entry widget for directory
        default_directory = '~/.NLU-Application'
        self.directory_entry = tk.Entry(self.root, bg="#ffffff", fg="#333333", justify="center")
        self.directory_entry.insert(tk.END, default_directory)
        self.directory_entry.place(x=30, y=90, width=260, height=30)

        # Entry widget for assistant name
        self.assistant_name_entry = tk.Entry(self.root, bg="#ffffff", fg="#333333", justify="center")
        self.assistant_name_entry.insert(tk.END, "NLU Assistant")
        self.assistant_name_entry.place(x=30, y=140, width=260, height=30)

        # Install button
        install_button = tk.Button(self.root, text="Install", command=self.install_action, bg="#01aaed", fg="#000000", justify="center")
        install_button.place(x=220, y=190, width=71, height=30)

        # Label
        label = tk.Label(self.root, text="Install your own NLU Personal Assistant", fg="#333333", justify="center")
        label.place(x=30, y=30, width=280, height=30)

    def install_action(self):
        directory = self.directory_entry.get()
        downloader = Downloader("~/Downloads", directory)
        downloader.download_and_extract()
        downloader.install_dependencies()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
