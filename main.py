import time
import csv  
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

url = ["https://www.youtube.com/@michaeldonato"]  # Insert any link (this is a friend of mine)

for url in url:
    driver.get(f"{url}/videos?view=0&sort=p&flow=grid")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )
    except Exception as e:
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

    if video_elements:
        for video in video_elements:
            try:
                title = video.text.strip()

                parent = video.find_element(By.XPATH, "./../../..")
                views = parent.find_element(By.XPATH, ".//div[@id='metadata-line']/span[1]").text  
                upload_date = parent.find_element(By.XPATH, ".//div[@id='metadata-line']/span[2]").text  

                video_data.append({
                    "Title": title,  
                    "Upload_date": upload_date,
                    "Views": views
                })
            except Exception:
                continue

    channel_name = url.split("@")[-1]

    output_file = f"{channel_name}_video_data.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Upload_date", "Views"])
        writer.writeheader()
        writer.writerows(video_data)

    logging.info(f"Scraping completed. Total videos scraped: {len(video_data)}")
    logging.info(f"Data saved to: {output_file}")

driver.quit()
