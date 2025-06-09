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

        d_denominator = math.sqrt(sigma ** 2 * (math.exp(2 * r * T) - 1) / (2 * r)) if r != 0 else sigma * math.sqrt(T)

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
        """
        Calculate implied volatility

        The main algorithm is Newton's method, and the fallback is Bisection method
        """

        # check if the input is valid
        if not self.input_validation():
            return float('nan')

        sigma = 0.2 if self.model_type == 'BlackScholes' else 0.2 * self.S # initial guess of sigma

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

        # If Newton fails to converge, try Bisection method
        sigma_min = 1e-6      # Minimum volatility (near zero)
        sigma_max_bs = 5.0    # Maximum volatility for Black-Scholes
        sigma_max_bach = 5.0 * self.S  # Maximum volatility for Bachelier
        sigma_low = sigma_min
        sigma_high = sigma_max_bs if self.model_type == 'BlackScholes' else sigma_max_bach

        for iteration in range(self.max_interation):
            sigma_mid = (sigma_low + sigma_high) / 2.0
            
            price_mid = self.model.calculate_price(self.S, self.K, self.T, self.r, sigma_mid, self.option_type)
            diff_mid = price_mid - self.market_price
            
            # Check convergence
            if abs(diff_mid) < self.tolerance:
                return sigma_mid
            
            # Check if interval is too small
            if abs(sigma_high - sigma_low) < self.tolerance:
                return sigma_mid
            
            # Update bounds
            if diff_mid < 0:  # Price too low, need higher volatility
                sigma_low = sigma_mid
            else:  # Price too high, need lower volatility
                sigma_high = sigma_mid
        return float('nan')


    def calculate_vega(self, sigma) -> float:
        """
        Calculate the first derivative w.r.t. the volatility
        """
        h = 1e-4 
        price_up = self.model.calculate_price(self.S, self.K, self.T, self.r, sigma + h, self.option_type)
        price_down = self.model.calculate_price(self.S, self.K, self.T, self.r, sigma - h, self.option_type)
        
        vega = (price_up - price_down) / (2 * h)
        return vega
    
    def input_validation(self,) -> bool:
        """
        Validate the input, including the lower/upper bounds check for market price
        """
        # invalid inputs
        if self.T <= 0 or self.S <= 0 or self.K <= 0 or self.market_price < 0:
            return False
        
        # invalid option price violates the bounds
        if self.model_type == 'BlackScholes':
            if self.option_type == 'Call' and (self.market_price > self.S or self.market_price < self.S - self.K * math.exp(-self.r * self.T)):
                return False
            elif self.option_type == 'Put' and (self.market_price > self.K * math.exp(-self.r * self.T) or self.market_price < self.K * math.exp(-self.r * self.T) - self.S):
                return False
        else:
            if self.option_type == 'Call' and self.market_price < self.S - self.K * math.exp(-self.r * self.T):
                return False
            elif self.option_type == 'Put' and self.market_price < self.K * math.exp(-self.r * self.T) - self.S:
                return False
        
        return True
