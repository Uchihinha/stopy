import time
import requests
import sys
import argparse
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from database import insertWords, getWordByLetter

global defaultUrl
defaultUrl = "https://stopots.com"

driver = webdriver.Firefox()

isValidating = False
isAnswering = False
isRanking = False

def getCurrentValidationStep():
    currentStep = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[1]/h4[2]").text.split('/')[0]
    if currentStep == '':
        currentStep = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[1]/h4[1]").text.split('/')[0].split(' ')
        currentStep = currentStep[len(currentStep)-1]
    
    return currentStep

def getCountValidationStep():
    countSteps = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[1]/h4[2]"))).text.split('/')[1].split(' ')[0]

    if countSteps == '':
        countSteps = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[1]/h4[1]").text.split('/')[1]
    
    return countSteps

def getParams():
    parser = argparse.ArgumentParser(description='getting args') 
    parser.add_argument('--url', type=str, default=defaultUrl)
    parser.add_argument('--username', type=str, default='Nome de Teste')
     
    args = parser.parse_args()
    return args

def login(name):
    nameField = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    nameField.clear()
    nameField.send_keys(name)

    time.sleep(1)

    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-exclamation"))).click()
    # driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/button").click()

def setup():
    option = Options()
    option.headless = True

    params = getParams()

    driver.get(params.url)
    time.sleep(2)

    driver.find_element_by_xpath("/html/body/header/div/div[2]/div/form/button").click()

    time.sleep(2)

    login(params.username)

def storeWords(items):
    data = json.dumps(items, indent=4, ensure_ascii=False)
    fp = open(str(round(time.time() * 1000)) + '.json', 'w', encoding='utf8')
    fp.write(data)
    fp.close()

def addCurrentCategoryWord(items):
    currentCategory = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[1]/h4[2]").text
    if currentCategory == '':
        currentCategory = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[1]/h3").text

    try:
        validText = driver.find_element_by_class_name("valid").text
    except:
        print('CAIU NO ERRO AQUI')
        return items

    currentCategory = currentCategory.split(': ')[1]

    items.append({
        'category': currentCategory.upper(),
        'word': validText
    })

    return items
    
def setIsAnswering():
    global isAnswering
    try:
        driver.find_element_by_class_name('answers')
        isAnswering = True
    except:
        isAnswering = False

def setIsValidating():
    global isValidating
    try:
        driver.find_element_by_class_name('validation')
        isValidating = True
    except:
        isValidating = False

def setIsRanking():
    global isRanking
    try:
        driver.find_element_by_class_name('positions')
        isRanking = True
    except:
        isRanking = False

def getCurrentTurn():
    return driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/div[1]/span').text

def getCountTurn():
    return driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/div[1]/p[2]').text.split('/')[1]

def main():
    setup()

    items = []

    while True:
        setIsValidating()
        setIsAnswering()
        setIsRanking()

        print('------------------------')
        print(f'VALIDANDO: {isValidating}')
        print(f'RESPONDENDO: {isAnswering}')
        print(f'RANKING: {isRanking}')
        print('------------------------')

        if isValidating:
            time.sleep(1)
            currentStep = getCurrentValidationStep()
            totalSteps = getCountValidationStep()

            stepCounter = 0

            while True:
                currentStep = getCurrentValidationStep()

                time.sleep(0.5)
                if stepCounter != currentStep and currentStep != '':
                    items = addCurrentCategoryWord(items)
                    stepCounter = currentStep
                    print('STEP ' + stepCounter + '/' + totalSteps + ' CONCLUÍDO')
                    time.sleep(1)
                    button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-exclamation")))
                    button.click()
                elif currentStep == totalSteps:
                    insertWords(items)
                    items = []

                    print('Validação Finalizada!')
                    print('Rodada ' + getCurrentTurn() + ' de ' + getCountTurn())

                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "ranking")))
                    if getCurrentTurn() == getCountTurn():
                        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "positions")))
                    else:
                        time.sleep(5)
                        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-exclamation"))).click()
                    break
        elif isAnswering:
            counter = 0
            time.sleep(1)
            currentLetter = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div/ul/li[1]/span").text

            fields = driver.find_elements_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[1]/label")
            
            categorys = []

            for field in fields:
                categorys.append(field.find_element_by_tag_name("span").text)

            for category in categorys:
                customInput = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyzйáéíóúãõçêâô', 'ABCDEFGHIJKLMNOPQRSTUVWXYZЙÁÉÍÓÚÃÕÇÊÂÔ'), '" + category + "')]/../input")))

                customInput.clear()
                answer = getWordByLetter({'category': category, 'letter': currentLetter})

                if answer != '':
                    counter = counter + 1

                customInput.send_keys(answer)

            if counter == len(fields):
                print('Aguardando tempo para STOP')
                button = False
                while not button:
                    try:
                        time.sleep(1)
                        driver.find_element_by_class_name("answers").find_element_by_class_name('disable')
                        button = False
                    except:
                        button = True
                time.sleep(1)
                WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-exclamation"))).click()
            while not isValidating:
                setIsValidating()
                time.sleep(1)

            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-exclamation"))).click()
        elif isRanking:
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-exclamation"))).click()
            while isRanking:
                setIsRanking()
                time.sleep(1)
        else:
            print('.........')
        
main()