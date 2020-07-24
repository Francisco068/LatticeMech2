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
        self.e=np.ones((self.nbeams,2),dtype=np.float64)
        self.eT=np.zeros(2*self.nbeams,dtype=np.float64).reshape((self.nbeams,2))
        # 
        self.X=np.zeros(3*self.nnodes*3,dtype=np.float64).reshape((3*self.nnodes,3))
        #
        self.B=np.zeros(3*3*self.nnodes,dtype=np.float64).reshape((3*self.nnodes,3))
        self.K=np.zeros(9*self.nnodes*self.nnodes,dtype=np.float64).reshape((3*self.nnodes,3*self.nnodes))
        self.N_vs=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float64).reshape((self.nbeams),3*self.nnodes+3)
        self.T_vs=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float64).reshape((self.nbeams),3*self.nnodes+3)
        self.M_ves=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float64).reshape((self.nbeams),3*self.nnodes+3)
        self.M_vos=np.zeros((3*self.nnodes+3)*self.nbeams,dtype=np.float64).reshape((self.nbeams),3*self.nnodes+3)
        self.W=np.zeros(self.nbeams*9,dtype=np.float64).reshape((self.nbeams,3,3))
        self.ka=np.zeros(self.nbeams,dtype=np.float64)
        self.kb=np.zeros(self.nbeams,dtype=np.float64)
        self.V=np.zeros(self.nbeams,dtype=np.float64)
        self.t=np.zeros(self.nbeams,dtype=np.float64)
        self.knbi=np.zeros((self.nbeams,3,3),dtype=np.float64); # kn individuel par poutre
        self.ktbi=np.zeros((self.nbeams,3,3),dtype=np.float64); # kt individuel par poutre
        # order : [kn11,kn22,kn33,kn12,kn13,kn23]
        self.kn=np.zeros((6,self.nbeams),dtype=np.float64)
        self.kt=np.zeros((6,self.nbeams),dtype=np.float64)
        # Variables for optimization (Inverse homogenization)
        self.gamma=np.zeros(self.nbeams,dtype=np.float64)
        self.te0=np.zeros(self.nbeams,dtype=np.float64)
        self.te02=np.zeros(self.nbeams,dtype=np.float64)
        self.te03=np.zeros(self.nbeams,dtype=np.float64)
        self.nu0=np.ones(6,dtype=np.float64)
        self.nu=np.ones(6,dtype=np.float64)
        self.te=np.zeros(self.nbeams,dtype=np.float64)
        self.dim_probleme=self.nbeams+6
        self.f=np.zeros(self.dim_probleme,dtype=np.float64)
        self.J=np.zeros((self.dim_probleme,self.dim_probleme),dtype=np.float64)
        self.E=np.zeros(6,dtype=np.float64)
        self.step=0
        self.Lp=0.5
        self.eta=-1.0
        self.xi0=np.ones(0)
        self.n_cond=0
        self.cond_activated=np.zeros(self.nbeams,dtype=np.float64)
        self.kxi=np.zeros((0,0),dtype=np.float64)
        self.HomogenizationInitial(EL2)
    
    def InverseHomogenization(self,EL,num_ETarget):
        index_ETarget=EL.IndexObject(num_ETarget,EL.ETargets)[1]
        ETarget1=EL.ETargets[index_ETarget]
        ETarget1.GenerateTensors()
        for i in range(6):
            self.E[i]=ETarget1.tensor_target[i]

        # beginning of loop update te
        self.step=1
        self.n_cond=0
        while True:
            error_calcul=self.CalculError()
            print("error:{}".format(error_calcul))
            if (error_calcul<1e-5):
                break
            self.step+=1

            self.GenerateF()
            self.GenerateJ()
            self.UpdateVar()
            
            for i in range(self.nbeams):
                self.t[i]=self.te[i]
            self.HomogenizationLoop(EL)  
            pass  

                # activation des inégalités si besoin
            # for i in range(self.nbeams):
            #     if self.te[i]<1e-8 and self.cond_activated[i]!=1:
            #         self.cond_activated[i]=1
            #         self.n_cond+=1
            #         self.xi0=np.append(self.xi0,np.ones(1,dtype=np.float64))
            #         temp=np.zeros((1,self.nbeams),dtype=np.float64)
            #         temp[0,i]=1
            #         self.kxi=np.append(self.kxi,temp).reshape((self.n_cond,self.nbeams))

            # todo 8 : n'y a t-il pas des erreurs d'adresses ? 

    
    def CalculError(self):
        somme_err=0
        En=np.zeros(6,dtype=np.float64)
        En[0]=self.MatTe[0,0]
        En[1]=self.MatTe[1,1]
        En[2]=self.MatTe[2,2]
        En[3]=self.MatTe[0,1]
        En[4]=self.MatTe[0,2]
        En[5]=self.MatTe[1,2]
        print("E homogenized : {}".format(En))
        print("E target :{}".format(self.E))
        for i in range(6):
            somme_err+=(En[i]-self.E[i])**2
        return np.sqrt(somme_err)

    def GenerateF(self):
        self.dim_probleme=self.nbeams+6+self.n_cond
        self.f=np.zeros(self.dim_probleme)
        temp1=np.diag(3*self.te02)
        temp2=np.dot(self.nu,self.kt)
        temp3=np.dot(temp2,temp1)
        if self.n_cond>0:
            temp6=np.dot(self.xi0,self.kxi)
            self.f[0:self.nbeams]=self.gamma+np.dot(self.nu,self.kn)+temp3+temp6
        else:
            self.f[0:self.nbeams]=self.gamma+np.dot(self.nu,self.kn)+temp3
        temp4=np.dot(self.kn,self.te0)
        temp5=np.dot(self.kt,self.te03)
        self.f[self.nbeams:self.nbeams+6]=-self.E+temp4+temp5
        if self.n_cond>0:
            temp7=np.dot(self.kxi,self.te0-1e8)
            self.f[self.nbeams+6:self.nbeams+6+self.n_cond]=temp7
        pass

    def GenerateJ(self):
        self.J=np.zeros((self.dim_probleme,self.dim_probleme),dtype=np.float64)
        temp1=np.dot(self.nu,self.kt)
        temp2=6*np.dot(temp1,np.diag(self.te0))
        temp3=np.diag(temp2)
        self.J[0:self.nbeams,0:self.nbeams]=temp3
        temp4=self.kn+3*np.dot(self.kt,np.diag(self.te02))
        temp5=np.transpose(temp4)
        self.J[0:self.nbeams,self.nbeams:self.nbeams+6]=temp5
        self.J[self.nbeams:self.nbeams+6,0:self.nbeams]=temp4
        self.J[self.nbeams:self.nbeams+6,self.nbeams:self.nbeams+6]=np.zeros((6,6),dtype=np.float64)
        #ajout des conditions des inéquations activées 
        if self.n_cond>0:
            temp6=np.transpose(self.kxi)
            self.J[0:self.nbeams,self.nbeams+6:self.dim_probleme]=temp6
            self.J[self.nbeams+6:self.dim_probleme,0:self.nbeams]=self.kxi
        pass
    
    def UpdateVar(self):
        if self.n_cond>0:
            vars0=np.append(self.te0,self.nu0)
            vars0=np.append(vars0,self.xi0)
            self.xi=np.zeros(self.n_cond,dtype=np.float64)
        else:
            vars0=np.append(self.te0,self.nu0)
        try:
            delta_vars=np.linalg.lstsq(self.J,-self.f)
        except:
            print("Error inverting Jacobian Matrix")
            return
        #vars=vars0+delta_vars[0]
        vars=vars0+delta_vars[0]
        self.te[0:self.nbeams]=vars[0:self.nbeams]
        self.nu[0:6]=vars[self.nbeams:self.nbeams+6]
        for i in range(self.nbeams):
            if self.te[i]<0.00000001:
                self.te[i]=0.000000001

        # for i in range(self.nbeams):
        #     if self.te[i]>0.5:
        #         self.te[i]=0.5

        print("te : {}".format(self.te))
        print("nu : {}".format(self.nu))
        # if self.n_cond>0:
        #     self.xi[0:self.n_cond]=vars[self.nbeams+6:self.dim_probleme]
        #     self.xi0[0:self.n_cond]=vars[self.nbeams+6:self.dim_probleme]
        #     print("xi : {}".format(self.xi0))

    def HomogenizationLoop(self,EL2):
        # Initialise
        self.GeneratekakbVLoop(EL2)
        self.GenerateForcesKB(EL2)
        # Solve
        self.SolveX()
        # Results
        [self.N, self.T]=self.CalculateForces()
        self.GenerateEnergy(EL2)
        [self.MatVo, self.MatTe, self.detg]=self.CalculateStiffnessW()
        print("Matrix Stiffness :{}".format(self.MatTe))
        # extraction kn and kt for optimization
        self.Generateknkt()
        self.GenerateTe0()

    def HomogenizationInitial(self,EL2):
        # Initialise
        self.GeneratekakbV(EL2)
        self.GenerateDirectors(self.e,self.eT,EL2)
        self.dU=self.GeneratedU(EL2)
        self.GenerateForcesKB(EL2)
        # Solve
        self.SolveX()
        # Results
        [self.N, self.T]=self.CalculateForces()
        self.GenerateEnergy(EL2)
        [self.MatVo, self.MatTe, self.detg]=self.CalculateStiffnessW()
#        self.VerifKnbiKtbi() 
        print("Stiffness Tensor (in tensorial notation):")
        print("[{:>10e} {:>10e} {:>10e} ]".format(self.MatTe[0,0],self.MatTe[0,1],self.MatTe[0,2]))
        print("[{:>10e} {:>10e} {:>10e} ]".format(self.MatTe[1,0],self.MatTe[1,1],self.MatTe[1,2]))
        print("[{:>10e} {:>10e} {:>10e} ]".format(self.MatTe[2,0],self.MatTe[2,1],self.MatTe[2,2]))        
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
        # extraction kn and kt for optimization
        self.Generateknkt()

        for i in range(self.nbeams): # firstly I consider the penalisation == length of beams
            Le=EL2.beams[i].length
            mu=EL2.beams[i].mu
    #        self.gamma[i]=Le*mu*(self.Lp/Le)**self.eta
            self.gamma[i]=Le
            self.te[i]=self.t[i]
        self.GenerateTe0()
#        self.VerifyKnKt() # todo a supprimer
    
    def VerifyKnKt(self):
        mat=np.dot(self.kn,self.te0v)+np.dot(self.kt,self.te03)
        print(mat)

    def VerifKnbiKtbi(self):
        sum=np.zeros((3,3),dtype=np.float64)
        for i in range(self.nbeams):
            sum=sum+self.knbi[i]*self.t[i]+(self.t[i]*self.t[i]*self.t[i])*self.ktbi[i]
        print(self.MatTe)
        print(sum)
    
    def GenerateTe0(self):
        for i in range(self.nbeams):
            self.te0[i]=self.te[i]
            self.te02[i]=self.te[i]*self.te[i]
            self.te03[i]=self.te[i]*self.te[i]*self.te[i]
        self.nu0[:]=self.nu[:]

    def Generateknkt(self):
        # order : [kn11,kn22,kn33,kn12,kn13,kn23]
        for i in range(self.nbeams):
            self.kn[0,i]=self.knbi[i,0,0]
            self.kn[1,i]=self.knbi[i,1,1]
            self.kn[2,i]=self.knbi[i,2,2]
            self.kn[3,i]=self.knbi[i,0,1]
            self.kn[4,i]=self.knbi[i,0,2]
            self.kn[5,i]=self.knbi[i,1,2]

            self.kt[0,i]=self.ktbi[i,0,0]
            self.kt[1,i]=self.ktbi[i,1,1]
            self.kt[2,i]=self.ktbi[i,2,2]
            self.kt[3,i]=self.ktbi[i,0,1]
            self.kt[4,i]=self.ktbi[i,0,2]
            self.kt[5,i]=self.ktbi[i,1,2]

    def GeneratekakbV(self,EL2):
        index_b=0
        for i in EL2.beams:
            p=EL2.IndexObject(i.profile,EL2.profiles)[0]
            t=p.width
            E=p.E
            L=i.length
            self.ka[index_b]=E*t/L
            self.kb[index_b]=E*(t/L)**3
            self.V[index_b]=t*L
            self.t[index_b]=t
            index_b+=1
        print("ka init :{}".format(self.ka))
        print("kb init :{}".format(self.kb))

    def GeneratekakbVLoop(self,EL2):
        index_b=0
        for i in EL2.beams:
            p=EL2.IndexObject(i.profile,EL2.profiles)[0]
            t=self.t[index_b]
            E=p.E
            L=i.length
            self.ka[index_b]=E*t/L
            self.kb[index_b]=E*(t/L)**3
            self.V[index_b]=t*L
            index_b+=1
        print("ka loop :{}".format(self.ka))
        print("kb loop :{}".format(self.kb))

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
        mat=np.array([[0,0,0],[0,0,0],[0,0,0]])

        g=np.append(self.P1,self.P2).reshape((2,2))
        try:
            detg=np.linalg.det(g)
        except:
            print("error detg")
            return -1

        for i in range(self.nbeams):
            mat[:,:]=mat[:,:]+self.W[i,:,:]
        mat=1/detg*mat

        self.knbi=1/detg*self.knbi
        self.ktbi=1/detg*self.ktbi

        # the raw matrix obtained here is for strain vector (dUx/dx, dUy/dy, dUx/dy)
        # we need to fit it to strain vector (dUx/dx, dUy/dy, 2*dUx/dy) in Voigt notation
        MatVo=np.ndarray((3,3),dtype=np.float64)
        MatVo[:,:]=mat[:,:]
        MatVo[2,2]=MatVo[2,2]/4
        MatVo[0,2]=MatVo[0,2]/2
        MatVo[1,2]=MatVo[1,2]/2
        MatVo[2,0]=MatVo[2,0]/2
        MatVo[2,1]=MatVo[2,1]/2
        # refit to strain vector (dUx/dx, dUy/dy, sqrt(2)*dUx/dy) in tensorial notation
        MatTe=np.ndarray((3,3),dtype=np.float64)
        MatTe[:,:]=mat[:,:]
        MatTe[2,2]=MatTe[2,2]/2
        MatTe[0,2]=MatTe[0,2]/np.sqrt(2)
        MatTe[1,2]=MatTe[1,2]/np.sqrt(2)
        MatTe[2,0]=MatTe[2,0]/np.sqrt(2)   
        MatTe[2,1]=MatTe[2,1]/np.sqrt(2)  

        # same refit for individual components of knbi and ktbi
        for i in range(self.nbeams):
            self.knbi[i,2,2]=self.knbi[i,2,2]/2
            self.knbi[i,0,2]=self.knbi[i,0,2]/np.sqrt(2)
            self.knbi[i,1,2]=self.knbi[i,1,2]/np.sqrt(2)
            self.knbi[i,2,0]=self.knbi[i,2,0]/np.sqrt(2)   
            self.knbi[i,2,1]=self.knbi[i,2,1]/np.sqrt(2)  

            self.ktbi[i,2,2]=self.ktbi[i,2,2]/2
            self.ktbi[i,0,2]=self.ktbi[i,0,2]/np.sqrt(2)
            self.ktbi[i,1,2]=self.ktbi[i,1,2]/np.sqrt(2)
            self.ktbi[i,2,0]=self.ktbi[i,2,0]/np.sqrt(2)   
            self.ktbi[i,2,1]=self.ktbi[i,2,1]/np.sqrt(2) 
        
        return MatVo, MatTe, detg

    def GenerateEnergy(self,EL2):
        '''Calculus of nodes's energy'''
        n=self.nnodes
        index_beam=0
        for i in EL2.beams:
            index_n1=EL2.IndexObject(i.node_1,EL2.nodes)[1]
            index_n2=EL2.IndexObject(i.node_2,EL2.nodes)[1]
            # normal forces

            deplEv=self.X[3*index_n2:3*index_n2+2,:]+i.delta_1*self.dU[0]+i.delta_2*self.dU[1]
            deplOv=self.X[3*index_n1:3*index_n1+2,:]

            deplNE=self.DotProductV(self.e[index_beam,:],deplEv)
            deplNO=self.DotProductV(self.e[index_beam,:],deplOv)

            deplTE=self.DotProductV(self.eT[index_beam,:],deplEv)
            deplTO=self.DotProductV(self.eT[index_beam,:],deplOv)

            energyN=np.outer(self.N[index_beam,:],deplNE)-np.outer(self.N[index_beam,:],deplNO)
            energyT=np.outer(self.T[index_beam,:],deplTE)-np.outer(self.T[index_beam,:],deplTO)
            self.W[index_beam,:,:]=energyN+energyT

            self.knbi[index_beam,:,:]=energyN/self.t[index_beam]
            self.ktbi[index_beam,:,:]=energyT/(self.t[index_beam])**3
            index_beam+=1

    def CalculateModulus(self,EL2):
        rho=0
        for i in range(self.nbeams):
            vol=self.V[i]
            rho=rho+vol
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
        self.B=np.zeros(3*3*self.nnodes,dtype=np.float64).reshape((3*self.nnodes,3))
        self.K=np.zeros(9*self.nnodes*self.nnodes,dtype=np.float64).reshape((3*self.nnodes,3*self.nnodes))
        index_beam=0
        for i in EL2.beams:
            index_n1=EL2.IndexObject(i.node_1,EL2.nodes)[1]
            index_n2=EL2.IndexObject(i.node_2,EL2.nodes)[1]
            # normal forces
            kae=self.ka[index_beam]*self.e[index_beam,:]
            deplN=self.DotProductV(i.delta_1*kae,self.dU[0])+self.DotProductV(i.delta_2*kae,self.dU[1])
            n=self.nnodes
            self.N_vs[index_beam,3*index_n2:3*index_n2+2]=kae
            self.N_vs[index_beam,3*index_n1:3*index_n1+2]=self.N_vs[index_beam,3*index_n1:3*index_n1+2]-kae
            self.N_vs[index_beam,3*n:3*n+3]=deplN
                                                
            # transverses forces
            kbe=self.kb[index_beam]*self.eT[index_beam,:]
            deplT=self.DotProductV(i.delta_1*kbe,self.dU[0])+self.DotProductV(i.delta_2*kbe,self.dU[1])
            self.T_vs[index_beam,3*index_n2:3*index_n2+2]=kbe
            self.T_vs[index_beam,3*index_n1:3*index_n1+2]=self.T_vs[index_beam,3*index_n1:3*index_n1+2]-kbe

            kbL=-self.kb[index_beam]*i.length/2
            self.T_vs[index_beam,3*index_n1+2]=kbL
            self.T_vs[index_beam,3*index_n2+2]=self.T_vs[index_beam,3*index_n2+2]+kbL
            self.T_vs[index_beam,3*n:3*n+3]=deplT
                                                
            # moments
            kbe2=-self.kb[index_beam]*self.eT[index_beam,:]*i.length/2
            self.M_ves[index_beam,3*index_n2:3*index_n2+2]=kbe2
            self.M_ves[index_beam,3*index_n1:3*index_n1+2]=\
                self.M_ves[index_beam,3*index_n1:3*index_n1+2]-kbe2

            kbL2=self.kb[index_beam]*i.length*i.length/6
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
        print("K : {}".format(self.K))
        print("B : {}".format(self.B))
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
        self.P1=np.array([L1*Y11,L1*Y12],dtype=np.float64)
        self.P2=np.array([L2*Y21,L2*Y22],dtype=np.float64)
        #
        # le codage se fait désormais avec (dUx/dx, dUy/dy, dUx/dy)
        dU1=np.array([[self.P1[0],0,self.P1[1]],[0,self.P1[1],self.P1[0]]],dtype=np.float64)
        dU2=np.array([[self.P2[0],0,self.P2[1]],[0,self.P2[1],self.P2[0]]],dtype=np.float64)
        return np.array([dU1,dU2])

