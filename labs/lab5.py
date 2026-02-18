import requests
import streamlit as st
from openai import OpenAI

st.title('Lab 5: OpenWeather API')

api_key = st.secrets['EddieOpenWeather_API_KEY']
# location in form City, State, Country
# e.g., Syracuse, NY, US
# default units is degrees Fahrenheit
def get_current_weather(location, units='imperial'):
    url = (
    f'https://api.openweathermap.org/data/2.5/weather'
    f'?q={location}&appid={api_key}&units={units}'
    )
    response = requests.get(url)
    if response.status_code == 401:
        raise Exception('Authentication failed: Invalid API key (401 Unauthorized)')
    if response.status_code == 404:
        error_message = response.json().get('message')
        raise Exception(f'404 error: {error_message}')
    data = response.json()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    return {'location': location,
    'temperature': round(temp, 2),
    'feels_like': round(feels_like, 2),
    'temp_min': round(temp_min, 2),
    'temp_max': round(temp_max, 2),
    'humidity': round(humidity, 2)
    }

st.sidebar.header('Enter Location')
location = st.sidebar.text_input('Location', placeholder='Ex. Syracuse, NY, US')
#units = st.sidebar.selectbox('Units', ['imperial', 'metric'])
#if st.sidebar.button('Get Weather'):
#    try:
#        weather = get_current_weather(location, units=units)
#        st.write(weather)
#    except Exception as e:
#        st.error(e)

openai_api_key = st.secrets.EddieOpenAPIKey

if location:
    client = OpenAI(api_key=openai_api_key)

    weather = get_current_weather(location, units='imperial')

    prompt = f'''You are an outfit recommendation chatbot. Assume that this outfit is for a 6'4 man and give an output in this way only and do not add any more or any less.
    Hat? Yes/No \n \n
    Shirt: \n \n
    Pants: \n \n
    Jacket? Yes/No \n \n
    Shoes: \n \n

    Current weather:
    Temperature: {weather['temperature']}°F
    Feels like: {weather['feels_like']}°F

    Suggested outfit:
    '''

    response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": prompt}]
)

    st.write(response.choices[0].message.content)


else:
    st.info("Enter a location in the sidebar to get started.")