"""
Data parser
"""
import json
import twitter2
import folium
import pandas
import csv
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def form():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("map", usr = user))
    else:
        return render_template("input_page.html")

@app.route("/<usr>")
def map(usr):
    twitter2.get_friends_file(usr)
    generate_csv()
    generate_map()
    return render_template("Great_map.html")


def delete_multiple_element(list_object, indices):
    """
    Deletes from list multiple indexes which are in list
    >>> delete_multiple_element([51, 52, 53, 54, 55, 56, 57, 58, 59], [4, 2, 6])
    [51, 52, 54, 56, 58, 59]
    """
    indices = sorted(indices, reverse=True)
    for idx in indices:
        if idx < len(list_object):
            list_object.pop(idx)

def reading_dict(path):
    """
    Reads the file and generates data
    >>> ":-)" == ":-("
    False
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def generate_csv():
    """
    Generates the csv file from json
    """
    data = reading_dict("friends.json")

    header = ["name", "location", "latitude", "longitude"]

    users_lists = []
    for uuser in data["users"]:
        vval1 = uuser["screen_name"]
        vval2 = uuser["location"]
        vval2 = vval2.replace(",", "")
        users_lists.append([vval1, vval2])

    for userr in users_lists:
        try:
            geolocator = Nominatim(user_agent="GeoFinder")
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            location = geolocator.geocode(userr[-1])
            if location == None:
                del userr[-1]
            else:
                tupple = (location.latitude, location.longitude)
                userr.append(tupple[0])
                userr.append(tupple[1])
        except GeocoderUnavailable:
            del userr[-1]

    bad_user_ind = []
    for usser in users_lists:
        if len(usser) != 4:
            bad_user_ind.append(users_lists.index(usser))



    delete_multiple_element(users_lists, bad_user_ind)


    with open('user_new.csv', 'w', encoding='UTF8', newline="") as ffile:
        writerr = csv.writer(ffile)
        writerr.writerow(header)
        writerr.writerows(users_lists)

def generate_map():
    """
    Generates the map from csv
    """
    data = pandas.read_csv("user_new.csv")
    latitudee = data["latitude"]
    longiitude = data["longitude"]
    user_name = data["name"]
    locattion = data["location"]
    mapy = folium.Map(zoom_start=10)
    fg = folium.FeatureGroup(name="Films_map")
    for latit, longi, namme, locattion in zip(latitudee, longiitude, user_name, locattion):
        fg.add_child(folium.Marker(location=(latit, longi), radius=10, popup=namme + "\n" + locattion, icon=folium.Icon(color="red", icon="info-sign")))
    mapy.add_child(fg)
    mapy.save('templates/Great_map.html')


if __name__ == "__main__":
    app.run(debug=True)
