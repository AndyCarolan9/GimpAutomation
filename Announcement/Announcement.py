#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import gtk
import gimpui
import gobject
from datetime import datetime
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
CREST_LAYER_GROUP = "Crests"
HOME_CREST_ALIGNMENT_LAYER = "HomeCrestMarker"
AWAY_CREST_ALIGNMENT_LAYER = "AwayCrestMarker"

## Load the competitions from text file
directory = os.path.dirname(os.path.abspath(__file__))
comps_file_name = os.path.join(directory, "competitions.txt")
with open(comps_file_name) as comps_file:
    competitions = [line.strip() for line in comps_file]

## Load the teams from text file
teams_file_name = os.path.join(directory, "LouthTeams.txt")
with open(teams_file_name) as teams_file:
    teams = [line.strip() for line in teams_file]

# Source: https://github.com/nerudaj/gimp-pixel-art-utils/tree/main
#UI Helpers - TODO: Move this to it's own file
def create_label(text, parent, spacing):
    label = gtk.Label(text)
    parent.pack_start(label, True, True, spacing)
    return label

def create_button(label, box, spacing = 0):
    btn = gtk.Button()
    btn.set_label(label)
    box.pack_start(btn, True, True, spacing)
    return btn

def create_value_input(value, box, spacing = 0):
    input_entry = gtk.Entry()
    input_entry.set_text("{}".format(value))
    box.pack_start(input_entry, True, True, spacing)
    return input_entry

def create_vbox(parent, grow_horizontally, spacing):
    box = gtk.VBox()
    parent.pack_start(box, grow_horizontally, True, spacing)
    return box

def create_hbox(parent, grow_vertically, spacing):
    box = gtk.HBox()
    parent.pack_start(box, grow_vertically, True, spacing)
    return box
# UI Helpers End

def create_dropdown(items, controls_vbox, label = "", labels_vbox = None):
    if(labels_vbox is not None):
        label_box = create_hbox(labels_vbox, True, 0)
        create_label(label, label_box, 10)
    select_box = create_hbox(controls_vbox, False, 5)
    combox = gtk.combo_box_new_text()
    for item in items:
        combox.append_text(item)
    combox.set_active(0)
    select_box.pack_start(combox, True, True, 5)
    return combox

def create_ui(image):
    window = gtk.Window()
    window.set_title("Announcement")
    window.connect('destroy', close_ui)
    window_box = gtk.VBox()
    window.add(window_box)
    window.set_keep_above(True)

    horizontal_spacing = 10
    vertical_spacing = 0

    # Main Vboxes
    bottom_controls_hbox = create_hbox(window_box, False, horizontal_spacing)
    labels_vbox = create_vbox(bottom_controls_hbox, True, horizontal_spacing)
    controls_vbox = create_vbox(bottom_controls_hbox, True, horizontal_spacing)

    # Competition selection
    competition_select_box = create_dropdown(competitions, controls_vbox, "Competition: ", labels_vbox)

    # Home team selection
    home_team_select_box = create_dropdown(teams, controls_vbox, "Home Team: ", labels_vbox)

    # Away team selection
    away_team_select_box = create_dropdown(teams, controls_vbox, "Away Team: ", labels_vbox)

    # Venue input box
    venue_label_box = create_hbox(labels_vbox, True, vertical_spacing)
    venue_controls_box = create_hbox(controls_vbox, False, vertical_spacing)
    create_label("Venue: ", venue_label_box, horizontal_spacing)
    venue_entry = create_value_input("", venue_controls_box)

    # Date input
    calendar_label_box = create_hbox(labels_vbox, True, 75)
    calendar_select_box = create_hbox(controls_vbox, False, 5)
    create_label("Date: ", calendar_label_box, 10)

    calendar = gtk.Calendar()
    calendar.set_display_options(gtk.CALENDAR_SHOW_HEADING|gtk.CALENDAR_SHOW_DAY_NAMES)
    calendar_select_box.pack_start(calendar, True, True, 5)

    # Time input
    time_label_box = create_hbox(labels_vbox, True, vertical_spacing)
    time_controls_box = create_hbox(controls_vbox, False, vertical_spacing)
    create_label("Time: ", time_label_box, 20)

    hour_adj = gtk.Adjustment(1.0, 1.0, 12.0, 1.0, 5.0, 0.0)
    hour_spinner = gtk.SpinButton(hour_adj, 0, 0)
    hour_spinner.set_wrap(True)

    time_controls_box.add(hour_spinner)

    minute_adj = gtk.Adjustment(0.0, 0.0, 55.0, 5.0, 5.0, 0.0)
    minute_spinner = gtk.SpinButton(minute_adj, 0, 0)
    minute_spinner.set_wrap(True)

    time_controls_box.add(minute_spinner)

    am_pm_select_box = create_dropdown(["AM", "PM"], time_controls_box)

    # Run button
    run_btn = create_button("Run", window_box)
    run_btn.connect("clicked", announcement_automation, image, competition_select_box, home_team_select_box, away_team_select_box, venue_entry, calendar, hour_spinner, minute_spinner, am_pm_select_box)

    window.show_all()

def close_ui():
    gtk.main_quit()

def plugin_entry(image, active_layer):
    create_ui(image)
    gtk.main()

def announcement_automation(widget, image, competition, home_team_name, away_team_name, venue_name, calendar, hour, minute, time_period):
    # Hide previously used crests
    hide_visible_crests(image)

    # Set new data
    set_layer_text(image, COMPETITION_LAYER_NAME, competition.get_active_text(), 65)
    set_layer_text(image, VENUE_LAYER_NAME, venue_name.get_text(), 32)
    set_date(image, calendar)
    set_time(image, hour, minute, time_period)
    set_team_data(image, home_team_name.get_active_text())
    set_team_data(image, away_team_name.get_active_text(), False)

    # Close widget
    close_ui()

def find_layer(layers, layer_name):
    for layer in layers:
        if layer.name == layer_name:
            return layer

    return None

def find_layer_in_group(layers, layer_name, group_name):
    layer_group = find_layer(layers, group_name)
    if(layer_group is None):
        pdb.gimp_message("Failed to find layer in group. Could not find layer group with name " + layer_name)
        return None

    return find_layer(layer_group.children, layer_name)

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

def set_time(image, hour, minute, time_period):
    hour_str = str(hour.get_value_as_int())
    min_str = str(minute.get_value_as_int())

    if(len(min_str) == 1):
        min_str = "0" + min_str

    set_layer_text(image, TIME_LAYER_NAME, "{0}:{1} {2}".format(hour_str, min_str, time_period.get_active_text()), 32)

def set_date(image, calendar):
    # Setup date variables
    date_array = calendar.get_date()
    date_time = datetime(date_array[0], date_array[1] + 1, date_array[2])
    day_name = date_time.strftime("%A")
    month_name = date_time.strftime("%B")
    day_date = date_time.strftime("%d")

    set_layer_text(image, DATE_LAYER_NAME, "{0}, {1} {2}".format(day_name, month_name, day_date), 32)

def set_team_data(image, team_name, is_home_team = True):
    if(is_home_team):
        set_layer_text(image, HOME_TEAM_LAYER_NAME, team_name, 32)
    else:
        set_layer_text(image, AWAY_TEAM_LAYER_NAME, team_name, 32)

    team_crest_layer = find_layer_in_group(image.layers, team_name, CREST_LAYER_GROUP)
    if(team_crest_layer is None):
        pdb.gimp_message("Unable to set visible and align crest. Could not find crest layer with name " + team_name)
        return

    # Set the layer active
    pdb.gimp_item_set_visible(team_crest_layer, True)
    align_crest_layer(image, team_crest_layer, is_home_team)

def align_crest_layer(image, crest_layer, is_home_team):
    align_reference_layer = None
    if(is_home_team):
        align_reference_layer = find_layer(image.layers, HOME_CREST_ALIGNMENT_LAYER)
    else:
        align_reference_layer = find_layer(image.layers, AWAY_CREST_ALIGNMENT_LAYER)

    if(align_reference_layer == None):
        pdb.gimp_message("Unable to align crest layer. Could not find layer to align to.")
        return

    xOffset, yOffset = align_reference_layer.offsets
    original_width = align_reference_layer.width
    original_height = align_reference_layer.height
    align_layer_centre(crest_layer, xOffset, yOffset, original_width, original_height)

def hide_visible_crests(image):
    crest_group = find_layer(image.layers, CREST_LAYER_GROUP)
    if(crest_group is None):
        pdb.gimp_message("Failed to hide visible crests. Could not find crest layer group.")
        return None

    for crest in crest_group.children:
        pdb.gimp_item_set_visible(crest, False)

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
          plugin_entry)

main()