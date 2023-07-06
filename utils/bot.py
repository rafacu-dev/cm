
import os, time
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from utils.models import Config


appID = '21975200'
appAPIHash = 'a2ad281bef0e2dc939f7d1bd0373540a'
tokenBot = '5644960260:AAGQyWU5LbInVlgxoLMGoZU0uztgm7qxPzk'

def sendNotificationTelegram(user,messaje):
    numeroTelefono = '+5351398557'
    clienteTelegram = TelegramClient('sesión', appID, appAPIHash)
    clienteTelegram.connect()
    
    if not clienteTelegram.is_user_authorized():
        # Pedimos el código de inicio de sesión que haya enviado Telegram al usuario
        clienteTelegram.send_code_request(numeroTelefono)
        try:
            while True:
                sesionCode = Config.objects.filter(key="sesionCode")
                print("Leyendo codigo de inicio de sesion")
                if sesionCode.exists():
                    clienteTelegram.sign_in(numeroTelefono, sesionCode[0].value)
                    print("Insertando código de sesión")
                    break
                time.sleep(2)
                

        except SessionPasswordNeededError:
            return
            #clienteTelegram.sign_in(numeroTelefono, input('Introduzca la contraseña: '))
    
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

#sendNotificationTelegram("@MaileenBarbarita","Probando...")