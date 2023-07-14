import cv2
import numpy as np

# Load the image and convert it to grayscale
img = cv2.imread(r"g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Endface\outer_flange_part2_bottom_92.482_degree.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply adaptive thresholding to obtain binary image
_, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find contours in the binary image
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Define minimum area threshold for ellipses
min_area_threshold = 700000  # Adjust this value as per your requirement

# Filter out smaller contours based on the minimum area
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold]

# Fit ellipses to the contours
ellipse_img = img
for contour in contours:
    if len(contour) >= 5:
        ellipse = cv2.fitEllipse(contour)
        ellipse_area = np.pi * (ellipse[1][0] / 2) * (ellipse[1][1] / 2)
        if ellipse_area >= min_area_threshold and ellipse[1][0] >= 0 and ellipse[1][1] >= 0:
            cv2.ellipse(ellipse_img, ellipse, (0, 255, 0), 2)

            # Calculate semi-major axis
            semi_major_axis = max(ellipse[1][0] / 2, ellipse[1][1] / 2)
            print("Semi-Major Axis:", semi_major_axis)

# Display the image with detected ellipses
cv2.imshow("Detected Ellipses", ellipse_img)
cv2.imwrite("G:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Testing\\" + "elipses_found.jpg", ellipse_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

ellipse_angles = []
for contour in contours:
    if len(contour) >= 5:
        ellipse = cv2.fitEllipse(contour)
        ellipse_area = np.pi * (ellipse[1][0] / 2) * (ellipse[1][1] / 2)
        if ellipse_area >= min_area_threshold and ellipse[1][0] >= 0 and ellipse[1][1] >= 0:
            ellipse_angles.append(ellipse[2])

# Check if ellipses were found
if len(ellipse_angles) > 0:
    # Calculate the average angle of inclination
    avg_angle = 90 + 90 - np.mean(ellipse_angles)

    # Calculate the individual distortion angles
    distortion_x = np.cos(np.radians(avg_angle))
    distortion_y = np.sin(np.radians(avg_angle))

    print("Overall Plane Distortion:")
    print("The object is inclined at an angle of {:.2f} degrees with respect to the image plane".format(avg_angle))
    print("Individual Distortion in X-axis: {:.2f} degrees".format(np.degrees(np.arccos(distortion_x))))
    print("Individual Distortion in Y-axis: {:.2f} degrees".format(np.degrees(np.arcsin(distortion_y))))
else:
    print("No ellipses found.")

##############
# Apply edge detection using Canny
edges = cv2.Canny(gray, 100, 200)

# Find contours in the image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Define a minimum area threshold for contours
min_contour_area = 200  # Adjust this value according to your needs

# Filter out smaller contours based on the minimum area
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

# Fit ellipses to the contours and calculate the angle of inclination
ellipse_angles = []
for cnt in contours:
    if len(cnt) >= 5:
        ellipse = cv2.fitEllipse(cnt)
        ellipse_angles.append(ellipse[2])

# Create the LineSegmentDetector object
lsd = cv2.createLineSegmentDetector()

# Detect line segments in the image
lines, _, _, _ = lsd.detect(gray)

# Calculate the angle of inclination for each line
line_angles = []
if lines is not None:
    for line in lines:
        for x1, y1, x2, y2 in line:
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            line_angles.append(angle)

# Check if ellipses were found
if len(ellipse_angles) > 0:
    # Calculate the average angle of inclination
    avg_angle = np.mean(ellipse_angles)

    # Calculate the plane of inclination
    plane_angle = (90 - avg_angle)/3

    print("Using ellipses:")
    print("The object is inclined at an angle of {:.2f} degrees with respect to the image plane".format(plane_angle))
    #print("Maximum ellipse angle:", max(ellipse_angles))
else:
    print("No ellipses found.")

# Check if lines were found
if len(line_angles) > 0:
    # Calculate the average angle of inclination
    avg_angle = np.mean(line_angles)

    # Calculate the plane of inclination
    plane_angle = 90 + avg_angle

    print("Using lines:")
    print("The object is inclined at an angle of {:.2f} degrees with respect to the image plane".format(plane_angle))
    #print("Maximum line angle:", max(line_angles))
else:
    print("No lines found.")

