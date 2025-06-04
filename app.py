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
    st.sidebar.title("Weather Forecasting with LLM")
    city = st.sidebar.text_input("Enter city name", "Mumbai")
    
    weather_api_key = "3940c21e08fc4477bd580407250406"
    gemini_api_key = "AIzaSyCuk2E_dLH0GP7RpQbiuy16QHqT5Csw598"
    
    submit = st.sidebar.button("Get Weather")

    if submit:
        st.title("Weather Updates for " + city + " is:")
        with st.spinner('Fetching weather data...'):
            weather_data = get_weather_data(city, weather_api_key)
            
            if "current" in weather_data:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature 🌡️", f"{weather_data['current']['temp_c']:.2f} °C")
                    st.metric("Humidity 💧", f"{weather_data['current']['humidity']}%")
                with col2:
                    st.metric("Pressure", f"{weather_data['current']['pressure_mb']} hPa")
                    st.metric("Wind Speed 💨", f"{weather_data['current']['wind_kph']} km/h")

                explanation = generate_weather_description(weather_data, gemini_api_key)
                st.write(explanation)
                
                # AI Insight on the Weather
                comment = generate_weather_comment(weather_data, gemini_api_key)
                st.markdown("#### AI Insight on the Weather ☁️")
                st.write(comment)

                weekly_data = get_weekly_forecast(city, weather_api_key)
                if "forecast" in weekly_data:
                    st.markdown("#### Weekly Weather Forecast 📅")
                    forecast_list = []
                    for day in weekly_data['forecast']['forecastday']:
                        forecast_list.append({
                            "Date": day['date'],
                            "Condition": day['day']['condition']['text'],
                            "High (°C)": day['day']['maxtemp_c'],
                            "Low (°C)": day['day']['mintemp_c']
                            })
                    df = pd.DataFrame(forecast_list)
                    st.table(df)

if __name__ == "__main__":
    main()
