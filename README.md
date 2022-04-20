# Get cita previa
This is a python program that facilitates the procedure for getting a CITA PREVIA appointment.
It's intended for two main appointments, "ASIGNACION NIE" and "INFORMACION GENERAL". Any other appoitment type might or might not work.
Feel free to make changes as desired.

## Requirements
* Python3
* Pip3
* Selenium
* Geckodriver
* Firefox

### Installing in Debian based distributions

* Install pip3 and geckodriver
```sh
sudo apt-get install pip3 firefox-geckodriver
```

* Install selenium
```sh
pip3 install selenium
```

### Installing in macOS

* Get pip
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

* Install pip
```sh
python3 get-pip.py
```

* Install selenium
```sh
pip3 install selenium
```

* Install geckodriver
```sh
brew install geckodriver
```

## Running the program
In order to run the program the command is as follows
```
python3 get_cita_previa.py --provincia <province> --ciudad <city> --tipo_cita <appointment_type> --tipo_documento <document_type> --documento <document> --nacimiento <year_birth> --nacionalidad <nationality> --nombre <name> --telefono <phone> --mail <mail>
```
For example
```
python3 get_cita_previa.py --provincia "Illes Balears" --ciudad "MALLORCA" --tipo_cita "INFORMACIÓN GENERAL - MALLORCA" --tipo_documento PASAPORTE --documento AAB123456 --nacimiento 1993 --nacionalidad ITALIA --nombre "JUAN PEREZ" --telefono 624624624 --mail unmail@gmail.com
```

## General Information
You'll have to access https://sede.administracionespublicas.gob.es/icpplus/index.html manually and complete it by hand and use that information to complete the paremeters required for running this program.
This program will run indefinitely. If it's not able to find an appointment the browser will close itself automatically and start again in a lapse of 10 seconds.
Once the program detects there's an available appointment it'll freeze until you finish the process manually.
After that, you can terminate the program.

In case you have misspelled the appointment type you can:
* Type in console again the appointment type to try again (you'll be asked for it in case you've misspelled it). If again it's wrong, the program will start again and give you the chance to write again and so on.
* Terminate the program, correct the misspelled appointment type and start again (check for upper case, lower case, spaces, etc).


# Obtener una Cita Previa
Este es un programa de Python que facilita el procedimiento para obtener una CITA PREVIA.
Esta intencionado para dos tipos principales de citas, "ASIGNACION NIE" e "INFORMACION GENERAL". Cualquier otro tipo de cita puede funcionar o no.
Sientase libre de realizar los cambios que crea convenientes.

## Requerimientos
* Python3
* Pip3
* Selenium
* Geckodriver
* Firefox

### Instalando los requerimientos en distribuciones Debian

* Instalar python3 y geckdriver
```sh
sudo apt-get install pip3 firefox-geckodriver
```

* Instalar selenium
```sh
pip3 install selenium
```

### Instalación en MacOS

* Descargar pip
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

* Instalar pip
```sh
python3 get-pip.py
```

* Instalar selenium
```sh
pip3 install selenium
```

* Instalar geckodriver
```sh
brew install geckodriver
```

## Correr el programa
Para poder correr el programa utilizar el siguiente comando
```
python3 get_cita_previa.py --provincia <province> --ciudad <city> --tipo_cita <appointment_type> --tipo_documento <document_type> --documento <document> --nacimiento <year_birth> --nacionalidad <nationality> --nombre <name> --telefono <phone> --mail <mail>
```
Por ejemplo
```
python3 get_cita_previa.py --provincia "Illes Balears" --city "MALLORCA" --tipo_cita "INFORMACIÓN GENERAL - MALLORCA" --tipo_documento PASAPORTE --documento AAB123456 --nacimiento 1993 --nacionalidad ITALIA --nombre "JUAN PEREZ" --telefono 624624624 --mail unmail@gmail.com
```

## Informacion general
Tendrá que acceder a https://sede.administracionespublicas.gob.es/icpplus/index.html y completar manualmente todos los parámetros requeridos para correr el programa como se muestra en el ejemplo.
Este programa correra indefinidamente. Si no le es posible conseguir una cita, se cerrará Firefox y comenzará nuevamente de forma automática luego de 10 segundos.
Una vez que el programa detecte que hay una cita disponible se detendra y esperará que termine usted el procedimiento manualmente.
Luego de esto usted podrá cerrar el programa.

En caso que haya escrito mal el tipo de cita que desea, usted puede:
* Escribir en la consola nuevamente el tipo de cita que desea (verá las instrucciones necesarias detalladas en la consola). Si nuevamente lo escribe mal, el programa comenzará nuevamente y le dará la oportunidad de escribirlo una vez más (y otra, y otra, ...).
* Cerrar el programa, corregir el tipo de cita y comenzar nuevamente (chequee por mayúsculas, minúsculas, acentos y espacios.
