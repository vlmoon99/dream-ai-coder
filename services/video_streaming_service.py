import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class VideoStreamingService:
    def __init__(self, url:str = 'http://localhost:3333/', driver_path: str = '/usr/local/bin/chromedriver', width: int = 640, height: int = 480, capture_interval: float = 0.1):
        self.url = url
        self.driver_path = driver_path
        self.width = width
        self.height = height
        self.capture_interval = capture_interval
        self.current_frames = []
        self.frame_lock = threading.Lock()
        self.driver = None
        self.screenshot_thread = None
        self._start_driver()
        self._start_capture()

    def _start_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.url)

    def _start_capture(self):
        self.screenshot_thread = threading.Thread(target=self._capture_screenshots)
        self.screenshot_thread.daemon = True
        self.screenshot_thread.start()

    def _capture_screenshots(self):
        while True:
            try:
                screenshot_base64 = self.driver.get_screenshot_as_base64()
                with self.frame_lock:
                    if len(self.current_frames) >= 30:
                        self.current_frames.pop(0)
                    self.current_frames.append(screenshot_base64)

                time.sleep(self.capture_interval)
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

    def get_frames(self):
        with self.frame_lock:
            return self.current_frames

    def quit(self):
        if self.driver:
            self.driver.quit()
