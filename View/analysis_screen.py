from tkinter.constants import END
from View.double_slider import Double_Slider
import tkinter as tk
import PIL
from tkvideo import tkvideo
from tkinter import filedialog
from Model.video import Video

class Analysis_Screen(tk.Toplevel):
    """
    The GUI for the analysis screen.
    """
    def __init__(self, master, filename, feedback, thread=None):
        tk.Toplevel.__init__(self, master)
        self.filename = filename
        self.title("Golf Analyzer")
        self.iconbitmap("Images/Golf.ico")
        self.feedback = feedback


        self.vid = Video(self.filename)
        self.frames = self.vid.get_video()
        self.curr_frame = 0
        self.min_frame = 0
        self.max_frame = len(self.frames) - 1
        self.is_playing = True

        self.build_window()

        self.delay = 15
        self.update()

    def pause(self):
        """
        Sets the video playback to false.
        """
        self.is_playing = False
    
    def play(self):
        """
        Sets the video playback to true.
        """
        if len(self.frames) > 0:
            self.is_playing = True

    def update_video(self):
        """
        Progresses the video by 1 frame. Runs every time the GUI updates.
        """
        if not self.curr_frame < self.min_frame and not self.curr_frame > self.max_frame:
            frame = self.frames[self.curr_frame]
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.video_display.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.curr_frame = self.curr_frame +  1
        else:
            self.curr_frame = self.min_frame

        self.video_slider.advance_slider(self.curr_frame)

    def update(self):
        """
        Updates the GUI every frame.
        """
        if self.is_playing:
            self.update_video()

        self.after(self.delay, self.update)

    def load_video(self):
        """
        Loads a video.
        """
        self.filename = self.get_filename()
        self.vid.__del__()
        self.vid = Video(self.filename)
        self.frames = self.vid.get_video()
        self.curr_frame = 0
    
    def change_frame(self, frame_numbers):
        """
        Restarts the video.
        """
        self.curr_frame = frame_numbers[0]

    def build_window(self):
        """
        Build and layout the window.
        """
        self.title = tk.Label(self, text="Whole Swing")
        
        self.video_display = tk.Canvas(self, width = 400, height = 400)
 
        self.play_btn = tk.Button(self, text="Play", command=self.play)
        self.pause_btn = tk.Button(self, text="Pause", command=self.pause)
        self.video_slider = Double_Slider(self, self.change_frame, num_bars=1, max_val=self.max_frame)
        self.advice_label = tk.Label(self, text="Analysis:")
        self.advice_list = tk.Listbox(self, height=6, width=60)

        counter = 1
        for advice in self.feedback:
            sentence = advice.split()
            line = ''
            for end, word in enumerate(sentence):
                
                if len(line) > 50 or end + 1 == len(sentence):
                    line = line + " " + word
                    print(line)
                    self.advice_list.insert('end', line)
                    line = ""
                    counter += 1
                else:
                    line = line + " " + word


            
        #self.advice_list.insert(4, "Your overall golf swing was rated as a grade B.")

        self.title.grid(row=1, column=3)
        self.video_display.grid(row=2, column=2, rowspan=3, columnspan=5)
        self.play_btn.grid(row=7, column=2)
        self.pause_btn.grid(row=7, column=3)
        self.video_slider.grid(row=8, column=1, columnspan=5)
        self.advice_label.grid(row=9, column=3)
        self.advice_list.grid(row=10, column=1, rowspan=3, columnspan=5)

