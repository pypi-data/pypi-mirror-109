import requests

class Weather:
  """
  Documents for Weather class

  how to Use

  1. Get your own api
  2. How to user Method:
    A. Get weather_naveen by City: passing city with api key
    B. Get weather_naveen by Longitude and Latitude wih api key
  3. Format the Data by:
    A. Calling next_12h() method
    B. Calling next_12h_simplified() method

  That's all good luck.
  """
  def __init__(self, api_key, city=None, lat=None, lon=None):
    if city:
      # Url for weather_naveen in Farenheit
      url_city=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={api_key}&units=metric"
      r = requests.get(url_city)
      self.data = r.json()


    elif lat and lon:
      url_lat_long=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={api_key}&units=imperial"
      r= requests.get(url_lat_long)
      self.data=r.json()

    else:
      raise TypeError ("Provide either a city or lat and lon arguments")
      #print("Provide either a city or lat and lon arguments")

    if(self.data["cod"]!= "200"):
      raise ValueError (self.data['message'])

  def next_12h(self):
    """
    Return 3-Hour data for the next 12 hours as a dict.
    """
    return self.data['list'][:4]

  def next_12h_simplified(self):
    """
    Return date, temperature and sky condition every 3 hours for the next 12 hours as a tuple of tuples.
    """
    simple_data=[]
    for dict in self.data['list'][:4]:
      #print(dict)
      simple_data.append((dict ['dt_txt'], dict ['main']['temp'], dict['weather_naveen'] [0]['description']))
    return simple_data