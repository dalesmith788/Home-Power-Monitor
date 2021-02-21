from datetime import datetime, timedelta
from pathlib import Path
import urllib.request, json, time

# import matplotlib as mpl
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# from bokeh.plotting import figure
# from bokeh.resources import CDN
# from bokeh.embed import file_html

envoy = "http://10.0.0.35/production.json"  # IP of Enovy s energy meter
mega = "http://10.0.0.123"
delay = 60  ## Seconds, delay between measurements
timer = 0
first_run = True

print("Program Running...")

while True:
    ## Getting data off Envoy S
    # get html object, read it and decode it from byte to str
    envoy_str = (urllib.request.urlopen(envoy).read().decode())
    envoy_jsn = json.loads(envoy_str)
    # print(json.dumps(jstruct, sort_keys=True, indent=4)) #Pretty Print the structure
    cons_wnow = envoy_jsn["consumption"][0]["wNow"]
    prod_wnow = envoy_jsn["production"][1]["wNow"]  # Production watts now.
    enet_wnow = envoy_jsn["consumption"][1]["wNow"]  # Net power
    cnet_wnow = cons_wnow - prod_wnow

    ## Data from Mega
    try: # read from mega
        mega_str = str((urllib.request.urlopen(mega).read().decode()).split('>')[2])[2:-5]
        mega_list=mega_str.split(" ")
        temp = mega_list[1]
        humidity = mega_list[4]
        tanklevel = mega_list[10]
    except: # handle missing data if mega inaccessible
        pass

    ## Smooth tanklevel
    ## fs = 1000  # Sampling frequency
    # Generate the time vector properly
    ## t = np.arange(1000) / fs
    ## fc = 300  # Cut-off frequency of the filter
    ## w = fc / (fs / 2) # Normalize the frequency
    ## b, a = tanklevel.butter(5, w, 'low')
    ## tanklevels = tanklevel.filtfilt(b, a, tanklevel)
    
    ## Print to Text File
    name_date = time.strftime("%Y_%m_%d")
    yname_date = datetime.strftime(datetime.now() - timedelta(1), "%Y_%m_%d")
    log_path = Path(f"logs/log_{name_date}.txt")
    # ylog_path = Path(f"Logs\solar_log_{yname_date}.txt")
    if not log_path.exists():  # Make a new file for a new date
        newfile = open(log_path, "w")
        newfile.write("Consumption, Production, NetPower, Temp, Humidity, Tank Level, H:M:S\n")  # Header
        newfile.close()
        print(f"Writing to new file: {log_path}")
    text_num = f"{cons_wnow}, {prod_wnow}, {enet_wnow}, {temp}, {humidity}, {tanklevel}, {time.strftime('%H:%M:%S')}"
    txt_file = open(log_path, "a")
    txt_file.write(f'{text_num}\n')
    txt_file.close()

    time.sleep(delay)

    # data = np.genfromtxt(
    #     log_path,
    #     delimiter=",",
    #     skip_header=1,
    #     names=["Consumption", "Production", "Net"],
    #     usecols=(0, 1, 2),
    # )
    # ydata = np.genfromtxt(
    #     ylog_path,
    #     delimiter=",",
    #     skip_header=1,
    #     names=["Consumption", "Production", "Net"],
    #     usecols=(0, 1, 2),
    # )
    # timestamp = np.loadtxt(log_path, dtype="U", delimiter=",", skiprows=1, usecols=(3))
    # times = [datetime.strptime(t, " %H:%M:%S") for t in timestamp]
    # ytimestamp = np.loadtxt(
    #     ylog_path, dtype="U", delimiter=",", skiprows=1, usecols=(3)
    # )
    # ytimes = [datetime.strptime(t, " %H:%M:%S") for t in ytimestamp]
    # x = mpl.dates.date2num(times)
    # yx = mpl.dates.date2num(ytimes)
    # tfmt = mpl.dates.DateFormatter(" %H:%M:%S")

    # # plot = figure()
    # plot.scatter(x, -data["Net"])

    # html = file_html(plot, CDN, "my plot")
    # html_list = html.split("\n")
    # html_list.insert(10, '<meta http-equiv="refresh" content="10" >\n')

    # html_new = "".join(html_list)

    # with open("derp.html", "w") as file1:
    #     file1.write(html_new)
    #     file1.close()
