import cv2 

def remove_bg(masked_filename, remove_filename):

    # Read the image 
    src = cv2.imread(masked_filename, 1) 

    # Convert image to image gray 
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) 

    # Applying thresholding technique 
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY) 

    # Using cv2.split() to split channels of coloured image 
    b, g, r = cv2.split(src) 

    # Making list of Red, Green, Blue Channels and alpha 
    rgba = [b, g, r, alpha] 

    # Using cv2.merge() to merge rgba into a coloured/multi-channeled image 
    dst = cv2.merge(rgba, 4) 

    # Writing and saving to a new image 
    cv2.imwrite(remove_filename, dst)
