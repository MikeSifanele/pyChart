import json
import pandas as pd

from websocket import create_connection

class BinaryWS:
    def __init__(self, app_id='30508') -> None:
        api_url = f"wss://ws.binaryws.com/websockets/v3?app_id={app_id}"
        self.ws = create_connection(api_url)

    def get_candlesticks(self, symbol='stpRNG', count=10_000_000, period=180, start=1):
        json_data = json.dumps({ 
                                "ticks_history": symbol, "adjust_start_time": 1, "count": count,
                                "end": "latest", "granularity": period, "start": start, "style": "candles"
                                })

        self.ws.send(json_data)

        response = self.ws.recv()

        candles = json.loads(response)['candles']
        

        return pd.DataFrame(candles)

ws = BinaryWS()
candles = ws.get_candlesticks(count=10)

candles