import geocoder
import tkinter as tk
import tk_tools
from tkintermapview import TkinterMapView
import requests
import urllib.parse
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")


def create_tab1(tab_control):
    tab1 = tk.Frame(tab_control)
    tab_control.add(tab1, text="Gauge")

    max_speed = 20000

    batV_gauge = tk_tools.Gauge(tab1, height=220, width=650,
                                max_value=16, min_value=8,
                                label='Bat voltage',
                                unit='V',
                                divisions=8,
                                yellow=60,
                                red=75,
                                red_low=30,
                                yellow_low=40)
    batV_gauge.grid(row=0, column=0, sticky='news')

    batI_gauge = tk_tools.Gauge(tab1, height=220, width=650,
                                max_value=6,
                                min_value=-8,
                                label='Bat current',
                                unit='A',
                                divisions=14, yellow=80, red=90,
                                red_low=20, yellow_low=30, bg='lavender')
    batI_gauge.grid(row=0, column=1, sticky='news')

    batT_gauge = tk_tools.Gauge(tab1, height=220, width=650,
                                max_value=6,
                                min_value=-8,
                                label='Bat temperature',
                                unit='C',
                                divisions=14, yellow=80, red=90,
                                red_low=20, yellow_low=30, bg='lavender')
    batT_gauge.grid(row=1, column=0, sticky='news')

    batG_gauge = tk_tools.Gauge(tab1, height=220, width=650,
                                max_value=6,
                                min_value=-8,
                                label='Bat gyro',
                                unit='A',
                                divisions=14, yellow=80, red=90,
                                red_low=20, yellow_low=30, bg='lavender')
    batG_gauge.grid(row=1, column=1, sticky='news')

    count = 0

    def update_gauge():
        nonlocal count
        up = True

        increment = 30

        if up:
            count += increment
            if count > max_speed:
                up = False
        else:
            count -= increment

            if count <= 0.0:
                up = True

        batV_gauge.set_value(count / 1000)
        batI_gauge.set_value((count - 10000) / 1000)
        batT_gauge.set_value((count - 10000) / 1000)
        batG_gauge.set_value((count - 10000) / 1000)

        root.after(50, update_gauge)

    root.after(100, update_gauge)


def create_tab2(tab_control):
    tab2 = tk.Frame(tab_control)
    tab_control.add(tab2, text="Map")
    g = geocoder.ip('me')


# address = 'Shivaji Nagar, Bangalore, KA 560001'
    if g.ok:
        # print("Your location is:", g.city, g.state, g.country)
        address = f"{g.city},{g.state},{g.country}"
    else:
        # print("Failed to get location.")
        address = 'Shivaji Nagar, Bangalore, KA 560001'

    url = 'https://nominatim.openstreetmap.org/search/' + \
        urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    lat = response[0]["lat"]
    lon = response[0]["lon"]
    loc = geolocator.reverse(lat+","+lon)
    location = str(loc)

    widgetmap_widget = TkinterMapView(
        tab2, width=600, height=400, corner_radius=0)
    response = requests.get(url).json()

    widgetmap_widget.pack(fill="both", expand=True)
    widgetmap_widget.set_tile_server(
        "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    widgetmap_widget.set_address(location, marker=True)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1500x800')

    tab_control = tk.ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")

    create_tab1(tab_control)
    create_tab2(tab_control)

    root.mainloop()
