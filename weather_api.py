from datetime import datetime, timedelta
from random import random

import requests

url = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"

weathers = ['Partly Cloudy (Night)', 'Partly Cloudy (Day)', 'Showers', 'Light Rain', 'Thundery Showers',
            'Cloudy', 'Moderate Rain', 'Fair (Night)', 'Light Showers', 'Heavy Rain', 'Fair (Day)',
            'Heavy Thundery Showers with Gusty Winds', 'Heavy Thundery Showers', 'Windy', 'Fair & Warm',
            'Heavy Showers']

rainy_weather = ['Showers', 'Light Rain', 'Thundery Showers', 'Moderate Rain', 'Light Showers', 'Heavy Rain'
                 , 'Heavy Thundery Showers with Gusty Winds', 'Heavy Thundery Showers', 'Heavy Showers', 'Windy']
no_sun_weather = ['Partly Cloudy (Night)', 'Partly Cloudy (Day)', 'Cloudy']
sunny_weather = ['Fair (Day)', 'Fair & Warm']

rainy_msg = [
    '☔Rain Rain Go Away☔\n\nIt is expected to rain in the next 2 hours. '
    'If you own a small plant, you may wish to shelter it from the heavy rain.',
    'Im sipping wine (sip, sip) in a robe (💧drip, drip💧)\n\nIt is expected to rain in the next 2 hours. '
    'If you own a small plant, you may wish to shelter it from the heavy rain.',
]

sunny_msg = [
    "Sun's out, Gun's out\n\nIt is expected to be p warm for the next 2 hours. "
    'You might wanna administer more water for your buddy tonight!.',
]

locations = ['Ang Mo Kio', 'Bedok', 'Bishan', 'Boon Lay', 'Bukit Batok', 'Bukit Merah', 'Bukit Panjang',
             'Bukit Timah', 'Central Water Catchment', 'Changi', 'Choa Chu Kang', 'Clementi', 'City', 'Geylang',
             'Hougang', 'Jalan Bahar', 'Jurong East', 'Jurong Island', 'Jurong West', 'Kallang', 'Lim Chu Kang',
             'Mandai', 'Marine Parade', 'Novena', 'Pasir Ris', 'Paya Lebar', 'Pioneer', 'Pulau Tekong', 'Pulau Ubin',
             'Punggol', 'Queenstown', 'Seletar', 'Sembawang', 'Sengkang', 'Sentosa', 'Serangoon', 'Southern Islands',
             'Sungei Kadut', 'Tampines', 'Tanglin', 'Tengah', 'Toa Payoh', 'Tuas', 'Western Islands',
             'Western Water Catchment',
             'Woodlands', 'Yishun']


def get_weather_forecast(location: str):
    forecasts = requests.get(url=url)
    if forecasts.status_code == 200:
        all_forecasts = forecasts.json()['items'][0]['forecasts']
        for forecast in all_forecasts:
            if forecast['area'] == location:
                return forecast['forecast']
    else:
        return "Error when checking weather"


def get_weather_msg(weather: str):
    if weather in rainy_weather:
        msg_idx = random.randint(0, len(rainy_msg) - 1)
        return rainy_msg[msg_idx]
    elif weather in sunny_weather:
        msg_idx = random.randint(0, len(sunny_msg) - 1)
        return sunny_msg[msg_idx]
    else:
        return None


def find_all_weathers():
    now = datetime.now()
    weathers = []

    for i in range(1, 3000, 3):
        query_time = now - timedelta(hours=i)
        date_str = query_time.strftime("%Y-%m-%dT%H:%M:%S")
        forecasts = requests.get(url=url + "?date_time=" + date_str)
        if forecasts.status_code == 200:
            all_forecasts = forecasts.json()['items'][0]['forecasts']
            for forecast in all_forecasts:
                temp = forecast['forecast']
                if temp not in weathers:
                    weathers.append(temp)
        else:
            return "Error when checking weather"

    return weathers


def main():
    print(find_all_weathers())


if __name__ == '__main__':
    main()
