from tkinter import *
from PIL import ImageTk, Image
import requests
import json

# API URL ve anahtar
url = 'http://api.openweathermap.org/data/2.5/weather'
api_key = 'a543c23103d66bdf2f81cafa803d89ba'

iconUrl = 'https://openweathermap.org/img/wn/{}@2x.png'

recent_cities = []

def getWeather(city):
    try:
        params = {'q': city, 'appid': api_key, 'units': 'metric', 'lang': 'tr'}
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP hataları için istisna fırlatır
        data = response.json()
        if data and data.get('cod') == 200:
            city = data['name'].capitalize()
            country = data['sys']['country']
            temp = int(data['main']['temp'])
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            icon = data['weather'][0]['icon']
            condition = data['weather'][0]['description']
            return (city, country, temp, humidity, wind_speed, icon, condition)
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"API isteği sırasında hata oluştu: {e}")
        return None

def add_city_to_list(city):
    if city not in recent_cities:
        recent_cities.append(city)
        # Bu fonksiyon şehir listesini günceller
        update_city_list()

def update_city_list():
    city_list.delete(0, END)
    for city in recent_cities:
        city_list.insert(END, city)

def main():
    city = cityEntry.get()
    weather = getWeather(city)
    if weather:
        add_city_to_list(city)
        locationLabel['text'] = '{}, {}'.format(weather[0], weather[1])
        tempLabel['text'] = '{}°C'.format(weather[2])
        humidityLabel['text'] = 'Nem: {}%'.format(weather[3])
        windLabel['text'] = 'Rüzgar: {} m/s'.format(weather[4])
        conditionLabel['text'] = weather[6]
        icon_url = iconUrl.format(weather[5])
        icon = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
        iconLabel.configure(image=icon)
        iconLabel.image = icon
    else:
        locationLabel['text'] = 'Şehir bulunamadı'
        tempLabel['text'] = ''
        humidityLabel['text'] = ''
        windLabel['text'] = ''
        conditionLabel['text'] = ''
        iconLabel.configure(image='')
        iconLabel.image = None

def show_help():
    help_window = Toplevel(app)
    help_window.title("Yardım")
    help_window.geometry("250x200")
    Label(help_window, text="Şehir adı girin ve 'Arama' düğmesine basın.", padx=10, pady=10).pack()
    Label(help_window, text="Hava durumu bilgileri güncellenecektir.", padx=10, pady=5).pack()

app = Tk()
app.geometry('400x500')
app.title('KK Hava Durumu')

cityEntry = Entry(app, justify='center')
cityEntry.pack(fill=BOTH, ipady=10, padx=18, pady=5)
cityEntry.focus()

searchButton = Button(app, text='Arama', font=('Arial', 15), command=main)
searchButton.pack(fill=BOTH, ipady=10, padx=20)

iconLabel = Label(app)
iconLabel.pack()

locationLabel = Label(app, font=('Arial', 40, 'bold'))
locationLabel.pack()

tempLabel = Label(app, font=('Arial', 40, 'bold'))
tempLabel.pack()

humidityLabel = Label(app, font=('Arial', 20))
humidityLabel.pack()

windLabel = Label(app, font=('Arial', 20))
windLabel.pack()

conditionLabel = Label(app, font=('Arial', 20))
conditionLabel.pack()

city_list = Listbox(app)
city_list.pack(fill=BOTH, padx=10, pady=5)

helpButton = Button(app, text='Yardım', font=('Arial', 15), command=show_help)
helpButton.pack(fill=BOTH, ipady=10, padx=20)

app.mainloop()
