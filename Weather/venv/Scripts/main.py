import tkinter as tk
import requests
import time

def getWeather(canvas):
    city = textfield.get()
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=3a772a1b358c5efc4215e344f43a0b2d"

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind_speed = json_data['wind']['speed']
    sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise'] + 7200))
    sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset'] + 7200))

    final_info = condition + "\n" + str(temp) + "°C"
    final_data = "\n" + "Max Temp: " + str(max_temp) + "\n" + "Min Temp: " + str(min_temp) + "\n" + "Pressure: " + str(pressure) + "\n" + "Humidity: " + str(humidity) + "\n" + "Wind Speed: " + str(wind_speed) + "\n" + "Sunrise: AM " + str(sunrise) + "\n" + "Sunset: PM " + str(sunset)
    label_1.config(text = final_info)
    label_2.config(text = final_data)

canvas =  tk.Tk()
canvas.geometry("600x500")
canvas.title("Weather App")

f = ("poppins", 15, "bold")
t = ("poppins", 35, "bold")

textfield = tk.Entry(canvas, font = t)
textfield.pack(pady = 20)
textfield.focus()
textfield.bind('<Return>', getWeather)


label_1 = tk.Label(canvas, font = t)
label_1.pack()
label_2 = tk.Label (canvas, font = f)
label_2.pack()

canvas.mainloop()