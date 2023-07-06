
import os
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


appID = os.environ.get('appID')
appAPIHash = os.environ.get('appAPIHash')
tokenBot = os.environ.get('tokenBot')

nombreUsuarioTelegram = ''


def sendNotificationTelegram(user,messaje):
    numeroTelefono = '+5351398557'
    clienteTelegram = TelegramClient('sesión', appID, appAPIHash)
    clienteTelegram.connect()
    
    if not clienteTelegram.is_user_authorized():
        clienteTelegram.send_code_request(numeroTelefono)
        # Pedimos el código de inicio de sesión que haya enviado Telegram al usuario
        try:
            if "sesionCode" in os.environ:
                clienteTelegram.sign_in(numeroTelefono, os.environ.get('sesionCode'))
            else:
                clienteTelegram.sign_in(numeroTelefono, input('Introduzca el Código de inicio de sesión: '))
        except SessionPasswordNeededError:
            clienteTelegram.sign_in(numeroTelefono, input('Introduzca la contraseña: '))
    
    try:    
        print("Creando un receptor de Telegram a partir del nombre de usuario de Tetlegram...")
        receptorNombre = clienteTelegram.get_input_entity(user)
        
        async def main():
            # Enviamos el mensaje al chat de Telegram
            # Se enviará al chat de Telegram del Bot con el usuario indicado en el receptor
            print("Enviando mensaje a chat de Bot del receptor de Telegram (usuario)...")
            await clienteTelegram.send_message(receptorNombre, messaje)
            print("Enviado mensaje a chat de Bot del receptor [{}] de Telegram".format(user))
    
        clienteTelegram.loop.run_until_complete(main()) # Para que se ejecute la tarea anterior del método asíncrono
    
    except Exception as e:
        print("Se ha producido un error en el envío por nombre de usuario: {}".format(e))
    
    clienteTelegram.disconnect()

sendNotificationTelegram()

sendNotificationTelegram("@MaileenBarbarita","Probando...")