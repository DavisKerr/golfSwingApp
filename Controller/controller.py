from View.capture_screen import Capture_Screen
from View.analysis_screen import Analysis_Screen
from Model.process_video import Video_Processor
from Model.swing_divider import Swing_Divider
from Model.golferClass import Golfer
from Model.video_writer import Video_Writer
from Model.make_detections_using_model import MakeDetections
from Model.calculate_score import EvaluateSwing
from Model.feedback import GiveFeedback
import threading
import time
import logging


class Controller:
    """
    Controlls how the application runs. Moderates how the Model and View interact. 
    """


    def __init__(self, root):
        """
        Initializes the controller. The root is the tkinter GUI controller.
        Screen1 is the first screen to display to the user.
        """
        self.root = root
        self.screen1 = Capture_Screen(self.root, self.change_window)
        
    
    def analyze_video(self, filename):
        """
        Analyzes the video and creates a new window to display the feedback.
        """
        #Read in the video and analyze the swing for data points
        video_processor = Video_Processor("generatedVideos/" + filename + ".avi", True)
        video_processor.read_video("full_swing")

        # Load the points into the golfer class
        golfer = Golfer(video_processor.points_frames)
        # Load in a  new video processor to split the video into frames
        new_video_processor = Video_Processor("generatedVideos/toProcess.avi")
        frames = new_video_processor.slice_video()

        # Load in a video splitter and pass in the frames and the golfer points.
        video_splitter = Swing_Divider(golfer, frames)
        video_splitter.slice_video("user_videos")

        #csv_writer = CSV_Creator(golfer.get_golfer())
        #csv_writer.generate_csv("swing.csv")

        # Make machine learning detections
        swing_scorer = EvaluateSwing()
        score = swing_scorer.process_probabilities("user_videos")
        
        feedback_giver = GiveFeedback(score)

        feedback = (feedback_giver.get_setup(), feedback_giver.get_bswing(), feedback_giver.get_fswing())

        self.screen = Analysis_Screen(self.root, "generatedVideos/full_swing.avi", feedback)
        logging.info("Thread is closed")

    def change_window(self, frames, recording):
        """
        Opens a new window, if the app is not recording, with the analysis of the golf swing. It opens a new
        thread to process the video before opening the new window.
        """
        if not recording and frames:
            writer = Video_Writer(frames)
            filename = "toProcess"
            writer.write_video(filename)

            self.x = threading.Thread(target=self.analyze_video, args=(filename,))
            self.x.start()
            self.screen1.thread = self.x
            

            