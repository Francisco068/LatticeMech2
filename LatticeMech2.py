from wx3.GUI_Forms import *
from canvas_opengl import *
from math_ext import *
from graph_2D import *
from latticeObjects import *
from Files_operations import *
from Tree_Grid import *
import json
import time
from FDR_Solver import *
import xml.etree.ElementTree as ET

from DiscreteLatticeMech.DiscreteLatticeMechCore import Solver, Writer

# todo : quand je change la longueur des vecteurs de base, il faut que je pense à recalculer les longueurs et modules de toutes les poutres !
# todo : de même quand je change une composante du profil !

class GUI3D(wx.App):
    
    def OnInit(self):
        self.GUI= MyFrame1(None)
        self.SetTopWindow(self.GUI)
        self.DIAL=target_dialog(None) 
        # file attributes
        self.File_saved = False
        self.Filename_defined = False
        self.Filename =""
        self.Filename_json =""
        self.Filename_txt =""
        # Initialise data elements
        self.EL=elements(self)
        # dialogs variables
        self.ETarget_number=1

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
        self.Bind(wx.EVT_MENU, self.AddETarget, id=self.GUI.m_menuItem14.GetId())
        self.Bind(wx.EVT_MENU, self.AddProfile, id=self.GUI.m_menuItem15.GetId())

        self.Bind(wx.EVT_MENU, self.Help, id=self.GUI.m_menuItem11.GetId())
        self.Bind(wx.EVT_MENU, self.Calculations_go, id=self.GUI.m_menuItem12.GetId())
        self.Bind(wx.EVT_MENU, self.InverseHomogenization, id=self.GUI.InvHomogenize.GetId())

        # Bind Toolbar event
        self.Bind(wx.EVT_TOOL, self.Delete_item, self.GUI.m_tool1)
        self.Bind(wx.EVT_TOOL, self.Add_point, self.GUI.m_tool2)
        self.Bind(wx.EVT_TOOL, self.Add_beam, self.GUI.m_tool3)
        self.Bind(wx.EVT_TOOL, self.Calculations_go, self.GUI.m_tool4)
        # Bind Grid evt
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGED, self.Cell_changed, self.GUI.m_grid1)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.Cell_selected, self.GUI.m_grid1)
        # Bind Tree_Ctrl evant
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.TreeCtrl_select,self.GUI.m_treeCtrl1)
        # Bind choice event
        self.Bind(wx.EVT_CHOICE, self.Choice_select, self.GUI.m_choice1)
        # Bind dialog event
        self.Bind(wx.EVT_BUTTON,self.DIALOK,self.DIAL.OkButton)
        self.Bind(wx.EVT_BUTTON,self.DIALCANCEL,self.DIAL.CancelButton)
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
        # initialise TreeCtrl, Grid and elements
        self.Tg=TreeGridOperations(self.GUI.m_treeCtrl1,self.GUI.m_grid1,self.EL)
        self.Tg.GridInit()
        self.Tg.TreeCtrlInit()
        self.EL.Elements_init()
        # end of user added elements 
        self.GUI.Show()
        self.Canvas2D.Refresh()
        return True

    def InverseHomogenization(self,event):
        self.DIAL.Show(True)
        event.Skip()

    def DIALOK(self,event):
        self.ETarget_number=int(self.DIAL.m_textCtrl2.Value)
        print("E Target number : {}".format(self.ETarget_number))
        self.DIAL.Show(False)
        event.Skip()

    def DIALCANCEL(self, event):
        self.DIAL.Show(False)
        event.Skip()

    def TreeCtrl_select(self,event):
        
        item_1 = event.Item
        self.Tg.Selection_item(item_1)

    def Graph_resize(self,event):
        self.Canvas2D.Refresh()
        event.Skip()
    
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
#        self.GUI.m_textCtrl2.AppendText("test cell selected\n")
        event.Skip()   
    
    def Cell_changed(self, event): #from menu
        """Action when cell changed"""  
        str1=self.Tg.Modify_TG_from_cell(self.GUI.m_panel1)
        self.EL.ReplaceElement(str1)
        self.FileSaved=False
        self.GUI.m_panel3.Refresh()
        event.Skip()   
    
    # def Calculations(self,writer):
    #     """Call calculations modules"""
    #     solver = Solver()
    #     try:
    #         with open("input_data.json", 'r') as f:
    #             data = json.load(f)
    #     except IOError as error:
    #         self.Message_dialog("could not open input file input_data.json",wx.ICON_ERROR)

    #     solver.solve(data)

    #     # Write to file
        
    #     writer.WriteTensorsToFile(solver.InputData, solver.CMatTensor, solver.FlexMatTensor)
    #     writer.WriteEffectivePropertiesToFile(solver.Bulk, solver.Ex, solver.Ey, solver.Poissonyx, solver.Poissonxy, solver.G,solver.rho)
    #     writer.PlotEffectiveProperties(solver.Bulk, solver.Ex, solver.Ey, solver.Poissonyx, solver.Poissonxy, solver.G)
    
    def Message_results(self,path):
        try:
            panel=self.GUI.m_textCtrl2
            panel.write("Path of results files : "+str(path)+"\n")
            result_file=open(path+"/CMatrix.txt","r")
            panel.write("Stiffness Matrix:\n")
            panel.write(result_file.read())
            result_file.close()
            Eff_file=open(path+"/EffectProperties.txt","r")
            panel.write("Effective properties:\n")
            panel.write(Eff_file.read())
            Eff_file.close()    
            Flex_file=open(path+"/FlexMatrix.txt","r")
            panel.write("Flexibility Matrix:\n")
            panel.write(Flex_file.read())
            Eff_file.close()     
        except:
            panel.write("Something wrong in data results !\n")  
        pass


    def Calculations_go(self, event): #from menu
        """menu Calculations Go"""  
        for i in self.EL.beams:
            i.evaluate_k(self.EL)
        if self.Filename_json=="":
            self.Filename_json="input_data.json"


        self.fs.Generate_json(self.Filename_json,self)

        try:
            with open(self.Filename_json, 'r') as f:
                data = json.load(f)
        except IOError as error:
            self.Message("could not open input file {}".format(self.Filenam_json))
            return

#        self.Message(json.dumps(data, indent=4, sort_keys=False))
        
        # Profiling time code
        start_time = time.time()

        sol=solverFDR(self.EL)
        # solver = Solver()
        # solver.solve(data)
        # The code to be evaluated
        end_time = time.time()
        # Time taken in seconds
        time_taken = end_time - start_time
        self.GUI.m_textCtrl2.AppendText("Exec time={}\n".format(time_taken))

        # writer = Writer()
        # writer.WriteTensorsToFile(solver.CMatTensor, solver.FlexMatTensor)
        # writer.WriteEffectivePropertiesToFile(solver.Bulk, solver.Ex, solver.Ey, solver.Poissonyx, solver.Poissonxy, solver.G, solver.rho)
        # writer.PlotEffectiveProperties(solver.Bulk, solver.Ex, solver.Ey, solver.Poissonyx, solver.Poissonxy, solver.G)

        # self.Message_results(writer.folder)
 
        event.Skip()

    def Help(self, event): #from menu
        """menu Help"""  
        self.GUI.m_textCtrl2.AppendText("test help\n")
        event.Skip()

    def Delete_item(self, event): #from menu
        """menu Delete item"""  
        self.EL.Mode="DELETE_ELEMENT"
        self.Canvas2D.Refresh()
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
        self.EL.Mode="ADD_POINT"
        event.Skip()

    def Add_beam(self, event): #from menu
        """menu Add beam"""  
        self.EL.Mode="ADD_BEAM_P1"
        event.Skip()
    
    def AddETarget(self, event): #from menu
        """menu Add ETarget"""  
        ETarget1=self.EL.AddETarget()
        self.Tg.Add_tree_ETarget(ETarget1)
        event.Skip()

    def AddProfile(self, event): #from menu
        """menu Add Profile"""  
        profile1=self.EL.AddProfile()
        self.Tg.Add_tree_profile(profile1)
        event.Skip()

    def File_open(self, event): #from menu
        """menu file open
        Open the xml file -> create tree ctrl and elements""" 
        if not(self.File_saved):
            rep=self.Message_dialog("Current content has not been saved! Proceed?",wx.ICON_QUESTION)
            if rep==wx.YES:
                self.File_save()
        
        with wx.FileDialog(self.GUI, "Open XML file", wildcard="xml files (*.xml)|*.xml",
                    style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the users changed their mind

            # Proceed loading the file chosen by the user
            self.Filename = fileDialog.GetPath()
        try:
            myfile=open(self.Filename, 'r')
        except IOError:
            wx.LogError("Cannot open file '%s'." % self.Filename)
            return -1

        try:
            tree=ET.parse(myfile)
        except:
            self.Message_dialog("Unable to parse file",wx.ICON_ERROR)
            myfile.close()
            return
        
        self.fs.Open_xml(tree, self.GUI.m_treeCtrl1,self.EL)
        self.File_saved=True
        self.Filename_defined=True
        myfile.close()
        event.Skip()

    def Define_filename(self):
        with wx.FileDialog(self.GUI, wildcard = "xml file (*.xml)|*.xml", 
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return ""    
            s=fileDialog.GetPath()
            return s
    
    def File_save(self, event):
        """menu file save
        Save the current project in xml"""
        if not(self.Filename_defined):
            self.Filename=self.Define_filename()
            if self.Filename=="":
                self.Filename="data1.xml"
            self.Filename_defined=True
        self.fs.Save_xml(self.GUI.m_treeCtrl1,self.Filename)
        event.Skip()

    def Define_filename_export(self):
        with wx.FileDialog(self.GUI, "Export file", \
            wildcard = "txt file (*.txt)|*.txt|Json File (*.json)|*.json",\
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return ""    

            # save the current contents in the file
            return fileDialog.GetPath()

    def File_save_as(self, event):
        """menu file save as
        Save the current project in xml"""

        self.Filename=self.Define_filename()
        if self.Filename=="":
            self.Message("Error : can not use Filename ")
            return -1
        else:
            self.Filename_defined=True
            self.fs.Save_xml(self.GUI.m_treeCtrl1,self.Filename)
            file=self.Filename
        event.Skip()

    def File_export(self, event):
        """menu file export
        Export the current project in txt|bmp|Json|"""
#        wx.SystemOptions.SetOption(wx.OSX_FILEDIALOG_ALWAYS_SHOW_TYPES, 1)
        
        file=self.Define_filename_export()
        if file=="":
            self.Message("Error : can not use Filename ")
            return -1
        
        str=file.split('.')
        str2=str[len(str)-1]
        if str2=="json":
            self.Filename_json=file
            self.fs.Generate_json(file, self)
        if str2=="txt":
            self.Filename_txt=file
            self.fs.Generate_txt(file,self)

        event.Skip()

    def File_close(self, event):
        """menu file close""" 
#        self.GUI.m_textCtrl2.AppendText("test file close\n")
        if not(self.File_saved):
            if not(self.Filename_defined):
                s="Save file"
                self.Filename=self.Define_filename(s)
                if self.Filename=="":
                    self.parent.Message("Error : can not use Filename ")
                    return -1
                else:
                    self.Filename_defined=True
                    self.fs.Save_xml(self.GUI.m_treeCtrl1,self.Filename)
        exit(0)
        event.Skip()

    def Message(self,msg):
        self.GUI.m_textCtrl2.AppendText(msg+"\n")

    def Message_dialog(self,msg_1 : str, categorie : int):
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