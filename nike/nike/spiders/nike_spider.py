import time
from typing import Any

import scrapy
from scrapy.http import Response
from ..product_questions import ProductQuestions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from scrapy import signals
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..items import NikeItem

class nike_spider(scrapy.Spider):
    name = "nike_spider"
    start_urls = ["https://www.nike.com/pl/w/wyprzedaz-3yaep"]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.nike.com/pl/w/wyprzedaz-3yaep")
        self.driver.implicitly_wait(5)
        cookies_link = self.driver.find_element(By.XPATH,'//*[@id="modal-root"]/div/div/div/div/div/section/div[2]/div/button')
        cookies_link.click()

    def parse(self, response):
        product_type = ProductQuestions.ask_product_type()
        color_dict = {
            "black":'//button[@aria-label="Filtruj według: Czerń"]',
            "blue":'//button[@aria-label="Filtruj według: Niebieski"]',
            "brown":'//button[@aria-label="Filtruj według: Brązowy"]',
            "green":'//button[@aria-label="Filtruj według: Zieleń"]',
            "grey":'//button[@aria-label="Filtruj według: Szary"]',
            "orange":'//button[@aria-label="Filtruj według: Pomarańczowy"]',
            "pink":'//button[@aria-label="Filtruj według: Różowy"]',
            "violet":'//button[@aria-label="Filtruj według: Fiolet"]',
            "red":'//button[@aria-label="Filtruj według: Czerwony"]',
            "white": '//button[@aria-label="Filtruj według: Biel"]',
            "yellow": '//button[@aria-label="Filtruj według: Żółty"]'

        }
        sizes_dict = {
            "xs":'//button[@aria-label="Filtruj według: XS"]',
            "s": '//button[@aria-label="Filtruj według: S"]',
            "m": '//button[@aria-label="Filtruj według: M"]',
            "l": '//button[@aria-label="Filtruj według: L"]',
            "xl": '//button[@aria-label="Filtruj według: XL"]',
        }
        if product_type == "clothes":
            self.driver.get('https://www.nike.com/pl/w/wyprzedaz-odziez-3yaepz6ymx6')
            self.driver.implicitly_wait(5)
            color_link = self.driver.find_element(By.XPATH,'//div[@aria-label="Wybierz kolor"]')
            color_link.click()
            self.driver.implicitly_wait(5)
            colors = ProductQuestions.ask_color()
            for color in colors:
                color_link = self.driver.find_element(By.XPATH,color_dict[color])
                self.driver.implicitly_wait(3)
                color_link.click()
                time.sleep(4)


            sex = ProductQuestions.ask_sex()
            sex_link = self.driver.find_element(By.XPATH,'//div[@aria-label="Płeć"]')
            sex_link.click()
            self.driver.implicitly_wait(3)
            time.sleep(3)
            if sex == "man":
                sex_link = self.driver.find_element(By.XPATH,'//button[@aria-label="Filtruj według: Mężczyźni"]')
                sex_link.click()
            else:
                sex_link = self.driver.find_element(By.XPATH,'//button[@aria-label="Filtruj według: Kobiety"]')
                sex_link.click()
            self.driver.implicitly_wait(5)
            #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, color_dict[colors[0]])))
            size_link = self.driver.find_element(By.XPATH,'//div[@aria-label="Rozmiar"]')
            size_link.click()
            sizes = ProductQuestions.ask_size()
            for size in sizes:
                size_link = self.driver.find_element(By.XPATH, sizes_dict[size])
                size_link.click()
                self.driver.implicitly_wait(3)
                time.sleep(4)

            price_min = ProductQuestions.ask_min_price()
            price_max = ProductQuestions.ask_max_price()
            item = NikeItem()
            div_element = response.css("div.product-card[data-testid='product-card']")
            for element in div_element:
                title = response.css("div.product-card__title::attr(id)").extract()
                price = response.css("div.product-price[data-testid='product-price-reduced']::text").extract()
                item['title'] = title
                item['price'] = price
                yield item
