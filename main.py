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
    video_data = []

    print(f"\nVideos from {url}:")
    if video_elements:
        for i, video in enumerate(video_elements):
            try:
                title = video.text.strip()

                parent = video.find_element(By.XPATH, "./../../..")
                views = parent.find_element(By.XPATH, ".//div[@id='metadata-line']/span[1]").text  # Corrected: Views
                upload_date = parent.find_element(By.XPATH, ".//div[@id='metadata-line']/span[2]").text  # Corrected: Upload Date

                video_data.append({
                    "title": title,
                    "upload_date": upload_date,
                    "views": views
                })

                print(f"{i+1}. Title: {title}")
                print(f"   Upload Date: {upload_date}")
                print(f"   Views: {views}")
            except Exception as e:
                print(f"Error extracting data for video {i+1}: {e}")
    else:
        print("No video titles found.")

driver.quit()
