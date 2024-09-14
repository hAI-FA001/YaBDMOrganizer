import wx

def convert_to_px(dip, width=True):
    dc = wx.ScreenDC()
    return int(dip * (dc.GetPPI().width if width else dc.GetPPI().height) / 96.0)