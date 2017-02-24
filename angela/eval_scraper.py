# intended to be a util file to be used with a single HTML eval form

import bs4
import re

### Usage: ###
# Chris's code call's Jae's code to generate a list of urls for each eval corresponding to a class
# Chris's then creates a soup object for each of the links in that list
# then my code processes each soup object for the information and spits back a dictionary with the information
# for that eval that can be processed into an sql database

# this code starts based off the assumption that it has the soup object

def get_eval_info

