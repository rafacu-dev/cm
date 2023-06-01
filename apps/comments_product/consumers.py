import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from asgiref.sync import sync_to_async,async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Recoge el nombre de la sala
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Se une a la sala
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Informa al cliente del éxito
        await self.accept()

    async def disconnect(self, close_code):#docker run -p 6379:6379 -d redis:5
        ''' Cliente se desconecta '''
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        ''' Cliente envía información y nosotros la recibimos '''
        text_data_json = json.loads(text_data)
        name = text_data_json["name"]
        text = text_data_json["text"]

        # Enviamos el mensaje a la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "name": name,
                "text": text,
            },
        )

    async def chat_message(self, event):
        ''' Recibimos información de la sala '''
        name = event["name"]
        text = event["text"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "name": name,
                    "text": text,
                }
            )
        )


class SignallingConsumer(WebsocketConsumer):
    def connect(self): 
        print("*-*******************--*-*-*-**************************           connect() is called.")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("disconnect() is called.")

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("receive() is called with " + text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("message contains: " + message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

     # Receive message from room group
    def chat_message(self, event):
        print("the message from the event is: " + event['message'])
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))