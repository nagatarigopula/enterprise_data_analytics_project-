import tensorflow as tf
import pandas as pd

df = pd.read_csv("data/processed/customer_churn.csv")
X = df[['clicks', 'time_spent', 'visits']]
y = df['churn_label']

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=10, batch_size=32)
model.save("models/customer_churn_nn.h5")
