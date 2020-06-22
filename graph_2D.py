import wx
import math
import numpy as np
import matplotlib
import matplotlib.mathtext as mt
from matplotlib.mathtext import MathTextParser

class view(object):
    """Deal with coordinates in screen vs world 

    translation_x: x coordinates of stored translation vector world coord 
    translation_y: y coordinates of stored translation vector world coord
    translation_P1x: x coord of first point of current translation additional vector
    translation_P1y: y coord of first point of current translation additional vector
    translation_activate: a current translation additional vector is mouse activated
    Mouse_position: stored actual mouse position
    zoom: zoom factor
    height: height of the graphic window for drawings
    width: width of the graphic window for drawings
    
    get_translation(): return the current translation additional vector in screen coordinates
    screen_to_world(x_screen,y_screen): convert screen coordinates in world coordinates
    world_to_screen(x_world,y_world): convert world coordinates in screen coordinates
    mathtext_to_wxbitmap(s): return a bitmap from a Latex string 
    """
    def __init__(self, translation_x,translation_y,translation_P1x,translation_P1y,zoom,
    translation_activate,Mouse_position,height,width):

        self.translation_x=translation_x
        self.translation_y=translation_y
        self.translation_P1x=translation_P1x
        self.translation_P1y=translation_P1y
        self.translation_activate=translation_activate
        self.Mouse_position=Mouse_position
        self.zoom=zoom
        self.height=height
        self.width=width
        #
        self.mathtext_parser = MathTextParser("Bitmap")
        rc = {"font.family" : "serif", "mathtext.fontset" : "stix"}
        mt.rcParams.update(rc)
        mt.rcParams["font.serif"] = ["Times New Roman"] + mt.rcParams["font.serif"]

    def get_translation(self):
        """return the translation vector in screen coordinates"""
        
        if self.translation_activate:
            P1=self.world_to_screen(self.translation_P1x,self.translation_P1y)
            P2=np.array([self.Mouse_position.x,self.Mouse_position.y])
            trans=P2-P1
        else:
            trans=np.array([0,0])
        return trans

    def screen_to_world(self,x_screen,y_screen):
        """ Convert screen coordinates in world coordinates

        (x_world,y_world)=(x_screen,y_screen)/zoom-Translation
        """
        pos_x=x_screen/self.zoom-(self.translation_x)
        pos_y=(self.height-y_screen)/self.zoom-(self.translation_y)
        return np.array([pos_x, pos_y])
        
    def world_to_screen(self,x_world,y_world):
        """ Convert world coordinates in screen coordinates

        (x_screen,y_screen)=((x_world,y_world)+Translation)*zoom
        """
        pos_x=(x_world+(self.translation_x))*self.zoom
        pos_y=self.height-(y_world+(self.translation_y))*self.zoom
        return np.array([pos_x, pos_y])  

    def mathtext_to_wxbitmap(self, s):
        """Convert a Latex string in bitmap """
        ftimage, depth = self.mathtext_parser.parse(s, 150)
        return wx.Bitmap.FromBufferRGBA(
            ftimage.get_width(), ftimage.get_height(),
            ftimage.as_rgba_str())      

class Graph_window(wx.Window):
    """Class wx.window for the graphic window
    
    
    view_1: embed functions for dealing with screen vs world coordinates
    EL: all elements objects (nodes, beams, periodicity vectors)
    Gd_pere: Initial window, necessary function for accessing tree_ctrl
    parent: sub window in initial window defining the limits of graphic window
    last_pos: last mouse position

    reassign_EL(EL): Replace the instance of elements passed in argument
    on_size(event): modify attributes on event SIZE
    on_paint(event): redraw all graphic components on event PAINT
    draw_x(dc, x, y, line_width): draw a cross on mouse position
    update_drawing(): force redrawing
    on_motion(event): update attributes focus on mouse move in mode DELETE ELEMENT,
                        ADD BEAM  
    def on_left_down(event): functions linked to left button according to current mode
    on_right_down(event): Activation of additional translation vector
    on_right_up(event): Add current translation vector to general one
    on_wheel(event): Wheel mouse management of zoom 
    key_zoom(code_zoom): Zoom in / out calculation according to code_zoom 
    Get_world_pos(): give world coordinates of current mouse position

     """
    def __init__(self,parent,Gd_pere):
        wx.Window.__init__(self, parent,size=parent.ClientSize)
        size=parent.ClientSize
        self.parent=parent
        self.Gd_pere=Gd_pere
        self.EL=Gd_pere.EL
        self.view_1=view(1,1,0,0,100,False,0,size.width,size.height)

        self.last_pos = self.ScreenToClient(wx.GetMousePosition())
        self.buffer = wx.BufferedDC()

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour("WHITE")

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_RIGHT_DOWN,self.on_right_down)
        self.Bind(wx.EVT_MOUSEWHEEL,self.on_wheel)
        self.Bind(wx.EVT_CHAR,self.on_char)
        self.Bind(wx.EVT_SHOW,self.On_show)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)


    def On_show(self,event):

        event.Skip()
        
    def reassign_EL(self,EL):
        self.EL=EL

    def on_char(self,event):
        """zoom in / out while char +/- is typed"""
        key=event.GetKeyCode()
        ctrl=event.ControlDown()
        if (key==388 or key==61) and ctrl==1:
            self.key_zoom(1)
        
        if (key==390 or key==54) and ctrl==1:
            self.key_zoom(2)
        
    def save_bmp(self):
        myImage=self.buffer
        myImage.SaveFile("image.bmp",wx.BITMAP_TYPE_BMP)

    def Resize(self):
        self.Size=self.Parent.ClientSize
        self._buffer = wx.Bitmap(self.Size)

    def on_size(self, event):
        """Modify attributes on event SIZE"""
        
        width, height = self.parent.GetClientSize()
        self._buffer = wx.Bitmap(width, height)
        self.view_1.width=width
        self.view_1.height=height
        self.Repaint()
        event.Skip()

    def Repaint(self):
        """Redraw all graphic components"""
        width, height = self.parent.GetClientSize()
        if width!=self.Size.width|height!=self.Size.height:
            self.SetSize(0,0,width,height)
            self._buffer = wx.Bitmap(width, height)
            self.view_1.width=width
            self.view_1.height=height

        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        Mouse_position= self.ScreenToClient(wx.GetMousePosition())
        self.view_1.Mouse_position=Mouse_position
        #
        #
        if self.view_1.translation_activate:
            dc.SetPen(wx.Pen("BLUE",2,wx.PENSTYLE_DOT_DASH))
            Pos=self.view_1.world_to_screen(self.view_1.translation_P1x,self.view_1.translation_P1y)
            dc.DrawLine(Pos[0],Pos[1],Mouse_position.x,Mouse_position.y)

        #
        self.draw_x(dc, Mouse_position.x, Mouse_position.y, 1)

        self.EL.draw(dc,self.view_1)

        size=self.Size
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.LIGHT) 
        dc.SetTextForeground((0,0,0))
        dc.SetFont(font) 
        if self.Gd_pere.File_saved:
            str1="(Saved)"
        else:
            str1="(**NOT Saved**)"
        str2="Mode :"+ self.EL.Mode+ " Zoom : %4.2f "+str1
        dc.DrawText(str2 % self.view_1.zoom,10,10) 



    def on_paint(self, event):
        """Redraw all graphic components on event PAINT"""
        self.Repaint()
        self.Repaint()
        event.Skip()

    def draw_x(self, dc, x, y, line_width):
        """Draw_x(dc, x, y, line_width): draw a cross on mouse position"""
        dc.SetPen(wx.Pen("RED", line_width))
        dc.DrawLine(x-10, y-10, x+10, y+10)  # \
        dc.DrawLine(x-10, y+10, x+10, y-10)  # /
   
    def update_drawing(self):
        """Force redrawing"""
        self.Refresh(False) 
    
    def on_motion(self, event):
        """update attributes focus on mouse move in mode DELETE ELEMENT, ADD BEAM"""
        self.view_1.Mouse_position = event.GetPosition()
        pos_mouse=np.array([self.view_1.Mouse_position.x,self.view_1.Mouse_position.y])
        if self.EL.Mode=="DELETE_ELEMENT":
            for i in self.EL.nodes:
                pos_node=self.view_1.world_to_screen(i.x,i.y)
                d=np.linalg.norm(pos_node-pos_mouse)
                i.delta_1_focus=0
                i.delta_2_focus=0
                if d<7 :
                    i.focused=True
                    break
                else:
                    i.focused=False
            for i in self.EL.beams:
                N1=self.EL.index_node(i.node_1)[0]
                N2=self.EL.index_node(i.node_2)[0]
                prof=self.EL.index_profile(i.profile)[0]
                Y1=self.EL.periods[0]
                Y2=self.EL.periods[1]
                Y1W=np.array([Y1.x,Y1.y])*Y1.length
                Y2W=np.array([Y2.x,Y2.y])*Y2.length
                
                N1_coord=np.array([N1.x,N1.y])
                N2_coord=np.array([N2.x+i.delta_1*Y1W[0]+i.delta_2*Y2W[0],N2.y+i.delta_1*Y1W[1]+i.delta_2*Y2W[1]])
	

                PS1=self.view_1.world_to_screen(N1_coord[0],N1_coord[1])
                PS2=self.view_1.world_to_screen(N2_coord[0],N2_coord[1])

                A=PS2-PS1
                B=pos_mouse-PS1
                L=np.linalg.norm(A)
                N=A/L
                H=np.dot(B,N)
                d=math.sqrt(np.linalg.norm(B)**2-H**2)
                if d<prof.width*self.view_1.zoom and H>10 and H<(L-10):
                    i.focused=True
                    break
                else:
                    i.focused=False

        if self.EL.Mode=="ADD_BEAM_P1":
            for i in self.EL.nodes:
                pos_node=self.view_1.world_to_screen(i.x,i.y)
                d=np.linalg.norm(pos_node-pos_mouse)
                i.delta_1_focus=0
                i.delta_2_focus=0
                if d<7 :
                    i.focused=True

                    break
                else:
                    i.focused=False

        if self.EL.Mode=="ADD_BEAM_P2":

            Y1W=np.array([self.EL.periods[0].x,self.EL.periods[0].y])*self.EL.periods[0].length
            Y2W=np.array([self.EL.periods[1].x,self.EL.periods[1].y])*self.EL.periods[1].length
            
            for i in self.EL.nodes:
                pos_node_iW=np.array([i.x,i.y])
                i.focused=False
                i.delta_1_focus=0
                i.delta_2_focus=0

                for delta_1 in range(-1,2):
                    for delta_2 in range(-1,2):
                        pos_node_W=pos_node_iW+delta_1*Y1W+delta_2*Y2W
                        pos_node_S=self.view_1.world_to_screen(pos_node_W[0],pos_node_W[1])
                        d=np.linalg.norm(pos_node_S-pos_mouse)
                        if d<7 :
                            
                            if ((delta_1==0 and delta_2==0) and i.number!=self.EL.P1_acquired.number) \
                            or delta_1!=0 or delta_2!=0:
                                i.focused=True
                                i.delta_1_focus=delta_1
                                i.delta_2_focus=delta_2
                               
        self.Refresh(False)
        event.Skip()

    def on_left_down(self, event):
        """Functions linked to left button according to current mode"""
        Pos_screen=event.GetPosition()

        Pos_world=self.view_1.screen_to_world(Pos_screen.x,Pos_screen.y)

        if self.EL.Mode=="DELETE_ELEMENT":
            self.Gd_pere.EL.Remove_focused_element()

        if self.EL.Mode=="ADD_POINT":
            self.Gd_pere.EL.Add_node(Pos_world)
        
        if self.EL.Mode=="ADD_BEAM_P1":
            self.Gd_pere.EL.Add_beam(1)
        
        if self.EL.Mode=="ADD_BEAM_P2":
            self.Gd_pere.EL.Add_beam(2)

        self.Refresh(False)
        event.Skip()

    def on_right_down(self, event):
        """Activation of additional translation vector"""
        Pos_screen=event.GetPosition()
        Pos_world=self.view_1.screen_to_world(Pos_screen.x,Pos_screen.y)        
        self.view_1.translation_P1x=Pos_world[0]
        self.view_1.translation_P1y=Pos_world[1]
        
        self.view_1.translation_activate=True
        self.Refresh(False)
        event.Skip()

    def on_right_up(self, event):
        """Add current translation vector to general one"""
        Pos_screen=event.GetPosition()
        Pos_world=self.view_1.screen_to_world(Pos_screen.x,Pos_screen.y)   
        self.view_1.translation_activate=False
        self.view_1.translation_x=self.view_1.translation_x+Pos_world[0]-self.view_1.translation_P1x
        self.view_1.translation_y=self.view_1.translation_y+Pos_world[1]-self.view_1.translation_P1y
        
        self.Refresh(False)
        event.Skip()

    def on_wheel(self, event):
        """Wheel mouse management of zoom """
        wheel=event.GetWheelRotation()
        Pos_mouse_screen=event.GetPosition()
        Pos_mouse_world=self.view_1.screen_to_world(Pos_mouse_screen.x,Pos_mouse_screen.y)
        if wheel>0 and self.view_1.zoom<1000:
            self.view_1.zoom=self.view_1.zoom*1.1
        
        if wheel<0 and self.view_1.zoom>1:
            self.view_1.zoom=self.view_1.zoom*0.9

        self.view_1.translation_x=(Pos_mouse_screen.x-Pos_mouse_world[0]*self.view_1.zoom)/self.view_1.zoom
        self.view_1.translation_y=(self.view_1.height-Pos_mouse_screen.y)/self.view_1.zoom-Pos_mouse_world[1]
        
        self.Refresh(False)
        event.Skip()
    
    def key_zoom(self,code_zoom):
        """Zoom in / out calculation according to code_zoom """
        Pos_mouse_screen=self.view_1.Mouse_position
        Pos_mouse_world=self.view_1.screen_to_world(Pos_mouse_screen.x,Pos_mouse_screen.y)
  
        if code_zoom==1 and self.view_1.zoom<1000:
            self.view_1.zoom=self.view_1.zoom*1.1

        if code_zoom==2 and self.view_1.zoom>1:
            self.view_1.zoom=self.view_1.zoom*0.9

        self.view_1.translation_x=(Pos_mouse_screen.x-Pos_mouse_world[0]*self.view_1.zoom)/self.view_1.zoom
        self.view_1.translation_y=(self.view_1.height-Pos_mouse_screen.y)/self.view_1.zoom-Pos_mouse_world[1]
        
        self.Refresh(False)

    def Get_world_pos(self):
        pos_world=self.view_1.screen_to_world(self.view_1.Mouse_position.x,self.view_1.Mouse_position.y)
        return pos_world
