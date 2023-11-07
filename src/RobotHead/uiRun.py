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
import uiPanel as pl
import udpCom

TEST_MD = False
PERIODIC = 500      # update in every 500ms
DEMO_TIME = 20

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(600, 560))
        # No boader frame:
        #wx.Frame.__init__(self, parent, id, title, style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.SetTransparent(gv.gTranspPct*255//100)
        #self.SetIcon(wx.Icon(gv.ICO_PATH))
        # Build UI sizer
        self.SetSizer(self._buidUISizer())
        self.demoTcount = DEMO_TIME
        self.demoingFlg = False
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        self.client = udpCom.udpClient(('127.0.0.1', 3004))


#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.CENTER
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        mSizer.AddSpacer(5)
        gv.iImagePanel = pl.PanelImge(self)
        mSizer.Add(gv.iImagePanel, flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 560),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        gv.iCtrlPanel = pl.PanelCtrl(self)
        mSizer.Add(gv.iCtrlPanel, flag=flagsR, border=2)
        return mSizer

    #-----------------------------------------------------------------------------
    def parseIncomeMsg(self, msg):
        """ Split the trojan connection's control cmd to:
            - reqKey: request key which idenfiy the action category.
            - reqType: request type which detail action type.
            - reqData: request data which will be used in the action.
        """
        reqKey = reqType = reqData = None
        try:
            if isinstance(msg, bytes): msg = msg.decode('utf-8')
            reqKey, reqType, reqData = msg.split(';', 2)
            return (reqKey.strip(), reqType.strip(), reqData)
        except Exception as err:
            print('The incoming message format is incorrect, ignore it.')
            print(err)
            return (reqKey, reqType, reqData)

#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            if not TEST_MD:
                if not self.demoingFlg:
                    msg = 'FD;check;?'
                    resp = self.client.sendMsg(msg, resp=True)
                    print("incoming message: %s" %str(resp))
                    if not resp is None:
                        result = self.parseIncomeMsg(resp)
                        gv.iImagePanel.setSleepFlg(result[-1])
                        if result[-1] == '1': self.demoingFlg = True
                else:
                    self.demoTcount -= 1
                    if self.demoTcount == 0:
                        self.demoTcount = DEMO_TIME
                        self.demoingFlg = False
                        print("reset demo")

            gv.iImagePanel.updateDisplay()

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
