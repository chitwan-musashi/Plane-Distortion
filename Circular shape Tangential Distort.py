import cv2
import numpy as np

# Load the image and convert it to grayscale
img = cv2.imread('inner-thrust-co-ax-and-dome__2023-05-04__30ms.bmp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection using Canny
edges = cv2.Canny(gray, 100, 200)

# Find contours in the image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Fit arcs to the contours and calculate the angle of inclination
angles = []
for cnt in contours:
    if len(cnt) >= 6:
        (x, y), (w, h), angle = cv2.fitEllipse(cnt)
        angles.append(angle)

# Calculate the average angle of inclination
avg_angle = np.mean(angles)

# Calculate the plane of inclination
plane_angle = 90 - avg_angle

print("The object is inclined at an angle of {:.2f} degrees with respect to the image plane".format(plane_angle))
