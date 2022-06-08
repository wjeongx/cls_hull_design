# Remove_Member_with_OneJoint.py
# exploring wxPython's
# wx.lib.filebrowsebutton.FileBrowseButton()
import wx
import wx.lib.filebrowsebutton
import string
import SACS_Input_Operation

class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle):
        wx.Frame.__init__(self, parent, -1, mytitle, size=(500,200))
        panel = wx.Panel(self)
        self.fbbr = wx.lib.filebrowsebutton.FileBrowseButton(
            panel, -1, labelText="Read SACS Input file :", fileMask="*sac*", size = wx.Size(1000,-1))
        
        self.fbbw = wx.lib.filebrowsebutton.FileBrowseButton(
            panel, -1, labelText="Write SACS input file :", fileMask="*sac*", size = wx.Size(1000,-1))
        
        # setup the layout with sizers
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        Apply_Button = wx.Button(panel, -1, "Apply")
        Cancel_Button = wx.Button(panel, -1, "Cancel")
        hsizer.Add(Apply_Button, 0, wx.ALIGN_CENTER)
        hsizer.Add(Cancel_Button, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.onApply, Apply_Button)
        self.Bind(wx.EVT_BUTTON, self.onCancel, Cancel_Button)
        
        # create a border space
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(self.fbbr, 1, wx.ALIGN_CENTER_VERTICAL)
        border.Add(self.fbbw, 1, wx.ALIGN_CENTER_VERTICAL)
        border.Add(hsizer, 0, wx.EXPAND|wx.ALL, 20)
        panel.SetSizer(border)
        
    def onApply(self, evt):
        fread = self.fbbr.GetValue()
        fwrite = self.fbbw.GetValue()
        
        SACS_Input_Operation.Remove_Free_Joints(fread, fwrite)
            
    def onCancel(self, evt):
        #wx.MessageBox("Missing or invalid SACS Input", "Error")
        self.Destroy()
        
def Run():
    app = wx.App(0)
    # create a MyFrame instance and show the frame
    caption = "wx.lib.filebrowsebutton.FileBrowseButton()"
    MyFrame(None, caption).Show()
    app.MainLoop()
