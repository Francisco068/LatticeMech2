from LatticeMech2 import *
import xml.etree.ElementTree as ET
import wx
from latticeObjects import *
import copy

class Files_system():
    def __init__(self,*args):
        pass

    def Open_xml(self,treeXml: ET, treeCtrl: wx.TreeCtrl,EL):
        root=treeXml.getroot()
        treeCtrl.DeleteAllItems()
        EL.Delete_all_items()

        Item1=treeCtrl.AddRoot(root.text)

        for child1 in root:
            Item2=treeCtrl.AppendItem(Item1,child1.text)
            for child2 in child1:
                treeCtrl.AppendItem(Item2,child2.text)
                str0=child2.text
                str1=str0.split(':')
                str10=str1[0].split('.')
                str11=str1[1].split(',')

                if str10[0]=="Profile":
                    EL.profiles.append(EL.Str2profile(str0))

                if str10[0]=="Y":
                    EL.periods.append(EL.Str2Y(str0))

                if str10[0]=="N":
                    EL.nodes.append(EL.Str2N(str0))

                if str10[0]=="beam":
                    EL.beams.append(EL.Str2beam(str0,EL))

        treeCtrl.ExpandAll()

    def Save_xml(self,tree,file):
        tree_root=tree.GetRootItem()
        str1=tree.GetItemText(tree_root)
        xml_root=ET.Element("root")
        xml_root.text=str1
        item_child1=tree.GetFirstChild(tree_root)
        while True:
            xml_child1=ET.SubElement(xml_root,"child1")
            str1=tree.GetItemText(item_child1[0])
            xml_child1.text=str1
            item_child2=tree.GetFirstChild(item_child1[0])
            if item_child2[0].IsOk():
                while True:
                    str1=tree.GetItemText(item_child2[0])
                    xml_child2=ET.SubElement(xml_child1,"child2")
                    xml_child2.text=str1
                    item_child2=tree.GetNextChild(item_child2[0],item_child2[1])
                    if not(item_child2[0].IsOk()):
                        break
            item_child1=tree.GetNextChild(item_child1[0],item_child1[1])
            if not(item_child1[0].IsOk()):
                break
        mydata=ET.tostring(xml_root,encoding='unicode',method='xml')
        try:
            myfile=open(file,'w')
            myfile.write(mydata)
            myfile.close()
        except IOError:
            self.parent.Message_dialog("IOError",wx.ICON_ERROR)
        self.File_saved=True

    def Generate_json(self,file,parent: GUI3D):
        """[summary]
        
        Arguments:
            file {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """        
        myfile=open(file,"w+")
        myfile.write("{\n")
        # Write number of elements
        myfile.write("\"comment1\": \"Define the number of elements\",\n")
        Number_beams=len(parent.EL.beams)
        if (Number_beams<1):
            parent.Message_dialog("Error:There's no beam",wx.ICON_ERROR)
            myfile.close()
            return -1
        myfile.write("\"NumberElements\": %i,\n" % Number_beams)
        # Write the direction vectors of each element
        myfile.write("\"comment2\": \"Define the direction vectors of each element\",\n")
        for i in parent.EL.beams:
            myfile.write("\"e_%i\":[%6.4f,%6.4f],\n" % (i.number,i.e_x,i.e_y))
        # Write basis periodicity vectors
        myfile.write("\"comment3\": \"define the global periodicity vectors\",\n")
        for i in parent.EL.periods:
            myfile.write("\"Y_%i\":[%6.4f,%6.4f],\n" % (i.number,i.x,i.y))
        # Write number node
        myfile.write("\"comment4\": \"number of inner nodes\",\n")
        Number_nodes=len(parent.EL.nodes)
        myfile.write("\"NumberNodes\": %i,\n" % Number_nodes)
        # Write List of origin and end points along with delta
        myfile.write("\"comment5\": \"List of origin and end points along with delta\",\n")
        str_Ob="\"Ob\": ["
        str_Eb="\"Eb\": ["
        str_Delta1="\"Delta1\": ["
        str_Delta2="\"Delta2\": ["
        for i in parent.EL.beams:
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
        for i in parent.EL.beams:
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
        for i in parent.EL.beams:
            str_Lb=str_Lb+str(i.length)+','
            prof=parent.EL.IndexObject(i.profile,parent.EL.profiles)[0]
            str_tb=str_tb+str(prof.width)+','
        str_Lb=str_Lb[0:len(str_Lb)-1]+"],\n"
        str_tb=str_tb[0:len(str_tb)-1]+"],\n"
        myfile.write(str_Lb)
        myfile.write(str_tb)
        # Write norme of the periodicity vectors
        myfile.write("\"comment8\": \"Norme of the periodicity vectors\",\n")
        str1=""
        for i in parent.EL.periods:
            str1=str1+"\"L%i\":%6.4f,\n" % (i.number,i.length)
        str1=str1[0:len(str1)-2]+"\n"
        myfile.write(str1)
        myfile.write("}\n")
        myfile.close()
        return 0

    def Generate_txt(self,file,parent: GUI3D):

        parent.EL.Fill_voids()

        myfile=open(file,"w+")
        # Write number of elements
        myfile.write("# Define the number of elements\n")
        Number_beams=len(parent.EL.beams)
        if (Number_beams<1):
            self.Message_dialog("Error:There's no beam",wx.ICON_ERROR)
            myfile.close()
            return -1
        myfile.write("nBarres:= %i;\n" % Number_beams)
        # Write the direction vectors of each element
        myfile.write("# Define the direction vectors of each element\n")
        for i in parent.EL.beams:
            myfile.write("e[%i]:=[%10e,%10e];\n" % (i.number,i.e_x,i.e_y))

        # Write basis periodicity vectors
        myfile.write("# define the global periodicity vectors\n")
        for i in parent.EL.periods:
            myfile.write("Y%i:=<%10e,%10e>;\n" % (i.number,i.x,i.y))
        
        # Write norme of the periodicity vectors
        myfile.write("# Norme of the periodicity vectors\n")
        for i in parent.EL.periods:
            myfile.write("L%i:=%10e;\n" % (i.number,i.length))

        # Write number node
        myfile.write("# number of inner nodes\n")
        Number_nodes=len(parent.EL.nodes)
        myfile.write("nNoeuds:= %i;\n" % Number_nodes)

        # Write List of origin and end points along with delta
        myfile.write("# List of origin and end points along with delta\n")
        str_Ob="Ob:=["
        str_Eb="Eb:=["
        str_Delta1="delta1:=["
        str_Delta2="delta2:=["
        for i in parent.EL.beams:
            str_Ob=str_Ob+str(i.node_1)+','
            str_Eb=str_Eb+str(i.node_2)+','
            str_Delta1=str_Delta1+str(i.delta_1)+','
            str_Delta2=str_Delta2+str(i.delta_2)+','
        str_Ob=str_Ob[0:len(str_Ob)-1]+"];\n"
        str_Eb=str_Eb[0:len(str_Eb)-1]+"];\n"
        str_Delta1=str_Delta1[0:len(str_Delta1)-1]+"];\n"
        str_Delta2=str_Delta2[0:len(str_Delta2)-1]+"];\n"
        myfile.write(str_Ob)
        myfile.write(str_Eb)
        myfile.write(str_Delta1)
        myfile.write(str_Delta2)
        # Write list of element axial and bending stiffness
        myfile.write("# List of element axial and bending stiffness\n")
        str_Ka="Kb:=["
        str_Kb="Kc:=["
        for i in parent.EL.beams:
            str_Ka=str_Ka+"%10e" % i.ka +','
            str_Kb=str_Kb+"%10e" % i.kb+','
        str_Ka=str_Ka[0:len(str_Ka)-1]+"];\n"
        str_Kb=str_Kb[0:len(str_Kb)-1]+"];\n"
        myfile.write(str_Ka)
        myfile.write(str_Kb)
        # Write list of element lengths and volumes
        myfile.write("# List of element lengths and volumes\n")
        str_Lb="Lb:=["
        str_tb="Tb:=["
        str_Vb="Vb:=["
        for i in parent.EL.beams:
            str_Lb=str_Lb+"%10e" % i.length+','
            prof=parent.EL.IndexObject(i.profile,parent.EL.profiles)[0]
            str_tb=str_tb+"%10e" % prof.width+','
            str_Vb=str_Vb+"%10e" % (i.length*prof.width)+','
        str_Lb=str_Lb[0:len(str_Lb)-1]+"];\n"
        str_tb=str_tb[0:len(str_tb)-1]+"];\n"
        str_Vb=str_Vb[0:len(str_Vb)-1]+"];\n"
        myfile.write(str_Lb)
        myfile.write(str_tb)
        myfile.write(str_Vb)
        myfile.close()
        return 0

