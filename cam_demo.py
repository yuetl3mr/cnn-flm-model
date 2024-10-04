import cv2 
import mediapipe as mp

face_mesh = mp.solutions.face_mesh.FaceMesh()
cam = cv2.VideoCapture(0)
while True:
    _, frame = cam.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    output = face_mesh.process(rgb_frame)
    landmark_point = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    if landmark_point:
        landmarks = landmark_point[0].landmark
        for landmark in landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
    
    print(landmark_point)
    cv2.imshow('Face', frame)
    cv2.waitKey(1)