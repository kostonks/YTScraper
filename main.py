import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

urls = ["https://www.youtube.com/@michaeldonato"] #Insert any links (this is a friend of mine)

for url in urls:
    driver.get(f"{url}/videos?view=0&sort=p&flow=grid")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )
    except Exception as e:
        print(f"Timeout or error loading page: {e}")
        continue

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    video_elements = driver.find_elements(By.ID, "video-title")

    print(f"\nVideo Titles from {url}:")
    if video_elements:
        for i, video in enumerate(video_elements):
            print(f"{i+1}. {video.text.strip()}")
    else:
        print("No video titles found.")

driver.quit()
