#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiRun.py
#
# Purpose:     This module is used as a sample to create the main wx frame.
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os
import sys
import time
import wx
import uiGobal as gv
import BraccioControllerPnl as pl
PERIODIC = 500      # update in every 500ms

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(1150, 560))
        # No boader frame:
        #wx.Frame.__init__(self, parent, id, title, style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        #self.SetTransparent(gv.gTranspPct*255//100)
        #self.SetIcon(wx.Icon(gv.ICO_PATH))
        # Build UI sizer
        self.SetSizer(self._buidUISizer())
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms

#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.LEFT
        mSizer = wx.BoxSizer(wx.VERTICAL)
        mSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.gripSizer = self._buildGripSizer()
        hbox1.Add(self.gripSizer, flag=flagsR, border=2)
        mSizer.AddSpacer(5)

        mSizer.Add(hbox1, flag=flagsR, border=2)
        return mSizer

    def _buildGripSizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Gripper Ctrl")
        label.SetFont(font)
        sizer.Add(label, flag=wx.LEFT, border=2)
        sizer.AddSpacer(10)
        self.gripDis = pl.angleDisplayPanel(self, "Gripper", limitRange=(70, 230))
        sizer.Add(self.gripDis, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticText(self, label=" Motor Axis Angle Control:".ljust(15)), flag=wx.LEFT)
        sizer.AddSpacer(5)
        self.gripperCtrl = wx.Slider(self, value = int(159), minValue = 158, maxValue = 230, size=(270, 30),
        style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.gripperCtrl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onGripAdj)
        sizer.Add(self.gripperCtrl, flag=wx.CENTRE)
        sizer.AddSpacer(5)
        return sizer
    
    def onGripAdj(self, event):
        val = self.gripperCtrl.GetValue()
        print(val)

#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.APP_NAME)
        gv.iMainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
