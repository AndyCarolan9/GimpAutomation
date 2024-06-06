#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

import sys
sys.stderr = open( 'c:\\temp\\gimpstderr.txt', 'a')

PIXEL_UNIT = 0
COLOR_WHITE = (255, 255, 255)
FONT_NAME = "Arial Bold Italic"

def announcement_automation(image, active_layer):
    set_competition_title(image)

def set_competition_title(image):
    layer_name = "Competition" #TODO: Competition should not be hard coded here. Create a data base of layer id and layer name.
    layer = find_layer(image.layers, layer_name) 
    if layer is None:
        pdb.gimp_message("Failed to find layer with name " + layer_name)
        return
    set_layer_text(layer, "Test Title", 65)

def find_layer(layers, layer_name):
    for layer in layers:
        if layer.name == layer_name:
            return layer

def set_layer_text(layer, text, font_size):
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