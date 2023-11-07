#-----------------------------------------------------------------------------
# Name:        uiGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Version:     v0.1.2
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""
import os, sys

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = 'Barccio Serial Controller'

TOPDIR = 'src'
LIBDIR = 'lib'
CONFIG_FILE_NAME = 'BraccioConfig.txt'

IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "icon.png")
BGIMG_PATH = os.path.join(dirpath, IMG_FD, "background.png")
SCE_FD = os.path.join(dirpath, 'Scenarios')

#-----------------------------------------------------------------------------
# find the lib directory
idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)
        
#-----------------------------------------------------------------------------
# Init the configure file loader.
import ConfigLoader
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()

#------<GLOBAL CONSTANTS>-------------------------------------------------------------
STR_DECODE = 'utf-8'
DEBUG = True

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gTestMD = CONFIG_DICT['TEST_MD']
gComPort = CONFIG_DICT['COM_PORT']
gbaudRate = CONFIG_DICT['COM_RATE']

gUpdateRate = 3     # main frame update rate 1 sec.
#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # MainFrame.
