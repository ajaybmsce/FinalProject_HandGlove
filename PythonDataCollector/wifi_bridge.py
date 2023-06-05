import socket
import json
import pandas as pd

UDP_IP = "0.0.0.0"
UDP_PORT = 8080
SAMPLES_PER_SYMBOL = 1000
SYMBOLS = ['0', '1', '2', '3', '4', '5']

columns = ['symbol']
for i in range(6):
    columns.extend([f"{i}_ax", f"{i}_ay", f"{i}_az", f"{i}_gx", f"{i}_gy", f"{i}_gz"])

df = pd.DataFrame(columns=columns)

def record_samples(symbol):
    global df
    samples = []
    print(f"Recording samples for symbol {symbol}")
    for _ in range(SAMPLES_PER_SYMBOL):
        data, addr = UDPClientSocket.recvfrom(2048)
        json_data = json.loads(data.decode('utf-8'))
        sample = {'symbol': symbol}
        for i in range(6):
            sensor_data = json_data[str(i)]
            sample[f"{i}_ax"] = sensor_data['ax']
            sample[f"{i}_ay"] = sensor_data['ay']
            sample[f"{i}_az"] = sensor_data['az']
            sample[f"{i}_gx"] = sensor_data['gx']
            sample[f"{i}_gy"] = sensor_data['gy']
            sample[f"{i}_gz"] = sensor_data['gz']
        samples.append(sample)

    df = df.append(samples, ignore_index=True)
    print(f"Samples recorded for symbol {symbol}")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPClientSocket:
    UDPClientSocket.bind((UDP_IP, UDP_PORT))
    print("Running...")

    for symbol in SYMBOLS:
        input(f"\nPlease make the hand symbol {symbol}. Press Enter when ready...")
        record_samples(symbol)

df.to_csv("hand_gesture_data.csv", index=False)
print("Data recording complete. Saved as hand_gesture_data.csv")

        
