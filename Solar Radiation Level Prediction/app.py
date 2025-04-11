from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model from the pickle file
with open('ml_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Extract hour from time input
def extract_hour(time_str):
    h, _, _ = map(int, time_str.split(':'))
    return h

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input values from the form
    time = request.form['time']
    temperature = float(request.form['temperature'])
    pressure = float(request.form['pressure'])
    humidity = float(request.form['humidity'])
    wind_direction = float(request.form['wind_direction'])
    speed = float(request.form['speed'])

    # Convert the time to the hour (in integer)
    hour = extract_hour(time)

    # Prepare the input feature vector for prediction
    input_features = np.array([[hour, temperature, pressure, humidity, wind_direction, speed]])

    # Make prediction
    predicted_radiation = model.predict(input_features)[0]

    # Determine the category based on predicted radiation
    if predicted_radiation < 700:
        category = "SAFE"
        warning_message = """Warning: Generally safe for short periods in the sun, but still exposes you to UV risk.
                            <br>Precautions:
                            <ul>
                                <li>Use sunscreen with SPF 30 or higher.</li>
                                <li>Wear protective clothing and sunglasses.</li>
                                <li>Seek shade when possible, especially during peak sunlight hours (10 am to 4 pm).</li>
                            </ul>"""
    elif 700 <= predicted_radiation <= 990:
        category = "MODERATE"
        warning_message = """Warning: Prolonged exposure may lead to sunburn, skin aging, and increased long-term skin cancer risk.
                            <br>Precautions:
                            <ul>
                                <li>Limit direct sun exposure to 20-30 minutes.</li>
                                <li>Apply broad-spectrum sunscreen regularly.</li>
                                <li>Wear protective clothing, a wide-brimmed hat, and sunglasses.</li>
                                <li>Reapply sunscreen every 2 hours, especially after sweating or swimming.</li>
                            </ul>"""
    else:
        category = "UNSAFE"
        warning_message = """Warning: High risk of sunburn, eye damage, and long-term skin damage leading to skin cancer.
                            <br>Precautions:
                            <ul>
                                <li>Avoid prolonged sun exposure.</li>
                                <li>Seek shade or stay indoors during peak radiation hours.</li>
                                <li>Use high SPF sunscreen, and wear UV-protective clothing and sunglasses.</li>
                                <li>Stay hydrated and take frequent breaks from the sun.</li>
                            </ul>"""

    return render_template('results.html', predicted_radiation=predicted_radiation, category=category, warning_message=warning_message)

if __name__ == "__main__":
    app.run(debug=True)
