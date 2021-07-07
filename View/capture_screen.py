from View.double_slider import *
import tkinter as tk
import PIL
from tkvideo import tkvideo
from tkinter import filedialog
from Model.video import Video

class Capture_Screen(tk.Toplevel):

    def __init__(self, master, new_window_func):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.new_window_func = new_window_func
        #self.filename="swing01_Trim.mp4"
        #self.vid = Video(self.filename)
        self.frames = []#self.vid.get_video()
        self.min_frame = 0
        self.max_frame = 0
        self.build_window()

        self.is_playing = False

        self.recording = False

        self.thread = None

        self.delay = 15
        self.update()

    
    def get_filename(self):
        """Open a filedialog for File."""
        return filedialog.askopenfilename()
    
    def load_video(self):
        self.filename = self.get_filename()
        if len(self.frames) > 0:
            self.vid.__del__()
        self.vid = Video(self.filename)
        self.frames = self.vid.get_video()
        self.curr_frame = 0
        self.min_frame = 0
        self.max_frame = len(self.frames) - 1
        self.video_slider.max_val = self.max_frame - 1
        self.play()

    def remove(self):
        self.window.destroy()
    
    def trim_video(self, values):
        if not self.recording:
            self.min_frame = min(values)
            self.max_frame = max(values)
            self.curr_frame = self.min_frame
 
    def pause(self):
        self.is_playing = False

    def record(self):
        print("Recording...")
        if not self.recording:
            self.recording = True
            try:
                self.vid = Video(0)
            except ValueError:
                print("Error Loading Video from source!")
                self.recording = False
    
    def stop_recording(self):
        print("Stop Recording...")
        if self.recording:
            self.recording = False
            self.vid.save_video("recording1")
        
    
    def update_video(self):
        if not self.curr_frame < self.min_frame and not self.curr_frame > self.max_frame:
            frame = self.frames[self.curr_frame]
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.video_display.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.curr_frame = self.curr_frame +  1
        else:
            self.curr_frame = self.min_frame

        

    def update_recording(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.video_display.create_image(0, 0, image = self.photo, anchor = tk.NW)

    def play(self):
        if len(self.frames) > 0:
            self.is_playing = True

    def update(self):
        # Get a frame from the video source
        #ret, frame = self.vid.get_frame()
        if self.recording:
            self.update_recording()
        elif self.is_playing: 
            self.update_video()
        
        if self.thread and self.thread.is_alive():
                self.submit_btn['state'] = tk.DISABLED
        else:
            self.submit_btn['state'] = tk.NORMAL
        
 
        self.after(self.delay, self.update)    

    def build_window(self):
        self.title = Label(self, text="Record and trim golf stroke video")
        
        self.video_display = tk.Canvas(self, width = 400, height = 400)
 
        self.play_btn = Button(self, text="Play", command=self.play)
        self.pause_btn = Button(self, text="Pause", command=self.pause)
        self.record_btn = Button(self, text="Record", command=self.record)
        self.stop_btn = Button(self, text="Stop", command=self.stop_recording)
        self.video_slider = Double_Slider(self, self.trim_video, max_val=len(self.frames) - 1)
        self.submit_btn = Button(self, text="Submit Selection", command=(lambda : self.new_window_func(self.frames[self.min_frame:self.max_frame + 1], self.recording)))
        self.btnFile = Button(self, text="File", command=self.load_video)

        self.btnFile.grid(row=0, column=1)
        self.title.grid(row=2, column=3)
        self.video_display.grid(row=3, column=1, rowspan=3, columnspan=5)
        self.play_btn.grid(row=7, column=1)
        self.pause_btn.grid(row=7, column=2)
        self.record_btn.grid(row=7, column=3)
        self.stop_btn.grid(row=7, column=4)
        self.video_slider.grid(row=8, column=1, columnspan=5)
        self.submit_btn.grid(row=9, column=3)

