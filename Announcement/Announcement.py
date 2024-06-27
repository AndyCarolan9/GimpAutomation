#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import os
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

## Load the competitions from text file
directory = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(directory, "competitions.txt")
with open(file_name) as file:
    competitions = [line.strip() for line in file]

def announcement_automation(image, active_layer, competition_index):
    set_layer_text(image, COMPETITION_LAYER_NAME, competitions[competition_index], 65)
    set_layer_text(image, DATE_LAYER_NAME, "Monday 12th June", 32)
    set_layer_text(image, TIME_LAYER_NAME, "7:30 PM", 32)
    set_layer_text(image, VENUE_LAYER_NAME, "Home", 32)
    set_layer_text(image, HOME_TEAM_LAYER_NAME, "Glen Emmets", 32)
    set_layer_text(image, AWAY_TEAM_LAYER_NAME, "Away Team", 32)

def find_layer(layers, layer_name):
    for layer in layers:
        if layer.name == layer_name:
            return layer

def align_layer_centre(layer, original_x_offset, original_y_offset, original_width, original_height):
    original_center_x = original_x_offset + (original_width / 2)
    original_center_y = original_y_offset + (original_height / 2)
    layer_half_width = layer.width / 2
    layer_half_height = layer.height / 2
    new_x_offset = original_center_x - layer_half_width
    new_y_offset = original_center_y - layer_half_height
    layer.set_offsets(new_x_offset, new_y_offset)

def set_layer_text(image, layer_name, text, font_size):
    layer = find_layer(image.layers, layer_name) 
    if layer is None:
        pdb.gimp_message("Failed to set text in layer. Could not find layer with name " + layer_name)
        return
    #TODO: This should get the font, size & color value from the layer to copy. Need method to get info from layer markup as get methods do not work correctly
    xOffset, yOffset = layer.offsets
    original_width = layer.width
    original_height = layer.height
    pdb.gimp_text_layer_set_text(layer, text)
    pdb.gimp_text_layer_set_color(layer, COLOR_WHITE)
    pdb.gimp_text_layer_set_font_size(layer, font_size, PIXEL_UNIT)
    pdb.gimp_text_layer_set_font(layer, FONT_NAME)
    align_layer_centre(layer, xOffset, yOffset, original_width, original_height)

register(
          "python_fu_Announcement",
          "Imports game data and fills in the Announcement Template",
          "Imports game data and fills in the Announcement Template",
          "Andrew Carolan",
          "Copyright (C) 2024 Andrew Carolan",
          "2024",
          "<Image>/Automation/Announcement",
          "*",
          [
            (PF_OPTION, "competition_index",   "Competition Name:", 0, competitions)
          ],
          [],
          announcement_automation)

main()