from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# URL de la página a scrapear
cnn_url = "https://www.rspb.org.uk/birds-and-wildlife/aquatic-warbler"
#cnn_url = "https://www.rspb.org.uk/birds-and-wildlife/arctic-tern"

# Función para scrapear con Selenium
def scrape_with_selenium(url):
    options = Options()
    options.headless = False  # Establecer en True para ejecutar en modo headless
    driver = webdriver.Chrome(options=options)

    # Navegar a la página
    driver.get(url)

    # Aceptar cookies
    # Buscar el botón "Accept All" dentro del div con clase buttons y hacer clic en el botón
    try:
        # Usar el selector CSS para buscar el botón dentro del div con clase buttons
        accept_button = driver.find_element(By.CSS_SELECTOR, 'rspb-cookie-banner .buttons button.btn-primary')
        accept_button.click()  # Hacer clic en el botón "Accept All"
    except Exception as e:
        print("No se pudo hacer clic en el botón de aceptar cookies:", e)

    ## ESTA PARTE DE ARRIBA FUNCIONA ##

    # Esperar a que el contenido dinámico cargue
    time.sleep(3)

    # Extraer y mostrar el nombre del pajaro
    nombreP = driver.find_elements(By.TAG_NAME, 'h1')
    for nombre in nombreP:
        print(nombre.text)

    # Extraer y mostrar el nombre cientifico del pajaro
    nombreC = driver.find_elements(By.CSS_SELECTOR, 'span.info.latin')
    for nombrePC in nombreC:
        print(nombrePC.text)

    # Extraer y mostrar el grupo del pajaro
    grupoP = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-rspb-frontend-app-c287].info.ng-star-inserted')
    for grupo in grupoP:
        print(grupo.text)

    # Extraer y mostrar la foto del pajaro
    fotoP = driver.find_elements(By.CSS_SELECTOR, 'img[_ngcontent-rspb-frontend-app-c201]')
    print(fotoP[0].get_attribute('src'))

     # Extraer y mostrar la identificacion del pajaro
    ideP = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-rspb-frontend-app-c287].intro')
    for ide in ideP:
        print(ide.text)

    # Extraer y mostrar el canto del pajaro
    enlace = driver.find_element(By.CSS_SELECTOR, 'a[_ngcontent-rspb-frontend-app-c63]')
    url = enlace.get_attribute('href')
    print(url)

    bird_data_list = []  # Lista para almacenar cada pájaro con su nombre y ubicación

    # Extraer los nombres
    nombreL = driver.find_elements(By.CSS_SELECTOR, 'span.custom-title')
    nombres = [nombre.text for nombre in nombreL] if nombreL else []

    # Extraer las ubicaciones
    ubicacionL = driver.find_elements(By.CSS_SELECTOR, 'span.custom-subtitle')
    ubicaciones = [ubicacion.text for ubicacion in ubicacionL] if ubicacionL else []

    # Asegurar que ambos tengan el mismo número de elementos
    if len(nombres) == len(ubicaciones):
        for nombre, ubicacion in zip(nombres, ubicaciones):
            bird_data_list.append({
                'nombre': nombre,
                'ubicacion': ubicacion
            })
    else:
        print("Error: La cantidad de nombres y ubicaciones no coincide.")

    # Mostrar el resultado
    for bird in bird_data_list:
        print(bird)




    # Cerrar el navegador
    driver.quit()

# Ejecutar el scraping
scrape_with_selenium(cnn_url)

## ESTA PARTE DE ARRIBA FUNCIONA ##
