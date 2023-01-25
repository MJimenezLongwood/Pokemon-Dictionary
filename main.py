from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

user_agent = "user-agent=Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"


def loadDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--noerrdialogs')
    options.add_argument('disable-infobars')
    options.add_argument(user_agent)
    prefs = {"credentials_enable_service": False,
             "profile": {"password_manager_enabled": False}}
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    driver = webdriver.Chrome(
        service=ChromeService(
            "chromedriver.exe"),
        options=options)

    return driver

def readJson():
    with open('PokemonData.json', 'r') as inFile:
        pokemon = json.load(inFile)
    inFile.close()

    return pokemon

def writeJson(data):
    with open('PokemonData.json', 'w') as inFile:
        json.dump(data, inFile)
    inFile.close()

def getData(driver):
    pokemonDictionary = readJson()
    #pokemonDictionary = {}

    grid = driver.find_element(By.CLASS_NAME, 'infocard-list.infocard-list-pkmn-lg')
    pokemon = grid.find_elements(By.CLASS_NAME, 'infocard')

    for i in pokemon:
        info = i.find_element(By.CLASS_NAME, 'infocard-lg-data.text-muted')
        pokemonName = info.find_element(By.TAG_NAME, 'a')

        pokemonType = info.find_elements(By.TAG_NAME, 'small')
        pokemonType = pokemonType[1]

        pokemonTypings = pokemonType.find_elements(By.TAG_NAME, 'a')
        primaryType = pokemonTypings[0]

        try:
            secondaryType = pokemonTypings[1]
            print((pokemonName.text, primaryType.text, secondaryType.text))
            pokemonDictionary[pokemonName.text] = (primaryType.text, secondaryType.text)
        except:
            print((pokemonName.text, primaryType.text))
            pokemonDictionary[pokemonName.text] = (primaryType.text)

    writeJson(pokemonDictionary)


if (__name__ == '__main__'):
    driver = loadDriver()
    driver.get('https://pokemondb.net/pokedex/game/red-blue-yellow')
    getData(driver)
