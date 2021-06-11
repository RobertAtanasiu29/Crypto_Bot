# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 22:44:24 2021

@author: Robert Atanasiu
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

r = requests.get("https://api.binance.com/api/v3/depth",
                 params=dict(symbol="ETHBUSD"))
results = r.json()


frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],
                             dtype=float)
          for side in ["bids", "asks"]}


frames_list = [frames[side].assign(side=side) for side in frames]
data = pd.concat(frames_list, axis="index", 
                 ignore_index=True, sort=True)



price_summary = data.groupby("side").price.describe()
price_summary.to_markdown()


r = requests.get("https://api.binance.com/api/v3/ticker/bookTicker", params=dict(symbol="ETHBUSD"))
book_top = r.json()

name = book_top.pop("symbol")  # get symbol and also delete at the same time
s = pd.Series(book_top, name=name, dtype=float)
s.to_markdown()


fig, ax = plt.subplots()

#ax.set_title(f"Last update: {t} (ID: {last_update_id})")

sns.scatterplot(x="price", y="quantity", hue="side", data=data, ax=ax)

ax.set_xlabel("Price")
ax.set_ylabel("Quantity")

plt.show()