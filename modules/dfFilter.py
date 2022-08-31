def dfFiltering(df, filterMap):
    evs0 = df.shape[0]
    
    for iVar in filterMap:
        if iVar in df.columns:
            lowTrue = [ls[1][0] for ls in filterMap[iVar] if ls[0]==True]
            lowFalse = [ls[1][0] for ls in filterMap[iVar] if ls[0]==False]
            upTrue = [ls[1][1] for ls in filterMap[iVar] if ls[0]==True]
            upFalse = [ls[1][1] for ls in filterMap[iVar] if ls[0]==False]
            bTrue = False
            for i in range(len(lowTrue)):
                print("keeping %s in (%f, %f)" % (iVar, lowTrue[i], upTrue[i]))
                bTrue = bTrue | ((df[iVar] >= lowTrue[i]) & (df[iVar] <= upTrue[i]))
            bFalse = True
            for i in range(len(lowFalse)):
                print("keeping %s out of (%f, %f)" % (iVar, lowFalse[i], upFalse[i]))
                bTrue = bTrue & ((df[iVar] < lowFalse[i]) | (df[iVar] > upFalse[i]))
            df = df[bTrue & bFalse]
        else:
            print("%s is in filterMap but not in df --> ignored" % iVar)
            
    evs1 = df.shape[0]
            
    if len(filterMap)==0:
        print("no filters applied")
    else:
        print("filters applied: events = %d --> %d" % (evs0, evs1))
        
    return df