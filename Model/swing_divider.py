import cv2 as cv

class Swing_Divider:
    """
    Divides the swing video into three parts: setup, forward swing, and backswing.
    """

    def __init__(self, golfer, frames):
        self.golfer = golfer
        self.frames = frames

    def split_video_for_setup(self, frames, golfer, start_frame=0):
        """
        Splits the video from the beginning of the swing to the time the right hand passes the 
        right hip.
        """
        for frame_number in range(start_frame, len(frames)):
            if golfer.get_point(7, frame_number) and golfer.get_point(14, frame_number):
                if golfer.get_point(7, frame_number)[0] < golfer.get_point(14, frame_number)[0]:
                    return frames[start_frame : frame_number], frame_number

    def split_video_for_backswing(self, frames, golfer, start_frame):
        """
        Splits the video from the time the right hand starts to go back down.
        """
        passed = False
        for frame_number in range(start_frame, len(frames)):
            if golfer.get_point(4, frame_number) and golfer.get_point(2, start_frame):
                hand_y = golfer.get_point(4, frame_number)[1]
                shoulder_y = golfer.get_point(2, start_frame)[1]
                if passed:
                    if hand_y >= shoulder_y + 10 or hand_y <= shoulder_y - 10:
                        return frames[start_frame : frame_number], frame_number 
                else:
                    if hand_y < shoulder_y:
                        passed = True


    def write_video(self, filename, frames, folder):
        """
        Saves a collections of frames as a new video.
        """
        full_path = folder + '/' + filename + '.avi'
        print(len(frames))
        out = cv.VideoWriter(full_path, cv.VideoWriter_fourcc(*'DIVX'), 15, ((frames[0].shape[1],frames[0].shape[0])))
        
        for frame in frames:
            out.write(frame)
        
        out.release()

        return full_path

    def slice_video(self, folder):
        """
        Slices the video into the three segments of the swing.
        """
        videos = {}

        setup, setup_frame_number = self.split_video_for_setup(self.frames, self.golfer)
        videos["setup"] = self.write_video("setup", setup, folder)

        backswing, backswing_frame_number = self.split_video_for_backswing(self.frames, self.golfer, setup_frame_number)
        videos["backward"] = self.write_video("backward", backswing, folder)

        videos["swing"] = self.write_video("forward", self.frames[backswing_frame_number + 1 :], folder)

        return videos

