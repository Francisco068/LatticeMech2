from wx3.GUI_Forms import *
from canvas_opengl import *
from math_ext import *
from graph_2D import *
from lattice_objects import *
from Files_operating import *

class GUI3D(wx.App):
    def OnInit(self):
        self.GUI= MyFrame1(None)
        self.SetTopWindow(self.GUI)
        # Initialise data elements
        self.EL=elements()
        self.EL.periods.append(periodicity(1,0,1,1))
        self.EL.periods.append(periodicity(0,1,1,2))
        self.EL.nodes.append(node(0,0,5,1))
        # Bind MenuBar event
        self.Bind(wx.EVT_MENU, self.File_open, id=self.GUI.m_menuItem1.GetId())
        self.Bind(wx.EVT_MENU, self.File_save, id=self.GUI.m_menuItem2.GetId())
        self.Bind(wx.EVT_MENU, self.File_save_as, id=self.GUI.m_menuItem3.GetId())
        self.Bind(wx.EVT_MENU, self.File_export, id=self.GUI.m_menuItem13.GetId())
        self.Bind(wx.EVT_MENU, self.File_close, id=self.GUI.m_menuItem4.GetId())        
        self.Bind(wx.EVT_MENU, self.Delete_item, id=self.GUI.m_menuItem5.GetId())
        self.Bind(wx.EVT_MENU, self.Visu_2D, id=self.GUI.m_menuItem6.GetId())
        self.Bind(wx.EVT_MENU, self.Visu_3D, id=self.GUI.m_menuItem7.GetId())
        self.Bind(wx.EVT_MENU, self.Yield_limits, id=self.GUI.m_menuItem8.GetId())        
        self.Bind(wx.EVT_MENU, self.Add_point, id=self.GUI.m_menuItem9.GetId())
        self.Bind(wx.EVT_MENU, self.Add_beam, id=self.GUI.m_menuItem10.GetId())
        self.Bind(wx.EVT_MENU, self.Help, id=self.GUI.m_menuItem11.GetId())
        self.Bind(wx.EVT_MENU, self.Calculations_go, id=self.GUI.m_menuItem12.GetId())
        # Bind Toolbar event
        self.Bind(wx.EVT_TOOL, self.Delete_item, self.GUI.m_tool1)
        self.Bind(wx.EVT_TOOL, self.Add_point, self.GUI.m_tool2)
        self.Bind(wx.EVT_TOOL, self.Add_beam, self.GUI.m_tool3)
        self.Bind(wx.EVT_TOOL, self.Calculations_go, self.GUI.m_tool4)
        # Bind Grid evt
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGED, self.Cell_changed, self.GUI.m_grid1)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.Cell_selected, self.GUI.m_grid1)
        # Bind choice event
        self.Bind(wx.EVT_CHOICE, self.Choice_select, self.GUI.m_choice1)
        # Bind char event
        self.Bind(wx.EVT_CHAR_HOOK,self.on_char)

        # Initialise Tree Ctrl
        self.TreeCtrl_init()
        # Initialise Grid
        self.Grid_init()
        # initialise Choice 2D / 3D
        self.GUI.m_choice1.Select(2)
        # initialise graphic canvas
        self.Canvas3D = OpenGLCanvas(self.GUI.m_panel3)
        self.Canvas3D.Shown=False
        self.Canvas2D = Graph_window(self.GUI.m_panel3,self)
        self.Canvas2D.Show(True)
        # 
        self.Bind(wx.EVT_SIZE, self.Graph_resize, self.GUI.m_panel3)        
        # initialise File system
        self.fs=Files_system(self)
        # end of user added elements 
        self.GUI.Show()
        return True

    def Graph_resize(self,event):
#        self.Canvas2D = Graph_window(self.GUI.m_panel3,self)
        event.Skip()
    
    def on_char(self,event):
        """zoom in / out while char +/- is typed"""
        key=event.GetKeyCode()
        ctrl=event.ControlDown()
        if (key==388 or key==61) and ctrl==1:
            self.GUI.m_panel2.key_zoom(1)
    
    def Choice_select(self, event):
        """Choice selection of graphic window appearance"""  
        s=self.GUI.m_choice1.Selection
        self.GUI.m_textCtrl2.AppendText("test choice select %i\n" % s)
        if s==0 :
            self.Canvas2D.Show(False)
            self.Canvas3D.Shown=True
            self.GUI.m_textCtrl2.AppendText("Activation 3D %i\n" % s)
        if s==2 :
            self.Canvas2D.Show(True)
            self.Canvas3D.Shown=False
            self.GUI.m_textCtrl2.AppendText("Activation 2D %i\n" % s)
            
        event.Skip()   

    def Cell_selected(self, event): #from menu
        """Action when cell selected"""  
        self.GUI.m_textCtrl2.AppendText("test cell selected\n")
        event.Skip()   
    

    def Cell_changed(self, event): #from menu
        """Action when cell changed"""  
        self.GUI.m_textCtrl2.AppendText("test cell changed\n")
        event.Skip()   
    
    def TreeCtrl_init(self):
        """Initialise Tree Ctrl"""
        Tree_Lattice_Id=self.GUI.m_treeCtrl1.AddRoot("Lattice")
        materialId=self.GUI.m_treeCtrl1.AppendItem(Tree_Lattice_Id,"Material:")
        basisId=self.GUI.m_treeCtrl1.AppendItem(Tree_Lattice_Id, "Basis:")
        NodesId=self.GUI.m_treeCtrl1.AppendItem(Tree_Lattice_Id, "Nodes:")
        beamsId=self.GUI.m_treeCtrl1.AppendItem(Tree_Lattice_Id, "Beams:")
        self.GUI.m_treeCtrl1.AppendItem(basisId, "Y.1:(1,0)")
        self.GUI.m_treeCtrl1.AppendItem(basisId, "Y.2:(0,1)")
        self.GUI.m_treeCtrl1.AppendItem(NodesId, "N.1:(0,0)")
        self.GUI.m_treeCtrl1.AppendItem(materialId, "modulus(GPa):210")
        self.GUI.m_treeCtrl1.ExpandAll()
    
    def Set_grid_perso(self,col,row,labels_col,labels_row):
        """Set_grid_perso(self,col,row,labels_col,labels_row)
        define labels of row and col 
        """
        Number_cols=self.GUI.m_grid1.GetNumberCols()
        Number_rows=self.GUI.m_grid1.GetNumberRows()
        if Number_cols>col :
            self.GUI.m_grid1.DeleteCols(col,Number_cols-col)
        if Number_cols<col:
            self.GUI.m_grid1.AppendCols(col-Number_cols)
        if Number_rows>row:
            self.GUI.m_grid1.DeleteRows(row,Number_rows-row)
        if Number_rows<row:
            self.GUI.m_grid1.AppendRows(row-Number_rows)
        for i in range(col):
            self.GUI.m_grid1.SetColLabelValue(i, labels_col[i])
        for i in range(row):
            self.GUI.m_grid1.SetRowLabelValue(i, labels_row)
    
    def Grid_init(self):
        self.Set_grid_perso(2,1,["X","Y"],"Y.1")
        self.GUI.m_grid1.SetCellValue(0,0,"1")
        self.GUI.m_grid1.SetCellValue(0,1,"0")

    def Calculations_go(self, event): #from menu
        """menu Calculations Go"""  
        self.GUI.m_textCtrl2.AppendText("test Go\n")
        event.Skip()

    def Help(self, event): #from menu
        """menu Help"""  
        self.GUI.m_textCtrl2.AppendText("test help\n")
        event.Skip()

    def Delete_item(self, event): #from menu
        """menu Delete item"""  
        self.GUI.m_textCtrl2.AppendText("test delete item\n")
        event.Skip()

    def Visu_2D(self, event): #from menu
        """menu Visu 2D"""  
        self.GUI.m_textCtrl2.AppendText("test Visu 2D\n")
        event.Skip()

    def Visu_3D(self, event): #from menu
        """menu Visu 3d"""  
        self.GUI.m_textCtrl2.AppendText("test Visu 3D\n")
        event.Skip()

    def Yield_limits(self, event): #from menu
        """menu Yield limits"""  
        self.GUI.m_textCtrl2.AppendText("test Yield limits\n")
        event.Skip()

    def Add_point(self, event): #from menu
        """menu add point"""  
        self.GUI.m_textCtrl2.AppendText("test add point\n")
        event.Skip()

    def Add_beam(self, event): #from menu
        """menu Add beam"""  
        self.GUI.m_textCtrl2.AppendText("test Add beam\n")
        event.Skip()

    def File_open(self, event): #from menu
        """menu file open""" 
        self.Message("Try File open")
        fs.Open_file()
        event.Skip()
    
    def File_save(self, event):
        """menu file save""" 
        self.fs.Save_file()
        event.Skip()

    def File_save_as(self, event):
        """menu file save as""" 
        self.GUI.m_textCtrl2.AppendText("test file save as\n")
        event.Skip()

    def File_export(self, event):
        """menu file export""" 
        self.fs.Export_file()
        event.Skip()

    def File_close(self, event):
        """menu file close""" 
        self.GUI.m_textCtrl2.AppendText("test file close\n")
        event.Skip()

    def Message(self,msg):
        self.GUI.m_textCtrl2.AppendText(msg+"\n")

    def Message_dialog(self,msg_1, categorie):
        """Show msg_1 associated win an icon category"""
        #categorie = wx.ICON_ERROR ou wx.ICON_WARNING ou wx.ICON_INFORMATION
        msg=wx.MessageDialog(None,message=msg_1,style=wx.YES_NO | wx.CANCEL | categorie)
        ret=msg.ShowModal()
        # Shows the dialog, returning one of wx.ID_OK, wx.ID_CANCEL, wx.ID_YES, wx.ID_NO or wx.ID_HELP.
        return ret
        msg.Destroy()    

if __name__ == "__main__":
    app = GUI3D(0)
    
    app.MainLoop()