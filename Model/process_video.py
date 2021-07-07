import cv2 as cv
import numpy as np
import time

class Video_Processor:

    def __init__(self, video_source, net=False):
        self.nPoints = 15
        self.POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13]]
        self.inWidth = 368
        self.inHeight = 368
        self.threshold = 0.1
        self.video_source = video_source
        self.points_frames = []
        if net:
            self.net = self.create_net()

    def create_net(self):
        protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
        weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
        net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)
        #net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
        #print("Using CPU device")
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        print("Using GPU device")
        return net

    def load_video(self):
        return cv.VideoCapture(self.video_source)

    def create_writer(self, destination, frame):
        return cv.VideoWriter(destination ,cv.VideoWriter_fourcc('M','J','P','G'), 10, (frame.shape[1],frame.shape[0]))

    def read_video(self, filename):
        cap = self.load_video()
        hasFrame, frame = cap.read()
        vid_writer = self.create_writer("generatedVideos/" + filename + ".avi", frame)
        while cv.waitKey(0) < 0:
            t = time.time()
            hasFrame, frame = cap.read()
            frameCopy = np.copy(frame)
            if not hasFrame:
                cv.waitKey()
                break

            frameWidth = frame.shape[1]
            frameHeight = frame.shape[0]
            inpBlob = cv.dnn.blobFromImage(frame, 1.0 / 255, (self.inWidth, self.inHeight),
                                (0, 0, 0), swapRB=False, crop=False)
            self.net.setInput(inpBlob)
            output = self.net.forward()

            H = output.shape[2]
            W = output.shape[3]
            points, frameCopy = self.get_points(output, frameWidth, frameHeight, W, H, frameCopy)
            self.points_frames.append(points)
            frame = self.draw_skeleton(points, frame, t)
            cv.putText(frame, "time taken = {:.2f} sec".format(time.time() - t), (50, 50), cv.FONT_HERSHEY_COMPLEX, .8, (255, 50, 0), 2, lineType=cv.LINE_AA)

            vid_writer.write(frame)

        vid_writer.release()

    def get_points(self, output, frameWidth, frameHeight, W, H, frameCopy):
        points = []
        for i in range(self.nPoints):
            probMap = output[0, i, :, :]

            minVal, prob, minLoc, point = cv.minMaxLoc(probMap)

            x = (frameWidth * point[0]) / W
            y = (frameHeight * point[1]) / H

            if prob > self.threshold : 
                cv.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv.FILLED)
                cv.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv.LINE_AA)

                points.append((int(x), int(y)))
            else :
                points.append(None)

        return points, frameCopy


    def draw_skeleton(self, points, frame, t):
        for pair in self.POSE_PAIRS:
            partA = pair[0]
            partB = pair[1]

            if points[partA] and points[partB]:
                cv.line(frame, points[partA], points[partB], (0, 255, 255), 3, lineType=cv.LINE_AA)
                cv.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv.FILLED)
                cv.circle(frame, points[partB], 8, (0, 0, 255), thickness=-1, lineType=cv.FILLED)

        return frame
    
    def slice_video(self):
        cap = self.load_video()
        success, frame = cap.read()
        frames = []
        while success:
            frames.append(frame)
            success, frame = cap.read()
        return frames
            
            
