#!/bin/python3
#Copyright 2019 STEPHEN SCHWETZ
#Copyright 2019 RODOLFO QUESADA ZUMBADO
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#requires python-pytz pkg installed via pip or pkg manager
import urllib.request, json
from datetime import datetime
from pytz import timezone
import time
import urllib.parse  

#address of weatherlink live
bucket_type = 0.2 
local_address = "WLL_IP_ADDRESS"
windy_api_key = "WINDY.COM_API_KEY"

# davis wetherlink live local api
#https://weatherlink.github.io/weatherlink-live-local-api/

# windy api docs
# https://community.windy.com/topic/8168/report-you-weather-station-data-to-windy

# davis json api
json_noaa_ext_url="http://"+local_address+"/v1/current_conditions"
print(json_noaa_ext_url)

with urllib.request.urlopen(json_noaa_ext_url) as url:
 weatherlink_data = json.loads(url.read().decode())

# windy api
#    station - 32 bit integer; required for multiple stations; default value 0; alternative names: si, stationId
#    shareOption - text one of: Open, Only Windy, Private; default value is Open
#    name - text; user selected station name
#    longitude - number [degrees]; required; east–west position on the Earth`s surface
#    elevation - number [metres]; height above the Earth's sea level (reference geoid); alternative names: elev, elev_m, altitude
#    tempheight - number [metres]; temperature sensor height above the surface; alternative names: agl_temp
#    windheight - number [metres]; wind sensors height above the surface; alternative names: agl_wind

# measurements

#    station - 32 bit integer; required for multiple stations; default value 0; alternative names: si, stationId
#    time - text; iso string formated time "2011-10-05T14:48:00.000Z"; when time (or alternative) is NOT present server time is used
#    dateutc - text; UTC time formated as "2001-01-01 10:32:35"; (alternative to time)
#    ts - unix timestamp [s] or [ms]; (alternative to time)
#    temp - real number [°C]; air temperature
#    tempf - real number [°F]; air temperature (alternative to temp)
#    wind - real number [m/s]; wind speed
#    windspeedmph - real number [mph]; wind speed (alternative to wind)
#    winddir - integer number [deg]; instantaneous wind direction
#    gust - real number [m/s]; current wind gust
#    windgustmph - real number [mph]; current wind gust (alternative to gust)
#    rh - real number [%]; relative humidity ; alternative name: humidity
#    dewpoint - real number [°C];
#    pressure - real number [Pa]; atmospheric pressure
#    baromin - real number [inches Hg];
#    precip - real number [mm]; precipitation over the past hour
#    rainin - real number [in]; rain inches over the past hour (alternative to precip)
#    uv - number [index];



windy_data = {}

### must url-escape this value properly, later!

temp_c = ((float(weatherlink_data['data']['conditions'][0]["temp"]) - 32) * 5/9)
windy_data["temp"] = str(temp_c)
windy_data["windspeedmph"] = str(weatherlink_data['data']['conditions'][0]["wind_speed_avg_last_1_min"])

#If the wind direction is not None set the wind direction
if str(weatherlink_data['data']['conditions'][0]["wind_dir_scalar_avg_last_1_min"]) != "None":
  windy_data["winddir"] = str(weatherlink_data['data']['conditions'][0]["wind_dir_scalar_avg_last_1_min"])
  
windy_data["windgustmph"] = str(weatherlink_data['data']['conditions'][0]["wind_speed_hi_last_10_min"])
windy_data["rh"] = str(weatherlink_data['data']['conditions'][0]["hum"])

dewpoint_c  = ((float(weatherlink_data['data']['conditions'][0]["dew_point"]) - 32) * 5/9)
windy_data["dewpoint"] = str(dewpoint_c)
windy_data["baromin"] = str(weatherlink_data['data']['conditions'][2]["bar_sea_level"])
windy_data["precip"] = str(float(weatherlink_data['data']['conditions'][0]["rainfall_last_60_min"] * bucket_type))
#windy_data["uv"] = weatherlink_data["davis_current_observation"]["uv_index"]
windy_data["dateutc"]= urllib.parse.quote(str(datetime.utcfromtimestamp(weatherlink_data["data"]["ts"]).strftime('%Y-%m-%d %H:%M:%S')))
windy_url = "https://stations.windy.com/pws/update/"+windy_api_key+"?temp="+windy_data["temp"]+""

for k,v in windy_data.items():
 if k != "temp":
  windy_url+="&"+k+"="+v

print(windy_url)

windy_response = urllib.request.urlopen(windy_url).read()

if windy_response == b'SUCCESS':
 print("updated")
else:
 print("failed")
 print(windy_response)

