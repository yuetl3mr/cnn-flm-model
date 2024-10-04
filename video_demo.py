import cv2 
import mediapipe as mp
import pandas as pd

face_mesh = mp.solutions.face_mesh.FaceMesh()

video_path = 'demo.mp4' 
cap = cv2.VideoCapture(video_path)

results = []

frame_width = 640
frame_height = 480

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_point = output.multi_face_landmarks

    if landmark_point:
        landmarks = landmark_point[0].landmark
        for landmark in landmarks:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
        
        results.append({'frame': cap.get(cv2.CAP_PROP_POS_FRAMES), 'detected': True})
    else:
        results.append({'frame': cap.get(cv2.CAP_PROP_POS_FRAMES), 'detected': False})

    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

results_df = pd.DataFrame(results)

total_frames = len(results_df)
detected_frames = results_df['detected'].sum()
not_detected_frames = total_frames - detected_frames

print(f'Total frames: {total_frames}')
print(f'Detected frames: {detected_frames}')
print(f'Not detected frames: {not_detected_frames}')

results_df.to_csv('face_detection_results2.csv', index=False)
