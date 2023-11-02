#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiPanel.py
#
# Purpose:     This module is used to create different function panels.
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import wx
import math

from datetime import datetime
import uiGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class angleDisplayPanel(wx.Panel):
    """ Panel to display image. """

    def __init__(self, parent, title, limitRange = (75, 220), panelSize=(300, 300)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.title = title
        self.limitRange = limitRange
        self.angle1 = None
        self.angle2 = None
        self.bmp = wx.Bitmap(gv.BGIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)
        
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour('GREEN'))
        dc.DrawText(self.title, 5, 5)
        # draw the range detail.
        dc.SetPen(wx.Pen('Green'))
        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        x1, y1 = 150-math.sin(math.radians(self.limitRange[0]))*130, 150+math.cos(math.radians(self.limitRange[0]))*130
        dc.DrawLine(150,150, x1, y1)
        dc.DrawText(str(self.limitRange[0]), x1+5, y1-5)

        x2, y2 = 150-math.sin(math.radians(self.limitRange[1]))*130, 150+math.cos(math.radians(self.limitRange[1]))*130
        dc.DrawLine(150,150, x2, y2)
        dc.DrawText(str(self.limitRange[1]), x2+5, y2-5)
        dc.SetTextForeground(wx.Colour('YELLOW'))
        dc.SetPen(wx.Pen(wx.Colour('YELLOW'), width=3, style=wx.PENSTYLE_SHORT_DASH))
        if not self.angle1 is None:
            dc.DrawText("Output-1 Axis:%s" %str(self.angle1), 160, 180)
            x3, y4 = 150-math.sin(math.radians(self.angle1))*130, 150+math.cos(math.radians(self.angle1))*130
            dc.DrawLine(150,150, x3, y4)

        if not self.angle2 is None:
            dc.DrawText("Output-2 Axis:%s" %str(self.angle2), 160, 200)
            x5, y6 = 150-math.sin(math.radians(self.angle2))*130, 150+math.cos(math.radians(self.angle2))*130
            dc.DrawLine(150,150, x5, y6)

    #-----------------------------------------------------------------------------
    def updateAngle(self, angle1=None, angle2=None):
        self.angle1 = angle1
        self.angle2 = angle2

    #-----------------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test debug panel. """

    print('Test Case start: type in the panel you want to check:')
    print('0 - PanelImge')
    print('1 - PanelCtrl')
    #pyin = str(input()).rstrip('\n')
    #testPanelIdx = int(pyin)
    testPanelIdx = 1    # change this parameter for you to test.
    print("[%s]" %str(testPanelIdx))
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel',
                         pos=(300, 300), size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)

    testPanel = angleDisplayPanel(mainFrame, title="grip")
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()



