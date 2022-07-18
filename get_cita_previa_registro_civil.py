import argparse
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys

from helpers.webdriver.find_element import find_element_by_id_and_send_keys, \
    find_element_by_id_and_click_it_with_javascript
from helpers.webdriver.select_element import select_element_by_visible_text_and_id
from helpers.webdriver.waits import wait_presence_of_element_located_by_id

parser = argparse.ArgumentParser()
parser.add_argument('--provincia', type=str,
                    help='Nombre de la provincia en la cual desea obtener una cita. Ej: "Illes Balears"')
parser.add_argument('--tipo_documento', type=str, choices=['NIE', 'DNI', 'PASAPORTE'],
                    help='El tipo de documento con el que realizara el pedido de cita. NIE, DNI o PASAPORTE')
parser.add_argument('--documento', type=str, help='El numero de documento en cuestion con el que realizara el tramite')
parser.add_argument('--nacimiento', type=str, help='El año de su nacimiento en formato de 4 números. Ej: 1987, 1993')
parser.add_argument('--nacionalidad', type=str, help='El país de nacionalidad de su documento')
parser.add_argument('--nombre', type=str, help='El nombre completo de la persona que va realizar el tramite')
parser.add_argument('--telefono', type=str,
                    help='Su numero de telefono. Solo se aceptan telefonos españoles. NO anteponga el prefijo "+34"')
parser.add_argument('--mail', type=str, help='El mail en el cual desea recibir los datos de su cita')
args = parser.parse_args()

PROVINCE = args.provincia
DOCUMENT_TYPE = args.tipo_documento
DOCUMENT = args.documento
BIRTH_YEAR = args.nacimiento
NATIONALITY = args.nacionalidad
NAME = args.nombre
PHONE = args.telefono
MAIL = args.mail

options = FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

appointment_available = False

while not appointment_available:
    try:
        print('Loading cita previa website')
        driver.get("https://sede.administracionespublicas.gob.es/icpplustiej/citar?i=es&org=JUS-RC")

        # Waiting for login page to be fully loaded
        wait_presence_of_element_located_by_id(driver, 5, 'portadaForm')

        # Select appointment province
        print('Filling in office data')
        find_element_by_id_and_send_keys(driver, 'provincia', [Keys.ARROW_DOWN])
        select_element_by_visible_text_and_id(driver, 'provincia', PROVINCE)

        # Select appointment office
        wait_presence_of_element_located_by_id(driver, 5, 'sede')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        find_element_by_id_and_send_keys(driver, 'sede', [Keys.ARROW_DOWN])
        select_element_by_visible_text_and_id(driver, 'sede',
                                              'REGISTRO CIVIL Nº 1 PALMA MALLORCA, TRAVESSIA D\'EN BALLESTER, 20')

        # Select appointment type NACIONALIDAD
        wait_presence_of_element_located_by_id(driver, 5, 'tramiteGrupo[4]')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        find_element_by_id_and_send_keys(driver, 'tramiteGrupo[4]', [Keys.ARROW_DOWN])
        select_element_by_visible_text_and_id(driver, 'tramiteGrupo[4]',
                                              'NACIONALIDAD: OPCIÓN DE NACIONALIDAD ESPAÑOLA CUANDO EL INTERESADO SEA MAYOR DE 18 AÑOS O EMANCIPADO')

        # Click Aceptar
        find_element_by_id_and_click_it_with_javascript(driver, 'btnAceptar')

        # Scroll to end of page
        wait_presence_of_element_located_by_id(driver, 5, 'btnEntrar')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # Click Entrar
        find_element_by_id_and_click_it_with_javascript(driver, 'btnEntrar')

        # Complete document data
        wait_presence_of_element_located_by_id(driver, 5, 'txtIdCitado')
        print('Filling in passport, name and nationality data')

        # Click document type option
        find_element_by_id_and_click_it_with_javascript(driver, 'rdbTipoDocPas')

        # Fill passport data
        find_element_by_id_and_send_keys(driver, 'txtIdCitado', [DOCUMENT])

        # Fill full name
        find_element_by_id_and_send_keys(driver, 'txtDesCitado', [NAME])

        # Fill birthdate
        find_element_by_id_and_send_keys(driver, 'txtAnnoCitado', [BIRTH_YEAR])

        # Fill nationality
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        find_element_by_id_and_send_keys(driver, 'txtPaisNac', [Keys.ARROW_DOWN])
        select_element_by_visible_text_and_id(driver, 'txtPaisNac', NATIONALITY)

        # Click Aceptar
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        find_element_by_id_and_click_it_with_javascript(driver, 'btnEnviar')

        # Click Enviar
        wait_presence_of_element_located_by_id(driver, 5, 'btnConsultar')
        find_element_by_id_and_click_it_with_javascript(driver, 'btnEnviar')

        # Complete data
        wait_presence_of_element_located_by_id(driver, 5, 'txtTelefonoCitado')
        print('Filling in appointment data')
        find_element_by_id_and_send_keys(driver, 'txtTelefonoCitado', [PHONE])

        find_element_by_id_and_send_keys(driver, 'emailUNO', [MAIL])
        find_element_by_id_and_send_keys(driver, 'emailDOS', [MAIL])

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        find_element_by_id_and_send_keys(driver, 'txtObservaciones', [
            'ACTO JURA AL REY Y LA CONSTITUCION POR CONCESION DE LA NACIONALIDAD ESPAÑOLA POR JUDEIDAD SEFARADI'])

        find_element_by_id_and_send_keys(driver, 'txtIdExtranjero', [DOCUMENT])

        find_element_by_id_and_send_keys(driver, 'txtDesExtranjero', [NAME])

        # Click Next button
        print('Requesting appointment')
        find_element_by_id_and_click_it_with_javascript(driver, 'btnSiguiente')

        try:
            wait_presence_of_element_located_by_id(driver, 5, 'cita_1')
            find_element_by_id_and_click_it_with_javascript(driver, 'cita_1')

            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            find_element_by_id_and_click_it_with_javascript(driver, 'btnSiguiente')

            driver.switch_to.alert.accept()

            wait_presence_of_element_located_by_id(driver, 5, 'chkTotal')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            find_element_by_id_and_click_it_with_javascript(driver, 'chkTotal')

            find_element_by_id_and_click_it_with_javascript(driver, 'enviarCorreo')

            find_element_by_id_and_click_it_with_javascript(driver, 'aceptaRgpd')

            find_element_by_id_and_click_it_with_javascript(driver, 'btnConfirmar')

            appointment_available = True

        except TimeoutException:
            # In case there're no appointments available we'll sleep this for 5 minutes
            print('No appointments available\n')
            time.sleep(300)
            driver.close()
            driver.quit()
            driver = webdriver.Firefox(options=options)

    except Exception as ex:
        print(ex)
        # 5 minutes sleep
        time.sleep(300)
        driver.close()
        driver.quit()
        driver = webdriver.Firefox(options=options)
