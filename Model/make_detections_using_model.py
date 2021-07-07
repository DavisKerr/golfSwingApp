"""
Erick comments:
Change the (pkl) file in line 12
"""

import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import pickle
import numpy as np
import pandas as pd

class swing_analyzer():

    def __init__(self, model_name, video_name):
        self.model_name = model_name
        self.video_name = video_name
        self.quality_class = []
        self.prob = []
        
    def analyze_video(self):
        self.cap = cv2.VideoCapture("generatedVideos/" + self.video_name + ".avi")
        mp_drawing = mp.solutions.drawing_utils # Drawing helpers
        mp_holistic = mp.solutions.holistic # Mediapipe Solutions

        with open('body_language.pkl', 'rb') as f:
            model = pickle.load(f)

            # Initiate holistic model
            with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                
                while cv2.waitKey(0) < 0:
                    ret, frame = self.cap.read()
                    
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

                        self.quality_class.append(body_language_class)
                        self.prob.append(body_language_prob)

                        print(body_language_class, body_language_prob)
                        
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
                                    
                    #cv2.imshow('Raw Webcam Feed', image)

                    if cv2.waitKey(10):
                        break
        self.cap.release()










# mp_drawing = mp.solutions.drawing_utils # Drawing helpers
# mp_holistic = mp.solutions.holistic # Mediapipe Solutions

# with open('body_language.pkl', 'rb') as f:
#     model = pickle.load(f)

#     #cap = cv2.VideoCapture(0)
#     # Initiate holistic model
#     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        
#         while cap.isOpened():
#             ret, frame = cap.read()
            
#             # Recolor Feed
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False        
            
#             # Make Detections
#             results = holistic.process(image)
                        
#             # Recolor image back to BGR for rendering
#             image.flags.writeable = True   
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
#             mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
#                                     mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
#                                     mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
#                                     )
            
#             try:
#                 # Extract Pose landmarks
#                 pose = results.pose_landmarks.landmark
#                 pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                

#                 # Make Detections
#                 X = pd.DataFrame([pose_row])
#                 body_language_class = model.predict(X)[0]
#                 body_language_prob = model.predict_proba(X)[0]
#                 print(body_language_class, body_language_prob)
                
#                 # Grab ear coords
#                 coords = tuple(np.multiply(
#                                 np.array(
#                                     (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x, 
#                                     results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
#                             , [640,480]).astype(int))
                
#                 cv2.rectangle(image, 
#                             (coords[0], coords[1]+5), 
#                             (coords[0]+len(body_language_class)*20, coords[1]-30), 
#                             (245, 117, 16), -1)
#                 cv2.putText(image, body_language_class, coords, 
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
#                 # Get status box
#                 cv2.rectangle(image, (0,0), (250, 60), (245, 117, 16), -1)
                
#                 # Display Class
#                 cv2.putText(image, 'CLASS'
#                             , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#                 cv2.putText(image, body_language_class.split(' ')[0]
#                             , (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
#                 # Display Probability
#                 cv2.putText(image, 'PROB'
#                             , (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#                 cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)],2))
#                             , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
#             except:
#                 pass
                            
#             cv2.imshow('Raw Webcam Feed', image)

#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()