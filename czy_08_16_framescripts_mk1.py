import rhinoscriptsyntax as rs
import scriptcontext as sc

#defines:
TRUE=1
FALSE=0
OK=0
ERROR=-1
OVERFLOW=-2


def edge_counter(crvs):
    return len(crvs)
    
#class triangle()
class tri_fram():
    
    
    def frame_div(self,srf,gap):
        
        cen=rs.SurfaceAreaCentroid(srf)
        
        if not rs.IsSurface(srf):
            print "err0: selection is not a surface"
            return ERROR
        srfBounds=rs.DuplicateEdgeCurves(srf)
        #edge num counter
        bdrNum=edge_counter(srfBounds)
    
        #if triangle
        if bdrNum==3:
            #init min & max
            minBound=srfBounds[0]
            maxBound=srfBounds[0]
            psBound=srfBounds[0]
        #confirm div
            for srfBound in srfBounds:
                if rs.CurveLength(srfBound)>=rs.CurveLength(maxBound):
                    maxBound=srfBound
                    
                elif rs.CurveLength(srfBound)<=rs.CurveLength(minBound):
                    minBound=srfBound
                else:
                    psBound=srfBound
            minNum=round(rs.CurveLength(minBound)/gap,0)
            maxNum=round(rs.CurveLength(maxBound)/gap,0)
            
            ShrPts=rs.DivideCurve(minBound,minNum)
            LngPts=rs.DivideCurve(maxBound,maxNum)
            print "min: Length:", rs.CurveLength(minBound),"ID:",minBound
            print "max: Length:",rs.CurveLength(maxBound),"ID:",maxBound
            print "cutter Length:",rs.CurveLength(psBound),"ID:", psBound
            newfrm=self.frame_construct_tri(ShrPts,LngPts,minBound,maxBound,psBound,cen)
        else:
            return OK

    def frame_construct_tri(self,Pts1,Pts2,Edge1,Edge2,cutter,cen):
        framex=[]
        framey=[]
        newfrmx=[]
        newfrmy=[]
        #direction define
        #####cen1=rs.CurveMidPoint(Edge1)
        #####cen2=rs.CurveMidPoint(Edge2)
        basePtVals=rs.CurveCurveIntersection(Edge1,Edge2)
        for basePtVal in basePtVals:
            if basePtVal==None or basePtVal[0]==2:
                print "error in edge intersection"
                return ERROR
        
        #if (rs.VectorAngle(rs.VectorCreate(cen,Pts2[0]),rs.VectorCreate(Pts1[1],Pts1[0]))>270) or (rs.VectorAngle(rs.VectorCreate(Pts1[0],cen2),rs.VectorCreate(Pts1[1],Pts1[0]))<90) :
        #    
        #    stPt1=Pts1[0]
        #    print "L1 proceed"
        #else: 
        #    stPt1=Pts1[len(Pts1)-1]
        #    print "L1 reverse"
        #if (rs.VectorAngle(rs.VectorCreate(Pts2[0],cen1),rs.VectorCreate(Pts2[1],Pts2[0]))<90) or (rs.VectorAngle(rs.VectorCreate(Pts2[0],cen1),rs.VectorCreate(Pts2[1],Pts2[0]))>270):
        #    stPt2=Pts2[0]
        #    print "angle= "  ,rs.VectorAngle(rs.VectorCreate(cen1,Pts2[0]),rs.VectorCreate(Pts2[1],Pts2[0]))
        #    print "L2 proceed"
        #else:
        #    stPt2=Pts2[len(Pts2)-1]
        #    print "L2 reverse"
        #
        newEdge1=rs.CopyObject(Edge1,rs.VectorCreate(Pts2[0],basePtVals[0][1]))
        newEdge2=rs.CopyObject(Edge2,rs.VectorCreate(Pts1[0],basePtVals[0][1]))
        for Pt1 in Pts1:
            framex.append(rs.CopyObject(newEdge2,rs.VectorCreate(Pt1,Pts1[0])))
        for Pt2 in Pts2:
            framey.append(rs.CopyObject(newEdge1,rs.VectorCreate(Pt2,Pts2[0])))
        for elex in framex:
            Int1=rs.CurveCurveIntersection(elex,Edge1)
            Int2=rs.CurveCurveIntersection(elex,cutter)
            #rs.AddPoint(Int1[0][1])
            #rs.AddPoint(Int2[0][1])
            if (Int1 is None) or (Int2 is None):
                print "no intersection"
                return ERROR
            if rs.PointCompare(Int1[0][1],Int2[0][1]):
                print "same point"
            else:
                newfrmx.append(rs.AddLine(Int1[0][1],Int2[0][1]))
        for eley in framey:
            Int1=rs.CurveCurveIntersection(eley,Edge2)
            Int2=rs.CurveCurveIntersection(eley,cutter)
            if (Int1 is None) or (Int2 is None):
                print "no intersection"
                return ERROR
            if rs.PointCompare(Int1[0][1],Int2[0][1]):
                print "same point"
            else:
                newfrmy.append(rs.AddLine(Int1[0][1],Int2[0][1]))
                
        rs.DeleteObjects(framex)
        rs.DeleteObjects(framey)
        rs.DeleteObjects(newEdge1)
        rs.DeleteObjects(newEdge2)
        
        return newfrmx,newfrmy

    




def draw_frame(crvset1,crvset2):
    return OK


    
def normal_confirm():
    return OK

#def 

def main():
    cstFrames=rs.GetObjects("select operating surfaces",rs.filter.surface)
    gap=rs.GetInteger("set the gap between keels",1200)
    
    print "ListLength:" ,len(cstFrames)
    
    
    i=0
    for cstFrame in cstFrames:
        i+=1
        print "surface", i,":",cstFrame
        myFrameTri=tri_fram()
        myFrameTri.frame_div(cstFrame,gap)

    
    
main()