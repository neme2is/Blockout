import json
import requests
import datetime
import pprint

endpoint = "https://blockoutdates.disney.com/data/en/parks-feed.json"
main_pass = 12


def get_feed(data):
    dl = data[8].get("park_data").get("blockouts")
    dca = data[9].get("park_data").get("blockouts")
    return dl, dca


def check_if_modified(data, park):
    if park is "disneyland":
        n = 8
    else:
        n = 9
    today = str(datetime.datetime.now().replace(microsecond=0)).replace("-", "").split()[0]
    modified = data[n].get("modified").replace("T", " ").replace("-", "").split()[0]
    if int(modified) < int(today):
        return True


def get_dates(park):
    dates = []
    for i in park:
            start = i.get("start_date")
            end = i.get("end_date")
            s_date = datetime.datetime.strptime(start, '%Y%m%d').strftime('%m/%d/%y')
            e_date = datetime.datetime.strptime(end, '%Y%m%d').strftime('%m/%d/%y')

            if "2018" in start:
                if filter_passes(i.get("passes"), 12):
                    if start == end:
                        dates.append(e_date)
                    else:
                        dates.append(s_date + " - " + e_date)
    return dates


def get_data():
    data = requests.get(endpoint).json()
    dl, dca = get_feed(data)

    if check_if_modified(data, "disneyland"):
        disneyland = get_dates(dl)
        california = get_dates(dca)
        disneyland.sort()
        california.sort()
        print("Disneyland:\n", disneyland)
        print("California:\n", california)
    else:
        print("Nothing updated.")
        disneyland = get_dates(dl)
        california = get_dates(dca)
        print(disneyland)
        get_dates(dca)


def filter_passes(list, type):
    for i in list:
        if i.get("term_id") == type:
            return True


get_data()
