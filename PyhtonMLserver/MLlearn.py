import tensorflow as tf
import pandas as pd

# Load the dataset from CSV file
data = pd.read_csv('your_dataset.csv')

# Split the dataset into input features (X) and target variable (y)
X = data.drop('symbol', axis=1)
y = data['symbol']

# Convert the target variable to one-hot encoded format
y = pd.get_dummies(y)

# Build the neural network model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(36,)),
    tf.keras.layers.BatchNormalization(),  # Batch normalization layer
    tf.keras.layers.Dropout(0.2),  # Dropout layer
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.BatchNormalization(),  # Batch normalization layer
    tf.keras.layers.Dropout(0.2),  # Dropout layer
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.BatchNormalization(),  # Batch normalization layer
    tf.keras.layers.Dropout(0.2),  # Dropout layer
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.BatchNormalization(),  # Batch normalization layer
    tf.keras.layers.Dropout(0.2),  # Dropout layer
    tf.keras.layers.Dense(6, activation='softmax')  # Output layer with 6 neurons for classification
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10, batch_size=32)

# Save the trained model
model.save('trained_model.h5')

        
