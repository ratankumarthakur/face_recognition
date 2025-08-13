#add_faces.py
import cv2
import pickle
import numpy as np
import os

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0

name = input("Enter Your Name: ")
roll = input("Enter Your Roll Number: ")
label = f"{name}_{roll}"

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        if i % 10 == 0:
            faces_data.append(resized_img)
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q') or len(faces_data) == 50:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data).reshape(len(faces_data), -1)
labels = [label] * len(faces_data)

if not os.path.exists('data'):
    os.makedirs('data')

# Append or save name/roll and faces
if 'names.pkl' not in os.listdir('data/'):
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(labels, f)
else:
    with open('data/names.pkl', 'rb') as f:
        existing_labels = pickle.load(f)
    existing_labels += labels
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(existing_labels, f)

if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        existing_faces = pickle.load(f)
    combined_faces = np.append(existing_faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(combined_faces, f)

print(f"✅ Successfully saved {len(faces_data)} face samples for {label}")