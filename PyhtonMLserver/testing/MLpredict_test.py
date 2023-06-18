import socket
import json
import tensorflow as tf
import numpy as np

UDP_IP = "0.0.0.0"
UDP_PORT = 8080

# Load the trained model
model = tf.keras.models.load_model('trained_model.h5')

# Create a UDP socket
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocket.bind((UDP_IP, UDP_PORT))
print("ML Server running...")

while True:
    data, addr = UDPClientSocket.recvfrom(2048)
    json_data = json.loads(data.decode('utf-8'))

    # Extract the sensor values from the received JSON data
    sensor_values = []
    for i in range(6):
        sensor_values.extend(list(json_data[str(i)].values()))

    # Convert the sensor values to a numpy array
    input_data = np.array(sensor_values).reshape(1, 36)

    # Perform prediction using the loaded model
    prediction = model.predict(input_data)
    predicted_class = np.argmax(prediction)

    print("Predicted class:", predicted_class)

  