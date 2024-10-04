import numpy as np 
import pandas as pd
import cv2 
import mediapipe as mp
import os

face_mesh = mp.solutions.face_mesh.FaceMesh()

data = np.load('face_images.npz')
images = np.moveaxis(data['face_images'], -1, 0)  

keypoints_df = pd.read_csv('facial_keypoints.csv')
keypoints_df.fillna(method='ffill', inplace=True) 

results = []

output_directory = 'not_detected'
os.makedirs(output_directory, exist_ok=True)

for idx, image in enumerate(images):
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)
    if image.ndim == 2:  
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_point = output.multi_face_landmarks

    if landmark_point:
        landmarks = landmark_point[0].landmark
        detected_points = []
        
        for landmark in landmarks:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            detected_points.append((x, y))  
        if idx < len(keypoints_df):
            ground_truth = keypoints_df.iloc[idx].values
            detected_array = np.array(detected_points).flatten()

            num_points = min(len(ground_truth), len(detected_array))
            detected_array = detected_array[:num_points]
            ground_truth_array = ground_truth[:num_points]

            accuracy = np.mean(np.isclose(detected_array, ground_truth_array, atol=60))
            results.append({'image_index': idx, 'detected': True, 'accuracy': accuracy})
        else:
            results.append({'image_index': idx, 'detected': True, 'accuracy': None})
    else:
        results.append({'image_index': idx, 'detected': False, 'accuracy': None})
        cv2.imwrite(os.path.join(output_directory, f'image_{idx}.png'), image)

# Chuyển kết quả vào DataFrame
results_df = pd.DataFrame(results)

# Tính toán thống kê
total_images = len(results_df)
detected_images = results_df['detected'].sum()
not_detected_images = total_images - detected_images
# average_accuracy = results_df['accuracy'].mean()

# In ra kết quả
print(f'Total images: {total_images}')
print(f'Detected images: {detected_images}')
print(f'Not detected images: {not_detected_images}')
print(f'Average accuracy: {(100 - total_images/detected_images)}%')

# Lưu kết quả vào file CSV
results_df.to_csv('face_detection_results.csv', index=False)
