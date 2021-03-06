import cv2 as cv

class Video_Writer:
    """
    Writes a video to a file.
    """
    def __init__(self, frames):
        self.frames = frames
    
    def write_video(self, filename):
        """
        Writes a video to the specified filename using the given frames.
        """
        out = cv.VideoWriter('generatedVideos/' + filename + '.avi', cv.VideoWriter_fourcc(*'DIVX'), 15, ((self.frames[0].shape[1], self.frames[0].shape[0]))) 
        for frame in self.frames:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            out.write(frame)