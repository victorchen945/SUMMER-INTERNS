import rhinoscriptsyntax as rs

crvs=[300]
newcrvs=[]



def is_same_crv(crv1,crv2):
    stpt1=rs.CurveStartPoint(crv1)
    endpt1=rs.CurveEndPoint(crv1)
    stpt2=rs.CurveStartPoint(crv2)
    endpt2=rs.CurveEndPoint(crv2)
    if ((stpt1==stpt2) and (endpt1==endpt2)) or ((stpt1==endpt2) and (stpt2==endpt1)):
        return True
    else:
        return False
    
###newcrvs.append(crvs[num])
def main():
    newcrs.append(crvs)
    for i in range(num+1):
        for j in range(i+1,num):
            if (crvs[j])!=-1:
                if (is_same_crv(crvs[i],crvs[j])):
                    crvs[j]=-1
                else:
                    ###newcrv=rs.AddCurve(
                    newcrs.append(crvs[j])
    return newcrs

main()
