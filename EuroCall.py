"""
    In this class the following are calculated:
    The price of a European Call options using the Black-Scholes model.
    The Delta of the option. This represents the change in the price of an option resulting
    The probability of exercising the option In The Money.
"""


import math
import datetime
import numpy as np
from scipy import stats


class EuropeanCall:
    def d1(self, asset_price, strike_price, risk_free_rate, volatility, dt):
        term1 = math.log(asset_price/strike_price)
        term2 = (risk_free_rate + (.5 * (volatility**2))) * dt
        numerator = term1 + term2
        denominator = volatility * (dt**.5)

        return numerator/denominator
        #  return (math.log(asset_price/strike_price) + (risk_free_rate + (volatility**2)/2) * dt)
        #  / (volatility*(dt**.5))

    def d2(self, d1, volatility, dt):
        return d1 - (volatility * math.sqrt(dt))

    def price(self, asset_price, d1, strike_price, d2, risk_free_rate, dt):
        n1 = stats.norm.cdf(d1)
        n2 = stats.norm.cdf(d2)
        discount = math.exp(-risk_free_rate * dt)
        return (asset_price * n1) - (strike_price * discount * n2)

    def delta(self, d1):
        return stats.norm.cdf(d1)

    def exercise_prob(self):
        denominator = self.volatility * self.asset_price * (self.dt**.5)
        term1 = self.strike_price - self.asset_price
        term2 = self.drift * self.asset_price * self.dt
        numerator = term1 - term2
        return 1 - stats.norm.cdf(numerator/denominator)

    def __init__(self, asset_price, strike_price, volatility, expiration_date, risk_free_rate, drift):
        self.asset_price = asset_price
        self.strike_price = strike_price
        self.volatility = volatility
        self.expiration_date = expiration_date
        self.risk_free_rate = risk_free_rate
        self.drift = drift
        #print(expiration_date)

        dt = np.busday_count(datetime.date.today(), expiration_date)/252
        #print(dt)
        d1 = self.d1(asset_price, strike_price, risk_free_rate, volatility, dt)
        d2 = self.d2(d1, volatility, dt)
        self.dt = dt
        self.price = self.price(asset_price, d1, strike_price, d2, risk_free_rate, dt)
        self.delta = self.delta(d1)

