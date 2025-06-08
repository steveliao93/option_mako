import math
from scipy.stats import norm
from abc import ABC, abstractmethod

class PricingModel(ABC):
    @abstractmethod
    def calculate_price(self, S: float, K: float, T: float, r: float, 
                       sigma: float, option_type: str) -> float:
        """ 
        Input:
            S: Spot price
            K: Strike price
            T: Time to maturity
            r: Risk-free rate
            sigma: Volatility
            option_type: 'Call' or 'Put'
        
        Output:
            Option price
        """
        pass

class BSModel(PricingModel):
    def calculate_price(self, S: float, K: float, T: float, r: float, 
                       sigma: float, option_type: str) -> float:
        """
        Calculate Black-Scholes option price.
        """
        if T <= 0 or sigma <= 0:
            return 0.0
        
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        if option_type == "Call":
            price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return max(price, 0.0)
    
class BachelierModel(PricingModel):
    def calculate_price(self, S: float, K: float, T: float, r: float, sigma: float, option_type: str) -> float:
        """
        Calculate Bachelier option price.
        """
        if T <= 0 or sigma <= 0:
            return 0.0
        
        F = S * math.exp(r * T)

        d_denominator = math.sqrt(sigma ** 2 * (math.exp(2 * r * T) - 1) / (2 * r))

        d = (F - K) / d_denominator

        if option_type == "Call":
            price = math.exp(-r * T) * ((F - K) * norm.cdf(d) + d_denominator * norm.pdf(d))
        else:
            price = math.exp(-r * T) * ((K - F) * norm.cdf(-d) + d_denominator * norm.pdf(d))
        
        return max(price, 0.0)
    

class ImpliedVol:
    def __init__(self, S: float, K: float, T: float, r: float, market_price: float, option_type: str, model_type: str):
        self.model_type = model_type
        self.models = {'BlackScholes': BSModel(), 'Bachelier': BachelierModel()}
        self.model = self.models[model_type]
        self.tolerance = 1e-8
        self.max_interation = 100

        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.market_price = market_price
        self.option_type = option_type

    def calculate_implied_vol(self, ) -> float:

        # invalid inputs
        if self.T <= 0 or self.S <= 0 or self.K <= 0 or self.market_price < 0:
            return float('nan')

        sigma = 0.2 if self.model_type == 'BlackScholes' else 20 # initial guess of sigma

        # Newton's method
        for _ in range(self.max_interation):
            price = self.model.calculate_price(self.S, self.K, self.T, self.r, sigma, self.option_type)
            vega = self.calculate_vega(sigma)

            if abs(vega) < 1e-10:
                break

            price_diff = price - self.market_price

            if abs(price_diff) < self.tolerance:
                return sigma
            
            sigma_updated = sigma - price_diff/vega

            if sigma_updated <= 0:
                sigma = sigma / 2
            else:
                sigma = sigma_updated
        return float('nan') # fail to converge


    def calculate_vega(self, sigma) -> float:
        h = 1e-4 
        price_up = self.model.calculate_price(self.S, self.K, self.T, self.r, sigma + h, self.option_type)
        price_down = self.model.calculate_price(self.S, self.K, self.T, self.r, sigma - h, self.option_type)
        
        vega = (price_up - price_down) / (2 * h)
        return vega
