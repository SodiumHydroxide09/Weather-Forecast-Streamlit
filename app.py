import streamlit as st 
import requests
import google.generativeai as genai
import pandas as pd

def get_weather_data(city, weather_api_key):
    base_url = "http://api.weatherapi.com/v1/current.json"
    complete_url = base_url + "?key=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()

def generate_weather_description(data, gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')

    try:
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        prompt = f"The current weather in your city is {description} with a temperature of {temperature:.1f}°C. Explain this in a simple way for a general audience."
        response = model.generate_content(prompt) 
        return response.text
    except Exception as e:
        return str(e)

def generate_weather_comment(data, gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')

    try:
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        prompt = f"The current weather is '{description}' and the temperature is {temperature:.1f}°C. Give a short, friendly comment on this weather for a general user."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return str(e)

def get_weekly_forecast(city, weather_api_key):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    complete_url = base_url + "?key=" + weather_api_key + "&q=" + city + "&days=7"
    response = requests.get(complete_url)
    return response.json()

def main():
    st.set_page_config(page_title="LLM-Powered Weather App", page_icon="⛅", layout="wide")

    st.sidebar.title("🌤️ Weather Forecasting with AI")
    city = st.sidebar.text_input("Enter city name", "Mumbai")

    weather_api_key = "3940c21e08fc4477bd580407250406"
    gemini_api_key = "AIzaSyCuk2E_dLH0GP7RpQbiuy16QHqT5Csw598"

    submit = st.sidebar.button("🔍 Get Weather")

    if not submit:
        # --- Homepage UI ---
        st.markdown(
            """
            <div style='text-align: center; padding: 2rem 1rem;'>
                <h1 style='color: #4A90E2; font-size: 3rem;'>🌍 Welcome to AI Weather Insight</h1>
                <h3 style='color: #6c757d;'>Your daily forecast with smart, simple explanations ✨</h3>
                <p style='font-size: 1.2rem; max-width: 600px; margin: 1rem auto;'>
                    This app gives you the current weather, AI-generated explanations, friendly comments,
                    and a 7-day forecast using the power of LLMs.
                </p>
                <img src='https://cdn-icons-png.flaticon.com/512/1779/1779940.png' width='180'>
                <p style='color: #888;'>Start by entering your city name in the sidebar </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if submit:
        st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌍 Weather Report for " + city + "</h1>", unsafe_allow_html=True)
        with st.spinner('⏳ Fetching latest weather updates...'):
            weather_data = get_weather_data(city, weather_api_key)

            if "current" in weather_data:
                st.markdown("## 📊 Current Weather Metrics")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🌡️ Temperature", f"{weather_data['current']['temp_c']:.2f} °C")
                col2.metric("💧 Humidity", f"{weather_data['current']['humidity']}%")
                col3.metric("🔵 Pressure", f"{weather_data['current']['pressure_mb']} hPa")
                col4.metric("💨 Wind Speed", f"{weather_data['current']['wind_kph']} km/h")

                st.divider()

                st.markdown("## 📘 Easy Explanation")
                explanation = generate_weather_description(weather_data, gemini_api_key)
                st.success(explanation)

                st.markdown("## 🤖 AI Insight on the Weather")
                comment = generate_weather_comment(weather_data, gemini_api_key)
                st.warning(comment)

                st.divider()

                weekly_data = get_weekly_forecast(city, weather_api_key)
                if "forecast" in weekly_data:
                    st.markdown("## 📅 Weekly Weather Forecast")
                    forecast_list = []
                    for day in weekly_data['forecast']['forecastday']:
                        forecast_list.append({
                            "📆 Date": day['date'],
                            "🌤️ Condition": day['day']['condition']['text'],
                            "🔺 High (°C)": day['day']['maxtemp_c'],
                            "🔻 Low (°C)": day['day']['mintemp_c']
                        })
                    df = pd.DataFrame(forecast_list)
                    st.table(df)
            else:
                st.error("❌ Failed to fetch weather data. Please check the city name or try again later.")

if __name__ == "__main__":
    main()
