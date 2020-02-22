from LatticeMech_3D_Gui import *
import xml.etree.ElementTree as ET
import wx

class Files_system():
    def __init__(self, parent,*args):
        self.File_saved = False
        self.Filename_defined = False
        self.Filename =""
        self.Filename_export_define = False
        self.Filename_export =""
        self.parent=parent

    def Open_file(self):
            """Open the xml file -> create tree ctrl and elements""" 
            if not(self.File_saved):
                rep=self.parent.Message_dialog("Current content has not been saved! Proceed?")
                if rep==wx.YES:
                    self.Save_file()
            
            with wx.FileDialog(parent, "Open XML file", wildcard="xml files (*.xml)|*.xml",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return     # the users changed their mind

                # Proceed loading the file chosen by the user
                parent.Filename = fileDialog.GetPath()
                try:
                    myfile=open(parent.Filename, 'r')
                except IOError:
                    wx.LogError("Cannot open file '%s'." % parent.Filename)
                    return -1
            try:
                tree=ET.parse(myfile)
            except:
                parent.Message_perso("Unable to parse file",wx.ICON_ERROR)
                myfile.close()
                return
            root=tree.getroot()
            parent.tree_ctrl_1.DeleteAllItems()
            parent.EL=elements()
            Item1=parent.tree_ctrl_1.AddRoot(root.text)
            for child1 in root:
                Item2=parent.tree_ctrl_1.AppendItem(Item1,child1.text)
                for child2 in child1:
                    parent.tree_ctrl_1.AppendItem(Item2,child2.text)
                    str0=child2.text
                    str0=str0.replace('(','').replace(')','')
                    str1=str0.split(':')
                    str10=str1[0].split('.')
                    str11=str1[1].split(',')

                    if str10[0]=="modulus(GPa)":
                        Material_E=float(str11[0])
                    if str10[0]=="Y":
                        x=float(str11[0])
                        y=float(str11[1])
                        vect=np.array([x,y])
                        vect1=normalize_vector(vect)
                        L=np.linalg.norm(vect)
                        parent.EL.periods.append(periodicity(vect1[0],vect1[1],L,int(str10[1])))
                    if str10[0]=="N":
                        x=float(str11[0])
                        y=float(str11[1])
                        parent.EL.nodes.append(node(x,y,5,int(str10[1])))
                    if str10[0]=="beam":
                        node_1=int(str11[0])
                        node_2=int(str11[1])
                        delta_1=int(str11[2])
                        delta_2=int(str11[3])
                        width=float(str11[5])
                        number=int(str10[1])
                        parent.EL.beams.append(beam(node_1,node_2,delta_1,delta_2,str11[4],0,width,0,0,0,0,Material_E,number))
                        a=parent.EL.beams[len(parent.EL.beams)-1]
                        a.evaluate_k(parent.EL)
            parent.tree_ctrl_1.ExpandAll()
            parent.panel_1.reassign_EL(parent.EL)
            parent.File_saved=True
            parent.Filename_defined=True
            myfile.close()

    def Define_filename_export(self):
        with wx.FileDialog(self.parent.GUI, "Save file", \
            wildcard = "txt file (*.txt)|*.txt|Json File (*.json)|*.json|bmp file (*.bmp)|*.bmp",\
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return ""    

            # save the current contents in the file
            return fileDialog.GetPath()

    def Define_filename(self,s):
        with wx.FileDialog(self.parent.GUI, set_iterator, \
            wildcard = "xml file (*.xml)",\
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return ""    

            # save the current contents in the file
            return fileDialog.GetPath()

    def Save_file_as(self):
        """Save the current project in xml"""
#        wx.SystemOptions.SetOption(wx.OSX_FILEDIALOG_ALWAYS_SHOW_TYPES, 1)
        
        s="Save file as"
        self.Filename=self.Define_filename(s)
        if self.Filename=="":
            self.parent.Message("Error : can not use Filename ")
            return -1
        else:
            self.Filename_defined=True
        
        file=self.Filename

    def Export_file(self):
        """Export the current project in txt|bmp|Json|"""
#        wx.SystemOptions.SetOption(wx.OSX_FILEDIALOG_ALWAYS_SHOW_TYPES, 1)
        
        s="Export file"
        self.Filename_export=self.Define_filename_export(s)
        if self.Filename=="":
            self.parent.Message("Error : can not use Filename ")
            return -1
        else:
            self.Filename_export_defined=True
        
        file=self.Filename_export

    def Save_file(self):
        """Save the current project in xml"""
#        wx.SystemOptions.SetOption(wx.OSX_FILEDIALOG_ALWAYS_SHOW_TYPES, 1)
        if not(self.Filename_defined):
            s="Save file"
            self.Filename=self.Define_filename(s)
            if self.Filename=="":
                self.parent.Message("Error : can not use Filename ")
                return -1
            else:
                self.Filename_defined=True
        
        file=self.Filename
        tree_root=self.tree_ctrl_1.GetRootItem()
        str1=self.tree_ctrl_1.GetItemText(tree_root)
        xml_root=ET.Element("root")
        xml_root.text=str1
        item_child1=self.tree_ctrl_1.GetFirstChild(tree_root)
        while True:
            xml_child1=ET.SubElement(xml_root,"child1")
            str1=self.tree_ctrl_1.GetItemText(item_child1[0])
            xml_child1.text=str1
            item_child2=self.tree_ctrl_1.GetFirstChild(item_child1[0])
            if item_child2[0].IsOk():
                while True:
                    str1=self.tree_ctrl_1.GetItemText(item_child2[0])
                    xml_child2=ET.SubElement(xml_child1,"child2")
                    xml_child2.text=str1
                    item_child2=self.tree_ctrl_1.GetNextChild(item_child2[0],item_child2[1])
                    if not(item_child2[0].IsOk()):
                        break
            item_child1=self.tree_ctrl_1.GetNextChild(item_child1[0],item_child1[1])
            if not(item_child1[0].IsOk()):
                break
        mydata=ET.tostring(xml_root,encoding='unicode',method='xml')
        try:
            myfile=open(file,'w')
            myfile.write(mydata)
            myfile.close()
        except IOError:
            self.Message_perso("IOError",wx.ICON_ERROR)
        self.File_saved=True

    def Generate_json(self,file):
        myfile=open(file,"w+")
        myfile.write("{\n")
        # Write number of elements
        myfile.write("\"comment1\": \"Define the number of elements\",\n")
        Number_beams=len(self.EL.beams)
        if (Number_beams<1):
            self.Message_perso("Error:There's no beam",wx.ICON_ERROR)
            myfile.close()
            return -1
        myfile.write("\"NumberElements\": %i,\n" % Number_beams)
        # Write the direction vectors of each element
        myfile.write("\"comment2\": \"Define the direction vectors of each element\",\n")
        for i in self.EL.beams:
            myfile.write("\"e_%i\":[%6.4f,%6.4f],\n" % (i.number,i.e_x,i.e_y))
        # Write basis periodicity vectors
        myfile.write("\"comment3\": \"define the global periodicity vectors\",\n")
        for i in self.EL.periods:
            myfile.write("\"Y_%i\":[%6.4f,%6.4f],\n" % (i.number,i.x,i.y))
        # Write number node
        myfile.write("\"comment4\": \"number of inner nodes\",\n")
        Number_nodes=len(self.EL.nodes)
        myfile.write("\"NumberNodes\": %i,\n" % Number_nodes)
        # Write List of origin and end points along with delta
        myfile.write("\"comment5\": \"List of origin and end points along with delta\",\n")
        str_Ob="\"Ob\": ["
        str_Eb="\"Eb\": ["
        str_Delta1="\"Delta1\": ["
        str_Delta2="\"Delta2\": ["
        for i in self.EL.beams:
            str_Ob=str_Ob+str(i.node_1)+','
            str_Eb=str_Eb+str(i.node_2)+','
            str_Delta1=str_Delta1+str(i.delta_1)+','
            str_Delta2=str_Delta2+str(i.delta_2)+','
        str_Ob=str_Ob[0:len(str_Ob)-1]+"],\n"
        str_Eb=str_Eb[0:len(str_Eb)-1]+"],\n"
        str_Delta1=str_Delta1[0:len(str_Delta1)-1]+"],\n"
        str_Delta2=str_Delta2[0:len(str_Delta2)-1]+"],\n"
        myfile.write(str_Ob)
        myfile.write(str_Eb)
        myfile.write(str_Delta1)
        myfile.write(str_Delta2)
        # Write list of element axial and bending stiffness
        myfile.write("\"commentt6\": \"List of element axial and bending stiffness\",\n")
        str_Ka="\"Ka\": ["
        str_Kb="\"Kb\": ["
        for i in self.EL.beams:
            str_Ka=str_Ka+str(i.ka)+','
            str_Kb=str_Kb+str(i.kb)+','
        str_Ka=str_Ka[0:len(str_Ka)-1]+"],\n"
        str_Kb=str_Kb[0:len(str_Kb)-1]+"],\n"
        myfile.write(str_Ka)
        myfile.write(str_Kb)
        # Write list of element lengths and volumes
        myfile.write("\"comment7\": \"List of element lengths and volumes\",\n")
        str_Lb="\"Lb\": ["
        str_tb="\"tb\": ["
        for i in self.EL.beams:
            str_Lb=str_Lb+str(i.length)+','
            str_tb=str_tb+str(i.width)+','
        str_Lb=str_Lb[0:len(str_Lb)-1]+"],\n"
        str_tb=str_tb[0:len(str_tb)-1]+"],\n"
        myfile.write(str_Lb)
        myfile.write(str_tb)
        # Write norme of the periodicity vectors
        myfile.write("\"comment8\": \"Norme of the periodicity vectors\",\n")
        str1=""
        for i in self.EL.periods:
            str1=str1+"\"L%i\":%6.4f,\n" % (i.number,i.length)
        str1=str1[0:len(str1)-2]+"\n"
        myfile.write(str1)
        myfile.write("}\n")
        myfile.close()
        return 0

    def Generate_txt(self,file):
        myfile=open(file,"w+")
        # Write number of elements
        myfile.write("# Define the number of elements\n")
        Number_beams=len(self.EL.beams)
        if (Number_beams<1):
            self.Message_perso("Error:There's no beam",wx.ICON_ERROR)
            myfile.close()
            return -1
        myfile.write("NumberElements= %i\n" % Number_beams)
        # Write the direction vectors of each element
        myfile.write("# Define the direction vectors of each element\n")
        for i in self.EL.beams:
            myfile.write("e_%i=[%6.4f,%6.4f]\n" % (i.number,i.e_x,i.e_y))
        # Write basis periodicity vectors
        myfile.write("# define the global periodicity vectors\n")
        for i in self.EL.periods:
            myfile.write("Y_%i=[%6.4f,%6.4f]\n" % (i.number,i.x,i.y))
        # Write number node
        myfile.write("# number of inner nodes\n")
        Number_nodes=len(self.EL.nodes)
        myfile.write("NumberNodes= %i\n" % Number_nodes)
        # Write List of origin and end points along with delta
        myfile.write("# List of origin and end points along with delta\n")
        str_Ob="Ob=["
        str_Eb="Eb=["
        str_Delta1="Delta1=["
        str_Delta2="Delta2=["
        for i in self.EL.beams:
            str_Ob=str_Ob+str(i.node_1)+','
            str_Eb=str_Eb+str(i.node_2)+','
            str_Delta1=str_Delta1+str(i.delta_1)+','
            str_Delta2=str_Delta2+str(i.delta_2)+','
        str_Ob=str_Ob[0:len(str_Ob)-1]+"]\n"
        str_Eb=str_Eb[0:len(str_Eb)-1]+"]\n"
        str_Delta1=str_Delta1[0:len(str_Delta1)-1]+"]\n"
        str_Delta2=str_Delta2[0:len(str_Delta2)-1]+"]\n"
        myfile.write(str_Ob)
        myfile.write(str_Eb)
        myfile.write(str_Delta1)
        myfile.write(str_Delta2)
        # Write list of element axial and bending stiffness
        myfile.write("# List of element axial and bending stiffness\n")
        str_Ka="Ka=["
        str_Kb="Kb=["
        for i in self.EL.beams:
            str_Ka=str_Ka+str(i.ka)+','
            str_Kb=str_Kb+str(i.kb)+','
        str_Ka=str_Ka[0:len(str_Ka)-1]+"]\n"
        str_Kb=str_Kb[0:len(str_Kb)-1]+"]\n"
        myfile.write(str_Ka)
        myfile.write(str_Kb)
        # Write list of element lengths and volumes
        myfile.write("# List of element lengths and volumes\n")
        str_Lb="Lb=["
        str_tb="tb=["
        for i in self.EL.beams:
            str_Lb=str_Lb+str(i.length)+','
            str_tb=str_tb+str(i.width)+','
        str_Lb=str_Lb[0:len(str_Lb)-1]+"]\n"
        str_tb=str_tb[0:len(str_tb)-1]+"]\n"
        myfile.write(str_Lb)
        myfile.write(str_tb)
        # Write norme of the periodicity vectors
        myfile.write("# Norme of the periodicity vectors\n")
        for i in self.EL.periods:
            myfile.write("L%i=%6.4f\n" % (i.number,i.length))
        myfile.close()
        return 0

    def File_save_bmp(self,event):
        self.panel_1.save_bmp()
        self.panel_1.GetCapture()
        event.Skip()