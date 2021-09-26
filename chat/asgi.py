import os

from django.core.asgi import get_asgi_application
from django.utils.translation import gettext_lazy as _

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

http_application = get_asgi_application()
senders = []


async def websocket_application(scope, receive, send):
    senders.append(send)
    while True:
        message = await receive()
        if message['type'] == 'websocket.connect':
            await send({'type': 'websocket.accept'})
        elif message['type'] == 'websocket.disconnect':
            break
        elif message['type'] == 'websocket.receive':
            print(_('Received message: '), message['text'])
            if message['text'] is not None:
                # WebSocketHandler().asgi_send(send, message)
                for sender in senders:
                    await sender({
                            'type': 'websocket.send',
                            'text': message['text']
                    })
        else:
            pass


async def application(scope, receive, send):
    if scope['type'] == 'http':
        await http_application(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_application(scope, receive, send)
    else:
        raise Exception(_('Unknown scope type!'))
