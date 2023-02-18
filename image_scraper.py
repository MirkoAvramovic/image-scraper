from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\mirko\\OneDrive\\Radna površina\\Python projekti\\image-scraper\\chromedriver.exe"

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    
    url = "https://www.google.rs/search?q=%22dylan+dog%22&tbm=isch&ved=2ahUKEwib0_XV_J_9AhUmQKQEHZABASIQ2-cCegQIABAA&oq=%22dylan+dog%22&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgARQAFgAYIcGaABwAHgAgAF1iAF1kgEDMC4xmAEAqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=oj3xY5v6MKaAkdUPkIOEkAI&bih=657&biw=1366&hl=en"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips: max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
    return image_urls

def download_image(download_path, url, file_name):
    try:    
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        
        print("Success")
    except Exception as e:
        print('FAILED -', e)

urls = get_images_from_google(wd, 1, 6)

for i, url in enumerate(urls):
    download_image("imgs/", url, str(i) + ".jpg")

wd.quit()