import math as m
import numpy as np
import sympy as sp
from decimal import *
import scipy as scp

# "*"說明這是variable(s)
#二項分佈scp.stats.binom.cdf/pmf/sf(</=/>)(*r,*n,*π)
#柏松分佈scp.stats.poisson.cdf/pmf/sf(</=/>)(*x, mu=*lambda)
#正態分佈scp.stats.norm.cdf[ppf]/pdf/sf[isf](</=/>)(*x/*ans,loc=*mu,scale=*sigma)，Z-value尋找雙尾測試右側邊界scp.norm.ppf(1 - *⍺/2)
#t-value(有df和⍺)scp.stats.t.ppf(1 - *⍺/2, *df)
#數據組z-score用別的方法scp.stats.zscore(*data)
#t-score會輸出t-value和p-value(小心數據溢出)(需要數據組和̅x)scp.stats.ttest_1samp(*data, *̅x)


def rounding(x, ndigits=0):
    # 用 str(x) 避免誤差，Decimal是十進制的意思
    d = Decimal(str(x))
    exponent = Decimal(f"1e-{ndigits}") if ndigits > 0 else Decimal('1')
    return float(d.quantize(exponent, rounding=ROUND_HALF_UP))

def percentage_change(from_a, to_b):
    x = ((to_b - from_a) / from_a) * 100
    return (f"Net change: {x} %")

def x_2(a=0, b=0, c=0):
    x = sp.symbols("x")
    if b**2 - 4*a*c != 0:
        ans1, ans2 = sp.solve(a * x**2 + b * x + c)
        return [
            f'{ans1} ≈≈ "{ans1.evalf(3)}"',
            f'{ans2} ≈≈ "{ans2.evalf(3)}"'
        ]
    else:
        ans = sp.solve(a * x**2 + b * x + c)
        ans = ans[0]
        return f'{ans} ≈≈ "{ans.evalf(3)}"'

def xy_1(a,b,c,d,e,f):
    A = np.array([[a,b],[d,e]])
    B = np.array([c,f])
    x = np.linalg.solve(A, B)
    return x


if __name__ == "__main__":
    a = 10000 * 1.05**40
    print(a)
