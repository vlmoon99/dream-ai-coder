import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class VideoStreamingService:
    def __init__(self, url: str = 'http://localhost:7000/', driver_path: str = '/usr/local/bin/chromedriver'):
        self.url = url
        self.driver_path = driver_path
        self.frame_lock = threading.Lock()
        self.driver = None
        self._start_driver()

    def _start_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.url)

    def capture_screenshot(self):
        try:
            screenshot_base64 = self.driver.get_screenshot_as_base64()
            return screenshot_base64
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    def quit(self):
        if self.driver:
            self.driver.quit()
