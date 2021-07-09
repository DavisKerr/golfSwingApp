import cv2 as cv
from Model.video_writer import Video_Writer

class Video:
    def __init__(self, video_source, dim=(400,400)):
        # Open the video source
        self.vid = cv.VideoCapture(video_source)
    
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
    
        # Get video source width and height
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.video_source = video_source
        self.dim = dim
        
        self.recorded_video = []
    
    def rescaleFrame(self, frame, scale=0.75):
        width = (int)(frame.shape[1] * scale)
        height = (int)(frame.shape[0] * scale)

        dimensions = (width, height)

        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    
    def get_frame(self):
        if self.vid.isOpened() and self.video_source == 0:
            ret, frame = self.vid.read()
            if ret:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                self.recorded_video.append(frame)
                frame = cv.resize(frame, self.dim, interpolation = cv.INTER_AREA)
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)
    
    def save_video(self, filename):
        writer = Video_Writer(self.recorded_video)
        writer.write_video(filename)

    def load_video(self):
        return cv.VideoCapture(self.video_source)

    def get_video(self):
        frames = self.prepare_video()
        for i in range(len(frames)):
            frames[i] = cv.resize(frames[i], self.dim, interpolation = cv.INTER_AREA)
            frames[i] = cv.cvtColor(frames[i], cv.COLOR_BGR2RGB)
        return frames

    def prepare_video(self):
        cap = self.load_video()
        success, frame = cap.read()
        frames = []
        while success:
            frames.append(frame)
            success, frame = cap.read()
        return frames
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()