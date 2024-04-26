import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import os
from natsort import natsorted
import tempfile

def pose_estimation(video):
    with tempfile.TemporaryDirectory() as tmp_dir:
    # video_path = 'clip.mp4'
    # output_images_dir = 'outputImages'
    # output_video_dir = 'outputVideo'
    # os.makedirs(output_images_dir, exist_ok=True)
    # os.makedirs(output_video_dir, exist_ok=True)
    # Initialize MediaPipe Pose and Drawing utilities
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        pose = mp_pose.Pose()

        # Open the video file
        cap = cv2.VideoCapture(video)
        # Initialize an empty frame and black background image
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            black_background = np.zeros_like(frame_rgb)
        else:
            print("Failed to read the first frame from the video file.")
            cap.release()
            exit()
        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a black background image
            black_background = np.zeros_like(frame_rgb)

            # Process the frame with MediaPipe Pose
            result = pose.process(frame_rgb)

            # Draw the pose landmarks on the black background
            if result.pose_landmarks:
                mp_drawing.draw_landmarks(black_background, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # image_path = os.path.join(output_images_dir, f'frame_{frame_number}.png')
            image_path = os.path.join(tmp_dir, f'frame_{frame_number}.png')
            cv2.imwrite(image_path, black_background)

            frame_number += 1
        cap.release()
        # 取得所有輸出影像路徑並自然排序
        # image_paths = natsorted(os.path.join(output_images_dir, f'frame_{frame_num}.png') for frame_num in range(frame_number))
        image_paths = natsorted(os.path.join(tmp_dir, f'frame_{frame_num}.png') for frame_num in range(frame_number))
        # 建立影片編碼器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 30.0  # 影片幀率
        frame_size = (black_background.shape[1], black_background.shape[0])  # 影格大小
        # out = cv2.VideoWriter(os.path.join(output_video_dir, 'output_video.mp4'), fourcc, fps, frame_size)
        out = cv2.VideoWriter('output.mp4', fourcc, fps, frame_size)
        # 寫入影格並編碼成影片
        for image_path in image_paths:
            frame = cv2.imread(image_path)
            out.write(frame)

        # 釋放影片編碼器
        out.release()
        with open('output.mp4', 'rb') as f:
            video_bytes = f.read()
        st.video(video_bytes)
    # return video

def GAN_model(video):
    # 將pose estimation後的圖片做GAN model
    return video

def main():
    st.title("YYDS影片生成器")

    # 輸入影片
    uploaded_file = st.file_uploader("選擇一個影片檔", type=['mp4', 'avi', 'mov'])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.video(uploaded_file)

    pose_estimation_button = st.button("pose_estimation", key="pose_estimation")
    if pose_estimation_button and uploaded_file is not None:
        pose_estimation(uploaded_file)
    #     st.session_state.processed_video1 = pose_estimation(uploaded_file)
    # if 'processed_video1' in st.session_state:
    #     st.video(st.session_state.processed_video1)

   
    generate_button = st.button("generate", key="generate")
    if generate_button and uploaded_file is not None:
        st.session_state.processed_video2 = GAN_model(uploaded_file)
    if 'processed_video2' in st.session_state:
            st.video(st.session_state.processed_video2)

if __name__ == "__main__":
    main()