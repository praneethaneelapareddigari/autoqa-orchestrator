import pytest, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    return webdriver.Chrome(options=opts)

def test_cart_placeholder():
    d = make_driver()
    try:
        d.get("https://www.example.com/")
        assert "Example" in d.title
    finally:
        d.quit()
