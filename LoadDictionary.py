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

    webElement = driver.find_element(By.CLASS_NAME, 'resp-scroll')
    pokemonTable = webElement.find_element(By.CLASS_NAME, 'data-table')
    pokemonBody = pokemonTable.find_element(By.TAG_NAME, 'tbody')
    pokemon = pokemonBody.find_elements(By.TAG_NAME, 'tr')

    prevPokemonName = 0
    for i in pokemon:
        pokemonInfo = i.find_elements(By.TAG_NAME, 'td')

        pokemonName = pokemonInfo[1].find_element(By.TAG_NAME, 'a')

        if (pokemonName.text != prevPokemonName):
            pokemonTypings = pokemonInfo[2].find_elements(By.TAG_NAME, 'a')
            primaryType = pokemonTypings[0]

            pokemonBaseStat = pokemonInfo[3]
            pokemonHP = pokemonInfo[4]
            pokemonAtk = pokemonInfo[5]
            pokemonDef = pokemonInfo[6]
            pokemonSpAtk = pokemonInfo[7]
            pokemonSpDef = pokemonInfo[8]
            pokemonSpd = pokemonInfo[9]

            print(pokemonName.text)

            try:
                secondaryType = pokemonTypings[1]
                pokemonDictionary[pokemonName.text] = (primaryType.text, secondaryType.text, pokemonBaseStat.text,
                                                       pokemonHP.text, pokemonAtk.text, pokemonDef.text, pokemonSpAtk.text,
                                                       pokemonSpDef.text, pokemonSpd.text)
            except:
                pokemonDictionary[pokemonName.text] = (primaryType.text, pokemonBaseStat.text,
                                                       pokemonHP.text, pokemonAtk.text, pokemonDef.text, pokemonSpAtk.text,
                                                       pokemonSpDef.text, pokemonSpd.text)
        prevPokemonName = pokemonName.text
    writeJson(pokemonDictionary)


if (__name__ == '__main__'):
    driver = loadDriver()
    driver.get('https://pokemondb.net/pokedex/all')
    getData(driver)
