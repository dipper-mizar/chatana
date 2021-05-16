from django.http import HttpResponse

connections = []
senders = []


class WebSocketHandler:
    @staticmethod
    def connect(request):
        """Connect to web socket server and send something
         that is from the client to the others
         """
        if request.is_websocket():
            connections.append(request.websocket)
            for message in request.websocket:
                if type(message) is None:
                    message = str(message, encoding='utf-8')
                for connection in connections:
                    if connection != request.websocket:
                        try:
                            connection.send(message)
                        except Exception as e:
                            return HttpResponse('Unknown error occurred '
                                                'when server returned messages(expected)!')

    @staticmethod
    def asgi_send(send, message):
        senders.append(send)
        for sender in senders:
            send({
                'type': 'websocket.send',
                'text': message['text']
            })
