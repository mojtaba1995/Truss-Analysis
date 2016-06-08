#from pip._vendor.colorama.win32 import COORD
from _io import open
from xml.dom.expatbuilder import parseString
from ctypes.wintypes import DOUBLE
from math import sqrt
from symbol import power
# from goto import with_goto
# import goto
# from goto import _find_labels_and_gotos
# from goto import _inject_ops
# from goto import _is_single_attr_lookup
# from cProfile import label
# from goto import _make_code





def DATA():
    #FEM1
    global NPOIN,NELEM,NBOUN,NPROP,NNODE,NEVAB,NSVAB,NDOFN,NDIME,NSTRE
    
    #FEM2      
    global PROPS ,COORD ,LNODS,IFPRE ,FIXED,RLOAD,ELOAD,MATNO,STRES,XDISP,TDISP
    global TREAC,ASTIF,ASLOD,REACT

    PROPS = [[0 for x in range(5)] for x in range(2)] 
    COORD = [[0 for x in range(2)] for x in range(50)] 
    LNODS = [[0 for x in range(2)] for x in range(75)] 
    IFRPE = [0 for x in range(100)] 
    RLOAD = [[0 for x in range(2)] for x in range(50)] 
    ELOAD = [[0 for x in range(4)] for x in range(75)] 
    MATNO = [0 for x in range(75)] 
    STRES = [[0 for x in range(1)] for x in range(75)] 
    XDISP = [0 for x in range(100)] 
    TDISP = [[0 for x in range(2)] for x in range(50)] 
    TREAC = [[0 for x in range(2)] for x in range(50)] 
    ASTIF = [[0 for x in range(100)] for x in range(100)] 
    ASLOD = [0 for x in range(100)] 
    REACT = [0 for x in range(100)] 
    FIXED = [0 for x in range(100)]
    IFPRE = [0 for x in range(100)]
    global ESTIF
    ESTIF = [[[0 for x in range(75)] for x in range(4)] for x in range(4)]
   
    
    fileRead = open("TRUSS.TXT","r")
    global fileWrite 
    fileWrite = open("TRUSS_RES.txt","w+")
    if fileRead.mode == 'r':
        fl = fileRead.readlines() # readlines reads the individual lines into a list
    lineNumber=0    
    for x in fl:
        lineNumber=lineNumber+1        
        if lineNumber==1 :
            TITLE=x
        if lineNumber==2 :
            l2=x
            a = [int(x1) for x1 in l2.split('   ')]  
            NPOIN=a[0]
            NELEM=a[1]
            NBOUN=a[2]
#             NMATS=a[3]
            NPROP=a[4]
            NNODE=a[5]
            NDOFN=a[6]
            NDIME=a[7]
            NSTRE=a[8] 
    IPOIN=[0 for x in range(a[8]+2)]        
    lineNumber=0 
    for x in fl:
        lineNumber=lineNumber+1  
        if 2<lineNumber<3+a[3] :
            b = [float(x1) for x1 in x.split('   ')]
#             JMATS=b[0]
            i=b[0]-1
            i=int(i)
            PROPS[i][0]=b[1]
            PROPS[i][1]=b[2]
        if 3+a[3]<=lineNumber<3+a[3]+a[1] :
            c = [int(x1) for x1 in x.split('    ')] 
            JMATS=c[0]-1
            LNODS[JMATS][0]=c[1]
            LNODS[JMATS][1]=c[2]
            MATNO[JMATS]=c[3]  
        if 3+a[3]+a[1]<=lineNumber<3+a[3]+a[1]+a[0]:
            d = [float(x1) for x1 in x.split('        ')] 
            JPOIN=d[0]-1
            JPOIN=int(JPOIN)
            COORD[JPOIN][0]=d[1]
            COORD[JPOIN][1]=d[2]
        if 3+a[3]+a[1]+a[0]<=lineNumber<3+a[3]+a[1]+a[0]+a[2]:
            e = [float(x1) for x1 in x.split('    ')]  
            NODFX=e[0]
            ICODE = [0 for x in range(NDOFN)]
            PRESC = [0 for x in range(NDOFN)]
            for x in range(0,NDOFN):
                ICODE[x]=e[2*x+1]
                PRESC[x]=e[2*x+2]
                i=0
            
#               READ(7,*) NODFX,(ICODE(IDOFN),PRESC(IDOFN),IDOFN=1,NDOFN) 
        if 3+a[3]+a[1]+a[0]+a[2]<=lineNumber<3+a[3]+a[1]+a[0]+a[2]+a[8]:
            f = [float(x1) for x1 in x.split('        ')] 
            
            IPOIN[i]=f[0]
            IPOIN[i]=int(IPOIN[i])
            for x in range(0,NDOFN):
                RLOAD[IPOIN[i]-1][x]=f[x+1]
            i=i+1
            
#             FIXME : very sensetive to read type ...
     
    NSVAB=NPOIN*NDOFN                                                 
    NEVAB=NNODE*NDOFN  
#     for ISVAB in range(1,NSVAB):
#         IFRPE[ISVAB-1]=0
#         FIXED[ISVAB-1]=0.0
   
    
    k=int(NODFX)    
    for x in range(1,k+1):
        for IDOFN in range(1,NDOFN+1):
            INDEX=(x-1)*NDOFN+IDOFN
            INDEX=int(INDEX)
            IFPRE[INDEX-1]=ICODE[IDOFN-1]
            FIXED[INDEX-1]=PRESC[IDOFN-1]
        
    fileWrite.write(TITLE) 
    fileWrite.write("NPOIN ="+str(a[0])+" , "+"NELEM ="+str(a[1])+" , "+
                    "NBOUN ="+str(a[2])+" , "+"NMATS ="+str(a[3])+" , "+
                    "NPROP ="+str(a[4])+" , "+"NNODE ="+str(a[5])+" , "+
                    "NDOFN ="+str(a[6])+" , "+"NDIME ="+str(a[7])+" , "+
                    "NSTRE ="+str(a[8])+'\n')
    fileWrite.write("MATERIAL PROPERTIES\n")
    for x in range(0,a[3]) :
        fileWrite.write(str(x+1)+'   '+str(PROPS[x][0])+'   '+str(PROPS[x][1])+'\n')
  
    fileWrite.write('ELEMENT   NODES   MAT.\n')
    for x in range(0,a[1]) :
        fileWrite.write(str(x+1)+'   '+str(LNODS[x][0])+'   '+str(LNODS[x][1])+'   '+str(MATNO[x])+'\n')
    
    fileWrite.write('NODE     COORD.\n')
    for x in range(0,a[0]) :
        fileWrite.write(str(x+1)+'   '+str(COORD[x][0])+'   '+str(COORD[x][1])+'\n')
    fileWrite.write('RESTRAINED NODES,FIXITY CODE AND PRESCRIBED VALUES\n')
    for x in range(0,a[2]) :
        fileWrite.write(str(x+1)+'   ')
        for x in range(0,NDOFN):
            fileWrite.write(str(ICODE[x])+'   '+str(PRESC[x])+'   ')
        fileWrite.write('\n')
    fileWrite.write('NODE   LOADS\n')
    for IDOFN in range(1,NDOFN):
        INDEX=(NODFX-1)*NDOFN+IDOFN
        INDEX=int(INDEX)
        IFRPE[INDEX-1]=ICODE[IDOFN-1]
        FIXED[INDEX-1]=PRESC[IDOFN-1]
    for x in range(0,NSTRE) :
        fileWrite.write(str(IPOIN[x])+'   ')
        for y in range(0,NDOFN):
            fileWrite.write(str(RLOAD[IPOIN[x]-1][y])+'   ')
#             print(IPOIN[x])
#             print(RLOAD[IPOIN[x]-1][y])
        fileWrite.write('\n')     

def STIFFA():
        for x in range(1,NELEM+1):
            LPROP=MATNO[x-1]
            YOUNG=PROPS[LPROP-1][0]                                              
            XAREA=PROPS[LPROP-1][1]                                              
            NODE1=LNODS[x-1][0]                                              
            NODE2=LNODS[x-1][1]                                                                                                                                         
            ELENG=abs(COORD[NODE2-1][1]-COORD[NODE1-1][1])                                                                                          
            FMULT=YOUNG*XAREA/ELENG                                           
            ESTIF[0][0][x-1]=FMULT                                    
            ESTIF[0][1][x-1]=-FMULT                                      
            ESTIF[1][0][x-1]=-FMULT                                      
            ESTIF[1][1][x-1]=FMULT                                                

def STIFFB():
    
    for x in range(1,NELEM+1):
        LPROP=MATNO[x-1]                                                
        YOUNG=PROPS[LPROP-1][0]                                              
        XAREA=PROPS[LPROP-1][1]                                              
        NODE1=LNODS[x-1][0]                                             
        NODE2=LNODS[x-1][1]  
    
        D1=COORD[NODE2-1][0]-COORD[NODE1-1][0]                                  
        D2=COORD[NODE2-1][1]-COORD[NODE1-1][1]                                  
        ELENG=sqrt(D1*D1+D2*D2)                                     
        SINTH=D2/ELENG                                                    
        COSTH=D1/ELENG                                                    
        FMULT=YOUNG*XAREA/ELENG
        ESTIF[0][0][x-1]=FMULT*COSTH*COSTH      
        ESTIF[0][1][x-1]=FMULT*SINTH*COSTH                                      
        ESTIF[1][0][x-1]=FMULT*SINTH*COSTH                                      
        ESTIF[1][1][x-1]=FMULT*SINTH*SINTH  
                                   
        for INODE in range(1,NNODE+1):
            for JNODE in range(1,NNODE+1):                                       
                KOUNT=((-1)**INODE)*((-1)**JNODE)  
                for KNODE in range(1,NNODE+1):
                    for LNODE in range(1,NNODE+1):
                        INDEX=(INODE-1)*NNODE+KNODE                                       
                        JNDEX=(JNODE-1)*NNODE+LNODE 
                        ESTIF[INDEX-1][JNDEX-1][x-1]=KOUNT*ESTIF[KNODE-1][LNODE-1][x-1] 
                        
                    
def ASSEMB() : 
#     ESTIF = [[0 for x in range(4)] for x in range(4)]
    for IPOIN in range(1,NPOIN+1):
        for IDOFN in range(1,NDOFN+1):
            NROWS=(IPOIN-1)*NDOFN+IDOFN
            ASLOD[NROWS-1]=ASLOD[NROWS-1]+RLOAD[IPOIN-1][IDOFN-1]
            
    for IELEM in range(1,NELEM+1):
        for INODE in range(1,NNODE+1):
            NODEI=LNODS[IELEM-1][INODE-1]
            for IDOFN in range(1,NDOFN+1):
                NROWS=(NODEI-1)*NDOFN+IDOFN                                     
                NROWE=(INODE-1)*NDOFN+IDOFN                                     
                ASLOD[NROWS-1]=ASLOD[NROWS-1]+ELOAD[IELEM-1][NROWE-1]  
                
                for JNODE in range(1,NNODE+1): 
                    NODEJ=LNODS[IELEM-1][JNODE-1]
                    for JDOFN in range(1,NDOFN+1):
                        NCOLS=(NODEJ-1)*NDOFN+JDOFN                                     
                        NCOLE=(JNODE-1)*NDOFN+JDOFN                                     
                        ASTIF[NROWS-1][NCOLS-1]=ASTIF[NROWS-1][NCOLS-1]+ESTIF[NROWE-1][NCOLE-1][IELEM-1]
def GREDUC():
    NEQNS=NSVAB
    for IEQNS in range(1,NEQNS+1):
        if IFPRE[IEQNS-1]!=1 :
            PIVOT=ASTIF[IEQNS-1][IEQNS-1]
            if abs(PIVOT)>1.0E-10 :
#                 fileWrite.write(str(PIVOT)+' IDONTKNOW  '+str(IEQNS))
                if IEQNS!=NEQNS :
                    IEQN1=IEQNS+1
                    for IROWS in range(IEQN1,NEQNS+1):
                        FACTR=ASTIF[IROWS-1][IEQNS-1]/PIVOT
                        if FACTR!=0 :
                            for ICOLS in range(IEQNS,NEQNS+1):
                                ASTIF[IROWS-1][ICOLS-1]=ASTIF[IROWS-1][ICOLS-1]-FACTR*ASTIF[IEQNS-1][ICOLS-1]
                            ASLOD[IROWS-1]=ASLOD[IROWS-1]-FACTR*ASLOD[IEQNS-1]
                else:
                    asdasd=11
            else:
#                 IDONT KNOW 
                fileWrite.write(str(PIVOT)+' IDONTKNOW  '+str(IEQNS))
        elif IFPRE[IEQNS-1]==1 :
            for IROWS in range(IEQNS,NEQNS+1):
                ASLOD[IROWS-1]=ASLOD[IROWS-1]-ASTIF[IROWS-1][IEQNS-1]*FIXED[IEQNS-1]
                ASTIF[IROWS-1][IEQNS-1]=0
                
def BAKSUB():
    NEQNS=NSVAB
    NEQN1=NEQNS+1
    for IEQNS in range(1,NEQNS+1):
        NBACK=NEQN1-IEQNS
        
        PIVOT=ASTIF[NBACK-1][NBACK-1]
        RESID=ASLOD[NBACK-1]
        
        if NBACK!=NEQNS :
            NBAC1=NBACK+1
            for ICOLS in range (NBAC1,NEQNS+1):
                RESID=RESID-ASTIF[NBACK-1][ICOLS-1]*XDISP[ICOLS-1]
        else:
            asd=0
        if IFPRE[NBACK-1]==0 :
            XDISP[NBACK-1]=RESID/PIVOT
        if IFPRE[NBACK-1]==1 :
            XDISP[NBACK-1]=FIXED[NBACK-1]
            REACT[NBACK-1]=-RESID
    
    KOUNT=0
    for IPOIN in range(1,NPOIN+1):
        for IDOFN in range (1,NDOFN+1):
            KOUNT=KOUNT+1
            TDISP[IPOIN-1][IDOFN-1]=XDISP[KOUNT-1]
            TREAC[IPOIN-1][IDOFN-1]=REACT[KOUNT-1]

def FORCE():
    FOMEM = [0 for x in range(4)] 
    for IELEM in range(1,NELEM+1):
        for IEVAB in range(1,NNODE+1):
            FOMEM[IEVAB-1]=0.0                                                  
            KOUNT=0
            for INODE in range(1,NNODE+1):
                LOCAL=LNODS[IELEM-1][INODE-1]
                for IDOFN in range(1,NDOFN+1):
                    KOUNT=KOUNT+1   
                    FOMEM[IEVAB-1]=FOMEM[IEVAB-1]+ESTIF[IEVAB-1][KOUNT-1][IELEM-1]*TDISP[LOCAL-1][IDOFN-1]
                   
        if NDOFN==1:
            STRES[IELEM-1][0]= abs(FOMEM[0])
        if NDOFN==2:
            STRES[IELEM-1][0]=sqrt((FOMEM[0]*FOMEM[0])+(FOMEM[1]*FOMEM[1]))
        if FOMEM[0]<0.0 :
            STRES[IELEM-1][0]=-STRES[IELEM-1][0] 
            

def RESULT():
    fileWrite.write(str('NODE DISPLACEMENTS      REACTIONS\n'))
    for IPOIN in range(1,NPOIN+1) :
        fileWrite.write(str(IPOIN)+'   ')
        for IDOFN in range(1,NDOFN+1):
            fileWrite.write(str(TDISP[IPOIN-1][IDOFN-1])+'   ')
        for IDOFN in range(1,NDOFN+1):
            fileWrite.write(str(TREAC[IPOIN-1][IDOFN-1])+'   ')
        fileWrite.write('\n')
    if NSTRE!=0 :
        for IELEM in range(1,NELEM+1) :
            fileWrite.write(str(IELEM)+'   ')
            for ISTRE in range(1,NSTRE+1):
                fileWrite.write(str(STRES[IELEM-1][ISTRE-1])+'   ')

            fileWrite.write('\n')
        fileWrite.write('\n')

DATA()
if NDOFN==1 :
    STIFFA()
if NDOFN==2 :
    STIFFB()
ASSEMB ()
GREDUC()                                                   
BAKSUB()        
FORCE() 
RESULT()    
