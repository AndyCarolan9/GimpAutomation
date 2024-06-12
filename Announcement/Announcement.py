#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

import sys
sys.stderr = open( 'c:\\temp\\gimpstderr.txt', 'a')

#Constants
PIXEL_UNIT = 0
COLOR_WHITE = (255, 255, 255)
FONT_NAME = "Arial Bold Italic"

# Layer Names
COMPETITION_LAYER_NAME = "Competition"
DATE_LAYER_NAME = "Date"
TIME_LAYER_NAME = "Time"
VENUE_LAYER_NAME = "Venue"
HOME_TEAM_LAYER_NAME = "HomeTeam"
AWAY_TEAM_LAYER_NAME = "AwayTeam"

def announcement_automation(image, active_layer):
    set_layer_text(image, COMPETITION_LAYER_NAME, "Title", 65)
    set_layer_text(image, DATE_LAYER_NAME, "Monday 12th June", 32)
    set_layer_text(image, TIME_LAYER_NAME, "7:30 PM", 32)
    set_layer_text(image, VENUE_LAYER_NAME, "Home", 32)
    set_layer_text(image, HOME_TEAM_LAYER_NAME, "Glen Emmets", 32)
    set_layer_text(image, AWAY_TEAM_LAYER_NAME, "Away Team", 32)

def find_layer(layers, layer_name):
    for layer in layers:
        if layer.name == layer_name:
            return layer

def set_layer_text(image, layer_name, text, font_size):
    layer = find_layer(image.layers, layer_name) 
    if layer is None:
        pdb.gimp_message("Failed to set text in layer. Could not find layer with name " + layer_name)
        return
    #TODO: This should get the font, size & color value from the layer to copy. Need method to get info from layer markup as get methods do not work correctly
    pdb.gimp_text_layer_set_text(layer, text)
    pdb.gimp_text_layer_set_color(layer, COLOR_WHITE)
    pdb.gimp_text_layer_set_font_size(layer, font_size, PIXEL_UNIT)
    pdb.gimp_text_layer_set_font(layer, FONT_NAME)

register(
          "python_fu_Announcement",
          "Imports game data and fills in the Announcement Template",
          "Imports game data and fills in the Announcement Template",
          "Andrew Carolan",
          "Copyright (C) 2024 Andrew Carolan",
          "2024",
          "<Image>/Automation/Announcement",
          "*",
          [],
          [],
          announcement_automation)

main()