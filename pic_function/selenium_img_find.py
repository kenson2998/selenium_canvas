import cv2
import numpy
from io import BytesIO
from PIL import Image
from selenium import webdriver
import time, os, random
from selenium.webdriver.common.keys import Keys  # 輸入指令用
from selenium.webdriver.common.action_chains import ActionChains  # selenium 動作操作
from selenium.webdriver.support.ui import WebDriverWait  # 等待元素
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tempfile


class GraphicalLocator:
    '''
    參考來源
    https://www.linkedin.com/pulse/html-canvas-testing-selenium-opencv-maciej-kusz
    '''

    def __init__(self, img_path):
        self.locator = img_path
        # x, y position in pixels counting from left, top corner
        self.x = None
        self.y = None
        self.img = cv2.imread(img_path)
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        self.threshold = None

    @property
    def center_x(self): return self.x + int(self.width / 2) \
        if self.x and self.width else None

    @property
    def center_y(self): return self.y + int(self.height / 2) \
        if self.y and self.height else None

    def find_me(self, drv):  # Clear last found coordinates
        self.x = self.y = None
        # Get current screenshot of a web page
        scr = drv.get_screenshot_as_png()
        # Convert img to BytesIO
        scr = Image.open(BytesIO(scr))
        # Convert to format accepted by OpenCV
        scr = numpy.asarray(scr, dtype=numpy.float32).astype(numpy.uint8)
        # Convert image from BGR to RGB format
        scr = cv2.cvtColor(scr, cv2.COLOR_BGR2RGB)

        # Image matching works only on gray images
        # (color conversion from RGB/BGR to GRAY scale)
        img_match = cv2.minMaxLoc(
            cv2.matchTemplate(cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY),
                              cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY),
                              cv2.TM_CCOEFF_NORMED))

        # Calculate position of found element
        self.x = img_match[3][0]
        self.y = img_match[3][1]

        # From full screenshot crop part that matches template image
        scr_crop = scr[self.y:(self.y + self.height),
                   self.x:(self.x + self.width)]

        # Calculate colors histogram of both template# and matching images and compare them
        scr_hist = cv2.calcHist([scr_crop], [0, 1, 2], None,
                                [8, 8, 8], [0, 256, 0, 256, 0, 256])
        img_hist = cv2.calcHist([self.img], [0, 1, 2], None,
                                [8, 8, 8], [0, 256, 0, 256, 0, 256])
        comp_hist = cv2.compareHist(img_hist, scr_hist,
                                    cv2.HISTCMP_CORREL)

        # Save treshold matches of: graphical image and image histogram
        self.threshold = {'shape': round(img_match[1], 2), 'histogram': round(comp_hist, 2)}

        # Return image with blue rectangle around match
        return cv2.rectangle(scr, (self.x, self.y),
                             (self.x + self.width, self.y + self.height),
                             (0, 0, 255), 2)


def script_click(x, y, driver):
    '''
    點擊的方法
    '''
    env = driver.find_element_by_css_selector("canvas")
    # env = driver.find_element_by_css_selector("*")
    action = ActionChains(driver)
    aabbcc = action.move_to_element_with_offset(env, x, y).click()
    # aabbcc = action.move_by_offset(x, y).click()
    print('點擊')
    aabbcc.perform()


def script_Sliding(driver, x1=1600, y1=800, x2=500, y2=800):
    '''
    點擊模擬手機滑動
    '''
    env = driver.find_element_by_css_selector("canvas")
    action = ActionChains(driver)
    ac1 = action.move_to_element_with_offset(env, x1, y1).click_and_hold()  # 點擊按住
    ac2 = ac1.move_to_element_with_offset(env, x2, y2).release().perform()  # 拖移到某個點後放開
    print('滑動')


def img_Sliding(img, driver, Rtime=10, J=0.7):
    T = 0
    while T < Rtime:
        try:
            print(img)
            img_check = GraphicalLocator(img)
            img_check.find_me(driver)
            # print(f'{game}圖片正確性:', img_check.threshold['shape'], img_check.threshold['histogram'])
            is_found = True if img_check.threshold['shape'] >= J else False
            if is_found:
                print(img, img_check.threshold['shape'])
                script_Sliding(driver)
                return 0
        except Exception as e:
            print(img, e)
    return 1


def img_single(img_list, driver, Rtime=10, J=0.7):
    '''
    單一對圖片點擊，當找到時 點擊後離開迴圈
    '''
    T = 0
    while T < Rtime:
        # try:
        #     print(img_list)
        img_check = GraphicalLocator(img_list)
        img_check.find_me(driver)
        print(f'{img_list}圖片正確性:', img_check.threshold['shape'], img_check.threshold['histogram'])
        is_found = True if img_check.threshold['shape'] >= J else False
        if is_found:
            print(img_list, img_check.threshold['shape'])
            script_click(img_check.center_x, img_check.center_y, driver)
            return 0
        # except Exception as e:
        #     print(img_list, e)
        T += 1
    return 1


def img_flow(img_list, driver, Rtime=10, J=0.7):
    '''
    一系列動作流程，會在這圖片區間一直做搜尋和點擊
    '''
    T = 0
    while T < Rtime:
        try:
            for i in img_list:
                img_check = GraphicalLocator(os.path.join(f"{i}"))
                img_check.find_me(driver)
                # print(f'{i}圖片正確性:', img_check.threshold['shape'], img_check.threshold['histogram'])
                is_found = True if img_check.threshold['shape'] >= J else False
                if is_found:
                    print(i, img_check.threshold['shape'])
                    script_click(img_check.center_x, img_check.center_y, driver)
                    continue
        except Exception as e:
            print(i, e)
        T += 1


def img_return(img_list, driver, Rtime=10, J=0.7):
    '''
      # 會在這圖片區間一直做搜尋和點擊，當找到時 點擊後離開迴圈
    '''

    T = 0
    while T < Rtime:
        try:
            for i in img_list:
                img_check = GraphicalLocator(os.path.join(f"{i}"))
                img_check.find_me(driver)
                # print(f'{i}圖片正確性:', img_check.threshold['shape'], img_check.threshold['histogram'])
                is_found = True if img_check.threshold['shape'] >= J else False
                if is_found:
                    print(i, img_check.threshold['shape'])
                    script_click(img_check.center_x, img_check.center_y, driver)
                    return 0
        except Exception as e:
            print(i, e)
        T += 1
    return 1


def img_wait(img, driver, Rtime=10, J=0.7):
    '''
        只等待某圖出現 出現後離開迴圈
    '''
    T = 0
    while T < Rtime:
        try:
            img_check = GraphicalLocator(img)
            img_check.find_me(driver)
            # is_found = True if img_check.threshold['shape'] >= 0.8 and \
            #                    img_check.threshold['histogram'] >= 0.2 else False
            is_found = True if img_check.threshold['shape'] >= J else False
            print(f'{img}圖片正確性:', img_check.threshold['shape'], img_check.threshold['histogram'])
            if is_found:
                return 0
        except Exception as e:
            print(img, e)
        T += 1
    return 1
