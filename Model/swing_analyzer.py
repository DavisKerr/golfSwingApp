import cv2 as cv

class Swing_Analyzer:

    def __init__(self, golfer, frames):
        self.golfer = golfer
        self.frames = frames

    def split_video_for_setup(self, frames, golfer, start_frame=0):
        for frame_number in range(start_frame, len(frames)):
            if golfer.get_point(4, frame_number) and golfer.get_point(1, frame_number):
                if golfer.get_point(4, frame_number)[1] < golfer.get_point(14, frame_number)[1] - 10:
                    return frames[start_frame : frame_number], frame_number

    def split_video_for_backswing(self, frames, golfer, start_frame):
        prev_y = golfer.get_point(4, start_frame)[1]
        for frame_number in range(start_frame, len(frames)):
            if golfer.get_point(4, frame_number):
                print(golfer.get_point(4, frame_number)[1])
                if golfer.get_point(4, frame_number)[1] > prev_y + 20:
                    return frames[start_frame : frame_number], frame_number
                else:
                    prev_y = golfer.get_point(4, frame_number)[1]

    def write_video(self, filename, frames):
        full_path = 'generatedVideos/' + filename + '.avi'
        out = cv.VideoWriter(full_path, cv.VideoWriter_fourcc(*'DIVX'), 15, ((frames[0].shape[1],frames[0].shape[0])))
        
        for frame in frames:
            out.write(frame)
        
        out.release()

        return full_path

    def slice_video(self):
        videos = {}

        setup, setup_frame_number = self.split_video_for_setup(self.frames, self.golfer)
        videos["Setup"] = self.write_video("setup", setup)

        backswing, backswing_frame_number = self.split_video_for_backswing(self.frames, self.golfer, setup_frame_number + 1)
        videos["Backswing"] = self.write_video("setup", backswing)

        videos["Swing"] = self.write_video("swing", self.frames[backswing_frame_number + 1 :])

        return videos

