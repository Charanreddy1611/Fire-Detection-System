import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from skimage.feature import hog
from skimage.transform import rescale
from skimage.color import rgb2gray
import cv2

# Step 1: Prepare the dataset
fire_folder = "/home/pi/Desktop/fire"  # Folder path containing fire images
non_fire_folder = "/home/pi/Desktop/nofire"  # Folder path containing non-fire images

# Load and process the images
X = []
y = []

# Process fire images
for filename in os.listdir(fire_folder):
    image_path = os.path.join(fire_folder, filename)
    image = cv2.imread(image_path)
    if len(image.shape) == 3:  # RGB image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    image = cv2.resize(image, (64, 64))  # Resize the image to a fixed size if needed
    features = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), transform_sqrt=True)
    X.append(features)
    y.append(1)  # 1 for fire

# Process non-fire images
for filename in os.listdir(non_fire_folder):
    image_path = os.path.join(non_fire_folder, filename)
    image = cv2.imread(image_path)
    if len(image.shape) == 3:  # RGB image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    image = cv2.resize(image, (64, 64))  # Resize the image to a fixed size if needed
    features = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), transform_sqrt=True)
    X.append(features)
    y.append(0)  # 0 for non-fire

X = np.array(X)
y = np.array(y)

# Step 2: Train the classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X, y)

# Step 3: Predict fire based on new image
def predict_fire(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64, 64))
    features = hog(resized, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), transform_sqrt=True)
    prediction = classifier.predict([features])
    if prediction[0] == 1:
        return "Fire detected"
    else:
        return "No fire detected"

# Create the desktop path for saving images
desktop_path = os.path.expanduser("~/Desktop")

# Continuously capture images from the USB camera and predict on user request
camera = cv2.VideoCapture(0)

while True:
    # Capture an image from the USB camera
    ret, frame = camera.read()

    if ret:
        cv2.imshow("Camera", frame)
        inp=int(input("give input"))
        
        if inp == 0:  # Press 'q' to exit
            break
        elif inp == 1:  # Press 'p' to predict
            result = predict_fire(frame)
            print(result)
            # Save the captured image on the desktop
            image_name = "captured_image.jpg"
            image_path = os.path.join
    else:
        print("Failed to capture frame from the camera")
        break

# Release the camera and close windows
camera.release()
cv2.destroyAllWindows()
