from time import sleep
from random import uniform, random, randint
import matplotlib.pyplot as plt

BANKRUPCY_CHANCE = 0.01
GREED_FACTOR = 2
MIN_PRICE = 20
LOTTERY_RATE = 0.05
PRICE_FLUCT = 0.05

class Seller:
    def __init__(self, s_price, adj_rate, sold) -> None:
        self.s_price = s_price
        self.adj_rate = adj_rate
        self.sold = sold
        self.amount = 1
        self.min_price = MIN_PRICE

class Buyer:
    def __init__(self, b_price, adj_rate, budget, bought) -> None:
        self.b_price = b_price
        self.adj_rate = adj_rate
        self.budget = budget
        self.bought = bought
        self.greed_val = uniform(0,GREED_FACTOR)
        self.bankrupcy_chance = BANKRUPCY_CHANCE




if __name__ == '__main__':
    m, n = 30, 400
    Sellers = [Seller(uniform(50, 140), 0.3, False) for _ in range(m)]
    Buyers = [Buyer(uniform(30, 60), 0.15, 100, False) for _ in range(n)]

    # Initialize lists to store data for plotting
    transactions = []
    average_prices = []
    average_demands = []
    # Create the initial plot
    fig, ax = plt.subplots()
    line_transactions, = ax.plot(transactions, label='Transactions')
    line_avg_prices, = ax.plot(average_prices, label='Average Price')
    line_avg_demands, = ax.plot(average_demands, label='Average Demand')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Value')
    ax.legend()

    while(1):

        i = 1
        for b, buyer in enumerate(Buyers):
            if buyer.bought: break
            for s, seller in enumerate(Sellers):
                if seller.sold: break
                if(seller.s_price <= buyer.b_price):
                    rand = random()
                    if buyer.greed_val * seller.s_price < buyer.budget and rand > 0.5:
                        buyer.bought = True
                        seller.amount -= 1
                        if seller.amount == 0: seller.sold = True
                        i+=1
                    
        s_sum, b_sum = 0, 0
        for seller in Sellers:
            if seller.sold:
                seller.sold = False
                seller.amount = 1
                seller.s_price *= (1 + seller.adj_rate)
            else:
                seller.s_price *= (1 - seller.adj_rate)
                if seller.s_price < MIN_PRICE: seller.s_price = MIN_PRICE
            if random() > 0.1: seller.s_price *= (1-PRICE_FLUCT)
            elif random() > 0.1: seller.s_price *= (1+PRICE_FLUCT)
            s_sum += seller.s_price
    
        for buyer in Buyers:
            b_sum += buyer.b_price
            if buyer.bought:
                buyer.b_price *= (1 - buyer.adj_rate)
                buyer.bought = False
                buyer.greed_val *= uniform(0,GREED_FACTOR)
                if random() > buyer.bankrupcy_chance:
                    buyer.b_price //= 10
                if random() > LOTTERY_RATE:
                    buyer.budget += 40
                    buyer.b_price *= 1.2
            else:
                buyer.b_price *= (1 + buyer.adj_rate)
                if buyer.budget < buyer.b_price: buyer.b_price = buyer.budget
                buyer.greed_val //= uniform(0,GREED_FACTOR)


        transactions.append(i)
        average_prices.append(s_sum / m)
        average_demands.append(b_sum / n)
        # Update the plot with the new values
        line_transactions.set_data(range(len(transactions)), transactions)
        line_avg_prices.set_data(range(len(average_prices)), average_prices)
        line_avg_demands.set_data(range(len(average_demands)), average_demands)
        # Adjust the plot limits if needed
        ax.relim()
        ax.autoscale_view()
        # Redraw the plot
        plt.draw()
        plt.pause(0.001)

        # sleep(0.01)

    