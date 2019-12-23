from selenium import webdriver



class driv_option(webdriver.ChromeOptions):
    def __init__(self):
        super().__init__()
        # self.add_argument('headless') # 背景執行
        # self.add_argument("--incognito")
        # self.add_argument('--auto-open-devtools-for-tabs') # 開發者工具
        self.add_argument('--no-sandbox')  # Linux 必要
        self.add_argument('--disable-infobars')  # 不顯示受到自动测试软件的控制

    def get_chrome_path(self):
        import os
        if os.name == 'nt':
            chrome_file = 'chromedriver.exe'
        else:
            chrome_file = 'chromedriver'
        Dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), chrome_file)
        if os.path.exists(Dir):
            # print(f'*chromedriver已找到 :{Dir}')
            return Dir
        else:
            print(f'*尚未找到{os.path.dirname(os.path.abspath(__file__))}')


def openchrome(url):
    setting = driv_option()
    driver = webdriver.Chrome(setting.get_chrome_path(), options=setting)
    # 視窗調整
    driver.maximize_window()
    # driver.set_window_size(width=1540, height=930)
    driver.get(url)  # 前往url
    # driver.refresh() # 重新整理
    # driver.quit() # 關閉
    return driver


if __name__ == '__main__':
    d = openchrome('http://www.google.com')
    e = WebDriverWait(d, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "*")))  # 等待指定元素5秒
    d.quit()
