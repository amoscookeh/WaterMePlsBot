import requests

url = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"

weathers = ["Partly Cloudy (Day)", "Partly Cloudy (Night)", "Showers", "Light Rain", "Cloudy"]
locations = ['Ang Mo Kio', 'Bedok', 'Bishan', 'Boon Lay', 'Bukit Batok', 'Bukit Merah', 'Bukit Panjang',
             'Bukit Timah', 'Central Water Catchment', 'Changi', 'Choa Chu Kang', 'Clementi', 'City', 'Geylang',
             'Hougang', 'Jalan Bahar', 'Jurong East', 'Jurong Island', 'Jurong West', 'Kallang', 'Lim Chu Kang',
             'Mandai', 'Marine Parade', 'Novena', 'Pasir Ris', 'Paya Lebar', 'Pioneer', 'Pulau Tekong', 'Pulau Ubin',
             'Punggol', 'Queenstown', 'Seletar', 'Sembawang', 'Sengkang', 'Sentosa', 'Serangoon', 'Southern Islands',
             'Sungei Kadut', 'Tampines', 'Tanglin', 'Tengah', 'Toa Payoh', 'Tuas', 'Western Islands', 'Western Water Catchment',
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

#
# def main():
#     print(get_weather_forcast('Clementi'))
#
# if __name__ == '__main__':
#     main()