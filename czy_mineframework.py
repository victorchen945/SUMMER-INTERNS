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
import rhinoscriptsyntax as rs
import random as r
import scriptcontext as sc
#import czy_toolset_sketchmaster as sk
#import czy_08_16_framescripts_mk1 as frm

#defines
TRUE=1
FALSE=0
OK=0
ERROR=-1

CRV=8
SRF=16


MAX=40

WIN_BACK1=300
WIN_BACK2=300
WIN_BACK3=300
WIN_BACK4=300
WIN_BACK0=300

WIN_THICK1=50
WIN_THICK2=700
WIN_BAL=1200

FAC=0.7

T0_LEN=600
T0_SCALE=0.95

T1_LEN=600
T1_SCALE=0.95

T2_LEN=600
T2_SCALE=0.95

T3_LEN=600
T3_SCALE=0.95

T4_LEN=600
T4_SCALE=0.95



class minefield():
    
    minefarm=[]
    mineshow=[]
    
    def _init_(self,sizex,sizey):
        for i in range (sizex+2):
            temp=[]
            temp1=[]
            for j in range(sizey+2):
                k=0
                temp.append(k)
                temp1.append(k-1)
            self.minefarm.append(temp)
            self.mineshow.append(temp1)
        #self.mine_testprint(sizex,sizey,3)
        return OK
    
    def mine_generate(self,x,y,num,seed):
        print "enter generate func"
        if num>x*y*0.5:
            print "too many mines"
            return ERROR
        r.seed(seed)
        self._init_(x,y)
        mines_x=[]
        mines_y=[]
        type=rs.GetInteger("select generation method!(0=RANDOM,1=EVEN,)",1)
        if type==0:
            
            for i in range(num):
                while 1:
                    mine_x=r.randint(1,x)
                    mine_y=r.randint(1,y)
                    if self.minefarm[mine_x][mine_y]!=1:
                        self.minefarm[mine_x][mine_y]=1
                        mines_x.append(mine_x)
                        mines_y.append(mine_y)
                        break
        if type==1:
            each=num//y+1
            for j in range(1,y+1):
                for i in range(each):
                    while 1:
                        mine_x=r.randint(1,x)
                        mine_y=j
                        if self.minefarm[mine_x][mine_y]!=1:
                            self.minefarm[mine_x][mine_y]=1
                            mines_x.append(mine_x)
                            mines_y.append(mine_y)
                            break
        #check minefarm here
        
        self.mine_field(x,y)
        return OK
    
    
    def mine_field(self,x,y):
        #print "go"
        for i in range(1,x+1):
            for j in range(1,y+1):
                if self.minefarm[i][j]==1:
                    self.mineshow[i][j]=-1
                else:
                    #print self.minefarm[i-1][j-1]
                    self.mineshow[i][j]=self.minefarm[i-1][j-1]+self.minefarm[i-1][j]+self.minefarm[i-1][j+1]+self.minefarm[i][j-1]+self.minefarm[i][j+1]+self.minefarm[i+1][j-1]+self.minefarm[i+1][j]+self.minefarm[i+1][j+1]
            #print self.minefarm[i]
            #print self.minefarm[i-1]
            #print self.mineshow[i]
            #print self.mineshow[i-1]
                    #print "i=",i, "j=",j, " ",self.mineshow[i][j]
                    #print self.minefarm
        #print self.mineshow
        
        self.mine_testprint(x,y,3)

        return OK
        
    def mine_testprint(self,x,y,scale):
    
        for i in range(1,x+1):
            for j in range(1,y+1):
                #print self.mineshow[i][j], " "
                if self.minefarm[i][j]==1:
                    rs.AddText("M",[scale*i,scale*j,0])
                elif self.mineshow[i][j]==0 or self.mineshow[i][j]==-1:
                    rs.AddText("0",[scale*i,scale*j,0])
                else:
                    rs.AddText(self.mineshow[i][j],[scale*i,scale*j,0])
        return OK
    
    def mine_combination(self):
        return OK


class elevation_melt():
    
    #define base center pts
    def _init(self,xsize,ysize,dx,dy):
        basepts=[[0 for i in range(ysize+2)] for j in range(xsize+2)]
        for i in range(1,xsize+1):
            for j in range(1,ysize+1):
                basepts[i][j]=rs.AddPoint((dx*i-dx/2,dy*j-dy/2,0))
        #rs.XformCPlaneToWorld
        return basepts
    def traverse_combine(self,x,y):
        visit=[[0 for i in range(y+2)]for j in range(x+2)]
        #init visit mark
        for i in range(1,x+1):
            for j in range(1,y+1):
                visit[i][j]=0
        #mark define horizonstart=1, horinzonend=2,verticalstart=3,verticalend=4
        myMine=minefield()
        
        for i in range(2,x):
            for j in range(1,y+1):
                if visit[i][j]!=0:
                    pass
                elif myMine.mineshow[i][j]==myMine.mineshow[i+1][j] and visit[i+1][j]==0 and (i+1)!=x:
                    visit[i][j]=1
                    visit[i+1][j]=2
                elif myMine.mineshow[i][j]==myMine.mineshow[i][j+1] and j<y:
                    visit[i][j]=3
                    visit[i][j+1]=4
                else:
                    pass
        return visit
        
    def generate(self,x,y,dx,dy):
        
        
        
        plbasepts=[[0 for i in range(y+2)] for j in range(x+2)]
        pls=[[0 for i in range(y+2)] for j in range(x+2)]
        srfs=[[0 for i in range(y+2)] for j in range(x+2)]
        cens=self._init(x,y,dx,dy)
        for i in range(1,x+1):
            for j in range(1,y+1):
                plbasepts[i][j]=rs.TransformObject(cens[i][j],rs.XformTranslation(rs.VectorCreate((0,0,0),(dx/2,dy/2,0))),TRUE)
                pls[i][j]=rs.PlaneTransform(rs.WorldXYPlane(),rs.XformTranslation(rs.VectorCreate(plbasepts[i][j],(0,0,0))))
                srfs[i][j]=rs.AddPlanarSrf(rs.AddRectangle(pls[i][j],dx,dy))
                
        #point to define outside and inside, can be preset or determine by input
        if 0:
            outpt=rs.GetObject("plane created,PLEASE SELECT THE OUTSIDE POINT!",rs.filter.point)
        if 1:
            outpt=rs.AddPoint((0,0,10000))
            
        #colordefination
        colorH=[220,220,220]
        colorM=[150,150,150]
        colorL=[90,90,90]
        WH=[170,170,255]
        WM=[170,170,255]
        WL=[170,170,255]
        ##followings are optional
        """RH=rs.ColorRedValue(colorH)
        GH=rs.ColorGreenValue(colorH)
        BH=rs.ColorBlueValue(colorH)
        RL=rs.ColorRedValue(colorL)
        GL=rs.ColorGreenValue(colorL)
        BL=rs.ColorBlueValue(colorL)
        RR=(rs.ColorRedValue(colorH)-rs.ColorRedValue(colorL))/8
        GR=(rs.ColorGreenValue(colorH)-rs.ColorGreenValue(colorL))/8
        BR=(rs.ColorBlueValue(colorH)-rs.ColorBlueValue(colorL))/8"""
        myMine=minefield()
        
        #colorlist[][0]=frame,[][1]=window,each have 3 value to define rgb
        """colorlist=[[[0 for i in range(3)]for j in range(2)] for k in range[8]]
        for m in range(8):
            colorlist[m][0][0]=RR*m+RL
            colorlist[m][0][1]=GR*m+GL
            colorlist[m][0][2]=BR*m+BL
            colorlist[m][1][0]=WL
            colorlist[m][1][1]=WL
            colorlist[m][1][2]=WL"""
        visit=self.traverse_combine(x,y)
        WIN_THICK=0
        for i in range(1,x+1):
            
            for j in range(1,y+1):
                if myMine.mineshow[i][j]==-1:
                    bdr=FALSE
                    if i==1 or i==x:
                        bdr=TRUE
                    else:
                        bdr=FALSE
                    if i==3 or i==x-2:
                        WIN_THICK=WIN_THICK1
                    else:
                        WIN_THICK=WIN_THICK2
                    self.type_0(dx,dy,cens[i][j],plbasepts[i][j],pls[i][j],srfs[i][j],outpt,colorH,WH,bdr,T0_SCALE,T0_LEN,WIN_BACK0,visit[i][j],WIN_THICK)
                elif myMine.mineshow[i][j]==0:
                    bdr=FALSE
                    if i==1 or i==x:
                        bdr=TRUE
                    else:
                        bdr=FALSE
                    if i==3 or i==x-2:
                        WIN_THICK=WIN_THICK1
                    else:
                        WIN_THICK=WIN_THICK2
                    self.type_0(dx,dy,cens[i][j],plbasepts[i][j],pls[i][j],srfs[i][j],outpt,colorH,WM,bdr,T1_SCALE,T1_LEN,WIN_BACK1,visit[i][j],WIN_THICK)
                elif myMine.mineshow[i][j]==1:
                    bdr=FALSE
                    if i==1 or i==x:
                        bdr=TRUE
                    else:
                        bdr=FALSE
                    if i==3 or i==x-2:
                        WIN_THICK=WIN_THICK1
                    else:
                        WIN_THICK=WIN_THICK2
                    self.type_0(dx,dy,cens[i][j],plbasepts[i][j],pls[i][j],srfs[i][j],outpt,colorH,WM,bdr,T1_SCALE,T1_LEN,WIN_BACK1,visit[i][j],WIN_THICK)
                elif myMine.mineshow[i][j]==2:
                    if i==1 or i==x:
                        bdr=TRUE
                    else:
                        bdr=FALSE
                    if i==3 or i==x-2:
                        WIN_THICK=WIN_THICK1
                    else:
                        WIN_THICK=WIN_THICK2
                    self.type_0(dx,dy,cens[i][j],plbasepts[i][j],pls[i][j],srfs[i][j],outpt,colorM,WL,bdr,T2_SCALE,T2_LEN,WIN_BACK2,visit[i][j],WIN_THICK)
                elif myMine.mineshow[i][j]==3:
                    if i==1 or i==x:
                        bdr=TRUE
                    else:
                        bdr=FALSE
                    if i==3 or i==x-2:
                        WIN_THICK=WIN_THICK1
                    else:
                        WIN_THICK=WIN_THICK2
                    self.type_0(dx,dy,cens[i][j],plbasepts[i][j],pls[i][j],srfs[i][j],outpt,colorM,WL,bdr,T3_SCALE,T3_LEN,WIN_BACK3,visit[i][j],WIN_THICK)
                elif myMine.mineshow[i][j]==4:
                    if i==1 or i==x:
                        bdr=TRUE
                    else:
                        bdr=FALSE
                    if i==3 or i==x-2:
                        WIN_THICK=WIN_THICK1
                    else:
                        WIN_THICK=WIN_THICK2
                    self.type_0(dx,dy,cens[i][j],plbasepts[i][j],pls[i][j],srfs[i][j],outpt,colorL,WL,bdr,T4_SCALE,T4_LEN,WIN_BACK4,visit[i][j],WIN_THICK)
                else:
                    bdr=FALSE
                    if i==1 or i==x:
                        bdr=TRUE
                    else:
                        bdr=FALSE
                    if i==3 or i==x-2:
                        WIN_THICK=WIN_THICK1
                    else:
                        WIN_THICK=WIN_THICK2
                    self.type_0(dx,dy,cens[i][j],plbasepts[i][j],pls[i][j],srfs[i][j],outpt,colorH,WM,bdr,T0_SCALE,T0_LEN,WIN_BACK0,visit[i][j],WIN_THICK)
        for i in range(1,x+1):
            for j in range(1,y+1):
                rs.DeleteObjects(srfs[i][j])
        
            
        return OK
    
    def combine_calculator(self,cenPt,vec,outrec,inrec,SCALE):
        
        boxrecs=[]
        
        newcen=rs.CopyObject(cenPt,vec)
        inrec=rs.ScaleObject(outrec,newcen,[SCALE,SCALE,SCALE],TRUE)
        inrecsrf=rs.BooleanDifference(rs.AddPlanarSrf(outrec),rs.AddPlanarSrf(inrec))
        inreccrv=rs.JoinCurves(rs.DuplicateEdgeCurves(inrecsrf))
        if not rs.IsCurveClosed(inreccrv):
            rs.MessageBox("outercrv not closed")
            return ERROR
        boxrecs.append(inreccrv)
        inrecsmall=rs.ScaleObject(outrec,newcen,[SCALE*FAC,SCALE*FAC,SCALE*FAC],TRUE)
        inrecsmallsrf=rs.BooleanDifference(rs.AddPlanarSrf(outrec),rs.AddPlanarSrf(inrecsmall))
        inrecsmallcrv=rs.JoinCurves(rs.DuplicateEdgeCurves(inrecsmallsrf))
        if not rs.IsCurveClosed(inrecsmallcrv):
            rs.MessageBox("innercrv not closed")
            return ERROR
        boxrecs.append(inrecsmallcrv)
        return boxrecs
    
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
        
    def type_1(self,dx,dy,cenPt,basePt,basePln,baseSrf,outsidePt,colorF,colorW,boundary):
        crvs=[]
        outrec=rs.AddRectangle(basePln,dx,dy)
        cenpt=rs.AddPoint(cenPt)
        inrec=rs.ScaleObject(outrec,cenPt,[T1_SCALE,T1_SCALE,T1_SCALE],TRUE)
        crvs.append(outrec)
        crvs.append(inrec)
        framesrf=rs.AddPlanarSrf(crvs)
        
        dir=rs.VectorScale(rs.CurveNormal(outrec),T1_LEN/rs.VectorLength(rs.CurveNormal(outrec)))
        #if not the sameside then reverse vector#
        if rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)>90 and rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)<270:
            dir=rs.VectorReverse(dir)
        frame=rs.ExtrudeSurface(framesrf,rs.AddLine((0,0,0),rs.PointAdd(dir,(0,0,0))))
        winvec=rs.VectorScale(dir,(T1_LEN-WIN_BACK1)/rs.VectorLength(dir))
        winvec2=rs.VectorScale(dir,WIN_THICK/rs.VectorLength(dir))
        windowbase=rs.CopyObject(rs.AddPlanarSrf(inrec),winvec)
        window=rs.ExtrudeSurface(windowbase,rs.AddLine(rs.PointAdd(winvec2,(0,0,0)),(0,0,0)))
        rs.ObjectColor(frame,colorF)
        rs.ObjectColor(window,colorW)
        index=rs.ObjectMaterialIndex(frame)
        if index==-1:
            print "color!" 
            rs.MaterialColor(index,colorF)
            rs.AddMaterialToObject(frame)
        rs.DeleteObjects([windowbase,cenpt,framesrf])
        return OK
        
    def type_2(self,dx,dy,cenPt,basePt,basePln,baseSrf,outsidePt,colorF,colorW):
        crvs=[]
        outrec=rs.AddRectangle(basePln,dx,dy)
        cenpt=rs.AddPoint(cenPt)
        inrec=rs.ScaleObject(outrec,cenPt,[T2_SCALE,T2_SCALE,T2_SCALE],TRUE)
        crvs.append(outrec)
        crvs.append(inrec)
        framesrf=rs.AddPlanarSrf(crvs)
        
        dir=rs.VectorScale(rs.CurveNormal(outrec),T2_LEN/rs.VectorLength(rs.CurveNormal(outrec)))
        #if not the sameside then reverse vector#
        if rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)>90 and rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)<270:
            dir=rs.VectorReverse(dir)
        frame=rs.ExtrudeSurface(framesrf,rs.AddLine((0,0,0),rs.PointAdd(dir,(0,0,0))))
        winvec=rs.VectorScale(dir,(T2_LEN-WIN_BACK2)/rs.VectorLength(dir))
        winvec2=rs.VectorScale(dir,WIN_THICK/rs.VectorLength(dir))
        windowbase=rs.CopyObject(rs.AddPlanarSrf(inrec),winvec)
        window=rs.ExtrudeSurface(windowbase,rs.AddLine(rs.PointAdd(winvec2,(0,0,0)),(0,0,0)))
        rs.ObjectColor(frame,colorF)
        rs.ObjectColor(window,colorW)
        index=rs.ObjectMaterialIndex(frame)
        if index==-1:
            print "color!" 
            rs.MaterialColor(index,colorF)
            rs.AddMaterialToObject(frame)
        rs.DeleteObjects([windowbase,cenpt,framesrf])
        return OK
        
    def type_3(self,dx,dy,cenPt,basePt,basePln,baseSrf,outsidePt,colorF,colorW):
        crvs=[]
        trashbin=[]
        outrec=rs.AddRectangle(basePln,dx,dy)
        cenpt=rs.AddPoint(cenPt)
        inrec=rs.ScaleObject(outrec,cenPt,[T3_SCALE,T3_SCALE,T3_SCALE],TRUE)
        crvs.append(outrec)
        crvs.append(inrec)
        framesrf=rs.AddPlanarSrf(crvs)
        
        dir=rs.VectorScale(rs.CurveNormal(outrec),T3_LEN/rs.VectorLength(rs.CurveNormal(outrec)))
        #if not the sameside then reverse vector#
        if rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)>90 and rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)<270:
            dir=rs.VectorReverse(dir)
        frame=rs.ExtrudeSurface(framesrf,rs.AddLine((0,0,0),rs.PointAdd(dir,(0,0,0))))
        winvec=rs.VectorScale(dir,(T3_LEN-WIN_BACK3)/rs.VectorLength(dir))
        winvec2=rs.VectorScale(rs.VectorReverse(dir),WIN_THICK/rs.VectorLength(dir))
        windowbase=rs.CopyObject(rs.AddPlanarSrf(inrec),winvec)
        window=rs.ExtrudeSurface(windowbase,rs.AddLine(rs.PointAdd(winvec2,(0,0,10000)),(0,0,10000)))
        rs.ObjectColor(frame,colorF)
        rs.ObjectColor(window,colorW)
        index=rs.ObjectMaterialIndex(frame)
        if index==-1:
            print "color!" 
            rs.MaterialColor(index,colorF)
            rs.AddMaterialToObject(frame)
        
        rs.DeleteObjects([windowbase,cenpt,framesrf])
        return OK
        
    def type_4(self,dx,dy,cenPt,basePt,basePln,baseSrf,outsidePt,colorF,colorW):
        crvs=[]
        outrec=rs.AddRectangle(basePln,dx,dy)
        cenpt=rs.AddPoint(cenPt)
        inrec=rs.ScaleObject(outrec,cenPt,[T4_SCALE,T4_SCALE,T4_SCALE],TRUE)
        crvs.append(outrec)
        crvs.append(inrec)
        framesrf=rs.AddPlanarSrf(crvs)
        
        dir=rs.VectorScale(rs.CurveNormal(outrec),T4_LEN/rs.VectorLength(rs.CurveNormal(outrec)))
        #if not the sameside then reverse vector#
        if rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)>90 and rs.VectorAngle(rs.VectorCreate(outsidePt,basePt),dir)<270:
            dir=rs.VectorReverse(dir)
        frame=rs.ExtrudeSurface(framesrf,rs.AddLine((0,0,0),rs.PointAdd(dir,(0,0,0))))
        winvec=rs.VectorScale(dir,(T4_LEN-WIN_BACK4)/rs.VectorLength(dir))
        winvec2=rs.VectorScale(dir,WIN_THICK/rs.VectorLength(dir))
        windowbase=rs.CopyObject(rs.AddPlanarSrf(inrec),winvec)
        window=rs.ExtrudeSurface(windowbase,rs.AddLine(rs.PointAdd(winvec2,(0,0,0)),(0,0,0)))
        rs.ObjectColor(frame,colorF)
        rs.ObjectColor(window,colorW)
        index=rs.ObjectMaterialIndex(frame)
        if index==-1:
            print "color!" 
            rs.MaterialColor(index,colorF)
            rs.AddMaterialToObject(frame)
        rs.DeleteObjects([windowbase,cenpt,framesrf])
        return OK
class elevation_fit():
    def _init(self):
        return OK
    def module_confirm(self):
        return OK
    def planar_projection(self):
        return OK

class elevation_combine():
    def _init(self):
        return OK
    def typedef(self):
        return OK
    def traverse(self):
        return OK
    def combine_horizon(self):
        return OK
    def combine_vertical(self):
        return OK
    
    
class rendersettings():
    type=[]
    def color_setting(self):
        return OK
    def brep_loft(self):
        return OK
    def bake_options(self):
        return OK

def confirm_size():
    if 1:
        while 1:
            
            x_size=rs.GetInteger("please confirm the x size",6,1)
            y_size=rs.GetInteger("please confirm the y size",10,1)
            if x_size<6 :
                rs.MessageBox("x size too small!")
            else:
                break
                
    num=rs.GetInteger("please confirm mine num",10,1)
    if num>x_size*y_size:
        rs.MessageBox("wrong mine number")
        return ERROR
    if 0:
        
        dx=rs.GetInteger("please confirm the x dimension",2400)
        dy=rs.GetInteger("please confirm the y dimension",3000)
        
    if 1:
        pt0=rs.GetPoint("please confirm the origin pt:")
        pt1=rs.GetPoint("please confirm the x axis pt:")
        pt2=rs.GetPoint("please confirm the y axis pt:")
        
        dx=rs.VectorLength(rs.VectorCreate(pt1,pt0))/x_size
        dy=rs.VectorLength(rs.VectorCreate(pt2,pt0))/y_size
    
    return x_size,y_size,num,dx,dy,[pt0,pt1,pt2]
    
def _transform(objects):
    
    PlnPt1=rs.GetPoint("select base point of plane:",rs.filter.point)
    PlnPt2=rs.GetPoint("select x-axis point of plane:",rs.filter.point)
    PlnPt3=rs.GetPoint("select y-axis point of plane:",rs.filter.point)
    
    targPln=rs.PlaneFromPoints(PlnPt1,PlnPt2,PlnPt3)
    xform=rs.XformChangeBasis(targPln,rs.WorldXYPlane())
    rs.TransformObjects(objects,xform)
    return OK
    
def adv_transform(obj,pt0,pt1,pt2):
    
    targPln=rs.PlaneFromPoints(pt0,pt1,pt2)
    xform=rs.XformChangeBasis(targPln,rs.WorldXYPlane())
    rs.TransformObjects(obj,xform)
    
    return OK
    