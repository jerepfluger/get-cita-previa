import argparse
import time

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument('--provincia', type=str, help='Nombre de la provincia en la cual desea obtener una cita. Ej: "Illes Balears"')
parser.add_argument('--ciudad', type=str, help='Nombre de la ciudad en la cual desea obtener una cita. Ej: "MALLORCA"')
parser.add_argument('--tipo_cita', type=str, help='El tipo de Cita que desea obtener. Ej: "INFORMACION GENERAL - IBIZA", "POLICIA-CERTIFICADOS Y ASIGNACION NIE"')
parser.add_argument('--tipo_documento', type=str, choices=['NIE', 'DNI', 'PASAPORTE'], help='El tipo de documento con el que realizara el pedido de cita. NIE, DNI o PASAPORTE')
parser.add_argument('--documento', type=str, help='El numero de documento en cuestion con el que realizara el tramite')
parser.add_argument('--nacimiento', type=str, help='El año de su nacimiento en formato de 4 números. Ej: 1987, 1993')
parser.add_argument('--nacionalidad', type=str, help='El país de nacionalidad de su documento')
parser.add_argument('--nombre', type=str, help='El nombre completo de la persona que va realizar el tramite')
parser.add_argument('--telefono', type=str, help='Su numero de telefono. Solo se aceptan telefonos españoles. NO anteponga el prefijo "+34"')
parser.add_argument('--mail', type=str, help='El mail en el cual desea recibir los datos de su cita')
parser.add_argument('--elegir_cita_automaticamente', type=str, choices=['SI', 'NO'], help='En caso que elija "SI" el sistema automáticamente le elegira la primer cita disponible. En caso de elegir "NO" usted podrá elegir la cita de su mayor conveniencia')
args = parser.parse_args()

PROVINCE = args.provincia
CITY = args.ciudad
APPOINTMENT_TYPE = args.tipo_cita
DOCUMENT_TYPE = args.tipo_documento
DOCUMENT = args.documento
BIRTH_YEAR = args.nacimiento
NATIONALITY = args.nacionalidad
NAME = args.nombre
PHONE = args.telefono
MAIL = args.mail
POLICE_APPOINTMENTS = {'POLICIA', 'POLICÍA', 'CERTIFICADO', 'AUTORIZACIÓN', 'ASILO', 'ASIGNACIÓN'}


options = FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)


def get_appointment_type_id(appointment_type):
    if appointment_type.split()[0].split('-')[0].upper() in POLICE_APPOINTMENTS:
        return 'tramiteGrupo[1]'

    return 'tramiteGrupo[0]'


def print_choosing_appointment_message():
    print('NO CIERRE EL PROGRAMA AÚN!')
    print('Debe seleccionar en este punto la cita deseada y luego completar con los datos faltantes')
    print('Una vez que tenga confirmada su cita ya podrá cerrar el programa')


def get_city_text(city_options):
    for city in city_options:
        if CITY.upper() in city:
            return city
    return ''


appointment_available = False


while not appointment_available:
    try:
        driver.get("https://icp.administracionelectronica.gob.es/icpplus/index.html")

        # Waiting for login page to be fully loaded
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'form')))
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        city_selector = Select(driver.find_element(By.ID, 'form'))
        city_selector.select_by_visible_text(PROVINCE)
        # Click Aceptar
        accept_button = driver.find_element(By.ID, 'btnAceptar')
        driver.execute_script("arguments[0].click();", accept_button)

        # Select procedure
        appointment_id = get_appointment_type_id(APPOINTMENT_TYPE)
        print(appointment_id)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, appointment_id)))
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
        procedure_selector = Select(driver.find_element(By.ID, appointment_id))
        try:
            #procedure_selector.select_by_visible_text(APPOINTMENT_TYPE)
            procedure_selector.select_by_value('4031')
        except NoSuchElementException:
            print('El trámite seleccionado no fue bien escrito. Revise por mayúsculas, minisculas o acentos que puedan estar mal escritor')
            print('El texto introducido debe ser exactamente igual a como esta escrito en la web. Escriba nuevamente el trámite que desea realizar y presione ENTER')
            APPOINTMENT_TYPE = input('En caso de haberlo escrito erroneamente una vez más el programa volverá a iniciar de manera automática y tendrá infinitas chances de probar')
            appointment_id = get_appointment_type_id(APPOINTMENT_TYPE)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
            procedure_selector = Select(driver.find_element(By.ID, appointment_id))
            procedure_selector.select_by_visible_text(APPOINTMENT_TYPE)
        # Click Aceptar
        accept_button = driver.find_element(By.ID, 'btnAceptar')
        driver.execute_script("arguments[0].click();", accept_button)

        # Click Aceptar
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'btnAceptar')))
        accept_button = driver.find_element(By.ID, 'btnAceptar')
        driver.execute_script("arguments[0].click();", accept_button)

        # Click Entrar
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'btnEntrar')))
        enter_button = driver.find_element(By.ID, 'btnEntrar')
        driver.execute_script("arguments[0].click();", enter_button)

        # Complete document data
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'txtIdCitado')))
        if DOCUMENT_TYPE.upper() != 'NIE':
            if DOCUMENT_TYPE.replace('.', '').upper() == 'DNI':
                dni_button = driver.find_element(By.ID, 'rdbTipoDocDni')
                driver.execute_script("arguments[0].click();", dni_button)
            else:
                passport_button = driver.find_element(By.ID, 'rdbTipoDocPas')
                driver.execute_script("arguments[0].click();", passport_button)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'txtIdCitado')))
        document_input = driver.find_element(By.ID, 'txtIdCitado')
        document_input.send_keys(DOCUMENT)

        name_lastname_input = driver.find_element(By.ID, 'txtDesCitado')
        name_lastname_input.send_keys(NAME)

        try:
            year_input = driver.find_element(By.ID, 'txtAnnoCitado')
            year_input.send_keys(BIRTH_YEAR)
        except NoSuchElementException:
            pass
        try:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            nationality_selector = Select(driver.find_element(By.ID, 'txtPaisNac'))
            #nationality_selector.select_by_visible_text(NATIONALITY)
            nationality_selector.select_by_value('117')
        except NoSuchElementException:
            pass

        # Click Aceptar
        accept_button = driver.find_element(By.ID, 'btnEnviar')
        driver.execute_script("arguments[0].click();", accept_button)
        time.sleep(3)

        # Click Enviar
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'btnEnviar')))
        send_button = driver.find_element(By.ID, 'btnEnviar')
        driver.execute_script("arguments[0].click();", send_button)
        time.sleep(3)

        try:
            options = driver.find_element(By.ID, 'idSede').text.split('\n')
            city_text = get_city_text(options)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            if city_text:
                office_selector = Select(driver.find_element(By.ID, 'idSede'))
                office_selector.select_by_visible_text(city_text)
            else:
                office_selector = driver.find_element(By.ID, 'idSede')
                driver.execute_script("arguments[0].click();", office_selector)
                office_selector.send_keys(Keys.DOWN)
                office_selector.send_keys(Keys.ENTER)
            # Click Siguiente
            next_button = driver.find_element(By.ID, 'btnSiguiente')
            driver.execute_script("arguments[0].click();", next_button)
        except NoSuchElementException:
            # This is used only in case we're asked to select an office in which case we'll select the first available option
            pass
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'txtTelefonoCitado')))
            # Complete data
            phone_text_input = driver.find_element(By.ID, 'txtTelefonoCitado')
            phone_text_input.send_keys(PHONE)
            email_text_input = driver.find_element(By.ID, 'emailUNO')
            email_text_input.send_keys(MAIL)
            confirm_email_input_text = driver.find_element(By.ID, 'emailDOS')
            confirm_email_input_text.send_keys(MAIL)
            # Click Next button
            next_button = driver.find_element(By.ID, 'btnSiguiente')
            driver.execute_script("arguments[0].click();", next_button)

            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'cita_1')))
            print_choosing_appointment_message()
            appointment_available = True

        except (TimeoutException, NoSuchElementException):
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
