# SOlcast Solar Forecast
This project loads, aggregates and displays solar yield actuals and forcasts from http://solcast.com.au over a number of days (maximum forecast available is 7 days ahead).

It uses Python for loading and analysis and Jupyter Lab for display. Jupyter Lab provides a flexible way for users to build simple scripts to analyse data that is specific to them.

The core code is contained in [solcast.py](solcast.py) and an example Jupyter notebook is provided in [forecast.ipynb](forecast.ipynb). Clicking [forecast.ipynb](forecast.ipynb) will display the last uploaded notebook so you can see what this looks like.

A file 'private.py' contains user keys and is not uploaded to the public github repository.
A template [template_private.py](template_private.py) is provided needs to be edited to add personal details and then renamed to 'private.py'

To use this project to forecast your solar yield, you will need to:

+ Register for a hobbyist account at https://solcast.com.au
+ Create and configure a solar array for each string (by default, the hobbyist account is limited to 2 arrays)
+ Create and API access key and make a note of this
+ Make a note of the resource id (rid) for each array
+ Create a folder in HA, download the code and save it to the folder e.g. /config/notebooks/Solcast
+ Create a file called private.py in the folder (using template_private.py) and enter your solcast api key and rids into file private
+ Load the Jupyter notebook (forecast.ipynb) and run the forecast
