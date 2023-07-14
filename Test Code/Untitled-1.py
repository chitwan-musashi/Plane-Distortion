
import cv2
import numpy as np
import math

#face = 'complete'
#face = 'right'
#face = 'left'
#face = 'top'
face = 'bottom'

# Load the image and convert it to grayscale
image = cv2.imread(r'g:\AI Engineering\Co-ops\Chitwan Singh\Plane Distortion\Endface\outer_flange_part2_bottom_92.482_degree.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# Apply Canny edge detection


edges = cv2.Canny(image, 5, 150)
# Display the result
cv2.imshow('Ellipse Detection', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply the Hough transform for ellipses
ellipses = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                            param1=50, param2=30, minRadius=0, maxRadius=1000000000)

# Extract detected ellipses
if ellipses is not None:
    ellipses = np.round(ellipses[0, :]).astype(int)

    for ellipse in ellipses:
        x, y, _ = ellipse  # Get the center coordinates and radius
        cv2.ellipse(image, (x, y), (10, 10), 0, 0, 360, (0, 255, 0), 2)  # Draw ellipse on the image

# Display the result
cv2.imshow('Ellipse Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
