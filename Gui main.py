from wx3.GUI_Forms import *
from canvas_opengl import *

class GUI3D(wx.App):
    def OnInit(self):
        self.GUI= MyFrame1(None)
        self.SetTopWindow(self.GUI)
        self.GUI.Show()
        return True

if __name__ == "__main__":
    app = GUI3D(0)
    canvas = OpenGLCanvas(app.GUI.m_panel2)
    app.MainLoop()