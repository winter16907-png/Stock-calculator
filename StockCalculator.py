import math as m
import os
import requests
import base64
import sympy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from calculator import *

phi = (1 + m.sqrt(5))/2 #黃金比例
tem = "abc"


def toolbox():
    print("""
a.Calculate the break even price
b.Monte Carlo method
""")
    request = input("input the corresponding tool: ")
    if "a" in request:
        return "a"
    elif "b" in request:
        return "b"
    elif "q" in request:
        return "q"


class StockCalculator:
    def __init__(self, stock_market:str, input1, input2, input3, input4, input5):
        self.stock_market = stock_market
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3
        self.input4 = input4
        self.input5 = input5

    def find_break_even_price(self):
        #input1=buy price, input2=quantity
        accuracy = 0.001
        if self.stock_market == "HK":
            transaction_buy = self.input1 * self.input2
            platform_usage_fee = 15
            stamp_duty_buy = m.ceil(transaction_buy * 0.001)
            hkex_buy = transaction_buy * 0.0000565
            sfc_buy = transaction_buy * 0.000027
            afrc_buy = transaction_buy * 0.0000015
            ccass_buy = max(transaction_buy * 0.000042,2)
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

    def montecarlo(self):
        S0 = self.input1
        mu = self.input2
        sigma = self.input3
        T = self.input4
        N = 252
        n_sim = self.input5

        dt = T / N      # Time step size

        stock_prices = np.zeros((N + 1, n_sim))
        stock_prices[0] = S0

        # Generate random variables from standard normal distribution
        # Size: (Number of days, Number of simulations)
        Z = np.random.standard_normal((N, n_sim))

        # Simulate price paths day by day
        for t in range(1, N + 1):
            # GBM formula: S_t = S_{t-1} * exp( (mu - 0.5*sigma^2)*dt + sigma*Z*sqrt(dt) )
            drift = (mu - 0.5 * sigma**2) * dt
            shock = sigma * Z[t - 1] * np.sqrt(dt)
            stock_prices[t] = stock_prices[t - 1] * np.exp(drift + shock)


        fig, ax = plt.subplots(1, 2, figsize=(15, 6))

        # Plot 1: Simulated Price Paths (Show first 100 paths for clarity)
        ax[0].plot(stock_prices[:, :100], linewidth=1)
        ax[0].set_title("Monte Carlo Simulation: Price Paths (First 100 Paths)")
        ax[0].set_xlabel("Time Steps (Days)")
        ax[0].set_ylabel("Stock Price")
        ax[0].grid(True, linestyle="--", alpha=0.6)

        # Plot 2: Histogram of Terminal Stock Prices (Ending Day Distribution)
        terminal_prices = stock_prices[-1, :]
        ax[1].hist(terminal_prices, bins=50, edgecolor='black', alpha=0.7, density=True)
        ax[1].set_title(f"Distribution of Terminal Prices at T = {T} Year")
        ax[1].set_xlabel("Stock Price")
        ax[1].set_ylabel("Density")
        ax[1].grid(True, linestyle="--", alpha=0.6)

        # Add key statistics summary onto the histogram plot
        mean_price = np.mean(terminal_prices)
        median_price = np.median(terminal_prices)
        pct_5 = np.percentile(terminal_prices, 5)
        pct_95 = np.percentile(terminal_prices, 95)

        stats_text = (
            f"Initial Price: {S0}\n"
            f"Mean: {mean_price:.2f}\n"
            f"Median: {median_price:.2f}\n"
            f"5th Pctl: {pct_5:.2f}\n"
            f"95th Pctl: {pct_95:.2f}"
        )
        ax[1].text(0.65, 0.7, stats_text, transform=ax[1].transAxes,
                   bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

        plt.tight_layout()
        plt.show()

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

    elif tool == "b":
        info = []
        info.append(info1 := float(input("Please input the current stock price: ")))
        info.append(info2 := float(input("Please input the average target price of the stock: ")))
        info[1] = change(info1,info2)
        info.append(info3 := float(input("Please input the HV or IV of the stock: ")))
        info.append(info4 := float(input("Please input the year of the simulation: ")))
        info.append(info5 := int(input("Please input the number of the simulation paths: ")))

        simulate = StockCalculator(None, info[0], info[1], info[2], info[3], info[4])
        simulate.montecarlo()



if __name__ == "__main__":
    while True:
        try:
            main()
        except ValueError:
            continue