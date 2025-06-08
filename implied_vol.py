import math
from scipy.stats import norm
from abc import ABC, abstractmethod

class PricingModel(ABC):
    @abstractmethod
    def calculate_price(self, S: float, K: float, T: float, r: float, 
                       sigma: float, option_type: str) -> float:
        pass

class BSModel(PricingModel):
    def calculate_price(self, S: float, K: float, T: float, r: float, 
                       sigma: float, option_type: str) -> float:
        """
        Calculate Black-Scholes option price.
        
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