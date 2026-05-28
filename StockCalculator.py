import math as m
import os
import requests
import base64
import sympy as sp
import numpy as np
from calculator import *

phi = (1 + m.sqrt(5))/2 #黃金比例
tem = "abc"


def toolbox():
    print("""
a.Calculate the break even price
""")
    request = input("input the corresponding tool: ")
    if "a" in request:
        return "a"


class StockCalculator:
    def __init__(self, stock_market:str, input1, input2, input3, input4):
        self.stock_market = stock_market
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3
        self.input4 = input4

    def find_break_even_price(self):
        #input1=buy price, input2=quantity
        if self.stock_market == "HK":
            transaction_buy = self.input1 * self.input2
            platform_usage_fee = 15
            stamp_duty_buy = m.ceil(transaction_buy * 0.001)
            hkex_buy = transaction_buy * 0.0000565
            sfc_buy = transaction_buy * 0.000027
            afrc_buy = transaction_buy * 0.0000015
            ccass_buy = transaction_buy * 0.000042
            while_buy = platform_usage_fee + stamp_duty_buy + hkex_buy + sfc_buy + afrc_buy + ccass_buy
            buy_total = transaction_buy + while_buy

            def calculate_net_proceeds(simulated_sell_price):
                # 計算模擬價格賣出時的淨收入
                sell_amount = simulated_sell_price * self.input2
                # 賣出手續費
                stamp_duty_sell = m.ceil(sell_amount * 0.001)
                hkex_sell = sell_amount * 0.0000565
                sfc_sell = sell_amount * 0.000027
                afrc_sell = sell_amount * 0.0000015
                ccass_sell = sell_amount * 0.000042
                total_fees_sell = platform_usage_fee + stamp_duty_sell + hkex_sell + sfc_sell + afrc_sell + ccass_sell
                net_proceeds = sell_amount - total_fees_sell

                return net_proceeds

            lowest_sell_price = max(self.input1 * 0.01, 0.001)  # 最低跌到1%
            highest_sell_price = self.input1 * 10.0  # 最高漲到10倍

            def binary_find_break_even_price(lowest_sell_price, highest_sell_price):
                accuracy = 0.001

                for _ in range(100):
                    simulated_sell_price = (lowest_sell_price + highest_sell_price) / 2
                    net = calculate_net_proceeds(simulated_sell_price)
                    diff = net - buy_total

                    if abs(diff) < accuracy:
                        return simulated_sell_price
                    elif diff > 0:
                        highest_sell_price = simulated_sell_price
                    elif diff < 0:
                        lowest_sell_price = simulated_sell_price

            break_even_price = binary_find_break_even_price(lowest_sell_price, highest_sell_price)
            break_even_price = rounding(break_even_price,4)
            return f"The break even price is ${break_even_price} (HKD)"

        elif self.stock_market == "US":
            buyprice = self.input1
            quantity = self.input2
            # 美股交易部分(每一筆訂單)
            def buy_stock(buyprice, quantity):
                commission_b = max(0.049 * quantity, 0.99)
                platform_b = max(0.005 * quantity, 1)
                delivery_b = 0.003 * quantity
                nms_b = 0.000003 * quantity
                fee_involved_b = commission_b + platform_b + delivery_b + nms_b
                return fee_involved_b

            def sell_stock(sellprice, quantity):
                commission_s = max(0.049 * quantity, 0.99)
                platform_s = max(0.005 * quantity, 1)
                delivery_s = 0.003 * quantity
                sec_s = max(0.0000206 * sellprice * quantity, 0.01)
                transaction_s = min(max(0.000195 * quantity, 0.01), 9.79)
                nms_s = 0.000003 * quantity
                fee_involved_s = commission_s + platform_s + delivery_s + sec_s + transaction_s + nms_s
                return fee_involved_s

            def binary_simulation(buyprice, quantity):
                lower_sellprice = buyprice
                higher_sellprice = buyprice * 2
                buy_fee = buy_stock(buyprice, quantity)
                while ((higher_sellprice * quantity) - (buyprice * quantity) - (buy_fee + sell_stock(higher_sellprice, quantity))) < 0:
                    higher_sellprice *= 2
                accuracy = 0.001



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

                return f"The break even price is ${rounding((lower_sellprice + higher_sellprice) / 2,4)} (USD)"
        return binary_simulation(buyprice, quantity)

def main():
    tool = toolbox()

    if tool == "a":
        currency = input("Input the currency will be used: ")
        currency = currency.upper()
        if "HK" in currency:
            region = "HK"
        elif "US" in currency:
            region = "US"

        info = []
        info.append(info1 := float(input("Please input the buy price of the stock: ")))
        info.append(info2 := float(input("Please input the quantity of the stock: ")))

        stock = StockCalculator(region, info[0], info[1], None, None)
        print(stock.find_break_even_price())


if __name__ == "__main__":
    while True:
        try:
            main()
        except ValueError:
            continue