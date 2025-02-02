import cv2
import time
import Pose as pm
import numpy as np
import socket
import pickle
import urllib.request


def run_pose_detector(nickname, url):
    cap = cv2.VideoCapture('Video/Jump.mp4')  # Adjust the video source as needed
    pTime = 0
    detector = pm.poseDetector()

    while True:
        img_arr = np.array(bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8)
        img_url = cv2.imdecode(img_arr, -1)
        img_url = cv2.resize(img_url, (1000, 800))

        img = detector.findPose(img_url)
        lmList = detector.findPosition(img, draw=False)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Display FPS and welcome message
        cv2.putText(img, f"FPS: {int(fps)}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, f"Welcome back, {nickname}!", (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow("Image", img_url)
        cv2.waitKey(1)


if __name__ == "__main__":
    # Set up socket connection to receive data from GUI
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(1)  # Listen for incoming connections
    print("Server is listening on port 12345...")

    while True:
        conn, addr = server_socket.accept()  # Accept connection
        print(f"Connection established with {addr}")

        try:
            data = conn.recv(1024)
            nickname, url = pickle.loads(data)  # Deserialize data received
            print(f"Received nickname: {nickname}, URL: {url}")
            run_pose_detector(nickname, url)  # Run the pose detector with received data
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
