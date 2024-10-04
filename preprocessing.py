# extract_landmarks.py

import cv2
import mediapipe as mp
import numpy as np
import os

mp_face_mesh = mp.solutions.face_mesh

def get_landmarks(image_path):
    image = cv2.imread(image_path)
    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    if results.multi_face_landmarks:
        landmarks = []
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                landmarks.append([landmark.x, landmark.y])
        return np.array(landmarks).flatten()  # Flatten to 1D array
    return None  

def process_images(input_folder, output_file):
    images = []
    landmarks = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)
            landmark = get_landmarks(image_path)
            if landmark is not None:
                images.append(image_path)
                landmarks.append(landmark)

    np.savez(output_file, images=images, landmarks=landmarks)

if __name__ == "__main__":
    input_folder = "./data"  
    output_file = "landmarks.npz"         
    process_images(input_folder, output_file)
