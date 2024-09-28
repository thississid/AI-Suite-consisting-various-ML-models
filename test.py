import math
diff, refereln, asd = map(int,input().split())
asdasda = diff-refereln
if(asdasda<=0 or asdasda >= 0):
    squared_difference = math.sqrt(asdasda*asdasda)
    if(squared_difference<=asd):
        print("Yes")
    else:
        print("No")