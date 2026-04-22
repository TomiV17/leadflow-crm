from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


# =========================
# 🚀 SCRAPER PRINCIPAL
# =========================
def scrape_google_maps(query):

    url = f"https://www.google.com/maps/search/{query}"

    print("SCRAPER INICIADO:", query)

    options = webdriver.ChromeOptions()

    # options.add_argument("--headless=new")  # debug ON

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 12)

    driver.get(url)

    print("CARGANDO URL:", url)

    # =========================
    # 🔥 ESPERAR PRIMEROS RESULTADOS
    # =========================
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "Nv2PK"))
    )

    time.sleep(3)

    # =========================
    # 🔥 SCROLL PARA CARGAR MÁS RESULTADOS
    # =========================
    try:
        scrollable_div = driver.find_element(
            By.XPATH,
            '//div[contains(@aria-label, "Resultados")]'
        )

        for _ in range(5):
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_div
            )
            time.sleep(2)

    except Exception as e:
        print("SCROLL ERROR:", e)

    # =========================
    # 🔥 AHORA SÍ LEVANTAMOS RESULTADOS
    # =========================
    results = driver.find_elements(By.CLASS_NAME, "Nv2PK")

    print("RESULTADOS ENCONTRADOS:", len(results))

    leads = []

    for i in range(min(len(results), 10)):

        try:
            results[i].click()
            time.sleep(2)

            nombre = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "DUwDvf"))
            ).text

            telefono = get_element_text(driver, By.XPATH,
                "//button[contains(@data-item-id,'phone')]")

            direccion = get_element_text(driver, By.XPATH,
                "//button[contains(@data-item-id,'address')]")

            web = get_element_attr(driver, By.XPATH,
                "//a[contains(@data-item-id,'authority')]", "href")

            leads.append({
                "nombre": clean_text(nombre),
                "empresa": nombre,
                "telefono": clean_text(telefono),
                "email": "",
                "web": web,
                "direccion": clean_text(direccion)
            })

            print("LEAD OK:", nombre)

        except Exception as e:
            print("ERROR LEAD:", e)
            continue

    driver.quit()

    print("LEADS FINALES:", len(leads))

    return leads



# =========================
# HELPERS
# =========================
def get_element_text(driver, by, value):
    try:
        return driver.find_element(by, value).text
    except:
        return ""


def get_element_attr(driver, by, value, attr):
    try:
        return driver.find_element(by, value).get_attribute(attr)
    except:
        return ""


def clean_text(text):
    if not text:
        return ""

    return (
        text.replace("\ue0c8", "")
            .replace("\ue0b0", "")
            .replace("\n", " ")
            .strip()
    )
