#!/usr/bin/python
"""Test ordering on Amazon via Webdriver."""
from __future__ import print_function
#from urlparse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from amazon_page import main_page
from amazon_page import product_page

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

driver = webdriver.Firefox(firefox_profile=firefox_profile)

# def searchForASIN(asin):
#     """Search for ASIN on Amazon."""
#     driver.get(main_page().amazon_home_url)
#     elem = driver.find_element_by_name(amazon_search_input)
#     elem.clear()
#     elem.send_keys(asin)
#     elem.send_keys(Keys.RETURN)
#     assert "1 Ergebnis" and asin in driver.page_source

def buySingleProduct(url):
    """Get a product page by URL, put it into cart and finish checkout."""
    #parsed_url = urlparse(url)
    assert "http" and "://" in url, "Bitte die URL komplett kopieren, inklusive \"http://\" bzw. \"https://\" am Anfang."
    assert "amazon" in url, "Die aufzurufende Seite ist nicht die Amazon-Seite oder konnte nicht erkannt werden."
    print("Open page '"+url+"'")
    driver.get(url)
    print("Find add-to-cart element")
    try:
        print("actually find element")
        #add_to_cart_button = driver.find_element_by_css_selector(amazon_add_to_cart)

        print("scroll element into view using native js")
        driver.execute_script("window.scrollTo(0, document.GetElementById("+amazon_add_to_cart+"));")
        print("Send 'click' to element")
        add_to_cart_button.click()
        print("Success.")
    except Exception, e:
        print("Element could not be found. General exception: "+str(e))
        #driver.close()

#searchForASIN('B013BGEBXG')
buySingleProduct('https://www.amazon.de/Whiskas-Katzenfutter-Fisch--Fleischauswahl-Packung/dp/B013BGEBXG/ref=sr_1_1?ie=UTF8&qid=1476204396&sr=8-1&keywords=B013BGEBXG')
