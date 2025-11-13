import math
import numpy as np
from integralImage import LocalSum

def to_abs(i, j, columns, rows):
    return int(round(i + rows)), int(round(j + columns))

def DetectEye(I, n):
    H, W = I.shape
    m = int(round(0.15 * n))
    P = {
        'P1': (-0.5*n, -0.5*m), 
        'P2': (-0.05*n, 0), 
        'P3': (-0.5*n, 0), 
        'P4': (-0.05*n, 0.5*m), 
        'P5': ( 0.05*n, -0.5*m), 
        'P6': ( 0.5*n, 0), 
        'P7': ( 0.05*n, 0),
        'P8': ( 0.5*n, 0.5*m),
        'P9': (-0.325*n, 0.833*m),
        'P10': (-0.225*n, 2*m), 
        'P11': (-0.1*n, 0.833*m), 
        'P12': ( 0.1*n, 2*m), 
        'P13': ( 0.225*n, 0.833*m),
        'P14': ( 0.325*n, 2*m),
    }
    # margins from kernel extremes (no magic numbers)
    # xs = [x for x,_ in P.values()]
    # ys = [y for _,y in P.values()]
    # margin_top    = int(round(abs(min(ys))))  # 0.5*m
    # margin_bottom = int(round(abs(max(ys))))  # 2.0*m
    # margin_left   = int(round(abs(min(xs))))  # 0.5*n
    # margin_right  = int(round(abs(max(xs))))  # 0.5*n
    margin_top    = round(0.5 * m)
    margin_bottom = round(2.0 * m)
    margin_left   = margin_right = round(0.5 * n)
    best_score, best_pos = -1e18, (0, 0)
    for i in range(margin_top, H - margin_bottom):
        for j in range(margin_left, W - margin_right):
            def rs(a,b):
                row1, col1 = to_abs(i, j, *P[a]); 
                row2, col2 = to_abs(i, j, *P[b])
                top, bottom = sorted([row1, row2]); 
                left, right = sorted([col1, col2])
                return LocalSum(I, top, left, bottom, right)


            LS1 = rs('P1','P2');  LS2 = rs('P5','P6')
            LS3 = rs('P3','P4');  LS4 = rs('P7','P8')
            LS5 = rs('P9','P10'); LS6 = rs('P11','P12'); LS7 = rs('P13','P14')
            score = (LS1 + LS2 + LS6) - (LS3 + LS4 + LS5 + LS7)
            if score > best_score:
                best_score, best_pos = score, (i, j)
    return best_pos

def ExtractDetectedEye(img_gray, center_rc, n):
    i, j = center_rc
    m = int(round(0.15 * n))
    top    = int(round(i - 0.5*m))
    bottom = int(round(i + 2.0*m))
    left   = int(round(j - 0.5*n))
    right  = int(round(j + 0.5*n))
    H, W = img_gray.shape
    top = max(0, top)
    left = max(0, left)
    bottom = min(H, bottom)
    right = min(W, right)
    out = np.zeros_like(img_gray)
    out[top:bottom+1, left:right+1] = img_gray[top:bottom+1, left:right+1]
    return out, (top, left, bottom, right)
