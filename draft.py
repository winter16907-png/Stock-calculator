import math as m

from sympy import lowergamma


# 美股交易部分(每一筆訂單)
def buy_stock(buyprice,quantity):
    commission_b = max(0.049 * quantity, 0.99)
    platform_b = max(0.005 * quantity, 1)
    delivery_b = 0.003 * quantity
    nms_b = 0.000003 * quantity
    fee_involved_b = commission_b + platform_b + delivery_b + nms_b
    return fee_involved_b

def sell_stock(sellprice,quantity):
    commission_s = max(0.049 * quantity, 0.99)
    platform_s = max(0.005 * quantity, 1)
    delivery_s = 0.003 * quantity
    sec_s = max(0.0000206 * sellprice, 0.01)
    transaction_s = min(max(0.000195 * quantity, 0.01), 9.79)
    nms_s = 0.000003 * quantity
    fee_involved_s = commission_s + platform_s + delivery_s + sec_s + transaction_s + nms_s
    return fee_involved_s

def binary_simulation(buyprice,quantity):
    lower_sellprice = buyprice
    higher_sellprice = buyprice * 8
    accuracy = 0.001

    buy_fee = buy_stock(buyprice,quantity)

    while (higher_sellprice - lower_sellprice) > accuracy:
        simulated_sellprice = (lower_sellprice + higher_sellprice) / 2

        fee_involved = buy_fee + sell_stock(simulated_sellprice, quantity)

        # 保本價： 總收入 (sell * qty) - 總支出 (buy * qty + fee_involved)
        net_profit = (simulated_sellprice * quantity) - (buyprice * quantity) - fee_involved

        if net_profit > 0:
            # 賺錢了，代表模擬賣價設太高，往左半邊找
            higher_sellprice = simulated_sellprice
        else:
            # 賠錢了，代表模擬賣價設太低，往右半邊找
            lower_sellprice = simulated_sellprice

    else:
        return (lower_sellprice + higher_sellprice) / 2
