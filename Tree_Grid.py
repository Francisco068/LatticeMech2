import wx   
from wx3.GUI_Forms import *
from LatticeMech2 import *
from lattice_objects import *

class Tree_Grid_operations():
    # def __init__(self,tree: wx.TreeCtrl,grid: wx.grid.Grid,EL: elements):
    def __init__(self,tree: wx.TreeCtrl,grid: wx.grid.Grid,EL):
        self.tree=tree
        self.grid=grid
        self.EL=EL

    def Search_branch_tree_ctrl_perso(self,nom):
        """Search in tree ctrl for branch "nom"
        return -1,0,0 if no branch "nom" is found
        return -2,item branch,0 if branch "nom" is found without child
        return 1, item branch, item last child if branch "nom" is found and have childs
        """
        item1=self.tree.GetRootItem()
        item2=self.tree.GetFirstChild(item1)
        f=True
        while  (f):
            str1=self.tree.GetItemText(item2[0])
            str2=str1.replace(':','')
            if str2==nom:
                break
            item2=self.tree.GetNextChild(item2[0],item2[1])
            f=item2[0].IsOk()
            if f==False:
                return -1, 0,0
        item3=self.tree.GetFirstChild(item2[0])
        f=item3[0].IsOk()
        if f==False:
            return -2,item2[0],0
        while  (f):
            item4=self.tree.GetNextChild(item3[0],item3[1])
            f=item4[0].IsOk()
            if f==False:
                break 
            item3=item4
        return 1, item2[0],item3[0]

    def Search_item_tree_ctrl_perso(self,nom,numero):
        """    Search_item_tree_ctrl_perso(nom,numero): Search an item in child named "nom" 
                with identifier "numero"
                
                "nom" must be 'Profiles' or 'Nodes' or 'Periods' or'Beams' 
                return -1,0 if the branch with name "nom" not found 
                            or if none child have identifier "numero"
                return -2,0 if there's no child in branch
                return 1, item if item found
                """
        item1=self.tree.GetRootItem()

        item2=self.tree.GetFirstChild(item1)
        str1=self.tree.GetItemText(item2[0])
        f=True
        while  (f):
            str2=str1.replace(':','')
            if str2==nom:
                break
            item2=self.tree.GetNextChild(item2[0],item2[1])
            f=item2[0].IsOk()
            if f==False:
                return -1, 0
            str1=self.tree.GetItemText(item2[0])
        
        item2=self.tree.GetFirstChild(item2[0])
        f=item2[0].IsOk()
        if f==False:
            return -2,0
        f=True
        while  (f):
            str1=self.tree.GetItemText(item2[0])   
            str2=str1.split(':')
            str3=str2[0].split('.')
            if int(str3[1])==numero:
                return 1, item2[0]
            item2=self.tree.GetNextChild(item2[0],item2[1])
            f=item2[0].IsOk()
            if f==False:
                break 
        return -1, 0
        
    def Selection_item(self, item_1: wx.TreeItemId):  
        """Copy values of item in tree ctrl to grid"""
        
        str_2 = self.tree.GetItemText(item_1)
        str_3 = str_2.split(':')
        str_4 = str_3[0].split('.')
        try:
            str_5 = str_3[1].split(',')
        except :
            return -1
        

        if (str_4[0]=="Profile"):
            self.Set_grid_perso(["E","nu","section","width"],str_3[0],str_5)
            self.EL.active_profile=int(str_4[1])

        if (str_4[0].strip()=="Y"):
            self.Set_grid_perso(["X","Y"],str_3[0],str_5)
        
        if (str_4[0].strip()=="N"):
            self.Set_grid_perso(["X","Y"],str_3[0],str_5)
        
        if (str_4[0].strip()=="beam"):
            self.Set_grid_perso(["node 1","node 2","delta 1","delta 2","profile"],str_3[0],str_5)

    def Set_grid_perso(self,labels_col,labels_row,cells):
        """Set_grid_perso(self,col,row,labels_col,labels_row,cells)"""
        col=len(labels_col)
        Number_cols=self.grid.GetNumberCols()
        Number_rows=self.grid.GetNumberRows()
        if Number_cols>col :
            self.grid.DeleteCols(col,Number_cols-col)
        if Number_cols<col:
            self.grid.AppendCols(col-Number_cols)
        for i in range(col):
            self.grid.SetColLabelValue(i, labels_col[i])
        self.grid.SetRowLabelValue(0, labels_row)
        
        for i in range(len(cells)):
            self.grid.SetCellValue(0,i,cells[i])

    def Add_tree_node(self,node):
        resultat=self.Search_branch_tree_ctrl_perso("Nodes")
        if (resultat[0]==-1):
            self.Message("Error: no branch of Node inputs")
            return

        str_tree="N.%i:%5.2f,%5.2f" % (node.number,node.x,node.y)

        self.tree.AppendItem(resultat[1],str_tree)
    
    def Add_tree_beam(self,beam):
        resultat=self.Search_branch_tree_ctrl_perso("Beams")
        if (resultat[0]==-1):
            self.Message("Error: No branch of beam inputs\n")
            return
            
        str_tree="beam.%i:%i,%i,%i,%i,%i" % (beam.number,beam.node_1\
            ,beam.node_2,beam.delta_1,beam.delta_2,beam.profile)
        self.tree.AppendItem(resultat[1],str_tree)
    
    def Remove_tree_node(self,numero: int):
        Item1=self.Search_item_tree_ctrl_perso("Nodes",numero)
        if Item1[0]==1:
            self.tree.Delete(Item1[1])
        else:
            self.Message("Error : Point not found in the tree\n")

    
    def Remove_tree_beam(self,numero: int):
        Item1=self.Search_item_tree_ctrl_perso("Beams",numero)
        if Item1[0]==1:
            self.tree.Delete(Item1[1])
        else:
            self.Message("Error : Element not found in the tree\n")
    
    def ReplaceTreeCtrl(self,item,str):
        """    Replace the string str associate with item in tree_ctrl 
                with identifier "numero"
                
                return -1 if the item is not not found 
                    else 0
                """
        item1=self.tree.GetRootItem()

        item2=self.tree.GetFirstChild(item1)
        f1=item2[0].IsOk()
        if f1==False:
            return -1
        while  (f1):
            item3=self.tree.GetFirstChild(item2[0])
            f2=item3[0].IsOk()
            if f2==False:
                break
            while (f2):
                str1=self.tree.GetItemText(item3[0])
                str2=str1.split(':')
                if str2[0]==item:
                    self.tree.SetItemText(item3[0],str)
                    f2=0
                    return 0
                item3=self.tree.GetNextChild(item3[0],item3[1])
                f2=item3[0].IsOk()
                if f2==False:
                    break 
            item2=self.tree.GetNextChild(item2[0],item2[1])
            f1=item2[0].IsOk()
            if f1==False:
                return -1    
        return -1
        
    
    def Modify_TG_from_cell(self, panel: wx.Panel):
        
        RowLabel=self.grid.GetRowLabelValue(0)
        name=RowLabel.split('.')
        number=int(name[1])
        str1=""
        for i in range(self.grid.GetNumberCols()):
            str1=str1+self.grid.GetCellValue(0,i)
            if i!=(self.grid.GetNumberCols()-1):
                str1=str1+','
        str1=RowLabel+':'+str1
        self.ReplaceTreeCtrl(RowLabel,str1)
        panel.Refresh()
        return str1

        pass

        # if (name[0]=="Profile"):
        #     str3="Material"
        #     val1=self.grid_1.GetCellValue(0,0)
        #     str_tree="modulus(GPa):"+str(val1)
        #     resultat=self.Search_branch_tree_ctrl_perso(str3)
        #     if resultat[0]==1:
        #         self.tree_ctrl_1.SetItemText(resultat[2],str_tree)
        #     else:
        #         self.Message_dialog("None entry found in tree ctrl",wx.ICON_ERROR)

        # if str2[0]=="N":
        #     str3="Nodes"
        #     val1=self.grid_1.GetCellValue(0,0)
        #     val2=self.grid_1.GetCellValue(0,1)
        #     str_tree='N'+'.'+str(numero)+':'+'('+val1+','+val2+')'
        #     f=0
        #     for i in self.EL.nodes:
        #         if i.number==numero :
        #             i.x=float(val1)
        #             i.y=float(val2)
        #             f=1
        #             break
        #     if f==0 :
        #         print("node not found")
        # if str2[0]=="Y":
        #     str3="Basis"
        #     val1=self.grid_1.GetCellValue(0,0)
        #     val2=self.grid_1.GetCellValue(0,1)
        #     str_tree='Y'+'.'+str(numero)+':'+'('+val1+','+val2+')'
        #     f=0
        #     for i in self.EL.periods:
        #         if i.number==numero :
        #             vect=np.array([float(val1),float(val2)])
        #             i.length=np.linalg.norm(vect)
        #             vect2=normalize_vector(vect)
        #             i.x=vect2[0]
        #             i.y=vect2[1]
        #             f=1
        #             break
        #     if f==0 :
        #         print("period vector not found")

        # if str2[0]=="beam":
        #     str3="Beams"
        #     val1=self.grid_1.GetCellValue(0,0)
        #     val2=self.grid_1.GetCellValue(0,1)
        #     val3=self.grid_1.GetCellValue(0,2)
        #     val4=self.grid_1.GetCellValue(0,3)
        #     val5=self.grid_1.GetCellValue(0,4)
        #     val6=self.grid_1.GetCellValue(0,5)
        #     str_tree='beam'+'.'+str(numero)+':'+'('+val1+','+val2+')'+',('+val3+','+val4+')'+','+val5+','+val6
        #     f=0
        #     for i in self.EL.beams:
        #         if i.number==numero :
        #             i.node_1=int(val1)
        #             i.node_2=int(val2)
        #             i.delta_1=int(val3)
        #             i.delta_2=int(val4)
        #             i.section=val5
        #             i.width=float(val6)
        #             i.evaluate_k(self.EL)
        #             f=1
        #             break
        #     if f==0 :
        #         print("period vector not found")

        # resultat=self.Search_item_tree_ctrl_perso(str3,numero)
        # if resultat[0]==1:
        #     self.tree_ctrl_1.SetItemText(resultat[1],str_tree)
        # else:
        #     self.Message_dialog("None entry found in tree ctrl",wx.ICON_ERROR)
            


    
    def Grid_init(self):
        str1=["X","Y"]
        str2="Y.1"
        str3=["1","0"]
        self.Set_grid_perso(str1,str2,str3)


    def TreeCtrl_init(self):
        """Initialise Tree Ctrl"""
        Tree_Lattice_Id=self.tree.AddRoot("Lattice")
        ProfilId=self.tree.AppendItem(Tree_Lattice_Id,"Profiles:")
        BasisId=self.tree.AppendItem(Tree_Lattice_Id, "Basis:")
        NodesId=self.tree.AppendItem(Tree_Lattice_Id, "Nodes:")
        BeamsId=self.tree.AppendItem(Tree_Lattice_Id, "Beams:")
        self.tree.AppendItem(BasisId, "Y.1:1,0")
        self.tree.AppendItem(BasisId, "Y.2:0,1")
        self.tree.AppendItem(NodesId, "N.1:0,0")
        self.tree.AppendItem(ProfilId, "Profile.1:210000,0.3,rect,0.3")
        self.tree.ExpandAll()