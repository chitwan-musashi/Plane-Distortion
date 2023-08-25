import cv2
import numpy as np
import math

#face = 'complete'
#face = 'right'
#face = 'left'
#face = 'top'
face = 'bottom'

# Load the image and convert it to grayscale
img = cv2.imread(r'g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Endface\outer_flange_part2_bottom_92.479_degree.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply histogram equalization to enhance contrast
equalized = cv2.equalizeHist(gray)

# Calculate the minimum and maximum pixel values
min_val = np.min(gray)
max_val = np.max(gray)

# Calculate the scaling factors
a = 0  # New minimum value
b = 255  # New maximum value
c = min_val  # Current minimum value
d = max_val  # Current maximum value

# Apply contrast stretching
stretched = np.uint8(((gray - c) * ((b - a) / (d - c))) + a)

# Apply edge detection using Canny
edges = cv2.Canny(stretched, 200, 400)

# Find contours in the image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Set the minimum and maximum area thresholds for filtering ellipses
if face == 'complete':
    min_area = 0
    max_area = 3000000
if face == 'right':
    min_area = 400000
    max_area = 10000000
if face == 'left':
    min_area = 400000
    max_area = 10000000
if face == 'top':
    min_area = 400000
    max_area = 10000000
if face == 'bottom':
    min_area = 4
    max_area = 100000000000
# Fit ellipses to the contours and calculate the angle of inclination
angles = []
for cnt in contours:

    perimeter = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)

    if len(cnt) >= 5:
        ellipse = cv2.fitEllipse(cnt)
        ellipse_area = math.pi * ellipse[1][0] * ellipse[1][1]
        if min_area <= ellipse_area <= max_area:
            angles.append(ellipse[2])
            cv2.ellipse(img, ellipse, (0, 255, 0), 2)  # Draw ellipse on the image

    
    # If the contour has a high approximation accuracy (close to 4 vertices), it can be considered a circle
    elif len(approx) >= 8:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(img, center, radius, (0, 255, 0), 2)

# Calculate the average angle of inclination
avg_angle = np.mean(angles)

# Calculate the plane of inclination
plane_angle = 90 - avg_angle

# Show the image with detected ellipses
cv2.imwrite("Ellipses.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("The object is inclined at an angle of {:.2f} degrees with respect to the image plane".format(plane_angle))
print("Maximum inclination angle: {:.2f} degrees".format(max(angles)))
