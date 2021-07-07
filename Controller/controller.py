from View.capture_screen import Capture_Screen
from View.analysis_screen import Analysis_Screen
from Model.process_video import Video_Processor
from Model.swing_analyzer import Swing_Analyzer
from Model.golferClass import Golfer
from Model.video_writer import Video_Writer
import threading
import time
import logging


class Controller:

    def __init__(self, root):
        self.root = root
        self.screen1 = Capture_Screen(self.root, self.change_window)
        
    
    def analyze_video(self, filename):
        video_processor = Video_Processor("generatedVideos/" + filename + ".avi", True)
        video_processor.read_video("full_swing")
        self.screen = Analysis_Screen(self.root, "generatedVideos/full_swing.avi")
        logging.info("Thread is closed")

    def change_window(self, frames, recording):
        if not recording and frames:
            writer = Video_Writer(frames)
            filename = "toProcess"
            writer.write_video(filename)

            self.x = threading.Thread(target=self.analyze_video, args=(filename,))
            self.x.start()
            self.screen1.thread = self.x
            

            