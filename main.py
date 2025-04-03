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

# Configure logging to display information messages
logging.basicConfig(level=logging.INFO)

# Set up Chrome options for headless browsing
options = Options()
options.add_argument("--headless")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

# List of YouTube channel URLs to scrape
url = ["https://www.youtube.com/@michaeldonato"]  # Insert any link (this is a friend of mine)

# Loop through each URL in the list
for url in url:
    # Navigate to the channel's videos page
    driver.get(f"{url}/videos?view=0&sort=p&flow=grid")

    try:
        # Wait until the video elements are loaded on the page
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )
    except Exception as e:
        # Skip to the next URL if an error occurs
        continue

    # Get the initial scroll height of the page
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  
        # Get the new scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        # Break the loop if no new content is loaded
        if new_height == last_height:
            break
        last_height = new_height

    # Find all video elements on the page
    video_elements = driver.find_elements(By.ID, "video-title")
    video_data = []  

    if video_elements:
        for video in video_elements:
            try:
                # Extract video title
                title = video.text.strip()

                # Navigate to the parent element to extract additional metadata
                parent = video.find_element(By.XPATH, "./../../..")
                views = parent.find_element(By.XPATH, ".//div[@id='metadata-line']/span[1]").text  
                upload_date = parent.find_element(By.XPATH, ".//div[@id='metadata-line']/span[2]").text  

                # Append video data to the list
                video_data.append({
                    "Title": title,  
                    "Upload_date": upload_date,
                    "Views": views
                })
            except Exception:
                # Skip the video if an error occurs
                continue

    # Extract the channel name from the URL
    channel_name = url.split("@")[-1]

    # Save the scraped data to a CSV file
    output_file = f"{channel_name}_video_data.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Upload_date", "Views"])
        writer.writeheader()
        writer.writerows(video_data)

    # Log the completion of scraping for the current channel
    logging.info(f"Scraping completed. Total videos scraped: {len(video_data)}")
    logging.info(f"Data saved to: {output_file}")

# Close the WebDriver
driver.quit()
