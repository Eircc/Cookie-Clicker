from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pygame
import time
import math
import sys

# -----------------------------------------------------------------------------------
# LOADING COOKIE CLICKER GAME
service = Service(r"C:\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://orteil.dashnet.org/cookieclicker/")

driver.implicitly_wait(10)
# -----------------------------------------------------------------------------------
# INITIALIZING PYGAME WINDOW
pygame.init()
WIDTH = 500
HEIGHT = 400
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
# -----------------------------------------------------------------------------------
# LOADING SAVE FILE
langauge = driver.find_element(By.ID, "langSelect-EN")
langauge.click()

time.sleep(5)

options = driver.find_element(By.ID, "prefsButton")
load_file_actions = ActionChains(driver)
load_file_actions.move_to_element(options)
load_file_actions.click()
load_file_actions.perform()
 
load_file = driver.find_element(By.ID, "FileLoadInput")
load_file_actions.move_to_element(load_file)
load_file_actions.click()
load_file_actions.perform()

time.sleep(5)

load_file_actions.move_to_element(options)
load_file_actions.click()
load_file_actions.perform()
# -----------------------------------------------------------------------------------
# FINDING BUILDING COSTS
def find_costs():
    item_costs = []
    for i in range(20):
        try:
            item_costs.append(driver.find_element(By.ID, "productPrice" + str(i)).text)
        except:
            pass

    n = item_costs.count("")
    for i in range(n): 
        item_costs.remove("")
    for i in range(len(item_costs)):
        item_costs[i] = item_costs[i].replace(",", "")
        if "million" in item_costs[i]:
            item_costs[i] = float(item_costs[i].split()[0]) * 10**6
        elif "billion" in item_costs[i]:
            item_costs[i] = float(item_costs[i].split()[0]) * 10**9
        elif "trillion" in item_costs[i]:
            item_costs[i] = float(item_costs[i].split()[0]) * 10**12
        item_costs[i] = int(item_costs[i])
    return item_costs

item_costs = find_costs()
# -----------------------------------------------------------------------------------
# FINDING BUILDING CPS
def find_cps(item_costs):
    default_cps = [0.1, 1, 8, 47, 260, 1400, 7800, 44000, 260000, 1600000, 10*10**6, 65*10**6, 430*10**6, 2.9*10**9, 21*10**9, 150*10**9, 1.1*10**12, 8.3*10**12, 64*10**12, 510*10**12]
    cps_actions = ActionChains(driver)
    item_cps = []
    for i in range(len(item_costs)):
        try:
            element = driver.find_element(By.ID, "productPrice" + str(i))
            cps_actions.move_to_element(element)
            cps_actions.perform()
            cps = driver.find_element(By.CLASS_NAME, "descriptionBlock")
            s = cps.text.split()
            a = s.index("produces")
            if s[a + 2] == "million":
                item_cps.append(float(s[a + 1]) * 10**6)
            elif s[a + 2] == "billion":
                item_cps.append(float(s[a + 1]) * 10**9)
            elif s[a + 2] == "trillion":
                item_cps.append(float(s[a + 1]) * 10**12)
            else:
                item_cps.append(float(s[a + 1].replace(",", "")))
        except:
            item_cps.append(default_cps[i])
    return item_cps

item_cps = find_cps(item_costs)
# -----------------------------------------------------------------------------------
# FINDING BUILDING VALUE
def find_value(item_costs, item_cps):
    value = []
    min = 9999999999999999
    for i in range(len(item_costs)):
        v = item_cps[i] / item_costs[i]
        if v < min:
            min = v
        value.append(v)
    for i in range(len(item_costs)):
        value[i] = value[i] / min
    temp = value.copy()
    temp.sort()
    temp.reverse()
    return value, temp

value, temp = find_value(item_costs, item_cps)
# -----------------------------------------------------------------------------------
# DRAWING CONTROL PANEL GUI
def display(clicker, buyer, scanning, value, temp):
    ORANGE = (209, 123, 65)
    WHITE = (235, 218, 206)
    screen.fill(ORANGE)
    pygame.draw.circle(screen, WHITE, (110, 108), 75)
    pygame.draw.circle(screen, WHITE, (110, 291), 75)

    font = pygame.font.SysFont('comicsansms', 20)
    auto_clicker = font.render('Auto Click', True, ORANGE)
    auto_clicker_rect = auto_clicker.get_rect(center=(110, 103))
    screen.blit(auto_clicker, auto_clicker_rect)
    auto_buy = font.render("Auto Buy", True, ORANGE)
    auto_buy_rect = auto_buy.get_rect(center=(110, 286))
    screen.blit(auto_buy, auto_buy_rect)

    font = pygame.font.SysFont('comicsansms', 12)
    if clicker:
        on_text = font.render('ON', True, ORANGE)
        on_text_rect = on_text.get_rect(center=(110, 133))
        screen.blit(on_text, on_text_rect)
    else:
        off_text = font.render('OFF', True, ORANGE)
        off_text_rect = off_text.get_rect(center=(110, 133))
        screen.blit(off_text, off_text_rect)
    if buyer:
        on_text = font.render('ON', True, ORANGE)
        on_text_rect = on_text.get_rect(center=(110, 316))
        screen.blit(on_text, on_text_rect)
    else:
        off_text = font.render('OFF', True, ORANGE)
        off_text_rect = off_text.get_rect(center=(110, 316))
        screen.blit(off_text, off_text_rect)

    pygame.draw.rect(screen, WHITE, (250, 20, 200, 40), 0, 4)
    font = pygame.font.SysFont('comicsansms', 15)
    if scanning:
        scanning_text = font.render("Scanning...", True, ORANGE)
        scanning_text_rect = scanning_text.get_rect(center=(350, 40))
        screen.blit(scanning_text, scanning_text_rect)
    else:
        scan_text = font.render("Rescan Values", True, ORANGE)
        scan_text_rect = scan_text.get_rect(center=(350, 40))
        screen.blit(scan_text, scan_text_rect)

    font = pygame.font.SysFont('comicsansms', 18, True)
    pygame.draw.rect(screen, WHITE, (250, 80, 200, 300), 2, 4)
    buy_order_text = font.render("Buy Order", True, WHITE)
    buy_order_text_rect = buy_order_text.get_rect(center=(350, 100))
    screen.blit(buy_order_text, buy_order_text_rect)

    pygame.draw.rect(screen, WHITE, (260, 120, 180, 46), 0, 4)
    pygame.draw.rect(screen, WHITE, (260, 171, 180, 46), 0, 4)
    pygame.draw.rect(screen, WHITE, (260, 222, 180, 46), 0, 4)
    pygame.draw.rect(screen, WHITE, (260, 273, 180, 46), 0, 4)
    pygame.draw.rect(screen, WHITE, (260, 324, 180, 46), 0, 4)

    font = pygame.font.SysFont('comicsansms', 10)
    for i in range(5):
        number = font.render(str(i + 1), True, ORANGE)
        number_rect = number.get_rect(center=(270, 130 + 51 * i))
        screen.blit(number, number_rect)

    buildings = ['cursor', 'grandma', 'farm', 'mine', 'factory', 'bank', 'temple', 'wizard tower', 'shipment', 'alchemy lab', 'portal', 'time machine', 'antimatter condenser', 'prism', 'chancemaker', 'fractal engine', 'javascript console', 'idleverse', 'cortex baker', 'you']
    font = pygame.font.SysFont('comicsansms', 15)
    for i in range(min(5, len(value))):
        index = value.index(temp[i])
        name = font.render(buildings[index], True, ORANGE)
        name_rect = name.get_rect(center=(350, 130 + 51 * i))
        screen.blit(name, name_rect)
        building_value = font.render('%.3f' %temp[i], True, ORANGE)
        building_value_rect = building_value.get_rect(center=(350, 150 + 51 * i))
        screen.blit(building_value, building_value_rect)
    
    pygame.display.update()
# -----------------------------------------------------------------------------------
# FIND DISTANCE BETWEEN TWO POINTS
def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
# -----------------------------------------------------------------------------------

clicker = False
buyer = False
scanning = False

default_cps = [0.1, 1, 8, 47, 260, 1400, 7800, 44000, 260000, 1600000, 10*10**6, 65*10**6, 430*10**6, 2.9*10**9, 21*10**9, 150*10**9, 1.1*10**12, 8.3*10**12, 64*10**12, 510*10**12]


balance = driver.find_element(By.ID, "cookies")
cookie = driver.find_element(By.ID, "bigCookie")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            options = driver.find_element(By.ID, "prefsButton")
            save_file_actions = ActionChains(driver)
            save_file_actions.move_to_element(options)
            save_file_actions.click()
            save_file_actions.perform()
            
            save_file = driver.find_element(By.ID, "FileLoadInput")
            save_file_actions.move_to_element_with_offset(save_file, -148, 0)
            save_file_actions.click()
            save_file_actions.perform()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if dist(x, y, 110, 108) <= 75:
                if clicker:
                    clicker = False
                else:
                    # program autoclicker
                    clicker = True
            elif dist(x, y, 110, 291) <= 75:
                if buyer:
                    buyer = False
                else:
                    # program autobuyer
                    buyer = True
            elif x >= 250 and x <= 450:
                if y >= 20 and y <= 60:
                    scanning = True
                    display(clicker, buyer, scanning, value, temp)
                    item_costs = find_costs()
                    item_cps = find_cps(item_costs)
                    value, temp = find_value(item_costs, item_cps)
                    scanning = False
            if x >= 260 and x <= 440:
                if y >= 120 and y <= 166:
                    index = value.index(temp[0])
                    element = driver.find_element(By.ID, "productPrice" + str(index))
                    buy_actions = ActionChains(driver)
                    buy_actions.move_to_element(element)
                    buy_actions.click()
                    buy_actions.perform()
                    item_costs = find_costs()
                    value, temp = find_value(item_costs, item_cps)
                    display(clicker, buyer, scanning, value, temp)
                elif y >= 171 and y <= 217:
                    index = value.index(temp[1])
                    element = driver.find_element(By.ID, "productPrice" + str(index))
                    buy_actions = ActionChains(driver)
                    buy_actions.move_to_element(element)
                    buy_actions.click()
                    buy_actions.perform()
                    item_costs = find_costs()
                    value, temp = find_value(item_costs, item_cps)
                    display(clicker, buyer, scanning, value, temp)
                elif y >= 222 and y <= 268:
                    if len(value) >= 3:
                        index = value.index(temp[2])
                        element = driver.find_element(By.ID, "productPrice" + str(index))
                        buy_actions = ActionChains(driver)
                        buy_actions.move_to_element(element)
                        buy_actions.click()
                        buy_actions.perform()
                        item_costs = find_costs()
                        value, temp = find_value(item_costs, item_cps)
                        display(clicker, buyer, scanning, value, temp)
                elif y >= 273 and y <= 319:
                    if len(value) >= 4:
                        index = value.index(temp[3])
                        element = driver.find_element(By.ID, "productPrice" + str(index))
                        buy_actions = ActionChains(driver)
                        buy_actions.move_to_element(element)
                        buy_actions.click()
                        buy_actions.perform()
                        item_costs = find_costs()
                        value, temp = find_value(item_costs, item_cps)
                        display(clicker, buyer, scanning, value, temp)
                elif y >= 324 and y <= 370:
                    if len(value) >= 5:
                        index = value.index(temp[4])
                        element = driver.find_element(By.ID, "productPrice" + str(index))
                        buy_actions = ActionChains(driver)
                        buy_actions.move_to_element(element)
                        buy_actions.click()
                        buy_actions.perform()
                        item_costs = find_costs()
                        value, temp = find_value(item_costs, item_cps)
                        display(clicker, buyer, scanning, value, temp)

    if clicker:
        cookie.click()
        time.sleep(0.1)
    if buyer:
        index = value.index(temp[0])
        price = item_costs[index]
        balance = driver.find_element(By.ID, "cookies").text.split()
        amount = float(balance[0].replace(",", ""))
        if balance[1] == "million":
            amount = amount * 10**6
        elif balance[1] == "billion":
            amount = amount * 10**9
        elif balance[1] == "trillion":
            amount = amount * 10**12
        elif balance[1] == "quadrillion":
            amount = amount * 10**15
        if price <= amount:
            element = driver.find_element(By.ID, "productPrice" + str(index))
            buy_actions = ActionChains(driver)
            buy_actions.move_to_element(element)
            buy_actions.click()
            buy_actions.perform()
            x = len(item_costs)
            item_costs = find_costs()
            if len(item_costs) > x:
                item_cps.append(default_cps[len(item_costs) - 1])
            value, temp = find_value(item_costs, item_cps)
    display(clicker, buyer, scanning, value, temp)
