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

import rhinoscriptsyntax as rs

#Air Support#
OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

MAXNUM=99999999

def main():
    
    objs=0
    
    for i in range(1):
        if 1:
            objs=rs.GetObjects("select objects",rs.filter.polysurface)
        if 0:
            objs=rs.GetObjects("select objects",rs.filter.curve)
        if 0:
            objs=rs.GetObjects("select objects",rs.filter.surface)
        if 0:
            objs=rs.GetObjects("select objects",rs.filter.point)
        if 0:
            objs=rs.GetObjects("select objects",rs.filter.mesh)
        if 0:
            objs=rs.GetObjects("select objects",rs.filter.instance)
    
        pt0=rs.GetPoint("plane start point")
        pt1=rs.GetPoint("plane x point")
        pt2=rs.GetPoint("plane y point")
    
        pln=rs.PlaneFromPoints(pt0,pt1,pt2)
    
        xform=rs.XformChangeBasis(pln,rs.WorldXYPlane())
    
        rs.TransformObjects(objs,xform)
    return OK

main()
