class Golfer:

    def __init__(self, points_frames):
        self.body = dict({})
        self.body[0] = [] # Top of Head
        self.body[1] = [] # Bottom of Head
        self.body[2] = [] # Right Shoulder
        self.body[3] = [] # Right Elbow
        self.body[4] = [] # Right Hand
        self.body[5] = [] # Left Shoulder
        self.body[6] = [] # Left Elbow
        self.body[7] = [] # Left Hand
        self.body[8] = [] # Right Hip
        self.body[9] = [] # Right Knee
        self.body[10] = [] # Right Foot
        self.body[11] = [] # Left Hip
        self.body[12] = [] # Left Knee
        self.body[13] = [] # Left Foot
        self.body[14] = [] # Lower Chest
        for frame in points_frames:
            for point in range(0, 15):
                self.body[point].append(frame[point])

    def get_point(self, point, frame):
        return self.body[point][frame]
    
    def get_golfer(self):
        return self.body
