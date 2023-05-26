# Solcast Daily Solar Forecast
This project loads, aggregates and displays solar yield estimates and forcasts from http://solcast.com.au over a number of days (6 days past, 7 days ahead).

It uses Python for loading and analysis and Jupyter Lab for display. Jupyter Lab provides a flexible way for users to build simple scripts to analyse data that is specific to them.

The core code is contained in [solcast.py](solcast.py) and an example Jupyter notebook is provided in [forecast.ipynb](forecast.ipynb). Clicking [forecast.ipynb](forecast.ipynb) will display the last uploaded notebook so you can see what this looks like.

A file 'private.py' contains user keys and is not uploaded to the public github repository.
A template [template_private.py](template_private.py) is provided needs to be edited to add personal details and then renamed to 'private.py'

To use this project to forecast your solar yield, you will need to:

+ Register a hobbyist account at https://solcast.com.au
+ Create and API access key and make a note of this
+ Create and configure a solar array for each string (by default, the hobbyist account is limited to 2 arrays)
+ Make a note of the resource id (rid) for each array
+ Create a folder in HA (e.g. /config/notebooks/Solcast), download the files from github and save them to this folder
+ Create a file called 'private.py' in the folder (copy and edit 'template_private.py')
+ Enter your solcast api key and rids into 'private.py'
+ Open the Jupyter notebook (forecast.ipynb) and run the forecast
