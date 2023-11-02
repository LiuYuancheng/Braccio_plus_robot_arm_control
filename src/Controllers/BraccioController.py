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
import BraccioCtrlManger as mgr
PERIODIC = 500      # update in every 500ms

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(1000, 900))
        # No boader frame:
        #wx.Frame.__init__(self, parent, id, title, style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        #self.SetTransparent(gv.gTranspPct*255//100)
        #self.SetIcon(wx.Icon(gv.ICO_PATH))
        self.commMgr = mgr.CtrlManager(self, None)
        # Build UI sizer
        self.angles = [None]*6
        self.SetSizer(self._buidUISizer())
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms

        self.Bind(wx.EVT_CLOSE, self.onClose)

#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.VERTICAL)
        mSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        gripSizer = self._buildGripSizer()
        hbox1.Add(gripSizer, flag=flagsL, border=2)

        wrstRSizer = self._buildWristRollSizer()
        hbox1.Add(wrstRSizer, flag=flagsL, border=2)

        wrstPSizer = self._buildWristPitchSizer()
        hbox1.Add(wrstPSizer, flag=flagsL, border=2)

        mSizer.Add(hbox1, flag=flagsL, border=2)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        elbowSizer = self._buildElbowSizer()
        hbox2.Add(elbowSizer, flag=flagsL, border=2)
                
        shoulderSizer = self._buildShoulderSizer()
        hbox2.Add(shoulderSizer, flag=flagsL, border=2)
        
        baseSizer = self._buildBaseSizer()
        hbox2.Add(baseSizer, flag=flagsL, border=2)

        mSizer.Add(hbox2, flag=flagsL, border=2)

        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(890, -1),
                        style=wx.LI_HORIZONTAL), flag=wx.LEFT, border=2)
        mSizer.AddSpacer(10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.retBt = wx.Button(self, label='Reset Poistion', size=(80, 22))
        self.retBt.Bind(wx.EVT_BUTTON, self.onReset)
        hbox3.Add(self.retBt, flag=flagsL, border=2)

        self.loadBt = wx.Button(self, label='Load Action Scenario', size=(140, 22))
        self.loadBt.Bind(wx.EVT_BUTTON, self.onLoad)
        hbox3.Add(self.loadBt, flag=flagsL, border=2)

        mSizer.Add(hbox3, flag=flagsL, border=2)

        return mSizer

#--UIFrame---------------------------------------------------------------------
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
        self.gripperCtrl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onGripperAdj)
        sizer.Add(self.gripperCtrl, flag=wx.CENTRE)
        sizer.AddSpacer(5)
        return sizer
    
    #--UIFrame---------------------------------------------------------------------
    def _buildWristRollSizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="WristRoll Ctrl")
        label.SetFont(font)
        sizer.Add(label, flag=wx.LEFT, border=2)
        sizer.AddSpacer(10)
        self.wristRollDis = pl.angleDisplayPanel(self, "WristRoll", limitRange=(5, 310))
        sizer.Add(self.wristRollDis, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticText(self, label=" Motor Axis Angle Control:".ljust(15)), flag=wx.LEFT)
        sizer.AddSpacer(5)
        self.wristRollDisCtrl = wx.Slider(self, value = int(158), minValue = 5, maxValue = 310, size=(270, 30),
        style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.wristRollDisCtrl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onWristRollAdj)
        sizer.Add(self.wristRollDisCtrl, flag=wx.CENTRE)
        sizer.AddSpacer(5)
        return sizer

    #--UIFrame---------------------------------------------------------------------
    def _buildWristPitchSizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="WristPitch Ctrl")
        label.SetFont(font)
        sizer.Add(label, flag=wx.LEFT, border=2)
        sizer.AddSpacer(10)
        self.wristPitchDis = pl.angleDisplayPanel(self, "wristPitch", limitRange=(85, 225))
        sizer.Add(self.wristPitchDis, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticText(self, label=" Motor Axis Angle Control:".ljust(15)), flag=wx.LEFT)
        sizer.AddSpacer(5)
        self.wristPitchDisCtrl = wx.Slider(self, value = int(158), minValue = 85, maxValue = 225, size=(270, 30),
        style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.wristPitchDisCtrl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onWristPitchAdj)
        sizer.Add(self.wristPitchDisCtrl, flag=wx.CENTRE)
        sizer.AddSpacer(5)
        return sizer

    #--UIFrame---------------------------------------------------------------------
    def _buildElbowSizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Elbow Ctrl")
        label.SetFont(font)
        sizer.Add(label, flag=wx.LEFT, border=2)
        sizer.AddSpacer(10)

        self.elbowDis = pl.angleDisplayPanel(self, "Elbow", limitRange=(80, 220))
        sizer.Add(self.elbowDis, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        
        sizer.Add(wx.StaticText(self, label=" Motor Axis Angle Control:".ljust(15)), flag=wx.LEFT)
        sizer.AddSpacer(5)
        
        self.elbowDisCtrl = wx.Slider(self, value = int(158), minValue = 80, maxValue = 220, size=(270, 30),
        style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.elbowDisCtrl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onElbowAdj)
        sizer.Add(self.elbowDisCtrl, flag=wx.CENTRE)
        
        sizer.AddSpacer(5)
        return sizer


    #--UIFrame---------------------------------------------------------------------
    def _buildShoulderSizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Shoulder Ctrl")
        label.SetFont(font)
        sizer.Add(label, flag=wx.LEFT, border=2)
        sizer.AddSpacer(10)

        self.shoulderDis = pl.angleDisplayPanel(self, "Shoulder", limitRange=(70, 240))
        sizer.Add(self.shoulderDis, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        
        sizer.Add(wx.StaticText(self, label=" Motor Axis Angle Control:".ljust(15)), flag=wx.LEFT)
        sizer.AddSpacer(5)
        
        self.shoulderDisCtrl = wx.Slider(self, value = int(158), minValue = 70, maxValue = 240, size=(270, 30),
        style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.shoulderDisCtrl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onShoulderAdj)
        sizer.Add(self.shoulderDisCtrl, flag=wx.CENTRE)
        
        sizer.AddSpacer(5)
        return sizer

    #--UIFrame---------------------------------------------------------------------
    def _buildBaseSizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Base Ctrl")
        label.SetFont(font)
        sizer.Add(label, flag=wx.LEFT, border=2)
        sizer.AddSpacer(10)

        self.baseDis = pl.angleDisplayPanel(self, "Base", limitRange=(70, 240))
        sizer.Add(self.baseDis, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        
        sizer.Add(wx.StaticText(self, label=" Motor Axis Angle Control:".ljust(15)), flag=wx.LEFT)
        sizer.AddSpacer(5)
        
        self.baseDisCtrl = wx.Slider(self, value = int(158), minValue = 70, maxValue = 240, size=(270, 30),
        style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.baseDisCtrl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onBaseAdj)
        sizer.Add(self.baseDisCtrl, flag=wx.CENTRE)
        
        sizer.AddSpacer(5)
        return sizer

    def onGripperAdj(self, event):
        val = self.gripperCtrl.GetValue()
        self.commMgr.movPart('grip', str(val))
        print(val)

    def onWristRollAdj(self, event):
        val = self.wristRollDisCtrl.GetValue()
        self.commMgr.movPart('wrtR', str(val))
        print(val)

    def onWristPitchAdj(self, event):
        val = self.wristPitchDisCtrl.GetValue()
        self.commMgr.movPart('wrtP', str(val))
        print(val)

    def onElbowAdj(self, event):
        val = self.elbowDisCtrl.GetValue()
        self.commMgr.movPart('elbw', str(val))
        print(val)

    def onShoulderAdj(self, event):
        val = self.shoulderDisCtrl.GetValue()
        self.commMgr.movPart('shld', str(val))
        print(val)

    def onBaseAdj(self, event):
        val = self.baseDisCtrl.GetValue()
        self.commMgr.movPart('base', str(val))

    def onReset(self, event):
        self.commMgr.resetPos()

    def updateDisplay(self, angles):
        if angles[0] != self.angles[0]:
            self.angles[0] = angles[0]
            angle1 = angles[0]
            angle2 = 157*2 - angle1
            self.gripDis.updateAngle(angle1=angle1, angle2=angle2)
            self.gripDis.updateDisplay()

        if angles[1] != self.angles[1]:
            self.angles[1] = angles[1]
            self.wristRollDis.updateAngle(angle1=angles[1])
            self.wristRollDis.updateDisplay()

        if angles[2] != self.angles[2]:
            self.angles[2] = angles[2]
            self.wristPitchDis.updateAngle(angle1=angles[2])
            self.wristPitchDis.updateDisplay()

        if angles[3] != self.angles[3]:
            self.angles[3] = angles[3]
            self.elbowDis.updateAngle(angle1=angles[3])
            self.elbowDis.updateDisplay()

        if angles[4] != self.angles[4]:
            self.angles[4] = angles[4]
            self.shoulderDis.updateAngle(angle1=angles[4])
            self.shoulderDis.updateDisplay()

        if angles[5] != self.angles[5]:
            self.angles[5] = angles[5]
            self.baseDis.updateAngle(angle1=angles[5])
            self.baseDis.updateDisplay()

    def onLoad(self, event):
        taskList = [('grip', '220'), ('base', '90'), ('shld', '155'), ('elbw', '90'), ('wrtP', '205'),
                    ('wrtR', '150'),
                    ('grip', '160'),
                    ('elbw', '130'),
                    ('base', '180'),
                    ('grip', '220'),
                ]
        self.commMgr.setTask(taskList)


#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            #print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            if not self.commMgr.hasNewTask():
                angles = self.commMgr.getPos()
                if not angles is None:
                    self.updateDisplay(angles)

    def onClose(self, event):
        self.commMgr.stop()
        self.Destroy()

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
