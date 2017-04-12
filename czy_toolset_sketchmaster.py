############################
###Tool_ENVIENGINE Set By Zhengyang Chen
###Tel:+86 13818034245
###WeChat:czy4050715
############################

###THIS TOOL IS FOR QUICK ENVIRONMENTAL SKETCH WHILE YOU HAVE THE COARSE CAD FILE####

import rhinoscriptsyntax as rs
import rhinoscriptsyntax as sc

#defines
TRUE=1
FALSE=0
OK=0
ERROR=-1
OVERFLOW=-2
style_MODERN=1
style_CLASSIC=0

class construct_element():
    
    def building_concept(self,crv,floors,ext=3000,divide=False):
        if not rs.IsCurveClosed(crv):
            #print "current curve is not closed!"
            #rs.MessageBox(
            temp=[]
            temp.append(crv)
            addl=rs.AddLine(rs.CurveStartPoint(crv),rs.CurveEndPoint(crv))
            temp.append(addl)
            crv=rs.JoinCurves(addl,True)
        
        if rs.IsCurvePlanar(crv):
            #print "OK"
            plane=rs.WorldXYPlane()
            xform = rs.XformPlanarProjection(plane)

            crv=rs.TransformObject(crv,xform)
        houses=[]
        srf=rs.AddPlanarSrf(crv)
        if divide==True:
            
            direction=rs.AddLine([0,0,0],[0,0,ext])
            for i in range(floors):
                house=rs.ExtrudeSurface(srf,direction)
                srf=rs.MoveObject(srf,rs.VectorCreate([0,0,ext],[0,0,0]))
                houses.append(house)
            rs.DeleteObject(direction)
            rs.DeleteObject(srf)
        else:
            height=ext*floors
            direction=rs.AddLine([0,0,0],[0,0,height])
            house=rs.ExtrudeSurface(srf,direction)
            rs.DeleteObject(direction)
            rs.DeleteObject(srf)
            
        return OK
        
    def ground(self,crv):
        print "not available yet"
        return OK
    def corridor(self,crv,divlen,height,style):
        #print "not available yet"
        
        basecrv=rs.TransformObject(crv,rs.XformPlanarProjection(rs.WorldXYPlane()))
        if rs.CurveCurveIntersection(crv):
            val=rs.MessageBox("self intersection found,proceed?",1)
            if val==2:
                return ERROR
        segnum=round(rs.CurveLength(crv)/divlen)
        stPts=rs.DivideCurve(crv,segnum)
        endPts=rs.TransformObjects(stPts,rs.XformTranslation(rs.VectorCreate([0,0,0],[0,0,height])),True)
        if style==style_MODERN:
            cols=[]
            #set columns:
            for i in range(len(stPts)):
                col=rs.AddLine(stPts[i],endPts[i])
                cols.append(col)
            #extrude top:
            vDirec=rs.VectorCrossProduct(rs.VectorCreate(rs.CurveStartPoint(crv),rs.CurveEndPoint(crv)),[0,0,1])
            newsrf1=rs.ExtrudeCurve(crv,
        if style==style_CLASSIC:
            #under construction
            print "not available yet"
            return ERROR
        return OK
    
def type_confirm(crvs):
    MyWorker=construct_element()
    
    type=rs.GetInteger("please confirm the type, (1=building,2=ground,3=corridor)",1,1)
    
    
    if type==1:
        floors=rs.GetInteger("please confirm the floor count:",6,1)
        extheight=rs.GetInteger("please confirm the storey height :",3000,1)
        div=rs.GetInteger("Do you want to split each storeys? Y=1,N=0",0,0)
        
        for crv in crvs:
            MyWorker.building_concept(crv,floors,extheight,div)
        
        
    elif type==2:
        Myworker.ground(crv)
    elif type==3:
        
        divlen=rs.GetInteger("please confirm the segment length:",4000,1)
        height=rs.GetInteger("please confirm the height of corridor",2000,1)
        style=rs.GetInteger("please confirm the style of corridor (classical=0,modern=1)",1,0)
        for crv in crvs:
            Myworker.corridor(crv,divlen,height,style)
    else:
        rs.MessageBox("wrong type choosed!")
        return ERROR
    
def main():
    
    crvs=rs.GetObjects("please choose the boundary crv:",rs.filter.curve)
    
    for crv in crvs:
        if not rs.IsCurve(crv):
            return ERROR
    type_confirm(crvs)
    
    return OK
    
    
    
main()