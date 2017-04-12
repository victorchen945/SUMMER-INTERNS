import rhinoscriptsyntax as rs
import scriptcontext as sc


OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-1

def divide():
    dist=rs.GetInteger("define the external",2000)
    pt01=rs.GetPoint("select L1 origin")
    pt02=rs.GetPoint("select L1 target")
    pt11=rs.GetPoint("select L2 origin")
    pt12=rs.GetPoint("select L2 target")
    
    pt21=rs.GetPoint("select L3 origin")
    pt22=rs.GetPoint("select L3 target")
    PtO=rs.GetPoint("select inside Pt")

def loft()



def main():
    
    return OK


main()