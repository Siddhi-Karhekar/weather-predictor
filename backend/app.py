from flask import Flask, render_template, request
import requests
import os
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv("OWM_API_KEY")
print("Loaded API Key:", API_KEY)
# Prometheus metrics
REQUEST_COUNT = Counter("weather_requests_total", "Total number of weather requests")
TEMPERATURE_GAUGE = Gauge("weather_temperature_celsius", "Current temperature in Celsius")
HUMIDITY_GAUGE = Gauge("weather_humidity_percent", "Current humidity percentage")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = {}
    if request.method == "POST":
        REQUEST_COUNT.inc()
        city = request.form["city"]
        if not API_KEY:
            weather = {"error": "Missing OpenWeatherMap API Key"}
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") == 200:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]

                # Update Prometheus metrics
                TEMPERATURE_GAUGE.set(temp)
                HUMIDITY_GAUGE.set(humidity)

                # Simple "prediction" logic
                predicted_temp = round(temp + 0.5, 2)

                weather = {
                    "city": city,
                    "temp": temp,
                    "desc": desc,
                    "humidity": humidity,
                    "predicted_temp": predicted_temp
                }
            else:
                weather = {"error": "City not found"}
    return render_template("index.html", weather=weather)


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

