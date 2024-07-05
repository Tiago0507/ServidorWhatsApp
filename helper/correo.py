# Se crea un entorno virtual con python -m venv myvenv, por myvenv puede estar el nombre que queramos. Luego con Ctrl+Shift+P
# seleccionamos el intérprete recomendado que está en la raíz del entorno virtual que se creó, es decir, myvenv

# Se instala el dotenv con pip install python-dotenv para poder definir variables de entorno que va a usar el script.
# Estas variables se definen en el archivo .env que debe llamarse sí o sí así

import smtplib # Librería para trabajar con correos en Python

# Al crear un correo en Python es como si estuviéramos haciendo Legos, lo vamos construyendo por medio de diferentes partes
from email.mime.multipart import MIMEMultipart # Le damos la estructura al correo
from email.mime.text import MIMEText # Se encarga de la parte de texto
from email.mime.image import MIMEImage # Se encarga de la parte de las imágenes
import os # Módulo del sistema operativo. Por medio de este cargaremos las variables del .env a las variables de entorno del
# sistema donde lo estemos ejecutando

from dotenv import load_dotenv # Módulo que permite cargar el .env

class EmailSender():
    def __init__(self):
        load_dotenv() # Se carga el .env. Es importante que esta línea esté de primera
        self.sender = os.getenv('USER') # Le pasamos la llave bajo la cual está la variable de entorno que queremos obtener
        # Accedemos al SMTP del gmail. Se accede mediante esa dirección y ese puerto. Recordar que SMTP es un protocolo
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls() # Esta línea permite una comunicación segura entre nosotros y el servidor de gmail
        # Se hace login con los datos que están en el .env
        self.server.login(self.sender, os.getenv('PASS'))

    def send_email(self, receiver, subject, content, image=None):
        message = MIMEMultipart() # Le da la estructura más básica para crear un correo
        # Le damos los datos necesarios para enviar el correo en formato diccionario
        message['Subject'] = subject
        message['From'] = self.sender
        message['To'] = receiver
        # Se adjunta el contenido del correo con el attach, y se le da un formato html en caso de que tenga html interno
        message.attach(MIMEText(content, 'html'))

        if image is not None:
            # Se abre la imagen con permisos de lectura binaria
            with open(image, 'rb') as file:
                read_image = MIMEImage(file.read())
                # Se añade un header para referenciar la imagen dentro del correo electrónico. Ya con esto creamos la imagen
                read_image.add_header('Content-ID', '<image1>')
                message.attach(read_image) # Se añade la imagen al cuerpo del correo
        # Se envía el correo
        self.server.sendmail(self.sender, receiver, message.as_string())

    def close_connection(self):
        self.server.quit() # Se cierra la conexión con el servidor de gmail

if __name__ == '__main__':
    email = EmailSender()
    email.send_email('daniva0610@gmail.com', 'Prueba envío de correo con Python', 'Hola jeje')
    email.close_connection()