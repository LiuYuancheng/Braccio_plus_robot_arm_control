#-----------------------------------------------------------------------------
# Name:        uiGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = 'uiFrame [Ver:0.X]'

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "geoIcon.ico")
BGIMG_PATH = os.path.join(dirpath, IMG_FD, "background.png")

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gTranspPct = 70     # Windows transparent percentage.
gUpdateRate = 3     # main frame update rate 1 sec.

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # MainFrame.
iImagePanel = None  # Image panel.
iCtrlPanel = None   # control panel

