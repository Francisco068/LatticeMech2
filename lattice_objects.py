import wx
import numpy as np
from math_ext import *
import copy

#"Profile.1:210,0.3,rect,0.1")
class profile(object):
    """ Class for object :profile of the beams"""
    def __init__(self,number,E,nu,section,width):
        self.number=number
        self.E=E
        self.nu=nu
        self.section=section
        self.width=width

class periodicity(object):
    """Class for object : periodicity vectors 
    
    x: x value
    y: y value
    length: length
    number: identifier 

    draw(dc, view): draw the vector 
    """
    def __init__(self,x,y,length,number):
        self.x=x
        self.y=y
        self.length=length
        self.number=number

    def draw(self, dc, view):
        """draw the vector """
        trans=view.get_translation()
        v=np.array([self.x,self.y])*self.length
        P1=view.world_to_screen(v[0],v[1])+trans
        P0=view.world_to_screen(0,0)+trans

        
        e1=normalize_vector(v)
        e2=rotate_vector(e1,5*np.pi/6)
        e3=rotate_vector(e1,7*np.pi/6)

        La=self.length/10
        P2=v+e2*self.length/10
        P3=v+e3*self.length/10
        P2=view.world_to_screen(P2[0],P2[1])+trans
        P3=view.world_to_screen(P3[0],P3[1])+trans
        
        dc.SetPen(wx.Pen("DARK GREEN", 3,style=wx.PENSTYLE_LONG_DASH))

        dc.DrawLine(P0[0],P0[1],P1[0],P1[1])
        dc.DrawLine(P1[0],P1[1],P2[0],P2[1])
        dc.DrawLine(P1[0],P1[1],P3[0],P3[1])

        Pos_text_1=(P0+P1)/2

        s=str(self.number)

        bitmap=view.mathtext_to_wxbitmap("$\overrightarrow {{Y_"+s+"}} $")

        dc.DrawBitmap(bitmap,Pos_text_1[0]-bitmap.Width-2,Pos_text_1[1]+2,True)

class node(object):
    """Class for object: node
    
    x: x coordinate
    y: y coordinate
    radius: radius for screen drawing in pixel
    number: identifier
    focused: True in case of mouse motion on it with mode delete or add beam
    delta_1_focus: delta 1 focus value in case with mode add beam P2
    delta_2_focus: delta 2 focus value in case with mode add beam P2

    draw(parent, dc, view): draw node and all periodic nodes around
     """
    def __init__(self, x, y, radius,number):
        self.x=x
        self.y=y
        self.radius=radius
        self.number=number
        self.focused=False
        self.delta_1_focus=0
        self.delta_2_focus=0

    def draw(self,parent, dc, view):
        """draw node and all periodic nodes around
        
        parent: class element parent
        dc: drawing functions class
        view: target graphic window
        """

        pos=np.array([self.x,self.y])

        trans=view.get_translation()
        
        Y1W=np.array([parent.periods[0].x,parent.periods[0].y])*parent.periods[0].length
        Y2W=np.array([parent.periods[1].x,parent.periods[1].y])*parent.periods[1].length

        pos1=pos-5*Y1W-5*Y2W

        for i in range(10):
            pos2=pos1
            for j in range(10):

                dc.SetPen(wx.Pen("GREY", 1))
                dc.SetBrush(wx.Brush("WHITE")) 
                pos2_S=view.world_to_screen(pos2[0],pos2[1])+trans

                dc.DrawCircle(pos2_S[0], pos2_S[1], self.radius)   

                pos2=pos2+Y1W

            pos1=pos1+Y2W

        dc.SetPen(wx.Pen("RED", 1))
        dc.SetBrush(wx.Brush("RED")) 

        pos_S=view.world_to_screen(pos[0],pos[1])+trans

        dc.DrawCircle(pos_S[0], pos_S[1], self.radius)   

        if self.focused:
            dc.SetPen(wx.Pen("ORANGE", 3))
            dc.SetBrush(wx.Brush("ORANGE")) 
            pos1=pos+self.delta_1_focus*Y1W+self.delta_2_focus*Y2W
            pos1_S=view.world_to_screen(pos1[0],pos1[1])+trans
            dc.DrawCircle(pos1_S[0], pos1_S[1], self.radius*1.5) 

        s=str(self.number)
        bitmap=view.mathtext_to_wxbitmap("$n_{"+s+"} $")

        dc.DrawBitmap(bitmap,pos_S[0]-bitmap.Width,pos_S[1]+self.radius+2,True)
  
class beam(object):
    """Class for object: beam 
    
    node_1: identifier of node 1 
    node_2: identifier of node 2 
    length: length of the beam
    width: width of the beam
    delta_1: delta 1 factor for Y1 translation vector added to node 2 coordinates 
    delta_2: delta 2 factor for Y2 translation vector added to node 2 coordinates
    e_x: value of x beam director
    e_y: value of y beam director
    ka: value of beam axial stiffness
    kb: value of beam bending stiffness
    material_E: Young modulus(GPa) of beam's material
    number: beam identifier
    section: string identifier for beam section type
    focused: True if mouse motion upon beam if case of delete mode

    evaluate_k(parent): evaluate length, director, stiffnesses ka and kb
    draw(parent, dc, view): draw the beam and periodic beams associated
    """
    def __init__(self,node_1,node_2,delta_1,delta_2,profile,length,
                 e_x,e_y,ka,kb,number):
        self.node_1=node_1
        self.node_2=node_2
        self.length=length
        self.delta_1=delta_1
        self.delta_2=delta_2
        self.e_x=e_x
        self.e_y=e_y
        self.ka=ka
        self.kb=kb
        self.number=number
        self.profile=profile
        self.focused=False
    
    def evaluate_k(self,parent):
        """evaluate length, director, stiffnesses ka and kb
        
        parent: class element (parent)
        """
        
        N1=parent.index_node(self.node_1)
        N2=parent.index_node(self.node_2)
        prof=parent.index_profile(self.profile)

        material_E=prof.E
        width=prof.width

        Y1=parent.periods[0]
        Y2=parent.periods[1]
        Y1W=np.array([Y1.x,Y1.y])*Y1.length
        Y2W=np.array([Y2.x,Y2.y])*Y2.length

        N1_coord=np.array([N1.x,N1.y])
        N2_coord=np.array([N2.x+self.delta_1*Y1W[0]+self.delta_2*Y2W[0],
                           N2.y+self.delta_1*Y1W[1]+self.delta_2*Y2W[1]])
        E=N2_coord-N1_coord
        self.length=np.linalg.norm(E)
        E_n=E/self.length
        self.e_x=E_n[0]
        self.e_y=E_n[1]
        
        self.ka=material_E*width/self.length
        self.kb=material_E*(width/self.length)**3

    def draw(self, parent, dc, view):
        """draw the beam and periodic beams associated
        
        parent : class element
        dc: drawing functions
        view: graphic window
        """
        prof=parent.index_profile(self.profile)
        width=view.zoom*prof.width

        N1=parent.index_node(self.node_1)
        N2=parent.index_node(self.node_2)
        Y1W=np.array([parent.periods[0].x,parent.periods[0].y])*parent.periods[0].length
        Y2W=np.array([parent.periods[1].x,parent.periods[1].y])*parent.periods[1].length

        N1_W=np.array([N1.x,N1.y])
        N2_W=np.array([N2.x,N2.y])+self.delta_1*Y1W+self.delta_2*Y2W

        trans=view.get_translation()

        N1_W1=N1_W-5*Y1W-5*Y2W
        N2_W1=N2_W-5*Y1W-5*Y2W

        for i in range(10):
            N1_W2=N1_W1
            N2_W2=N2_W1
            for j in range(10):

                dc.SetPen(wx.Pen("LIGHT BLUE", width))
                N1_S2=view.world_to_screen(N1_W2[0],N1_W2[1])+trans
                N2_S2=view.world_to_screen(N2_W2[0],N2_W2[1])+trans

                dc.DrawLine(N1_S2[0], N1_S2[1],N2_S2[0],N2_S2[1])   
                N1_W2=N1_W2+Y1W
                N2_W2=N2_W2+Y1W

            N1_W1=N1_W1+Y2W
            N2_W1=N2_W1+Y2W

        N1_S=view.world_to_screen(N1_W[0],N1_W[1])+trans
        N2_S=view.world_to_screen(N2_W[0],N2_W[1])+trans

        if self.focused==True:
            dc.SetPen(wx.Pen("ORANGE", width*1.5))
            dc.DrawLine(N1_S[0],N1_S[1],N2_S[0],N2_S[1])   
        else:
            dc.SetPen(wx.Pen("BLUE", width))
            dc.DrawLine(N1_S[0],N1_S[1],N2_S[0],N2_S[1])   

        s=str(self.number)
        bitmap=view.mathtext_to_wxbitmap("$b_{"+s+"} $")

        dc.DrawBitmap(bitmap,(N1_S[0]+N2_S[0])/2+width/2+2,
                      (N1_S[1]+N2_S[1])/2+width/2+2,True)
    
class elements(object):
    """"Arrays of basic elements of lattice 
    
    nodes[]: array of nodes
    beams[]: array of beams
    periods[]: array of periodicity vectors
    Mode: actual mode 
    P1_acquired: point 1 node for mode ADD BEAM P1
    P1_acquired_bool: True if a Point 1 node is yet acquired 

    draw(dc,view): draw all objects : nodes, beams, periodicity vectors
    index_node(node): return the index of an node based on identifier value

    """
    def __init__(self,parent):
        self.parent=parent
        self.nodes=[]
        self.beams=[]
        self.periods=[]
        self.profiles=[]
        self.Mode="ADD_POINT"
        self.P1_acquired=node(0,0,5,0)
        self.P1_acquired_bool=False
        self.P1_acquired.focused=False
        self.active_profile=1
        self.periods.append(periodicity(1,0,1,1))
        self.periods.append(periodicity(0,1,1,2))
        self.nodes.append(node(0,0,5,1))
        self.profiles.append(profile(1,210,0.3,"rect",0.1))

    def Delete_all_items(self):
        self.nodes=[]
        self.beams=[]
        self.periods=[]
        self.Mode="ADD_POINT"
        self.P1_acquired=node(0,0,5,0)
        self.P1_acquired_bool=False
        self.P1_acquired.focused=False
        self.active_profile=0

    
    def draw(self,dc,view):
        """draw all objects : nodes, beams, periodicity vectors
        
        dc: drawing functions
        view: graphic window
        """
        for i in self.beams:
            i.draw(self,dc,view)
        for i in self.nodes:
            i.draw(self, dc,view)

        if self.P1_acquired.focused==True:
            self.P1_acquired.draw(self,dc,view)

        for i in self.periods:
            i.draw(dc,view)
    
    def index_node(self,node):
        """return the node based on identifier value
        
        node: identifier value
        """
        for i in self.nodes:
            if i.number==node:
                return i
                break

    def index_profile(self,profile):
        """return the profile based on identifier value
        
        profile : identifier value
        """
        for i in self.profiles:
            if i.number==profile:
                return i
                break

    def Add_node(self,Pos_world):
        numero=0
        for i in self.nodes:
            if i.number >= numero :
                numero=i.number+1
        node1=node(Pos_world[0],Pos_world[1],5,numero)
        self.nodes.append(node1)
        self.parent.Tg.Add_tree_node(node1)
        self.parent.File_saved=False
        pass

    def Add_beam(self,n):
        if n==1:
            for i in self.nodes:
                if i.focused==True:
                    self.P1_acquired=copy.deepcopy(i)                    
                    self.Mode="ADD_BEAM_P2"
                    i.focused=False
                    self.P1_acquired_bool=True
                    break
        if n==2:
            for i in self.nodes:
                if i.focused==True:
                    self.Mode="ADD_BEAM_P1"
                    numero=1
                    for j in self.beams:
                        if numero<=j.number:
                            numero=j.number+1
                    #beam : (node_1,node_2,delta_1,delta_2,profile,length,e_x,e_y,ka,kb,number):
                    beam1=beam(self.P1_acquired.number,i.number,i.delta_1_focus,i.delta_2_focus,self.active_profile,\
                        0,0,0,0,0,numero)
                    self.beams.append(beam1)
                    index=len(self.beams)-1
                    self.beams[index].evaluate_k(self)
                    self.parent.Tg.Add_tree_beam(beam1)
                    self.parent.File_saved=False
                    self.P1_acquired.focused=False
                    self.P1_acquired_bool=False
                    break  
        pass

    def Remove_focused_element(self):
        for i in self.nodes:
            if i.focused==True and len(self.nodes)>1:
                numero=i.number
                self.nodes.remove(i)
                self.parent.File_saved=False
                self.parent.Tg.Remove_tree_node(numero)
                f=True
                while f:
                    f=False
                    for j in self.beams:
                        numero_beam=j.number
                        if numero==j.node_1 or numero==j.node_2:
                            self.beams.remove(j)
                            self.parent.Tg.Remove_tree_beam(numero_beam)
                            f=True
                            break
                break

        for i in self.beams:
            if i.focused==True:
                numero=i.number
                self.beams.remove(i)
                self.parent.File_saved=False
                self.parent.Tg.Remove_tree_beam(numero)
                break
        pass