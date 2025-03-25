import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

urls = ["https://www.youtube.com/@michaeldonato"]

for url in urls:
    driver.get(f'{url}/videos?view=0&sort=p&flow=grid')

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )
    except Exception as e:
        print(f"Timeout or error loading page: {e}")
        continue

    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    titles = soup.find_all('a', id='video-title')

    print(f"\n Video Titles from {url}:")
    if titles:
        for i, title in enumerate(titles):
            print(f"{i+1}. {title.text.strip()}")
    else:
        print(" No video titles found.")

driver.quit()
