import rhinoscriptsyntax as rs

divPts = rs.DivideCurve (crv,divCount)
newPts=[]
newCrvs=[]
rs.point
for i in range(gens):
    for divPt in divPts:
        t=rs.CurveClosestPoint(crv,divPt)
        curvatureData=rs.CurveCurvature(crv,t)
        curvatureVec=curvatureData[4]
        curvatureVec=rs.VectorScale(curvatureVec,scaleFactor)
        length=rs.VectorLength(curvatureVec)
        if length>max:
            curvatureVec=rs.VectorUnitize(curvatureVec)
            curvatureVec=rs.VectorScale(curvatureVec,max)
        newPt=rs.PointAdd(divPt,curvatureVec)
        #print curvatureVec
        newPts.append(newPt)
    newCrv=rs.AddInterpCurve(newPts)
    newCrvs.append(newCrv)
    crv=newCrv

#curve check:
#for i in range(gens)
checkCrv=newCrvs[checkitem-1]
checkPts=[]
i=divCount*(checkitem-2)
while i<divCount*(checkitem-1):
    checkPts=newPts[i]
    