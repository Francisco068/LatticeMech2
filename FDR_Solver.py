# FDR_Solver
import lattice_objects 
import numpy as np
import copy

class solverFDR():
    # def __init__(self,EL2: elements):
    # solve [K][X]=[B]
    # use of virtual strain notation '_vs'
    # in _vs variables the last four coeff -> (dUx/dx, dUx/dy, dUy/dx, dUy/dy)
    def __init__(self,EL2):
        self.P1=np.array(2)
        self.P2=np.array(2)
        self.nbeams=len(EL2.beams)
        self.nnodes=len(EL2.nodes)
        self.e=np.zeros(2*self.nbeams,dtype=np.float32).reshape((self.nbeams,2))
        self.eT=np.zeros(2*self.nbeams,dtype=np.float32).reshape((self.nbeams,2))
        self.X=np.zeros(3*self.nnodes*4,dtype=np.float32).reshape((3*self.nnodes,4))

        self.B=np.zeros(3*4*self.nnodes,dtype=np.float32).reshape((3*self.nnodes,4))
        self.K=np.zeros(9*self.nnodes*self.nnodes,dtype=np.float32).reshape((3*self.nnodes,3*self.nnodes))
        self.GenerateDirectors(self.e,self.eT,EL2)
        #
        self.dU=self.GeneratedU(EL2)

        self.N_vs=np.zeros((3*self.nnodes+4)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+4)
        self.T_vs=np.zeros((3*self.nnodes+4)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+4)
        self.M_ves=np.zeros((3*self.nnodes+4)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+4)
        self.M_vos=np.zeros((3*self.nnodes+4)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+4)
        self.GenerateForces_KB(EL2)
        self.SolveX()
        [self.N, self.T]=self.CalculateForces()
        [self.S1, self.S2]=self.CalculateSumForces(EL2)
        # Stiff Matrix : [sigma]=[Mat][strain]
        # [strain]=[dUx/dx, dUy/dy, dUx/dy, dUy/dx]^T 
        [self.Mat, self.MatVo, self.detg]=self.CalculateStiffness()
        [self.MS, self.MSVo, self.MSTe]=self.CalculateCompliance()
        self.CalculateModulus(EL2)
        [rho, K, Ex, Ey, nuyx, nuxy, muxy, etaxxy, etayxy,\
            etaxyx, etaxyy ]=self.CalculateModulus(EL2)
        print("rho={}\nK={}\nEx={}\nEy={}\nnuyx={}\nnuxy={}\nmuxy={}\netaxxy={}\netayxy={}\netaxyx={}\netaxyy={}\n".format(rho,K, Ex, Ey, nuyx,\
            nuxy, muxy, etaxxy, etayxy, etaxyx, etaxyy))

    def CalculateModulus(self,EL2):
        rho=0
        for i in EL2.beams:
            # todo : modifier la recherche de la largeur
            prof=EL2.index_profile(i.profile)
            V=i.length*EL2.profiles[prof[1]].width
            rho=rho+V
        rho=rho/self.detg
        K=1/(self.MSTe[0,0]+self.MSTe[0,1]+self.MSTe[1,0]+self.MSTe[1,1]) 
        Ex=1/self.MSTe[0,0]; Ey=1/self.MSTe[1,1]
        nuyx=-self.MSTe[0,1]*Ey; nuxy=-self.MSTe[1,0]*Ex
        muxy=1/(2*self.MSTe[2,2])
        etaxxy=self.MSTe[0,2]*2*muxy
        etayxy=self.MSTe[1,2]*2*muxy
        etaxyx=self.MSTe[2,0]*Ex
        etaxyy=self.MSTe[2,1]*Ey
        
        return [rho, K, Ex, Ey, nuyx, nuxy, muxy,\
             etaxxy, etayxy, etaxyx, etaxyy ]

    def CalculateCompliance(self):
        try:
            MS=np.linalg.inv(self.Mat)
        except:
            print("error : unable to calculate compliance matrix")
            return -1
        # MS : compliance matrix in natural notations
        # MSVo : compliance matrix in Voigt notations
        # MSTe : compliance matrix in basis tensor notation
        MSVo=np.zeros((3,3))
        MSVo[0:2,0:2]=copy.deepcopy(MS[0:2,0:2])
        MSVo[0,2]=MS[0,2]+MS[0,3]
        MSVo[1,2]=MS[1,2]+MS[1,3]
        MSVo[2,0]=MS[2,0]+MS[3,0]
        MSVo[2,1]=MS[2,1]+MS[3,1]
        MSVo[2,2]=MS[2,2]+MS[3,2]+MS[2,3]+MS[3,3]
        MSTe=copy.deepcopy(MSVo)
        MSTe[0,2]=MSTe[0,2]/np.sqrt(2)
        MSTe[1,2]=MSTe[1,2]/np.sqrt(2)
        MSTe[2,0]=MSTe[2,0]/np.sqrt(2)
        MSTe[2,1]=MSTe[2,1]/np.sqrt(2)
        MSTe[2,2]=MSTe[2,2]/2
        return [MS, MSVo, MSTe]

    def CalculateStiffness(self):
        g=np.append(self.P1,self.P2).reshape((2,2))
        try:
            detg=np.linalg.det(g)
        except:
            print("error detg")
            return -1
        Mat=1/detg*(np.outer(self.P1,self.S1).reshape((4,4))+np.outer(self.P2,self.S2).reshape((4,4)))
        # rearrange (dUx/dx, dUy/dy, dUx/dy, dUy/dx)
        L=copy.deepcopy(Mat[3,:]); 
        Mat[3,:]=Mat[1,:]; 
        Mat[1,:]=L
        C=copy.deepcopy(Mat[:,3]); 
        Mat[:,3]=Mat[:,2]; 
        Mat[:,2]=Mat[:,1]; 
        Mat[:,1]=C
        # Mat : Stiffness matrix in natural notation
        # MatVo : Stiffness Matrix in Voigt notation
        MatVo=np.zeros((3,3))
        MatVo[0:3,0:2]=Mat[0:3,0:2]
        MatVo[0,2]=(Mat[0,2]+Mat[0,3])/2
        MatVo[1,2]=(Mat[1,2]+Mat[1,3])/2
        MatVo[2,2]=(Mat[2,2]+Mat[2,3])/2
        return [Mat,MatVo,detg]

    def CalculateSumForces(self,EL2):
        S1=np.zeros((2,4))
        S2=np.zeros((2,4))
        index=0
        for i in EL2.beams:
            if (i.delta_1!=0) or (i.delta_2!=0):
                S1=S1+i.delta_1*(self.N[index]*self.e[index].reshape((2,1))+self.T[index]*self.eT[index].reshape((2,1)))
                S2=S2+i.delta_2*(self.N[index]*self.e[index].reshape((2,1))+self.T[index]*self.eT[index].reshape((2,1)))
            index+=1
        return [S1, S2]
    
    def CalculateForces(self):
        N=self.N_vs[:,0:3*self.nnodes].dot(self.X)+self.N_vs[:,3*self.nnodes:3*self.nnodes+4]
        T=self.T_vs[:,0:3*self.nnodes].dot(self.X)+self.T_vs[:,3*self.nnodes:3*self.nnodes+4]
        return [N,T]
    
    def SolveX(self):
        K_r=self.K[2:3*self.nnodes,2:3*self.nnodes]
        try:
            K_i=np.linalg.inv(K_r)
        except np.linalg.LinAlgError:
            print("matrix error ")
            return -1
        self.X[2:3*self.nnodes,:]=K_i.dot(self.B[2:3*self.nnodes,:])
        omega_rigid=np.array([1/2,-1/2])
        for i in range(2,3*self.nnodes,3):
            self.X[i,1:3]=self.X[i,1:3]+omega_rigid
        pass

    def DotProduct_v(self,v: np.array,dUn: np.array):
        return v[0]*dUn[0]+v[1]*dUn[1]


    def GenerateForces_KB(self,EL2):
        index_beam=0
        for i in EL2.beams:
            index_n1=EL2.index_node(i.node_1)[1]
            index_n2=EL2.index_node(i.node_2)[1]
            # normal forces
            kae=i.ka*self.e[index_beam,:]
            deplN=self.DotProduct_v(i.delta_1*kae,self.dU[0])+self.DotProduct_v(i.delta_2*kae,self.dU[1])
            n=self.nnodes
            self.N_vs[index_beam,3*index_n2:3*index_n2+2]=kae
            self.N_vs[index_beam,3*index_n1:3*index_n1+2]=self.N_vs[index_beam,3*index_n1:3*index_n1+2]-kae

            self.N_vs[index_beam,3*n:3*n+4]=deplN
                                                
            # transverses forces
            kbe=i.kb*self.eT[index_beam,:]
            deplT=self.DotProduct_v(i.delta_1*kbe,self.dU[0])+self.DotProduct_v(i.delta_2*kbe,self.dU[1])
            self.T_vs[index_beam,3*index_n2:3*index_n2+2]=kbe
            self.T_vs[index_beam,3*index_n1:3*index_n1+2]=self.T_vs[index_beam,3*index_n1:3*index_n1+2]-kbe
            kbL=-i.kb*i.length/2
            self.T_vs[index_beam,3*index_n1+2]=kbL
            self.T_vs[index_beam,3*index_n2+2]=self.T_vs[index_beam,3*index_n2+2]+kbL

            self.T_vs[index_beam,3*n:3*n+4]=deplT
                                                
            # moments
            kbe2=-i.kb*self.eT[index_beam,:]*i.length/2
            self.M_ves[index_beam,3*index_n2:3*index_n2+2]=kbe2
            self.M_ves[index_beam,3*index_n1:3*index_n1+2]=\
                self.M_ves[index_beam,3*index_n1:3*index_n1+2]-kbe2

            kbL2=i.kb*i.length*i.length/6
            self.M_ves[index_beam,3*index_n1+2]=kbL2
            self.M_ves[index_beam,3*index_n2+2]=\
                self.M_ves[index_beam,3*index_n2+2]+2*kbL2
            
            kbL3=-i.length/2
            self.M_ves[index_beam,3*n:3*n+4]=kbL3*deplT

            self.M_vos[index_beam,3*index_n2:3*index_n2+2]=kbe2
            self.M_vos[index_beam,3*index_n1:3*index_n1+2]=\
                self.M_vos[index_beam,3*index_n1:3*index_n1+2]-kbe2

            self.M_vos[index_beam,3*index_n1+2]=2*kbL2
            self.M_vos[index_beam,3*index_n2+2]=\
                self.M_vos[index_beam,3*index_n2+2]+kbL2
            
            self.M_vos[index_beam,3*n:3*n+4]=kbL3*deplT
            ##
            equ1=self.e[index_beam].reshape((2,1))*self.N_vs[index_beam,0:3*self.nnodes]\
                +self.eT[index_beam].reshape((2,1))*self.T_vs[index_beam,0:3*self.nnodes]
            
            self.K[3*index_n1:3*index_n1+2,:]=self.K[3*index_n1:3*index_n1+2,:]-equ1
            self.K[3*index_n2:3*index_n2+2,:]=self.K[3*index_n2:3*index_n2+2,:]+equ1
            self.K[3*index_n1+2,:]=self.K[3*index_n1+2,:]+self.M_vos[index_beam,0:3*self.nnodes]
            self.K[3*index_n2+2,:]=self.K[3*index_n2+2,:]+self.M_ves[index_beam,0:3*self.nnodes]

            equ2=self.e[index_beam].reshape((2,1))*self.N_vs[index_beam,3*self.nnodes:3*self.nnodes+4]\
                +self.eT[index_beam].reshape((2,1))*self.T_vs[index_beam,3*self.nnodes:3*self.nnodes+4]

            self.B[3*index_n1:3*index_n1+2,:]=self.B[3*index_n1:3*index_n1+2,:]+equ2
            self.B[3*index_n2:3*index_n2+2,:]=self.B[3*index_n2:3*index_n2+2,:]-equ2
            self.B[3*index_n1+2,:]=self.B[3*index_n1+2,:]-self.M_vos[index_beam,3*self.nnodes:3*self.nnodes+4]
            self.B[3*index_n2+2,:]=self.B[3*index_n2+2,:]-self.M_ves[index_beam,3*self.nnodes:3*self.nnodes+4]
            ##
            index_beam+=1
        pass

    # def GenerateDirectors(self, e: np.array, eT: np.array,EL2: elements):
    def GenerateDirectors(self, e: np.array, eT: np.array,EL2):
        number_seq=0
        for i in EL2.beams:
            e[number_seq,:]=np.array([i.e_x,i.e_y])
            eT[number_seq,:]=np.array([-i.e_y,i.e_x])
            number_seq=number_seq+1

    # def GenerateDu(self,EL2: elements):
    def GeneratedU(self,EL2):
        L1=EL2.periods[0].length
        L2=EL2.periods[1].length
        Y11=EL2.periods[0].x
        Y21=EL2.periods[1].x
        Y12=EL2.periods[0].y
        Y22=EL2.periods[1].y
        self.P1=np.array([L1*Y11,L1*Y12],dtype=np.float32)
        self.P2=np.array([L2*Y21,L2*Y22],dtype=np.float32)
        #
        dU1=np.array([[self.P1[0],self.P1[1],0,0],\
                    [0,0,self.P1[0],self.P1[1]]],dtype=np.float32)
        dU2=np.array([[self.P2[0],self.P2[1],0,0],\
                    [0,0,self.P2[0],self.P2[1]]],dtype=np.float32)
        return np.array([dU1,dU2])

