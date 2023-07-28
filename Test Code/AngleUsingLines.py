import cv2
import numpy as np

print("Pick one of these: 'top', 'bottom', 'bottom-left', 'bottom-right'")
partId = input("The side to check is: ")

print("Copy-Paste Image Path")
imagePath = input("The image location is: ")

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create the LineSegmentDetector object
lsd = cv2.createLineSegmentDetector()

# Detect line segments in the image
lines, _, _, _ = lsd.detect(gray)

# Define the minimum line length threshold (adjust as needed)
min_line_length = 200

# Draw the detected lines on the image
line_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
if lines is not None:
    for line in lines:
        for x1, y1, x2, y2 in line:
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if length > min_line_length:
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert coordinates to integers
                cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the image with detected lines
cv2.imshow("Detected Lines", line_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
