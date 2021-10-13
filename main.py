import cv2
import numpy as np
import pyautogui
import time

def locate_on_screen(template, threshold = 0.95, method = cv2.TM_CCORR_NORMED, out = None):
    w, h = template.shape[::-1]
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Apply template Matching
    res = cv2.matchTemplate(img, template, method)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        match_val = 1 - min_val
    else:
        top_left = max_loc
        match_val = max_val

    bottom_right = (top_left[0] + w, top_left[1] + h)
    center_point = (top_left[0] + (w/2), top_left[1] + (h/2))

    print(match_val)

    if out:
        cv2.rectangle(img, top_left, bottom_right, 0, 2)
        cv2.imwrite(out, img)
    
    if match_val < threshold:
        return None, None, None
    
    return center_point, top_left, bottom_right

if __name__ == "__main__":
    template = cv2.imread('chest1.jpg', cv2.IMREAD_GRAYSCALE)

    while True:
        loc, _, _ = locate_on_screen(template, out='result.png')
        if loc:
            print('loc: {}'.format(loc))
            x, y = pyautogui.position()
            pyautogui.moveTo(loc[0], loc[1])
            time.sleep(0.5)
            pyautogui.click(loc[0], loc[1])
            pyautogui.moveTo(x, y)
        time.sleep(10)
