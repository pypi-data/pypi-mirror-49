colo = ['red','orange','g','b','pink','y','c','m','purple','yellowgreen','silver','coral','plum','lime']
colo = colo*100
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import pandas as pd



def random_data(m,d,d_nonzero,k,sigma,zerosum=False):
    A= np.random.randn(m,d)
    while True :        
        C = np.random.randint(low=-1,high=1, size=(k, d))
        if (LA.matrix_rank(C)==k): break
    
    if (zerosum): C,k = np.ones((1,d)),1
        
    while True:
        sol, sol_reduc = np.zeros(d), np.random.rand(d_nonzero)
        list_i = np.random.randint(d, size=d_nonzero)
        C_reduc = np.array([C.T[i] for i in list_i]).T
        if (LA.matrix_rank(C_reduc)<k): continue
        proj = proj_c(C_reduc,d_nonzero).dot(sol_reduc)
        for i in range(len(list_i)):
            sol[list_i[i]]=proj[i]
        break
    y = A.dot(sol)+np.random.randn(m)*sigma
    return((A,C,y),sol)

def name(tol,string): return(string+'  tol={:.0e}'.format(float(tol)))   

def compare(L,show,lam):
    str1 = 'Execution time : \n \n'
    str2 = '\n Iterations : \n \n'
    str3 = '\n L2-difference between : \n \n'
    str4 = '\n For concomitant algorithms : \n \n'
    for i in range(len(L)) :
        x,niter,dt = L[i][0][:3]
        name = L[i][1]
        if (show=='sep' or show==True):
            plt.title('lam = '+str(lam))
            plt.bar(range(len(x)),x,label=name,color=colo[i])
            plt.legend()
            if (show=='sep'): plt.show()
        if (niter != 0):
            str1+= name+' :'+str(round(dt,5)) + '\n'
            str2+= name+' :'+str(niter)+ '\n'
        for j in range (i+1,len(L)): str3+= name + ' and '+L[j][1] +'             : ' + str(round(LA.norm((L[j][0][0]-x)),4)) + '\n'
    plt.show()
    printsigma =False
    for i in range(len(L)) :
        if (len(L[i][0])==4): 
            printsigma = True
            str4+=' Sigma '+L[i][1]+'  :'+str(round(L[i][0][3],3))
 
    print(str1)
    print(str2)
    if (len(L)>1): print(str3)
    if (printsigma): print(str4)
    
    
def influence(sol,top):
    l_influence = []
    for j in range(top):
        maxi = 0.
        for i in range(len(sol)): 
            if ( not (i in l_influence) and (abs(sol[i])>=maxi)): maxi,argmaxi = abs(sol[i]), i
        l_influence.append(argmaxi)
    return(l_influence)

def plot_influence(labels,l_influence):
    print("influent parameters  : \n \n")
    for beta in l_influence:
        string=''
        for colo in range(1,7):
            string+= str(labels.loc[beta+1,colo])
        print(string + '\n')


def plot_betai(labels,l_index,path,BETA):
    for i in range(len(l_index)) :
        leg = 'index = '+str(l_index[i]+1)
        if not (type(labels)==bool): leg+='  '+ str(labels.loc[l_index[i]+1,6])
        if (i>10): plt.plot(path,[BETA[ilam][l_index[i]] for ilam in range(len(path))],color=colo[l_index[i]])
        else:     plt.plot(path,[BETA[ilam][l_index[i]] for ilam in range(len(path))],label=leg,color=colo[l_index[i]])

def normalize(lb,lna,ly):
    for j in range(len(lb[0])):
        lb[:,j] =  lb[:,j]*ly/lna[j]
    return(lb)     
        
        
        
def old_normalize(lb,lna,ly):
    lbetaprime = []
    for beta in lb:
        lbetaprime.append( np.array([ly*beta[j]/(lna[j]) for j in range(len(beta))]) )
    return(lbetaprime)

def denorm(B,lna,ly): return(np.array([ly*B[j]/(np.sqrt(len(B))*lna[j]) for j in range(len(B))]) ) 
    

def affichage(LISTE_BETA,path,title=' ',labels=False,pix=False):
    naffichage = len(LISTE_BETA[0])//4
    l_index  = influence(LISTE_BETA[-1],naffichage)
    plt.figure(figsize=(10,3), dpi=80)
    if (pix=='path'): plt.plot(path,[0]*len(path),'r+')
    plot_betai(labels,l_index,path,LISTE_BETA)
    plt.title(title)
    plt.legend(loc=4, borderaxespad=0.)
    plt.xlabel("lam")
    plt.ylabel("Betai")
    #plt.savefig('path')
    if (type(pix)==bool and pix==True):
        plt.matshow([[(abs(LISTE_BETA[i][j])>1e-2) for i in range(len(LISTE_BETA))] for j in range(len(LISTE_BETA[0]))])
        plt.show()
    
def aff(M):
    (m,n)= M.shape
    for i in range(m):
        string =  ''
        for j in range(n):
            to_ad=str(round(abs(M[i,j]),3))
            string+=to_ad+' '*(5-len(to_ad))+' |'
        print(string + '//')    
        
        
        
def csv_to_mat(file):
    tab1=pd.read_csv(file)
    return(np.array(tab1)[:,1:])
    

    
    
def rescale(matrix):
    (A,C,y)=matrix
    my = sum(y)/len(y)
    la = [LA.norm(A[:,j]) for j in range(len(A[0]))]
    ly = LA.norm(y-my*np.ones(len(y)))
    An = np.array([[A[i,j]/(la[j])  for j in range(len(A[0]))] for i in range(len(A))])
    yn = np.array([ (y[j]-my)/ly for j in range(len(y)) ])
    Cn = np.array([[C[i,j]*ly/la[j] for j in range(len(A[0]))] for i in range(len(C))])
    return((An,Cn,yn),(la,ly,my))


def hub(r,rho) : 
    h=0
    for j in range(len(r)):
        if(abs(r[j])<rho): h+=r[j]**2
        elif(r[j]>0)     : h+= (2*r[j]-rho)*rho
        else             : h+= (-2*r[j]-rho)*rho
    return(h)
def L_LS(A,y,lamb,x): return(LA.norm( A.dot(x) - y )**2 + lamb * LA.norm(x,1))
def L_conc(A,y,lamb,x): return(LA.norm( A.dot(x) - y ) + np.sqrt(2)*lamb * LA.norm(y,1))
def L_H(A,y,lamb,x,rho): return(hub( A.dot(x) - y , rho) + lamb * LA.norm(x,1))


# Compute I - C^t (C.C^t)^-1 . C : the projection on Ker(C)
def proj_c(M,d):
    if (LA.matrix_rank(M)==0):  return(np.eye(d))
    return(np.eye(d)-LA.multi_dot([M.T,np.linalg.inv(M.dot(M.T) ),M]) )

from scipy.special import erfinv
def model_selection(n,p):
    x=0.
    dx = 0.1
    for i in range(10):
        bo = True
        while bo :
            x    += dx
            f     = erfinv(1-x)
            xp    = 8/p * (f**4+f**2)
            bo    = (xp>x)           
        x = x-dx
        dx = dx/10
    return(f*2/np.sqrt(n))
