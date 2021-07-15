'''
Code originally found at https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
'''

import cv2 as cv
import mediapipe as mp

class Video_Capture:
    """
    Captures a video using OpenCV for the use of returning each frame. 
    """
    def __init__(self, video_source=0, dim=(400,400)):
        # Open the video source
        self.vid = cv.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
   
        # Get video source width and height
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.video_source = video_source
        self.dim = dim

    def rescaleFrame(self, frame, scale=0.75):
        """
        Rescales a frame. 
        """
        width = (int)(frame.shape[1] * scale)
        height = (int)(frame.shape[0] * scale)

        dimensions = (width, height)

        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def load_video(self):
        """
        Loads the video from the source into OpenCV.
        """
        return cv.VideoCapture(self.video_source)

    def get_frames(self):
        """
        Gets a list of frames from the video.
        """
        cap = self.load_video()
        success, frame = cap.read()
        frames = []
        while success:
            frames.append(frame)
            success, frame = cap.read()
        return frames

    def get_frame(self):
        """
        Gets a frame from the source.
        """
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = cv.resize(frame, self.dim, interpolation = cv.INTER_AREA)
            #frame = self.rescaleFrame(frame, self.scale)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        """
        releases the video if deleted.
        """
        if self.vid.isOpened():
            self.vid.release() 