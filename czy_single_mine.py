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
import random as r
from czy_mineframework import minefield
from czy_mineframework import confirm_size

#air support#

TRUE=1
FALSE=0
OK=0
ERROR=-1
OVERFLOW=-2

def type_0(self,dx,dy,cenPt,basePt,basePln,baseSrf,outsidePt,colorF,colorW,boundary,SCALE,T_LEN,WIN_BACK,visit,WIN_THICK):
        crvs=[]
        boxrecs=[]
        
        outrec=rs.AddRectangle(basePln,dx,dy)
        cenpt=rs.AddPoint(cenPt)
        inrec=rs.ScaleObject(outrec,cenPt,[SCALE,SCALE,SCALE],TRUE)
        vecdef=rs.VectorCreate(basePt,cenPt)
        vecL=rs.VectorTransform(vecdef,rs.XformPlanarProjection(rs.WorldZXPlane()))
        vecR=rs.VectorReverse(vecL)
        print "def",vecdef
        vecD=rs.VectorAdd(vecdef,vecR)
        vecU=rs.VectorReverse(vecD)
        print "L",vecL,"R",vecR,"D",vecD,"U",vecU
        #rs.MessageBox("")
        
        
        if boundary==TRUE:
            print "boundary"
            inrec=rs.ScaleObject(outrec,cenPt,[1,SCALE,SCALE],TRUE)
            WIN_THICK=WIN_THICK2
        elif visit==1:
            boxrecs=self.combine_calculator(cenPt,vecR,outrec,inrec,SCALE)
        elif visit==2:
            boxrecs=self.combine_calculator(cenPt,vecL,outrec,inrec,SCALE)
        elif visit==3:
            boxrecs=self.combine_calculator(cenPt,vecU,outrec,inrec,SCALE)
        elif visit==4:
            boxrecs=self.combine_calculator(cenPt,vecD,outrec,inrec,SCALE)
        else:
            inrecsmall=rs.ScaleObject(outrec,cenPt,[SCALE*FAC,SCALE*FAC,SCALE*FAC],TRUE)
            boxrecs.append(inrecsmall)
        framesrfout=rs.AddPlanarSrf(outrec)
        framesrfin=rs.AddPlanarSrf(inrec)
        framesrfs=rs.BooleanDifference(framesrfout,framesrfin)
        
        
        dir=rs.VectorScale(rs.CurveNormal(outrec),T_LEN/rs.VectorLength(rs.CurveNormal(outrec)))
        #if not the sameside then reverse vector#
        if rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)>90 and rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)<270:
            dir=rs.VectorReverse(dir)
        outextrec=rs.CopyObject(inrec,dir)
        
        
        if boundary==FALSE :
            if visit==0:
                boxrecs.append(outextrec)
            else:
                framesrfs=rs.AddPlanarSrf(boxrecs[0])
                boxrecs[0]=rs.CopyObject(boxrecs[0],dir)
                
            bre=rs.AddLoftSrf(boxrecs)
            rs.ObjectColor(bre,colorF)
            rs.DeleteObjects([boxrecs[0],boxrecs[1]])
        
        
        frames=[]
        dirtmp=dir
        for framesrf in framesrfs:
            if boundary==TRUE:
                dir=rs.VectorScale(dir,600/rs.VectorLength(dir))
            frame=rs.ExtrudeSurface(framesrf,rs.AddLine((0,0,0),rs.PointAdd(dir,(0,0,0))))
            dir=dirtmp
            frames.append(frame)
            rs.DeleteObject(framesrf)
        #define the location of window, if winvec=0,0,0,0,0,0 the window is coherient to wall
        
        #original basis
        if 0:
            winvec=rs.VectorScale(dir,(T_LEN-WIN_BACK)/rs.VectorLength(dir))
        #changes
        if 1:
            winvec=rs.VectorCreate((0,0,0),(0,0,0)) 
        
        #if this is the boundary col of building, then the window is cornered
        if boundary==TRUE:
            winvec=rs.VectorCreate((0,0,0),(0,0,0))
        
        winvec2=rs.VectorScale(dir,WIN_THICK1/rs.VectorLength(dir))
        winpl=rs.AddPlanarSrf(outrec)
        if WIN_THICK==WIN_THICK1:
            
            #WIN_BAL=1200
            winvectmp=rs.VectorScale(dir,WIN_BAL/rs.VectorLength(dir))
            winvec=rs.VectorCreate((0,0,-WIN_BAL),(0,0,0))
            windowbase=rs.CopyObject(winpl,winvec)
            windowbase2=rs.CopyObject(windowbase,winvec2)
            window=rs.ExtrudeSurface(windowbase2,rs.AddLine(rs.PointAdd(winvec2,(0,0,0)),(0,0,0)))
            window2=rs.ExtrudeSurface(windowbase2,rs.AddLine((0,0,0),rs.PointAdd(winvectmp,(0,0,0))),FALSE)
            rs.ObjectColor(window2,colorW)
            
            rs.DeleteObjects([windowbase,windowbase2])
            
            
        else:
            
            windowbase=rs.CopyObject(winpl,winvec)
            windowbase2=rs.CopyObject(windowbase,winvec2)
            window=rs.ExtrudeSurface(windowbase2,rs.AddLine(rs.PointAdd(winvec2,(0,0,0)),(0,0,0)))
            
        rs.DeleteObjects([windowbase,windowbase2])
        rs.ObjectColor(frames,colorF)
        
        rs.ObjectColor(window,colorW)
        
        index=rs.ObjectMaterialIndex(frame)
        if index==-1:
            print "color!" 
            rs.MaterialColor(index,colorF)
            rs.AddMaterialToObject(frame)
        rs.DeleteObjects([windowbase,cenpt,framesrf,winpl])
        rs.DeleteObjects([framesrfout,framesrfin])
        return OK

def command_center():
    
    vals=confirm_size()
    
    
    myMine=minefield()
    myMine.mine_generate(vals[0],vals[1],vals[2],3)
    
    
    
    return OK
    
def main():
    
    #command_center()
    
    
    
    
    return OK
    
    
    
main()
