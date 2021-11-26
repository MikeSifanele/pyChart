import websocket
import json

class BinaryWS:    
    def __init__(self) -> None:
        api_url = "wss://ws.binaryws.com/websockets/v3?app_id=CODMT8b2lFKgSLd"
        self.ws = websocket.WebSocketApp(api_url, on_message = self.on_message, on_open = self.on_open)
        self.latest_response = ""

    def on_message(self, ws, message):
        print('Message recieved:')
        self.latest_response = message
        print(message)

    def on_open(self, ws):
        print('Connection open')

    def get_candlesticks(self, symbol='stpRNG', count=10_000_000, period=180):
        json_data = json.dumps({
                                "ticks_history": symbol,
                                "adjust_start_time": 1,
                                "count": count,
                                "end": "latest",
                                "granularity": period,
                                "start": 1,
                                "style": "candles"
                                })
        self.ws.send(json_data)

ws = BinaryWS()
ws.get_candlesticks(count=10)

