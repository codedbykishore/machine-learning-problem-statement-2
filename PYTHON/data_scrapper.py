# -*- coding: utf-8 -*-
"""data_scrapper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IfxIdzFBHYSDhO80EDtfVHtdzd2PndsJ
"""

!pip install bs4

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib

"""# **Scapping all route available**"""

from bs4 import BeautifulSoup
import requests
url = "https://mtcbus.tn.gov.in/Home/routewiseinfo"
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
route_html=soup.find("select", {"name": "selroute"})
route_list = [ route.text for route in route_html.find_all("option")]
print(route_list)

# removing heading
route_list = route_list[1:]
pd.DataFrame(route_list)

"""# Creating empty dataframe"""

import pandas as pd

route_df = pd.DataFrame(columns = ['route_id', 'stop_id', 'stop_name'])

"""# **For having progress bar**"""

!pip install tqdm

from tqdm import tqdm

"""# **Scrap Route Detail**"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# Initialize an empty list to store route data
route_data = []

# Iterate over each route in route_list
for route in tqdm(route_list):
    url = f"https://mtcbus.tn.gov.in/Home/routewiseinfo?csrf_test_name=3a87933c0527dbc37410c133a7f30868&selroute={route}&submit="
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    # Find route details
    route_detail = soup.find("ul", {"class": "route"})

    if route_detail:  # Ensure route_detail is not None
        for stop in route_detail.find_all("li"):
            try:
                stop_id, stop_name = stop.text.split("\t")
                # Append data to the list, not to the DataFrame
                route_data.append({"route_id": route, "stop_id": stop_id, "stop_name": stop_name})
            except ValueError:
                # Handle cases where the text split doesn't work as expected
                print(f"Skipping stop on route {route} due to unexpected format: {stop.text}")

# Convert the list to a DataFrame once all data is collected
route_df = pd.DataFrame(route_data)

# Show the resulting DataFrame
print(route_df)

# saving into csv file
route_df.head()
route_df.to_csv('route_detail.csv')