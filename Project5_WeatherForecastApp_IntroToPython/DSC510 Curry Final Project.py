#   File: DSC510 Curry Final Project.py
#   Name: Adam Curry
#   Date: 05/28/2019
#   Course: DSC510 - Intro to Programming
#   Desc: This program will find the current day (real time) and five day (3PM) forecast for any city in the world.
#   Usage: This program should be used when reviewing the final assignment for this course
########################################################

#   import necessary libraries
import requests
import json
import pytemperature
import datetime


#   this class will iterate through the various date instances to get the necessary weather values
class WeatherForecast:

    def __init__(self, _city_name):
        self._city_name = _city_name

    #   _for_data = json data obtained through API
    #   _index = the index used for the time of day of the weather
    #   _c_f = current or future, for current forecast or future forecast
    #   utcfromtimestamp will translate the unix format to utc and strftime converts to readable format
    def _jsonDate_(self, _for_data, _index=0, _c_f='F'):
        self._c_f = _c_f
        self._for_data = _for_data
        self._index = _index
        if _c_f == 'C':
            _date_ = datetime.datetime.today().strftime(' %A\n* %B %d, %Y | %I:%M: %p')
        else:
            _date_ = datetime.datetime.utcfromtimestamp(self._for_data['list'][self._index]['dt'])\
                .strftime(' %A\n* %B %d, %Y | %I:%M: %p')
        return _date_

    #   pytemperature converts the json kelvin temp to fahrenheit
    def _jsonTemp (self, _for_data, _index=0, _c_f='F'):
        self._c_f = _c_f
        self._for_data = _for_data
        self._index = _index
        if _c_f == 'C':
            _temp_ = pytemperature.k2f(_for_data['main']['temp'])
        else:
            _temp_ = pytemperature.k2f(_for_data['list'][self._index]['main']['temp'])
        return _temp_

    def _jsonHumidity(self, _for_data, _index=0, _c_f='F'):
        self._c_f = _c_f
        self._for_data = _for_data
        self._index = _index
        if _c_f == 'C':
            _humidity_ = _for_data['main']['humidity']
        else:
            _humidity_ = _for_data['list'][self._index]['main']['humidity']
        return _humidity_

    def _jsonDesc (self, _for_data, _index=0, _c_f='F'):
        self._c_f = _c_f
        self._for_data = _for_data
        self._index = _index
        if _c_f == 'C':
            _desc_ = _for_data['weather'][0]['description']
        else:
            _desc_ = _for_data['list'][self._index]['weather'][0]['description']
        return _desc_

    def _print_(self, _date_, _temp_, _humidity_, _desc_):
        self._date_ = _date_
        self._temp_ = _temp_
        self._humidity_ = _humidity_
        self._desc_ = _desc_.strip()
        print('******************************************************\n*{}'.format(self._date_))
        print('* The temperature at noon will be - {}°'.format(self._temp_))
        print('* The humidity will be - {}%'.format(self._humidity_))
        print('* The day will contain {}'.format(self._desc_))


#   userInput will gather city and check for errors in city entry, _i is to keep track of app iterations
def main(_i):
    global city_name
    global forecast_data
    city_name = ''
    while True:
        try:
            city_name = str(input('\nEnter the city name or type "exit" to quit: \n')).upper()
            if city_name == 'EXIT':
                forecast_data = ''
                iterStep(forecast_data, city_name, _i)
            else:
                #   call to the api obtained from https://openweathermap.org/
                response = requests.get('https://api.openweathermap.org/data/2.5/forecast?q={}&APPID=0642aa89e78ed42c35b28ac390c39819'.format(city_name))
                forecast_data = json.loads(response.text)
                test_main = forecast_data['city']['name']
                print('Connection success! Retrieving data for {}\n'.format(city_name))
                iterStep(forecast_data, city_name, _i)
        except KeyError:
            print('Are you sure that is correct? Try entering your city again, or type "exit" to quit.')
            continue
        break


#   iterStep will take the user input and exit if "exit" was entered, or call the forecast function
def iterStep(forecast_data, _city_name, _i):
    while True:
        if _city_name.lower() == 'exit':
            print('You viewed this weather application {} time(s)\n'
                  'Thanks for stopping by!'.format(_i))
        else:
            get_forecast(forecast_data, _city_name, _i)
        break


#   get_forecast iterates through the WeatherForecast class to get the weather values
def get_forecast(_forecast_data, _city_name, _i):
    #   call to get the current day weather json data
    curr_response = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&APPID=0642aa89e78ed42c35b28ac390c39819'.format(_city_name))
    curr_data = json.loads(curr_response.text)

    instance = WeatherForecast(city_name)

    curr_date = instance._jsonDate_(_for_data=curr_data, _c_f='C')
    curr_temp = instance._jsonTemp(_for_data=curr_data, _c_f='C')
    curr_hum = instance._jsonHumidity(_for_data=curr_data, _c_f='C')
    curr_desc = instance._jsonDesc(_for_data=curr_data, _c_f='C')

    #   4, 12, 20, 28, 36 are 3PM times indecies for the five day forecast
    date1_date = instance._jsonDate_(_for_data=_forecast_data, _index=4)
    date1_temp = instance._jsonTemp(_for_data=_forecast_data, _index=4)
    date1_hum = instance._jsonHumidity(_for_data=_forecast_data, _index=4)
    date1_desc = instance._jsonDesc(_for_data=_forecast_data, _index=4)

    date2_date = instance._jsonDate_(_for_data=_forecast_data, _index=12)
    date2_temp = instance._jsonTemp(_for_data=_forecast_data, _index=12)
    date2_hum = instance._jsonHumidity(_for_data=_forecast_data, _index=12)
    date2_desc = instance._jsonDesc(_for_data=_forecast_data, _index=12)

    date3_date = instance._jsonDate_(_for_data=_forecast_data, _index=20)
    date3_temp = instance._jsonTemp(_for_data=_forecast_data, _index=20)
    date3_hum = instance._jsonHumidity(_for_data=_forecast_data, _index=20)
    date3_desc = instance._jsonDesc(_for_data=_forecast_data, _index=20)

    date4_date = instance._jsonDate_(_for_data=_forecast_data, _index=28)
    date4_temp = instance._jsonTemp(_for_data=_forecast_data, _index=28)
    date4_hum = instance._jsonHumidity(_for_data=_forecast_data, _index=28)
    date4_desc = instance._jsonDesc(_for_data=_forecast_data, _index=28)

    date5_date = instance._jsonDate_(_for_data=_forecast_data, _index=36)
    date5_temp = instance._jsonTemp(_for_data=_forecast_data, _index=36)
    date5_hum = instance._jsonHumidity(_for_data=_forecast_data, _index=36)
    date5_desc = instance._jsonDesc(_for_data=_forecast_data, _index=36)

    instance._print_(_date_=curr_date, _temp_=curr_temp, _humidity_=curr_hum, _desc_=curr_desc)
    instance._print_(_date_=date1_date, _temp_=date1_temp, _humidity_=date1_hum, _desc_=date1_desc)
    instance._print_(_date_=date2_date, _temp_=date2_temp, _humidity_=date2_hum, _desc_=date2_desc)
    instance._print_(_date_=date3_date, _temp_=date3_temp, _humidity_=date3_hum, _desc_=date3_desc)
    instance._print_(_date_=date4_date, _temp_=date4_temp, _humidity_=date4_hum, _desc_=date4_desc)
    instance._print_(_date_=date5_date, _temp_=date5_temp, _humidity_=date5_hum, _desc_=date5_desc)
    #   iteration count for the final application usage count, and call back to userInput function
    _i = _i + 1
    main(_i)


#   call to the main function
if __name__ == '__main__':
    i = 0
    main(i)
else:
    'not going to run'
