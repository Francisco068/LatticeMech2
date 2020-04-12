# FDR_Solver
# from lattice_objects import elements
import numpy as np

class solverFDR():
    # def __init__(self,EL2: elements):
    def __init__(self,EL2):
        self.P1=np.array(2)
        self.P2=np.array(2)
        self.nbeams=len(EL2.beams)
        self.nnodes=len(EL2.nodes)
        self.e=np.zeros(2*self.nbeams).reshape((self.nbeams,2))
        self.eT=np.zeros(2*self.nbeams).reshape((self.nbeams,2))
        self.nodes=np.zeros(2*4*self.nnodes).reshape((2*self.nnodes,4))
        self.B=np.zeros(2*4*self.nnodes).reshape((2*self.nnodes,4))
        self.K=np.zeros(4*4*self.nnodes*self.nnodes).reshape((2*self.nnodes,2*self.nnodes,4))
        self.GenerateDirectors(self.e,self.eT,EL2)

        dU=self.GeneratedU(EL2)
        N_v=np.zeros(2*nnodes)
        self.GenerateN_v(EL2,dU)
        self.GenerateK_B(self.K,EL2)

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
        dU1=np.array([[P1[0],P1[1],0,0],[0,0,P1[0],P1[1]]],dtype=np.float32)
        dU2=np.array([[P2[0],P2[1],0,0],[0,0,P2[0],P2[1]]],dtype=np.float32)
        return np.array([dU1,dU2])

