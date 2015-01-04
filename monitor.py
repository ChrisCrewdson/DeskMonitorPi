import Adafruit_DHT
import plotly.plotly as py
import json
import time
import datetime

with open('./config.json') as config_file:
  plotly_user_config = json.load(config_file)

py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])

url = py.plot([
  {
    'x': [], 'y': [], 'type': 'scatter',
    'stream': {
      'token': plotly_user_config['plotly_streaming_tokens'][0],
      'maxpoints': 200
    }
  },
  {
    'x': [], 'y': [], 'type': 'scatter',
    'stream': {
      'token': plotly_user_config['plotly_streaming_tokens'][1],
      'maxpoints': 200
    }
  }], filename='Desk Monitor Pi')

print "View your streaming graph here: ", url

# temperature sensor middle pin connected channel 0 of mcp3008
sensor_pin = plotly_user_config["pin"]

hstream = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
hstream.open()
tstream = py.Stream(plotly_user_config['plotly_streaming_tokens'][1])
tstream.open()

#the main sensor reading and plotting loop
while True:
  sensor = Adafruit_DHT.DHT22
  humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

  if humidity is not None:
    # write the data to plotly
    hstream.write({'x': datetime.datetime.now(), 'y': humidity})

  if temperature is not None:
    # write the data to plotly
    tstream.write({'x': datetime.datetime.now(), 'y': temperature})

  # delay between stream posts
  time.sleep(60)

