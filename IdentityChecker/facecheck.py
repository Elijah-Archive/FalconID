import time
import requests
import urllib.request
import cv2
import os
from djitellopy import Tello

TESTING_MODE = False
APITOKEN = 'yourAPI'  # Your API Token
USE_Tello_Cam = False

def detect_face_snap():
    try:
        if USE_Tello_Cam:  
            tello = Tello()
            tello.connect()
            tello.streamon()
            frame_read = tello.get_frame_read()
        else:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open camera")
                return None

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        image_captured = False
        while not image_captured:
            if USE_Tello_Cam:
                frame = frame_read.frame
            else:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture frame")
                    continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x + w, y + h), (255, 0, 0), 2)
            
            cv2.imshow('Face Detection', frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s') and len(faces) > 0:
                cv2.imwrite('captured_face.jpg', frame)
                print("Face captured and saved as 'captured_face.jpg'!")
                image_captured = True
                break

        if USE_Tello_Cam:
            tello.streamoff()
            tello.end()
        else:
            cap.release()
        
        cv2.destroyAllWindows()
        
        if image_captured:
            return 'captured_face.jpg'
        return None

    except Exception as e:
        print(f"Error in detect_face_snap: {str(e)}")
        return None

def search_by_face(image_file):
    if image_file is None:
        return "No image file was captured", None
        
    if not os.path.exists(image_file):
        return f"Image file {image_file} does not exist", None
        
    if TESTING_MODE:
        print('****** TESTING MODE search, results are inaccurate, and queue wait is long, but credits are NOT deducted ******')
    
    try:
        site = 'https://facecheck.id'
        headers = {'accept': 'application/json', 'Authorization': APITOKEN}
        files = {'images': open(image_file, 'rb'), 'id_search': None}
        response = requests.post(site+'/api/upload_pic', headers=headers, files=files).json()
        
        if response.get('error'):
            return f"{response['error']} ({response['code']})", None
        
        id_search = response['id_search']
        print(response['message'] + ' id_search='+id_search)
        json_data = {'id_search': id_search, 'with_progress': True, 'status_only': False, 'demo': TESTING_MODE}
        
        while True:
            response = requests.post(site+'/api/search', headers=headers, json=json_data).json()
            if response.get('error'):
                return f"{response['error']} ({response['code']})", None
            if response.get('output'):
                return None, response['output']['items']
            print(f'{response["message"]} progress: {response["progress"]}%')
            time.sleep(1)
            
    except Exception as e:
        return f"Error during face search: {str(e)}", None

if __name__ == "__main__":
    # Step 1: Detect a face and snap a picture
    print("Press 's' to capture when a face is detected, or 'q' to quit")
    image_file = detect_face_snap()
    
    if image_file:
        # Step 2: Search the Internet by face
        error, urls_images = search_by_face(image_file)
        
        # Step 3: Display the results
        if urls_images:
            for im in urls_images:
                score = im['score']  # 0 to 100 score how well the face is matching found image
                url = im['url']  # URL to webpage where the person was found
                image_base64 = im['base64']  # Thumbnail image encoded as base64 string
                print(f"Match score: {score}")
                print(f"URL: {url}")
                print(f"Image data: {image_base64[:32]}...")
                print("-" * 50)
        else:
            print("Error:", error)
    else:
        print("No face was captured. Please try again.")