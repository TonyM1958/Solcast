##################################################################################################
"""
Module:   SOlcast Forecast
Created:  13 February 2023
Updated:  26 May 2023
By:       Tony Matthews
"""
##################################################################################################
# This is the code used for loading and displaying yield forecasts from Solcast.com.au.
##################################################################################################

import os.path
import json
import datetime
import math
import matplotlib.pyplot as plt
import requests
from requests.auth import HTTPBasicAuth

# global settings
debug_setting = 0       # debug setting: 0 = silent, 1 = info, 2 = details
page_width = 100        # maximum text string for display
figure_width = 24       # width of plots

def c_int(i):
    # handle None in integer conversion
    if i is None :
        return None
    return int(i)

def c_float(n):
    # handle None in float conversion
    if n is None :
        return float(0)
    return float(n)

##################################################################################################
# Solar forecast using solcast.com.au
##################################################################################################

# solcast settings
solcast_url = 'https://api.solcast.com.au/'
solcast_credentials = None
solcast_rids = []
solcast_save = 'solcast.json'
solcast_cal = 1.0

def solcast_setting(api_key = None, url = None, rids = None, save = None, cal = None, th = None, debug=None) :
    """
    Load account settings to use
    """ 
    global debug_setting, solcast_url, solcast_credentials, solcast_rids, solcast_save, solcast_cal
    if debug is not None :
        debug_setting = debug
        if debug_setting > 1 :
            print(f"Debug set to {debug}")
    if api_key is not None :
        solcast_credentials = HTTPBasicAuth(api_key, '')
        if debug_setting > 0 :
            print(f"Solcast credentials provided")
    if url is not None :
        solcast_url = url
        if debug_setting > 1 :
            print(f"Solcast url: {solcast_url}")
    if rids is not None :
        solcast_rids = rids
        if debug_setting > 1 :
            print(f"Solcast resource ids: {solcast_rids}")
    if save is not None :
        solcast_save = save
        if debug_setting > 1 :
            print(f"Solcast save: {solcast_save}")
    if cal is not None :
        solcast_cal = cal
        if debug_setting > 0 :
            print(f"Solcast calibration factor: {solcast_cal}")
    return

class Solcast :
    """
    Load Solcast Estimate / ACtuals / Forecast daily yield
    """ 

    def __init__(self, days = 7, reload = 2) :
        # days sets the number of days to get for forecasts and estimated.
        # The forecasts and estimated both include the current date, so the total number of days covered is 2 * days - 1.
        # The forecasts and estimated also both include the current time, so the data has to be de-duplicated to get an accurate total for a day
        global debug_setting, solcast_url, solcast_credentials, solcast_rids, solcast_save, solcast_cal
        data_sets = ['forecasts', 'estimated_actuals']
        self.data = {}
        self.today = str(datetime.date.today())
        if reload == 1 and os.path.exists(solcast_save):
            os.remove(solcast_save)
        if solcast_save is not None and os.path.exists(solcast_save):
            f = open(solcast_save)
            self.data = json.load(f)
            f.close()
            if len(self.data) == 0:
                print(f"No data in {solcast_save}")
            elif reload == 2 and 'date' in self.data and self.data['date'] != self.today:
                self.data = {}
            elif debug_setting > 0:
                print(f"Using data for {self.data['date']} from {solcast_save}")
        if len(self.data) == 0 :
            if debug_setting > 0:
                print(f"Loading data from solcast.com.au for {self.today}")
            self.data['date'] = self.today
            params = {'format' : 'json', 'hours' : 168, 'period' : 'PT30M'}     # always get 168 x 30 min values
            for t in data_sets :
                self.data[t] = {}
                for rid in solcast_rids :
                    response = requests.get(solcast_url + 'rooftop_sites/' + rid + '/' + t, auth = solcast_credentials, params = params)
                    if response.status_code != 200 :
                        print(f"** response code getting {t} for {rid} from {response.url} was {response.status_code}")
                        return
                    self.data[t][rid] = response.json().get(t)
            if solcast_save is not None :
                f = open(solcast_save, 'w')
                json.dump(self.data, f, sort_keys = True, indent=4, ensure_ascii= False)
                f.close()
        self.daily = {}
        self.rids = []
        for t in data_sets :
            for rid in self.data[t].keys() :            # aggregate sites
                if self.data[t][rid] is not None :
                    self.rids.append(rid)
                    for f in self.data[t][rid] :            # aggregate 30 minute slots for each day
                        period_end = f.get('period_end')
                        date = period_end[:10]
                        time = period_end[11:16]
                        if date not in self.daily.keys() :
                            self.daily[date] = {'forecast' : t == 'forecasts', 'kwh' : 0.0}
                        if rid not in self.daily[date].keys() :
                            self.daily[date][rid] = []
                        if time not in self.daily[date][rid] :
                            self.daily[date]['kwh'] += c_float(f.get('pv_estimate')) / 2      # 30 minute kw yield / 2 = kwh
                            self.daily[date][rid].append(time)
                        elif debug_setting > 1 :
                                print(f"** overlapping data was ignored for {rid} in {t} at {date} {time}")
        # ignore first and last dates as these are forecast and estimates only cover part of the day, so are not accurate
        self.keys = sorted(self.daily.keys())[1:-1]
        self.days = len(self.keys)
        # trim the range if fewer days have been requested
        while self.days > 2 * days :
            self.keys = self.keys[1:-1]
            self.days = len(self.keys)
        self.values = [self.daily[k]['kwh'] for k in self.keys]
        self.total = sum(self.values)
        if self.days > 0 :
            self.avg = self.total / self.days
        self.cal = solcast_cal
        return

    def __str__(self) :
        # return printable Solcast info
        global debug_setting
        s = f'Solcast yield for {self.days} days'
        if self.cal is not None and self.cal != 1.0 :
            s += f", calibration = {self.cal}"
        s += f" (E = estimated, F = forecasts):\n\n"
        for k in self.keys :
            tag = 'F' if self.daily[k]['forecast'] else 'E'
            y = self.daily[k]['kwh'] * self.cal
            d = datetime.datetime.strptime(k, '%Y-%m-%d').strftime('%A')[:3]
            s += "\033[1m--> " if k == self.today else "    "
            s += f"{k} {d} {tag}: {y:5.2f} kwh"
            s += " <--\033[0m\n" if k == self.today else "\n"
            for r in self.rids :
                n = len(self.daily[k][r])
                if n != 48 and debug_setting > 0:
                    print(f" ** {k} rid {r} should have 48 x 30 min values. {n} values found")
        return s

    def plot_daily(self) :
        if not hasattr(self, 'daily') :
            print(f"** no daily data available")
            return
        figwidth = 12 * self.days / 7
        self.figsize = (figwidth, figwidth/3)     # size of charts
        plt.figure(figsize=self.figsize)
        # plot estimated
        x = [f"{k} {datetime.datetime.strptime(k, '%Y-%m-%d').strftime('%A')[:3]} " for k in self.keys if not self.daily[k]['forecast']]
        y = [self.daily[k]['kwh'] * self.cal for k in self.keys if not self.daily[k]['forecast']]
        if x is not None and len(x) != 0 :
            plt.bar(x, y, color='orange', linestyle='solid', label='estimated', linewidth=2)
        # plot forecasts
        x = [f"{k} {datetime.datetime.strptime(k, '%Y-%m-%d').strftime('%A')[:3]} " for k in self.keys if self.daily[k]['forecast']]
        y = [self.daily[k]['kwh'] * self.cal for k in self.keys if self.daily[k]['forecast']]
        if x is not None and len(x) != 0 :
            plt.bar(x, y, color='green', linestyle='solid', label='forecast', linewidth=2)
        # annotations
        if hasattr(self, 'avg') :
            plt.axhline(self.avg, color='blue', linestyle='solid', label=f'average {self.avg:.1f} kwh / day', linewidth=2)
        title = f"Solcast yield on {self.today} for {self.days} days"
        if self.cal != 1.0 :
            title += f" (calibration = {self.cal})"
        title += f". Total yield = {self.total:.0f} kwh"    
        plt.title(title, fontsize=16)
        plt.grid()
        plt.legend(fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.show()
        return