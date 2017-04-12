 #########################                  
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
###########################

   ########     #########
  #        #   #         #
##          ###          ##
 #          # #          #
  #        #   #        #
   ########     ########
            
           #  #
           
#face simplifier!
#use for model checkout 


import rhinoscriptsyntax as rs
import Rhino as r

#air support

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-1

STEP=0.1
TOR=0.001

precL=0.01

class line_compare_battalion():
    
    
    
    #verifying the line segment is on a curve or not#
    def single_compare_company(self,line,crv,precL):
        pts=rs.DivideCurveLength(rs.CurveLength(line)*precL)
        for i in range(1/preL):
            if not rs.IsPointOnCurve(crv,pts[i]):
                return FALSE
        return TRUE
        
    def crv_crv_compare_company(self,crv1,crv2)
        
        
class surface_compare_battalion():
    def srfcompare_company(self,srf1,srf2):
        for i in range(0,1,STEP):
            for j in range(0,1,STEP):
                if rs.SurfaceParameter(srf1,(i,j))[0]-rs.SurfaceParameter(srf2,(i,j))[0]>TOR or rs.SurfaceParameter(srf1,(i,j))[1]-rs.SurfaceParameter(srf2,(i,j))[1]>TOR:
                    print "not the same"
                    return ERROR
        
        print "same"
        return OK
    def srfrelation_company(self,srf1,srf2):
        newsrf=rs.BooleanIntersection(
    
    
    
class destruct_battalion():
    def 
    def compare_company(self,srf1,srf2):
        co=rs.IntersectBreps(srf1,srf2)
        if (co is None) or rs.IsPoint(co):
            return FALSE
        elif 
        
        
        return OK
    def soft_destruct_company(self,srfs):
        for i in range
        
        return OK
    def hard_destruct_company(self,srfs):
        return OK
    def total_destruct_company(self,srfs):
        return OK


#company to do face collection
def scout_company(task):
    
    Srfs=[]
    
    preset=rs.GetObjects("please select faces for destruction",rs.filter.surface)
    
    if task==3 or task==2:
        for i in rage(len(preset)):
            Srfs[i]=preset[i]
    else:
        for i in range(len(preset)):
            if rs.IsPlaneSurface(preset[i]):
                Srfs.append(preset[i])
    
    return Srfs
    
    
    

def HQ():
    
    while 1:
        task=rs.GetInteger("please choose the type of destruction: (1=soft, 2=hard, 3=total)")
        if task==1 or task==2 or task==3:
            break
        else:
            rs.MessageBox("please choose the right type")
    
    srfs=scout_company(task) 
    
    return OK


def main():
    
    return OK

main()

