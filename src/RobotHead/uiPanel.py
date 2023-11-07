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

from datetime import datetime
import uiGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelImge(wx.Panel):
    """ Panel to display image. """

    def __init__(self, parent, panelSize=(640, 480)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.panelSize = panelSize
        self.sleepFlg = True
        self.toggle = False
        self.sleeps = [wx.Bitmap(gv.SLP_1_IMG, wx.BITMAP_TYPE_ANY),
                       wx.Bitmap(gv.SLP_2_IMG, wx.BITMAP_TYPE_ANY),
                       wx.Bitmap(gv.SLP_3_IMG, wx.BITMAP_TYPE_ANY)]
        self.wakes = [wx.Bitmap(gv.LOOK_L_IMG, wx.BITMAP_TYPE_ANY),
                       wx.Bitmap(gv.LOOK_R_IMG, wx.BITMAP_TYPE_ANY)]
        self.count = 0
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        bm = None 
        if self.sleepFlg:
            bm = self.sleeps[self.count%3]
        else:
            bm = self.wakes[self.count%2]
        dc.DrawBitmap(bm, 0, 0)
        
        dc.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour('GREEN'))
        displayStr= ''
        if self.sleepFlg:
            if self.toggle:
                displayStr = 'I am sleeping...zzzzz'
            else:
                displayStr = 'I will wake up if the camera keep detect your face during 2 Sec.'
        else:
            if self.toggle:
                displayStr = 'Hello! I see you ^_^ '
            else:
                displayStr = 'I will demo my arm movement now. '

        dc.DrawText(displayStr, 10, h-50)

    def setSleepFlg(self, val):
        self.sleepFlg = val == '0'


#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap2(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image) # used below 2.7
        return result

#--PanelImge--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bmp = bitMap

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.count += 1
        self.toggle = not self.toggle
        self.Refresh(True)
        self.Update()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelCtrl(wx.Panel):
    """ Function control panel."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.gpsPos = None
        self.SetSizer(self._buidUISizer())

#--PanelCtrl-------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsR = wx.CENTER
        ctSizer = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        ctSizer.AddSpacer(5)
        # Row idx 0: show the search key and map zoom in level.
        hbox0.Add(wx.StaticText(self, label="Control panel".ljust(15)),
                  flag=flagsR, border=2)
        ctSizer.Add(hbox0, flag=flagsR, border=2)
        return ctSizer

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
    if testPanelIdx == 0:
        testPanel = PanelImge(mainFrame)
    elif testPanelIdx == 1:
        testPanel = PanelCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()



