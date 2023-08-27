# Solcast Daily Solar Forecast

This project is now incorporated into [FoxESS-Cloud](https://github.com/TonyM1958/FoxESS-Cloud). To use this code in Jupyter Lab, you should load the module as follows:

```
!pip install foxesscloud --root-user-action=ignore --quiet

import foxesscloud.foxesscloud as f
print(f"foxesscloud version = {f.version}")

f.solcast_api_key = "<your api key>"
f.solcast_rids = ["<your rid 1>", "<your rid 2>"]

fcast = f.Solcast()
print(fcast)
fcast.plot_daily()
```


----

This project loads, aggregates and displays solar yield estimates and forcasts from http://solcast.com.au over a number of days (6 days past, 7 days ahead).

It uses Python for loading and analysis and Jupyter Lab for display. Jupyter Lab provides a flexible way for users to build simple scripts to analyse data that is specific to them.

The core code is contained in [solcast.py](solcast.py) and an example Jupyter notebook is provided in [forecast.ipynb](forecast.ipynb). Clicking [forecast.ipynb](forecast.ipynb) will display the last uploaded notebook so you can see what this looks like.

To forecast your solar yield, you will need to:

+ Register a hobbyist account at https://solcast.com.au
+ Create an API access key for your account and make a note of this
+ Create and configure a solar array for each string (by default, the hobbyist account is limited to 2 arrays)
+ Make a note of the resource id (rid) for each array
