import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import pickle
import pandas as pd
import numpy as np
import os

DISPLAY_DETECTIONS = False
VIDEO_FORMAT = ".mp4"
SETUP_PKL_MODEL = "Pickle/setup.pkl"
FORWARD_PKL_MODEL = "Pickle/forward.pkl"
BACKWARD_PKL_MODEL = "Pickle/back.pkl"

class MakeDetections:

    def __init__(self, videos_folder):
        """" Initialize the MakeDetections class.
        Params: videos_folder (directory of the folder with the videos to analyze)
        """
        # This list will contain tuples for each detection made each frame.
        # Tuple contains: (body_language_class, number representing how accurate the movement was)
        self.detections = list() 

        self.videos_list = list() # Create a list to store the directory of each video in the folder you pass in     

        self.create_list_of_files(videos_folder)
        print(self.videos_list)
        # Use the correct pkl model for the correct video, for example:
        # Use the setup pkl model to analyse the setup part of the user video.
        # Otherwise it will display a warning message.
        for video in self.videos_list:
            if "setup" in video:
                self.make_detections(video, SETUP_PKL_MODEL)
            elif "forward" in video:
                self.make_detections(video, FORWARD_PKL_MODEL)
            elif "backward" in video:
                self.make_detections(video, BACKWARD_PKL_MODEL)
            else:
                print("Sorry, you need to rename your videos")

    def create_list_of_files(self, videos_folder):
        """ Ensure that the items inside 'videos_folder' are videos with the correct 'VIDEO_FORMAT'
        Params: videos_folder (directory of the folder with the videos to analyze)
        """

        for filename in os.listdir(videos_folder):
            if filename.endswith('.avi'):  #VIDEO_FORMAT
                self.videos_list.append(f"{videos_folder}/{filename}")
            else:
                pass
        
    def make_detections(self, video, pkl_model):
        """ Analize a video using a pkl model and write each detection in a list called 'detections'
        If DISPLAY_DETECTIONS is set as 'True' the actual video will be presented using Mediapipe and OpenCV
        showing the detections in the screen as well.
        
        Params: video (directory of one video to analyze)
        pkl_model (A machine Learning Model built using Scikitlearn)
        """

        mp_drawing = mp.solutions.drawing_utils # Drawing helpers
        mp_holistic = mp.solutions.holistic # Mediapipe Solutions

        # Use the adecuate machine learning model to analyse the video
        with open(pkl_model, 'rb') as f:
            model = pickle.load(f)

            cap = cv2.VideoCapture(video)

            # Initiate holistic model
            with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                
                while cap.isOpened():
                    ret, frame = cap.read()

                    if ret == True:
                    
                        # Recolor Feed
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False        
                        
                        # Make Detections
                        results = holistic.process(image)
                                    
                        # Recolor image back to BGR for rendering
                        image.flags.writeable = True   
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                                )
                        
                        try:
                            # Extract Pose landmarks
                            pose = results.pose_landmarks.landmark
                            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                            

                            # Make Detections
                            X = pd.DataFrame([pose_row])
                            body_language_class = model.predict(X)[0]
                            body_language_prob = model.predict_proba(X)[0]

                            # Create a tuple containing 1) the name of the category "poor, medium or good" 
                            # and 2) the score of how accurate is the prediction between 0 and 1
                            tup = (body_language_class, round(body_language_prob[np.argmax(body_language_prob)],2))
                            
                            # Append the tuple to the detections list
                            self.detections.append(tup)

                            if DISPLAY_DETECTIONS == True:
                                # Grab ear coords
                                coords = tuple(np.multiply(
                                                np.array(
                                                    (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x, 
                                                    results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
                                            , [640,480]).astype(int))
                                
                                cv2.rectangle(image, 
                                            (coords[0], coords[1]+5), 
                                            (coords[0]+len(body_language_class)*20, coords[1]-30), 
                                            (245, 117, 16), -1)
                                cv2.putText(image, body_language_class, coords, 
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                                
                                # Get status box
                                cv2.rectangle(image, (0,0), (250, 60), (245, 117, 16), -1)
                                
                                # Display Class
                                cv2.putText(image, 'CLASS'
                                            , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                                cv2.putText(image, body_language_class.split(' ')[0]
                                            , (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                                
                                # Display Probability
                                cv2.putText(image, 'PROB'
                                            , (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                                cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)],2))
                                            , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                            
                        except:
                            pass

                        if DISPLAY_DETECTIONS == True:                
                            cv2.imshow('Making Detections', image)

                            # Press "q" to quit
                            if cv2.waitKey(10) & 0xFF == ord('q'):
                                break
                    else:
                        break 

                cap.release()
                cv2.destroyAllWindows()

#test = MakeDetections('videos/test')
#print(test.detections)
