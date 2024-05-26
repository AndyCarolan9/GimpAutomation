#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def AnnouncementAutomation(image, active_layer):
    gimp.message("Hello World")

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
          AnnouncementAutomation)

main()