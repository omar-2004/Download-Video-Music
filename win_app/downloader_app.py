import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from pytube import YouTube
from moviepy.editor import AudioFileClip
import CTkMessagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Downloader")
        # self.geometry("800x500")
        self.resizable(False, False)
        self.update()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # =================== Stingvar ===================
        self.URL = tk.StringVar()
        self.videoMode = tk.StringVar()
        self.folder_path = tk.StringVar()
        # ==============   Default values   ==============
        self.folder_path.set(os.path.join(
            os.path.expanduser("~"), "Downloads", "YTconvertor"))
        # =================== Frames =====================
        self.create_widgets()

    def on_closing(self):

        # get yes/no answers
        msg = CTkMessagebox.CTkMessagebox(title="Exit?", message="Do you want to close the program?",
                                          icon="question", option_2="Yes", option_1="No")
        response = msg.get()

        if response == "Yes":
            self.destroy()

    def DownloadContent(self):
        if self.URL.get() == "" or "https://" not in self.URL.get():
            tk.messagebox.showinfo(
                "Error", "Please enter a valid URL !")
            return

        if self.videoMode.get() == "":
            tk.messagebox.showinfo(
                "Error", "Please select a mode !")
            return

        if os.path.join(
                os.path.expanduser("~"), "Downloads", "YTconvertor") in self.folder_path.get():

            if self.videoMode.get() == "Video (MP4)":
                self.folder_path.set(os.path.join(
                    os.path.expanduser("~"), "Downloads", "YTconvertor", "Videos"))
            else:
                self.folder_path.set(os.path.join(
                    os.path.expanduser("~"), "Downloads", "YTconvertor", "Audios"))

            if not os.path.exists(self.folder_path.get()):
                os.makedirs(self.folder_path.get())

        self.Dwonloadbtn.configure(state="disabled")
        Download(self.URL.get(),  self.videoMode.get(),
                 self.folder_path.get(), self.progressBar, self, self.percentageLabel)
        self.Dwonloadbtn.configure(state="normal")

    def create_widgets(self):
        self.logo = ctk.CTkImage(light_image=Image.open(
            "./resources/logo.png"), size=(100, 100))

        ctk.CTkLabel(self, image=self.logo, text="").grid(
            row=0, column=0, columnspan=2, padx=20, pady=20)

        ctk.CTkLabel(self, text="Video URL :", justify="center", width=100).grid(
            row=1, column=0,  padx=20, pady=20)

        ctk.CTkEntry(self, textvariable=self.URL, placeholder_text="URL ...",
                     width=300).grid(
            row=1, column=1, padx=20, pady=20)

        ctk.CTkLabel(self, text="Video URL :", justify="center", width=100).grid(
            row=2, column=0,  padx=20, pady=20)

        ctk.CTkSegmentedButton(self, values=["Video (MP4)", "Audio (MP3)"],
                               command=lambda x: self.videoMode.set(x)).grid(
            row=2, column=1, padx=20, pady=20)

        ctk.CTkLabel(self, text="Save to :", justify="center", width=100).grid(
            row=3, column=0, padx=20, pady=20)

        self.folder_entry = ctk.CTkEntry(
            self, width=300, textvariable=self.folder_path, state="readonly")
        self.folder_entry.grid(row=3, column=1, padx=90, pady=20)

        ctk.CTkButton(
            self, text="Select Folder", width=50, command=lambda: self.folder_path.set(ctk.filedialog.askdirectory())).grid(row=3, column=1, pady=20, sticky="w")

        self.percentageLabel = ctk.CTkLabel(self, text="0%")
        self.percentageLabel.grid(
            row=4, column=0, columnspan=2, padx=40, pady=20, sticky="n")

        self.progressBar = ctk.CTkProgressBar(
            self, orientation="horizontal")
        self.progressBar.set(0)
        self.progressBar.grid(row=4, column=0, columnspan=2,
                              padx=150, pady=20, sticky="ews")

        self.Dwonloadbtn = ctk.CTkButton(
            self, text="Download", command=self.DownloadContent)
        self.Dwonloadbtn.grid(
            row=5, column=0, columnspan=2, padx=120, pady=20, ipadx=15, ipady=15, sticky="ew")


class Download:
    def __init__(self, URL, mode, folder_path, progressBar, app, percentage):
        self.URL = URL
        self.folder_path = folder_path
        self.progressBar = progressBar
        self.app = app
        self.mode = mode
        self.percentageLabel = percentage
        self.__Download__()

    def __Download__(self):
        try:
            video = YouTube(self.URL, on_progress_callback=self.on_progress)
            if self.mode == "Video (MP4)":
                try:
                    video_streams = [
                        stream for stream in video.streams if stream.mime_type.startswith('video')]
                    # Sort video streams by resolution in descending order
                    sorted_video_streams = sorted(
                        video_streams, key=lambda x: int(x.resolution[:-1]), reverse=True)
                    # Get the stream with the highest resolution
                    highest_quality_stream = sorted_video_streams[0]
                    # Download the video to the specified output folder
                    highest_quality_stream.download(self.folder_path)
                    # tk.messagebox.showinfo(
                    # "Success", "Video downloaded successfully !")
                    self.msg = CTkMessagebox.CTkMessagebox(
                        message="Video downloaded successfully !", icon="check", option_1="Done", option_2="Open Folder")
                    self.__open__folder__(self.msg.get(), self.folder_path)
                except Exception as e:
                    CTkMessagebox.CTkMessagebox(
                        title="Error", message=f"An error occurred: {e}", icon="cancel")
            else:
                try:
                    audio_stream = video.streams.filter(
                        only_audio=True).first()

                    audio_stream.download(self.folder_path)

                    # # Get the audio file path
                    # audio_path = os.path.join(
                    #     self.folder_path, f"{self.__clean__str__(video.title)}.{audio_stream.subtype}")

                    # # Convert the downloaded audio to MP3
                    # audio_clip = AudioFileClip(audio_path)
                    # audio_clip.write_audiofile(os.path.join(
                    #     self.folder_path, f"{self.__clean__str__(video.title)}.mp3"))

                    # # Remove the downloaded audio file
                    # audio_clip.close()
                    # os.remove(audio_path)
                    self.msg = CTkMessagebox.CTkMessagebox(
                        message="Audio downloaded successfully !", icon="check", option_1="Done", option_2="Open Folder")
                    self.__open__folder__(self.msg.get(), self.folder_path)

                except Exception as e:
                    CTkMessagebox.CTkMessagebox(
                        title="Error", message=f"An error occurred: {e}", icon="cancel")

        except Exception as e:
            CTkMessagebox.CTkMessagebox(
                title="Error", message=f"An error occurred: {e}", icon="cancel")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.percentageLabel.configure(text=f"{percentage:.2f}%")
        self.progressBar.set(percentage / 100)
        self.app.update()

    def __open__folder__(self, resp, path):
        os.startfile(path) if resp == "Open Folder" else None

    def __clean__str__(self, string):
        return string.replace("\\", "").replace("/", "")


if __name__ == '__main__':
    App().mainloop()
