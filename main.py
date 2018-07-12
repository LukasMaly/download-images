import os
import re
import shutil
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotVisibleException
)


def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def get_all_download_links(driver, url):
    '''Visits a page and retrieves all download links using regex'''
    driver.get(url)
    try:
        while True:
            button = driver.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "loadmore")))
            button.click()
    except ElementNotVisibleException:
        pass
    matches = re.findall(
        r'(?<=href=\")/download/.+.jpg(?=\")', driver.page_source)
    return matches


def download_images(prefix, dirname, links):
    length = len(links)
    for index, link in enumerate(links):
        print('Downloading {0} of {1} images'.format(index + 1, length))
        url = prefix + link
        f = urllib.request.urlopen(url)
        save_image_to_file(f, dirname, index)
        del f


def save_image_to_file(image, dirname, suffix):
    with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image, out_file)


def make_dir(dirname):
    current_path = os.getcwd()
    path = os.path.join(current_path, dirname)
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    driver = init_driver()
    image_links = get_all_download_links(
        driver, 'https://quotefancy.com/motivational-quotes')
    time.sleep(5)
    driver.quit()
    dirname = 'imgs'
    make_dir(dirname)
    download_images('https://quotefancy.com', dirname, image_links)
