import csv
import requests


class Api:

    def obtaining_api(self):

        apikey_solcast = "YOUR SOLCAST API"

        #############################################################################
        #####LOCATION
        endpoint = "http://dataservice.accuweather.com/locations/v1/cities/IN/search"
        apikey = "YOUR ACCUWEATHER API"
        city = input("enter your city name: ")
        params = {
            "apikey": apikey,
            "q": city,

            "details": "true"
        }
        response = requests.request("GET", endpoint, params=params)
        myjson = response.json()
        # print(myjson)
        lat = myjson[0]["GeoPosition"]["Latitude"]
        lon = myjson[0]["GeoPosition"]["Longitude"]
        print(lat, lon)

        #############################################################################
        # OPTANING API FOR WEATHER FORCAST
        url = "https://solcast.p.rapidapi.com/radiation/forecasts"

        querystring = {"api_key": apikey_solcast, "latitude": lat, "longitude": lon, "format": "json"}

        headers = {
            "X-RapidAPI-Key": "ab3dbf3a9bmsh4b3c3f5a60c89d5p121ce2jsnac7356643959",
            "X-RapidAPI-Host": "solcast.p.rapidapi.com"
        }

        mylist = []
        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
        mydata = response.json()

        csv_head = ['ghi', 'ghi10', 'ghi90', 'ebh', 'dni', 'dni10', 'dni90', 'dhi', 'air_temp', 'zenith', 'azimuth',
                    'cloud_opucity', 'period_end']
        name_we = "weather_output_data" + mydata["forecasts"][0]['period_end'].replace(':', '-').split('.')[0]
        for i in mydata["forecasts"]:
            lis = [i['ghi'], i['ghi90'], i['ghi10'], i['ebh'], i['dni'], i['dni10'], i['dni90'], i['dhi'],
                   i['air_temp'], i['zenith'], i['azimuth'], i['cloud_opacity'], i['period_end']]
            mylist.append(lis)
        with open("{}.csv".format(name_we), 'w+', encoding="UTF8", newline='') as F:
            writer = csv.writer(F)
            writer.writerow(csv_head)
            writer.writerows(mylist)
        print("done")
        F.close()

        ##############################################################################
        # OPTAINING API FOR SOLAR

        url = "https://solcast.p.rapidapi.com/pv_power/forecasts"

        querystring = {"api_key": apikey_solcast, "capacity": '5', "latitude": lat, "longitude": lon, "tilt": "23",
                       "format": "json"}

        headers = {
            "X-RapidAPI-Key": "ab3dbf3a9bmsh4b3c3f5a60c89d5p121ce2jsnac7356643959",
            "X-RapidAPI-Host": "solcast.p.rapidapi.com"
        }

        response_power = requests.request("GET", url, headers=headers, params=querystring)

        print(response_power.text)

        mypower = response_power.json()
        power_list = []
        csv_head_power = ['pv_estimate', 'period_end', 'period']
        for j in mypower["forecasts"]:
            lis_power = [j['pv_estimate'], j['period_end'], j['period']]
            power_list.append(lis_power)
        name = "solarpower_output_data" + mypower["forecasts"][0]['period_end'].replace(':', '-').split('.')[0]
        with open("{}.csv".format(name), 'w', encoding="UTF8", newline='') as Fa:
            writers = csv.writer(Fa)
            writers.writerow(csv_head_power)
            writers.writerows(power_list)
        print("done")
        Fa.close()
        return [name, name_we]

