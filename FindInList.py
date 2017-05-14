import numpy as np
import numba

# Was going to use numba, but it seems to be slightly slower with it than without it.
#@numba.autojit
def FindListInList(ListToSearchIn, ListToSearchFor):
    matchIndexList = []
    for bigInd in range(len(ListToSearchIn)-len(ListToSearchFor) + 1):
        curMatch = 1
        for littleInd in range(len(ListToSearchFor)):
            itemMatch = (ListToSearchFor[littleInd] == ListToSearchIn[bigInd + littleInd])
            curMatch = itemMatch & curMatch
        if curMatch:
            matchIndexList.append(bigInd)
    return matchIndexList
