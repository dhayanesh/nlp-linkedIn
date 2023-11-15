import traceback
import time
import os
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

def linked_scrap(gurl):
    def start_browser():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        time.sleep(1)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        driver.maximize_window()
        return driver

    driver = start_browser()

    def scroll_to_last_element(driver):
        while True:
            time.sleep(2)
            try:
                last_element = driver.find_elements(By.CSS_SELECTOR, 'div.ember-view.occludable-update')[-1]
                driver.execute_script("arguments[0].scrollIntoView()", last_element)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'article')))
                return True
            except (TimeoutException, IndexError) as e:
                logging.error(f"Exception occurred while scrolling: {e}")
                return False

    driver.get('https://www.linkedin.com/uas/login')


    username = driver.find_element(By.XPATH, "//input[@id='username']").send_keys('youremail@gmail.com')
    password = driver.find_element(By.XPATH, "//input[@id='password']").send_keys('yourpassword')
    singin = driver.find_element(By.XPATH, "//button[@aria-label='Sign in']").click()
    time.sleep(2)

    try:
        mainpath = "//div[@class='contextual-sign-in-modal__screen contextual-sign-in-modal__context-screen flex flex-col my-4 mx-3']"
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//div[@class='contextual-sign-in-modal__screen contextual-sign-in-modal__context-screen flex flex-col my-4 mx-3']")))

        driver.find_element(By.XPATH, "//button[@data-tracking-control-name='organization_guest_contextual-sign-in-modal_modal_dismiss']").click()
        print('clicked sign in')

    except:
        print('no sign in button')
    time.sleep(2)

    df = pd.DataFrame(columns=['content'])
    all_posts = []
    for url in gurl:
        driver.get(url)
        exception_count = 0
        sameurls_Status = 0

        while True:
            if exception_count > 300:
                break

            if driver.current_url == url:
                print('url is same')
            else:
                sameurls_Status += 1
            if sameurls_Status > 10:
                break

            scrol_Status = scroll_to_last_element(driver)
            if scrol_Status == False:
                exception_count += 1
            print('scrolling')
            
            articlelist = driver.find_elements(By.CSS_SELECTOR, 'div.update-components-text')
            for article in articlelist:
                article_text = article.text
                all_posts.append({'content': '<p>Content : ' + article_text + '</p>'})

            #df.to_csv('linkedin_posts.csv', index=False)

    driver.quit()
    df = pd.DataFrame(all_posts)
    df.to_csv('linkedin_posts.csv', index=False)
    return df

    return df

gurls = ['https://www.linkedin.com/in/justinwelsh/recent-activity/all/']
df = linked_scrap(gurls)
