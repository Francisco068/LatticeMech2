# FDR_Solver
# 2020/06/23 :
#   - passage en homogénéisation énergétique
#   - modification des tenseurs avec un format de calcul de Voigt et de notation tensorielle

import numpy as np
import copy

from latticeObjects import *

class solverFDR(object):
    # def __init__(self,EL2: elements):
    # EL2 : class elements 
    # solve [K][X]=[B]
    # [X] : array 3*nnodes of inknowns values (x_n,y_n,phi_n) of each point n 
    # [K] : array 3*nnodes x 3*nnodes of equilibrium matrix
    # [B] : array 4*nnodes of coefficients of of displacements (dUx/dx, dUx/dy, dUy/dx, dUy/dy)
    # use of special strain notation '_vs' in forces expressions
    #   forces variables with _vs appendices : array of 3*nnodes+4 
    #   are composed with inknowns coefficients and  
    #   the last three coeff -> (dUx/dx, dUy/dy, dUx/dy)

    def __init__(self,EL2 ):
        # variable initialisation
        self.P1=np.array(2)
        self.P2=np.array(2)
        self.nbeams=EL2.LenBeams()
        self.nnodes=EL2.LenNodes()
        self.e=np.zeros(2*self.nbeams,dtype=np.float32).reshape((self.nbeams,2))
        self.eT=np.zeros(2*self.nbeams,dtype=np.float32).reshape((self.nbeams,2))
        # 
        self.X=np.zeros(3*self.nnodes*3,dtype=np.float32).reshape((3*self.nnodes,3))
        #
        self.B=np.zeros(3*3*self.nnodes,dtype=np.float32).reshape((3*self.nnodes,3))
        self.K=np.zeros(9*self.nnodes*self.nnodes,dtype=np.float32).reshape((3*self.nnodes,3*self.nnodes))
        self.N_vs=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+3)
        self.T_vs=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+3)
        self.M_ves=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+3)
        self.M_vos=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float32).reshape((self.nbeams),3*self.nnodes+3)
        self.W=np.zeros(self.nbeams*9,dtype=np.float32).reshape((self.nbeams,3,3))
        # Calculus
        self.GenerateDirectors(self.e,self.eT,EL2)
        self.dU=self.GeneratedU(EL2)
        self.GenerateForcesKB(EL2)
        self.SolveX()
        [self.N, self.T]=self.CalculateForces()
        #
        # Stiffness tensor : [sigma]=[Mat][strain]
        self.GenerateEnergy(EL2)
        self.CalculateStiffnessW()
        [self.MatVo, self.MatTe, self.detg]=self.CalculateStiffnessW()
        self.MSTe=self.CalculateComplianceW()
        print("Compliance Tensor (in tensorial notation):")
        print("[{:>10e} {:>10e} {:>10e} ]".format(self.MSTe[0,0],self.MSTe[0,1],self.MSTe[0,2]))
        print("[{:>10e} {:>10e} {:>10e} ]".format(self.MSTe[1,0],self.MSTe[1,1],self.MSTe[1,2]))
        print("[{:>10e} {:>10e} {:>10e} ]".format(self.MSTe[2,0],self.MSTe[2,1],self.MSTe[2,2]))
        self.CalculateModulus(EL2)
        [rho, K, Ex, Ey, nuyx, nuxy, muxy, etaxxy, etayxy,\
            etaxyx, etaxyy ]=self.CalculateModulus(EL2)
        print("rho={}\nK={}\nEx={}\nEy={}\nnuyx={}\nnuxy={}\nmuxy={}\netaxxy={}\netayxy={}\netaxyx={}\netaxyy={}\n".format(rho,K, Ex, Ey, nuyx,\
            nuxy, muxy, etaxxy, etayxy, etaxyx, etaxyy))

    def CalculateComplianceW(self):
        try:
            MSTe=np.linalg.inv(self.MatTe)
        except:
            print("error : unable to calculate compliance matrix")
            return -1
        # MSTe : compliance matrix in basis tensor notation

        return MSTe

    def CalculateStiffnessW(self):
        ''' Calculate the stiffness tensor'''
        g=np.append(self.P1,self.P2).reshape((2,2))
        try:
            detg=np.linalg.det(g)
        except:
            print("error detg")
            return -1
        Mat=np.zeros((3,3),dtype=np.float32)
        for i in range(self.nbeams):
            Mat[:,:]=Mat[:,:]+self.W[i,:,:]
        Mat=1/detg*Mat
        # the raw matrix obtained here is for strain vector (dUx/dx, dUy/dy, dUx/dy)
        # we need to fit it to strain vector (dUx/dx, dUy/dy, 2*dUx/dy) in Voigt notation
        MatVo=np.ndarray((3,3),dtype=np.float32)
        MatVo[:,:]=Mat[:,:]
        MatVo[2,2]=MatVo[2,2]/4
        MatVo[0,2]=MatVo[0,2]/2
        MatVo[1,2]=MatVo[1,2]/2
        MatVo[2,0]=MatVo[2,0]/2
        MatVo[2,1]=MatVo[2,1]/2
        # refit to strain vector (dUx/dx, dUy/dy, sqrt(2)*dUx/dy) in tensorial notation
        MatTe=np.ndarray((3,3),dtype=np.float32)
        MatTe[:,:]=Mat[:,:]
        MatTe[2,2]=MatTe[2,2]/2
        MatTe[0,2]=MatTe[0,2]/np.sqrt(2)
        MatTe[1,2]=MatTe[1,2]/np.sqrt(2)
        MatTe[2,0]=MatTe[2,0]/np.sqrt(2)   
        MatTe[2,1]=MatTe[2,1]/np.sqrt(2)  
        
        return MatVo, MatTe, detg

    def GenerateEnergy(self,EL2):
        '''Calculus of nodes's energy'''
        n=self.nnodes
        index_beam=0
        for i in EL2.beams:
            index_n1=EL2.IndexNode(i.node_1)[1]
            index_n2=EL2.IndexNode(i.node_2)[1]
            # normal forces

            deplEv=self.X[3*index_n2:3*index_n2+2,:]+i.delta_1*self.dU[0]+i.delta_2*self.dU[1]
            deplOv=self.X[3*index_n1:3*index_n1+2,:]

            deplNE=self.DotProductV(self.e[index_beam,:],deplEv)
            deplNO=self.DotProductV(self.e[index_beam,:],deplOv)

            deplTE=self.DotProductV(self.eT[index_beam,:],deplEv)
            deplTO=self.DotProductV(self.eT[index_beam,:],deplOv)

            self.W[index_beam,:,:]=np.outer(self.N[index_beam,:],deplNE)-\
                np.outer(self.N[index_beam,:],deplNO)+np.outer(self.T[index_beam,:],deplTE)\
                    -np.outer(self.T[index_beam,:],deplTO)

            index_beam+=1

    def CalculateModulus(self,EL2):
        rho=0
        for i in EL2.beams:
            V=i.volume
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
        
        return [rho, K, Ex, Ey, nuyx, nuxy, muxy,etaxxy, etayxy, etaxyx, etaxyy ]

    def CalculateForces(self):
        N=self.N_vs[:,0:3*self.nnodes].dot(self.X)+self.N_vs[:,3*self.nnodes:3*self.nnodes+3]
        T=self.T_vs[:,0:3*self.nnodes].dot(self.X)+self.T_vs[:,3*self.nnodes:3*self.nnodes+3]
        return [N,T]
    
    def SolveX(self):
        K_r=self.K[2:3*self.nnodes,2:3*self.nnodes]
        try:
            K_i=np.linalg.inv(K_r)
        except np.linalg.LinAlgError:
            print("matrix error ")
            return -1
        self.X[2:3*self.nnodes,:]=K_i.dot(self.B[2:3*self.nnodes,:])

    def DotProductV(self,v: np.array,dUn: np.array):
        return v[0]*dUn[0]+v[1]*dUn[1]

    def GenerateForcesKB(self,EL2):
        index_beam=0
        for i in EL2.beams:
            index_n1=EL2.IndexNode(i.node_1)[1]
            index_n2=EL2.IndexNode(i.node_2)[1]
            # normal forces
            kae=i.ka*self.e[index_beam,:]
            deplN=self.DotProductV(i.delta_1*kae,self.dU[0])+self.DotProductV(i.delta_2*kae,self.dU[1])
            n=self.nnodes
            self.N_vs[index_beam,3*index_n2:3*index_n2+2]=kae
            self.N_vs[index_beam,3*index_n1:3*index_n1+2]=self.N_vs[index_beam,3*index_n1:3*index_n1+2]-kae
            self.N_vs[index_beam,3*n:3*n+3]=deplN
                                                
            # transverses forces
            kbe=i.kb*self.eT[index_beam,:]
            deplT=self.DotProductV(i.delta_1*kbe,self.dU[0])+self.DotProductV(i.delta_2*kbe,self.dU[1])
            self.T_vs[index_beam,3*index_n2:3*index_n2+2]=kbe
            self.T_vs[index_beam,3*index_n1:3*index_n1+2]=self.T_vs[index_beam,3*index_n1:3*index_n1+2]-kbe
            kbL=-i.kb*i.length/2
            self.T_vs[index_beam,3*index_n1+2]=kbL
            self.T_vs[index_beam,3*index_n2+2]=self.T_vs[index_beam,3*index_n2+2]+kbL
            self.T_vs[index_beam,3*n:3*n+3]=deplT
                                                
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
            self.M_ves[index_beam,3*n:3*n+3]=kbL3*deplT

            self.M_vos[index_beam,3*index_n2:3*index_n2+2]=kbe2
            self.M_vos[index_beam,3*index_n1:3*index_n1+2]=\
                self.M_vos[index_beam,3*index_n1:3*index_n1+2]-kbe2

            self.M_vos[index_beam,3*index_n1+2]=2*kbL2
            self.M_vos[index_beam,3*index_n2+2]=\
                self.M_vos[index_beam,3*index_n2+2]+kbL2
            
            self.M_vos[index_beam,3*n:3*n+3]=kbL3*deplT
            ##
            equ1=self.e[index_beam].reshape((2,1))*self.N_vs[index_beam,0:3*self.nnodes]\
                +self.eT[index_beam].reshape((2,1))*self.T_vs[index_beam,0:3*self.nnodes]
            
            self.K[3*index_n1:3*index_n1+2,:]=self.K[3*index_n1:3*index_n1+2,:]-equ1
            self.K[3*index_n2:3*index_n2+2,:]=self.K[3*index_n2:3*index_n2+2,:]+equ1
            self.K[3*index_n1+2,:]=self.K[3*index_n1+2,:]+self.M_vos[index_beam,0:3*self.nnodes]
            self.K[3*index_n2+2,:]=self.K[3*index_n2+2,:]+self.M_ves[index_beam,0:3*self.nnodes]

            equ2=self.e[index_beam].reshape((2,1))*self.N_vs[index_beam,3*self.nnodes:3*self.nnodes+3]\
                +self.eT[index_beam].reshape((2,1))*self.T_vs[index_beam,3*self.nnodes:3*self.nnodes+3]

            self.B[3*index_n1:3*index_n1+2,:]=self.B[3*index_n1:3*index_n1+2,:]+equ2
            self.B[3*index_n2:3*index_n2+2,:]=self.B[3*index_n2:3*index_n2+2,:]-equ2
            self.B[3*index_n1+2,:]=self.B[3*index_n1+2,:]-self.M_vos[index_beam,3*self.nnodes:3*self.nnodes+3]
            self.B[3*index_n2+2,:]=self.B[3*index_n2+2,:]-self.M_ves[index_beam,3*self.nnodes:3*self.nnodes+3]
            ##
            index_beam+=1
        pass

    def GenerateDirectors(self, e: np.array, eT: np.array,EL2):
        ''' generate array for directors '''
        number_seq=0
        for i in EL2.beams:
            e[number_seq,:]=np.array([i.e_x,i.e_y])
            eT[number_seq,:]=np.array([-i.e_y,i.e_x])
            number_seq=number_seq+1

    def GeneratedU(self,EL2):
        ''' Generate [dU1,dU2]
        for non orthonormal grid for lattice
        '''
        L1=EL2.periods[0].length
        L2=EL2.periods[1].length
        Y11=EL2.periods[0].x
        Y21=EL2.periods[1].x
        Y12=EL2.periods[0].y
        Y22=EL2.periods[1].y
        self.P1=np.array([L1*Y11,L1*Y12],dtype=np.float32)
        self.P2=np.array([L2*Y21,L2*Y22],dtype=np.float32)
        #
        # le codage se fait désormais avec (dUx/dx, dUy/dy, dUx/dy)
        dU1=np.array([[self.P1[0],0,self.P1[1]],[0,self.P1[1],self.P1[0]]],dtype=np.float32)
        dU2=np.array([[self.P2[0],0,self.P2[1]],[0,self.P2[1],self.P2[0]]],dtype=np.float32)
        return np.array([dU1,dU2])

