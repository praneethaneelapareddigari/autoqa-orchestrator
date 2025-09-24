import os, time, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    return webdriver.Chrome(options=opts)

def test_login_page_loads():
    d = make_driver()
    try:
        d.get("https://www.example.com/")
        assert "Example Domain" in d.title
    finally:
        d.quit()
