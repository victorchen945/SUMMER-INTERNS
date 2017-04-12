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

#Air Support#
OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

MAXNUM=99999999


class frame_construct_division():
    def planeconfirm_company(self,Pt0,Ptx,Pty):
        Pln=rs.PlaneFromPoints(Pt0,Ptx,Pty)
        return Pln
    def planediv_regiment(self,Pt0,Ptx,Pty,xmethod,ymethod):
        
        #define plane elements#
        
        Pln=self.planeconfirm_company(Pt0,Ptx,Pty)
        xVec=rs.VectorCreate(Ptx,Pt0)
        xAxis=rs.AddLine(Pt0,Ptx)
        yVec=rs.VectorCreate(Pty,Pt0)
        yAxis=rs.AddLine(Pt0,Pty)
        
        xPts=[]
        yPts=[]
        
        #find x,y location#
        divlenx=0
        divleny=0
        if xmethod>0:
            xPts=rs.DivideCurveLength(xAxis,xmethod)
            divlenx=xmethod
        else:
            xPts=rs.DivideCurve(xAxis,-xmethod)
            divlenx=xPts[1]-xPts[0]
        if ymethod>0:
            yPts=rs.DivideCurveLength(yAxis,ymethod)
            divleny=ymethod
        else:
            yPts=rs.DivideCurve(yAxis,-ymethod)
            divlenx=yPts[1]-yPts[0]
        
        #init basePts#
        basePts=[[0 for i in range(len(yPts))]for j in range(len(xPts))]
        farPts=[[0 for i in range(len(yPts))]for j in range(len(xPts))]
        cenPts=[[0 for i in range(len(yPts))]for j in range(len(xPts))]
        for i in range(len(xPts)-1):
            for j in range(len(yPts)-1):
                basePts[i][j]=rs.CopyObject(rs.AddPoint(xPts[i]),rs.VectorCreate(yPts[j],Pt0))
                farPts[i][j]=rs.CopyObject(basePts[i][j],rs.VectorAdd(rs.VectorCreate(xPts[i+1],xPts[i]),rs.VectorCreate(yPts[j+1],yPts[j])))
                cenPts[i][j]=rs.CopyObject(basePts[i][j],rs.VectorDivide(rs.VectorCreate(farPts[i][j],basePts[i][j]),2))
        self.recconstruct_battalion(basePts,cenPts,farPts,xPts,yPts)
        return basePts,cenPts,FarPts
        
    def recconstruct_battalion(self,base,cen,far,xPts,yPts):
        basePln=[[0 for i in range(len(yPts))]for j in range(len(xPts))]
        rec=[[0 for i in range(len(yPts)-1)]for j in range(len(xPts)-1)]
        basex=[[0 for i in range(len(yPts)-1)]for j in range(len(xPts)-1)]
        basey=[[0 for i in range(len(yPts)-1)]for j in range(len(xPts-1)]
        baserec4Pts=[[[] for i in range(len(yPts)-1)]for j in range(len(xPts)-1)]
        for i in range(len(xPts)-1):
            for j in range(len(yPts)-1):
                basex[i][j]=rs.CopyObject(base[i][j],rs.VectorCreate(xPts[i+1],xPts[i]))
                basey[i][j]=rs.CopyObject(base[i][j],rs.VectorCreate(yPts[j+1],yPts[j]))
                basePln[i][j]=rs.PlaneFromPoints(base[i][j],basex[i][j],basey[i][j])
                rec[i][j]=rs.AddRectangle(basePln[i][j],rs.VectorLength(rs.VectorCreate(xPts[i+1],xPts[i])),rs.VectorLength(rs.VectorCreate(yPts[j+1],yPts[j])))
                baserec4Pts.extend(base[i][j],basex[i][j],basey[i][j],far[i][j])
                rs.DeleteObjects([basex[i][j],basey[i][j]])
        
        crvs=rs.GetObjects("rectangles constructed,ask for crvs!",rs.filter.curve)
        self.crv_regiment(baserec4Pts,rec,crvs)
        return basePln,rec
        
    def crv_regiment(self,base4pts,recs,crvs):
        clspts=[[0 for i in range(len(base4pts[0]))]for j in range(len(base4pts))]
        mintotal[i][j]=[[0 for i in range(len(base4pts[0]))]for j in range(len(base4pts))]
        
        for i in range(len(base4pts)):
                for j in range(len(base4pts[i])): 
                    mintotal[i][j]=MAXNUM
                    
        for crv in crvs:
            for i in range(len(base4pts)):
                for j in range(len(base4pts[i])):
                    min=MAXNUM
                    clspt=(0,0,0)
                    for k in range(len(base4pts[i][j])
                        tmp=min
                        clstmp=rs.CurveClosestPoint(crv,base4pts[i][j][k])
                        tmp=rs.Distance(clstmp,base4pts[i][j][k])
                        if tmp<min:
                            min=tmp
                            clspt=clstmp
                    if min<mintotal[i][j]:
                        mintotal[i][j]=min
                        clspts[i][j]=clspt
                        
        rectransform_battalion(clspts,mintotal,base4pts)
        return clspts,mintotal
        
    def rectransform_battalion(self,clspts,mins,rec4pts):
        
        minmove=rs.GetInteger("set the minimum step",200,1)
        maxmove=rs.GetInteger("set the maximum step",500,minmove)
        facrange=rs.GetInteger("set the effective range of curve",3000,1)
        
        finalrec=[[0 for i in range(len(clspts[0]))]for j in range(len(clspts))]
        #assumpt linear relationship:
        step=(maxmove-minmove)/3000
        
        for i in range(clspts):
            for j in range(clspts[i]):
                if mins[i][j]>facrange:
                    rs.
                
    def xform_company(self,move,clspts,rec4pts):
        

def command_center():
    #get 3 points to confirm a plane
    pt1=rs.GetObject("select origin point of a plane",rs.filter.point)
    if not rs.IsPoint(pt1):
        return ERROR
    pt2=rs.GetObject("select x-axis point of a plane",rs.filter.point)
    if not rs.IsPoint(pt2):
        return ERROR
    pt3=rs.GetObject("select y-axis point of a plane",rs.filter.point)
    if not rs.IsPoint(pt3):
        return ERROR
        
    xme=0
    yme=0
    while 1:
        
        i=rs.GetInteger("choose x-axis separate method (1=ByLength,2=BySegment)",1)
        if i==1:
            xme=rs.GetInteger("please confirm the divide Length",1000)
            if not xme>0:
                rs.MessageBox("check the input")
                
            break
        elif i==2:
            xme=rs.GetInteger("please confirm the divide num",10,1)
            xme=0-xme
            break
        else:
            rs.MessageBox("ERROR!Follow the instruction")
            continue
            
    while 1:
        
        i=rs.GetInteger("choose y-axis separate method (1=ByLength,2=BySegment)",1)
        if i==1:
            yme=rs.GetInteger("please confirm the divide Length",1000)
            if not yme>0:
                rs.MessageBox("check the input")
                
            break
        elif i==2:
            yme=rs.GetInteger("please confirm the divide num",10,1)
            yme=0-yme
            break
        else:
            rs.MessageBox("ERROR!Follow the instruction")
            continue
        
    FrmDivision=frame_construct_division()
    FrmDivision.planediv_regiment(pt1,pt2,pt3,xme,yme)
    #constPln=FrmDivision.planeconfirm_company(pt1,pt2,pt3)
    
    

def general():
    command_center()
    
    
general()
