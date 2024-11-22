import cv2
import mediapipe as mp
import os
import numpy as np

# Đường dẫn tới thư mục chứa ảnh
folder_path = "C:/Users/yuetl/.cache/kagglehub/datasets/ashwingupta3012/human-faces/versions/1/Humans"  # Thay đổi đường dẫn tới thư mục ảnh
output_size = (640, 480)  # Kích thước của cửa sổ hiển thị
face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

# Khởi tạo các biến để thống kê kết quả
total_images = 0
detected_images = 0
max_images = 200  # Số lượng ảnh tối đa để xử lý
undetected_images = []  # Danh sách để lưu tên các ảnh không xác định

# Duyệt qua tất cả các file ảnh trong thư mục
for idx, image_file in enumerate(os.listdir(folder_path)):
    if total_images >= max_images:  # Kiểm tra giới hạn 200 ảnh
        break
    
    image_path = os.path.join(folder_path, image_file)
    
    # Đọc ảnh
    image = cv2.imread(image_path)
    if image is None:
        # Nếu không thể đọc ảnh, thêm tên file vào danh sách và bỏ qua ảnh này
        undetected_images.append(image_file)
        continue
    
    # Tăng số lượng ảnh đã kiểm tra
    total_images += 1
    
    # Chuyển ảnh sang RGB vì MediaPipe yêu cầu định dạng này
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Phát hiện các điểm landmark trên khuôn mặt
    output = face_mesh.process(rgb_image)
    landmark_point = output.multi_face_landmarks
    
    # Kiểm tra nếu tìm thấy các landmark
    if landmark_point:
        detected_images += 1
        landmarks = landmark_point[0].landmark
        for landmark in landmarks:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
    else:
        # Nếu không phát hiện được landmark, thêm tên file vào danh sách và bỏ qua ảnh này
        undetected_images.append(image_file)
    
    # Tính tỷ lệ phát hiện
    detection_rate = (detected_images / total_images) * 100 if total_images > 0 else 0
    
    # Tạo khung nhỏ để hiển thị chữ
    text_frame_height = 120  # Chiều cao của frame chữ
    text_frame = np.zeros((text_frame_height, output_size[0], 3), dtype=np.uint8)  # Tạo ảnh đen để làm nền cho chữ
    
    # Vẽ văn bản lên khung chữ
    cv2.putText(text_frame, f'Total images checked: {total_images}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(text_frame, f'Images with detected landmarks: {detected_images}', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(text_frame, f'Detection rate: {detection_rate:.2f}%', (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Hiển thị ảnh với điểm landmark
    resized_image = cv2.resize(image, output_size)
    
    # Nối ảnh gốc và frame chữ lại với nhau
    combined_image = np.vstack((resized_image, text_frame))  # Nối theo chiều dọc
    
    # Hiển thị ảnh kết hợp
    cv2.imshow('Face Landmarks with Statistics', combined_image)
    cv2.waitKey(500)

# Ghi các tên file không xác định vào file .txt
if undetected_images:
    with open('not_detected/undetected_images.txt', 'w') as file:
        for img_name in undetected_images:
            file.write(f'{img_name}\n')

# Giải phóng tài nguyên
face_mesh.close()
cv2.destroyAllWindows()
