#!/usr/bin/env python3

from selenium import webdriver
import time
from datetime import datetime
from prometheus_client import start_http_server, Gauge
import json
import locale
import logging

UPDATE_PERIOD = 30
PROMETHEUS_SERVER_PORT = 9999

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
logging.basicConfig(level=logging.INFO)

logging.info("App started")

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1200x600')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(60)
url = 'https://theflokiinu.com/#metrics'

logging.info("Started prometheus http server on port %s", PROMETHEUS_SERVER_PORT)
start_http_server(PROMETHEUS_SERVER_PORT)

prevStats = {
    "ethTotalSupply": "10,000,000,000,000",
    "ethBridge": "0",
    "ethBurned": "0",
    "ethLp": "0",
    "ethCirculating": "0",
    "bscTotalSupply": "10,000,000,000,000",
    "bscBridge": "0",
    "bscBurned": "0",
    "bscLp": "0",
    "bscCirculating": "0",
    "totalCirculating": "0",
    "combinedMarketCap": "0"
}


def find_metric_element(tokenomics, name):
    xpath = './/*/p[contains(text(),"%s")]/..//span' % name
    return tokenomics.find_element_by_xpath(xpath)


FLOKI_METRICS = Gauge(
    'floki_metrics', 'Floki Inu token metrics', ['metric_types'])
FLOKI_MARKET_CAP = Gauge(
    'floki_market_cap', 'Floki Inu MC')

while True:
    try:
        start_time = time.time()

        driver.get(url)

        tokenomics = driver.find_element_by_id("tokenomics")
        driver.execute_script("arguments[0].scrollIntoView();", tokenomics)

        stats = prevStats
        ethBridge = find_metric_element(tokenomics, "ETH Bridge")
        ethBurned = find_metric_element(tokenomics, "ETH Burned")
        ethLp = find_metric_element(tokenomics, "ETH LP")
        ethCirculating = find_metric_element(tokenomics, "ETH Circulating")
        bscBridge = find_metric_element(tokenomics, "BSC Bridge")
        bscBurned = find_metric_element(tokenomics, "BSC Burned")
        bscLp = find_metric_element(tokenomics, "BSC LP")
        bscCirculating = find_metric_element(tokenomics, "BSC Circulating")
        totalCirculating = find_metric_element(tokenomics, "Total Circulating")
        combinedMarketCap = find_metric_element(
            tokenomics, "Combined Market Cap")
        time.sleep(10)
        stats["ethBridge"] = ethBridge.text
        stats["ethBurned"] = ethBurned.text
        stats["ethLp"] = ethLp.text
        stats["ethCirculating"] = ethCirculating.text
        stats["bscBridge"] = bscBridge.text
        stats["bscBurned"] = bscBurned.text
        stats["bscLp"] = bscLp.text
        stats["bscCirculating"] = bscCirculating.text
        stats["totalCirculating"] = totalCirculating.text
        stats["combinedMarketCap"] = combinedMarketCap.text[1:]
        prevStats = stats
        timestamp = int(datetime.now().timestamp())
        logging.info('%s %s %s', datetime.now(), timestamp, json.dumps(stats))

        for key, str in stats.items():
            value = int(locale.atof(str))
            if (key == "combinedMarketCap"):
                FLOKI_MARKET_CAP.set(value)
            else:
                FLOKI_METRICS.labels(key).set(value)

        elapsed_time = time.time() - start_time
        logging.info('--- % s seconds ---', elapsed_time)
        if (elapsed_time < UPDATE_PERIOD):
            time.sleep(UPDATE_PERIOD - elapsed_time)
    except Exception as e:
        logging.error(e)
        time.sleep(5)
