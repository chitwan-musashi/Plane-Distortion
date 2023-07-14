import cv2
import numpy as np
from sklearn.cluster import KMeans

# Load the image and convert it to grayscale
img = cv2.imread('g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Testing\Image__2023-06-23__15-19-24.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection using Canny
edges = cv2.Canny(gray, 100, 200)

# Find contours in the image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Approximate contours as lines
lines = []
for contour in contours:
    if len(contour) >= 2:
        # Fit a line to the contour using least squares method
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        line = [x - 1000 * vx, y - 1000 * vy, x + 1000 * vx, y + 1000 * vy]
        lines.append(line)

if len(lines) >= 2:
    # Calculate the angles of the lines
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # Perform K-means clustering to identify dominant angles
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(np.array(angles).reshape(-1, 1))
    cluster_centers = kmeans.cluster_centers_

    # Select the dominant angle as the one closest to 90 degrees
    dominant_angle = cluster_centers[np.argmin(np.abs(cluster_centers - 90))][0]

    # Calculate the plane of inclination
    plane_angle = 90 - dominant_angle

    print("The object is inclined at an angle of {:.2f} degrees with respect to the image plane".format(plane_angle))
    print("Dominant angle:", dominant_angle)
else:
    print("Insufficient lines found. Unable to calculate the plane distortion angle.")