import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time

s = Service('/Users/ianveilleux/development/chromedriver')
driver = webdriver.Chrome(service=s)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
STORE_ID = '//*[@id="store"]/div/b'
CLICK_ID = '//*[@id="store"]/div'
COOKIE_ID = '//*[@id="cookie"]'
MY_POINTS = '//*[@id="money"]'


def buy_upgrade(my_score):
    for cost, upgrade in reversed(name_value_dict.items()):
        if my_score >= cost:
            try:
                upgrade.click()
                print(f'Upgrade purchased for {cost}')
            except StaleElementReferenceException as e:
                print(e)
                print('parker')
        else:
            continue

game_on = True
points = driver.find_element(By.XPATH, MY_POINTS)

timeout = time.time() + 5
cookie = driver.find_element(By.XPATH, COOKIE_ID)
five_min = time.time() + 60*5

while game_on:
    cookie.click()
    points_object = driver.find_element(By.XPATH, MY_POINTS)
    points = points_object.text.split(',')
    new_points = int(''.join([str(x) for x in points]))
    if time.time() > timeout:
        item_cost = driver.find_elements(By.XPATH, STORE_ID)
        item_name = driver.find_elements(By.XPATH, CLICK_ID)
        items_list = []
        object_list = []
        for name in item_name:
            if len(name.text.split("-")) > 1:
                object_list.append(name)
            big_list = name.text.split("-")
            items_list.append(big_list)

        values_list = []
        names_list = []

        for item in items_list:
            try:
                if len(item[0]) > 1:
                    names_list.append(item[0].strip())
                value = item[1].split('\n')[0]
                stripped_value = value.strip().split(',')
                new_number = ''.join([str(x) for x in stripped_value])
                values_list.append(int(new_number))
            except IndexError:
                pass

        name_value_dict = dict(zip(values_list, object_list))

        buy_upgrade(new_points)

        timeout = time.time() + 15

        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break
