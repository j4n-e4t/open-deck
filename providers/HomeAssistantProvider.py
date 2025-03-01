import json
import websocket


class HomeAssistantProvider:
    # connects to the WebSocket API
    # and listens for events

    ws = None
    url = None
    token = None
    current_msg_id = 1

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def connect(self):
        try:
            ws_url = (
                self.url.replace("https", "wss").replace("http", "ws")
                + "/api/websocket"
            )
            self.ws = websocket.create_connection(ws_url)
            # Send auth message required by Home Assistant
            auth_msg = {"type": "auth", "access_token": self.token}
            auth_response = json.loads(self.ws.recv())
            self.ws.send(json.dumps(auth_msg))
            auth_response = json.loads(self.ws.recv())
            if auth_response["type"] != "auth_ok":
                raise Exception("Authentication failed")
        except Exception as e:
            print(f"Connection error: {str(e)}")
            raise

    def close(self):
        self.ws.close()

    def send(self, domain, action, entity):
        response = self.ws.send(
            json.dumps(
                {
                    "id": self.current_msg_id,
                    "type": "call_service",
                    "domain": domain,
                    "service": action,
                    "target": {"entity_id": entity},
                }
            )
        )
        self.current_msg_id += 1
        print(response)

    def subscribe(self, event):
        self.ws.send(
            json.dumps(
                {
                    "id": self.current_msg_id,
                    "type": "subscribe_events",
                    "event_type": event,
                }
            )
        )
        self.current_msg_id += 1
