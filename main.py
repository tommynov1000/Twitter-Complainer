from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import sys
import time

try:
    with open(r"../config.json", mode="r") as file:
        config = json.load(file)
except FileNotFoundError:
    print("Config file was not found.")
    sys.exit(255)
USERNAME = config["Twitter Bot"]["username"]
PASSWORD = config["Twitter Bot"]["password"]
DOWN = config["Twitter Bot"]["promised down"]
UP = config["Twitter Bot"]["promised up"]


class InternetSpeedTwitterBot:
    """ Bot to check the current internet speed and send a tweet if it doesn't meet the minimum guaranteed speeds."""
    def __init__(self):
        self.down = None
        self.up = None
        executable_path = r"D:\Learning\Python\100 Days of code\Day 48 - Selenium\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=executable_path)

    def find_by_class_name(self, name):
        """ Shorthand for finding an element by class name"""
        return self.driver.find_element_by_class_name(name)

    def find_by_css(self, selector):
        """ Shorthand for finding an element by CSS selector"""
        return self.driver.find_element_by_css_selector(selector)

    def get_internet_speed(self):
        """ Gets the current internet speed from speedtest.net """

        # Find and click the start button.
        self.driver.get(url="https://www.speedtest.net/")
        time.sleep(2)
        speed_button = self.find_by_class_name("js-start-test")
        speed_button.click()

        # Find and get the download speed after waiting for 10 seconds.
        time.sleep(25)
        self.down = self.find_by_class_name("download-speed").text

        # Find and get upload speed after waiting another 10 seconds
        time.sleep(15)
        self.up = self.find_by_class_name("upload-speed").text

    def tweet_at_provider(self):
        """ Creates a tweet on twitter.com """
        # Open twitter log in screen.
        self.driver.get(url="https://twitter.com/login")

        # Input email and password
        time.sleep(2)
        email_input = self.driver.find_element_by_name('session[username_or_email]')
        email_input.send_keys(USERNAME)
        password_input = self.driver.find_element_by_name('session[password]')
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.ENTER)

        # Wait 3 seconds for page to load, then file complaint
        time.sleep(3)
        tweet = self.find_by_css('[data-block="true"]')
        tweet.send_keys(f"Hey Internet Provider, why is my internet speed "
                        f"{self.down}down/{self.up}up when I pay for {DOWN}down/{UP}up")

        # Click tweet
        self.find_by_css('[data-testid="tweetButtonInline"]').click()

    def exit(self):
        self.driver.close()


bot = InternetSpeedTwitterBot()
print("Getting internet speed")
bot.get_internet_speed()

if DOWN > float(bot.down) or UP > float(bot.up):
    print("Filing a complaint")
    bot.tweet_at_provider()

time.sleep(2)
bot.exit()
