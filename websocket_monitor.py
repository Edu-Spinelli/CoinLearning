import websocket
import json
import pandas as pd
from datetime import datetime

# Nome do arquivo CSV onde os dados serão armazenados
csv_file = 'sagausdt_data.csv'

# Função chamada quando uma mensagem é recebida
def on_message(ws, message):
    data = json.loads(message)
    symbol = data['s']  # Símbolo da moeda
    price = float(data['c'])  # Preço atual como float
    price = f"{price:.4f}"  # Formatando com 4 dígitos após a vírgula
    timestamp = datetime.utcfromtimestamp(data['E'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    
    # Exibindo no console
    print(f"{symbol} - Preço: {price} - Hora: {timestamp}")
    
    # Salvando no CSV
    df = pd.DataFrame([[timestamp, symbol, price]], columns=['timestamp', 'symbol', 'price'])
    df.to_csv(csv_file, mode='a', header=not pd.io.common.file_exists(csv_file), index=False)

# Função chamada em caso de erro
def on_error(ws, error):
    print(f"Erro: {error}")

# Função chamada quando a conexão é fechada
def on_close(ws):
    print("Conexão fechada")

# Função chamada quando a conexão é aberta
def on_open(ws):
    print("Conexão aberta")

# URL do WebSocket para o par SAGAUSDT
url = "wss://stream.binance.com:9443/ws/sagausdt@ticker"

# Criação do WebSocket
ws = websocket.WebSocketApp(url, 
                            on_message=on_message, 
                            on_error=on_error, 
                            on_close=on_close)

# Define o que fazer ao abrir a conexão
ws.on_open = on_open

# Mantém a conexão aberta
ws.run_forever()
