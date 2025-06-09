import unittest
from implied_vol import BSModel, BachelierModel, ImpliedVol
import math

class TestBlackScholesModel(unittest.TestCase):
    """Unit test for Black-Scholes model."""
    
    def setUp(self):
        self.model = BSModel()
    
    def test_call_option_price(self):
        """Test for the call option price lower/upper bounds"""
        S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
        
        price = self.model.calculate_price(S, K, T, r, sigma, 'Call')
        
        # lower/upper bounds
        self.assertGreater(price, max(S - K * math.exp(-r * T),0))
        self.assertLess(price, S)  
    
    def test_put_option_price(self):
        """Test for the put option price lower/upper bounds"""
        S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
        
        price = self.model.calculate_price(S, K, T, r, sigma, 'Put')
        
        # lower/upper bounds
        self.assertGreater(price, max(K * math.exp(-r * T) - S,0))
        self.assertLess(price, K * math.exp(-r * T))  # Put price should be less than strike
    
    def test_put_call_parity(self):
        """Test for the put call parity"""
        S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
        
        call_price = self.model.calculate_price(S, K, T, r, sigma, 'Call')
        put_price = self.model.calculate_price(S, K, T, r, sigma, 'Put')
        
        # Put-call parity: C - P = S - K*e^(-rT)
        expected_diff = S - K * math.exp(-r * T)
        actual_diff = call_price - put_price
        
        self.assertAlmostEqual(actual_diff, expected_diff, places=6)
    
    def test_zero_volatility(self):
        """Test for zero volatility input"""
        S, K, T, r, sigma = 100, 90, 1, 0.05, 0
        
        call_price = self.model.calculate_price(S, K, T, r, sigma, 'Call')
        put_price = self.model.calculate_price(S, K, T, r, sigma, 'Put')
        
        self.assertEqual(call_price, 0.0)
        self.assertEqual(put_price, 0.0)


class TestBachelierModel(unittest.TestCase):
    """Unit test for Bachelier model."""
    
    def setUp(self):
        self.model = BachelierModel()
    
    def test_call_option_price(self):
        """Test for the call option price lower bounds"""
        S, K, T, r, sigma = 100, 100, 1, 0.05, 20
        
        price = self.model.calculate_price(S, K, T, r, sigma, 'Call')
        
        # lower bound
        self.assertGreater(price, max(S - K * math.exp(-r * T),0))
    
    def test_put_option_price(self):
        """Test for the put option price lower bounds"""
        S, K, T, r, sigma = 100, 100, 1, 0.05, 20
        
        price = self.model.calculate_price(S, K, T, r, sigma, 'Put')
        
        # lower bound
        self.assertGreater(price, max(K * math.exp(-r * T) - S,0))
    
    def test_forward_symmetry(self):
        """Test for the forward symmetry"""
        S, K, T, r, sigma = 100, 110, 1, 0, 20
        
        call_price = self.model.calculate_price(S, K, T, r, sigma, 'Call')
        put_price = self.model.calculate_price(K, S, T, r, sigma, 'Put')
        
        # Due to symmetry in normal distribution
        self.assertAlmostEqual(call_price, put_price, places=6)


class TestImpliedVolatilityCalculator(unittest.TestCase):
    """Unit tests for implied volatility calculator."""
    
    def setUp(self):
        self.calculator = None
    
    def test_black_scholes_implied_vol(self):
        """Test for the BS implied vol"""
        S, K, T, r, true_sigma = 100, 100, 1, 0.05, 0.2
        
        # Calculate theoretical price
        bs_model = BSModel()
        market_price = bs_model.calculate_price(S, K, T, r, true_sigma, 'Call')
        
        # Calculate implied volatility
        self.calculator = ImpliedVol(S, K, T, r, market_price, 'Call', 'BlackScholes')
        implied_vol = self.calculator.calculate_implied_vol()
        
        # Should recover the original volatility
        self.assertAlmostEqual(implied_vol, true_sigma, places=6)
    
    def test_bachelier_implied_vol(self):
        """Test for the Bachelier implied vol"""
        S, K, T, r, true_sigma = 100, 100, 1, 0.05, 20
        
        # Calculate theoretical price
        bachelier_model = BachelierModel()
        market_price = bachelier_model.calculate_price(S, K, T, r, true_sigma, 'Call')
        
        # Calculate implied volatility
        self.calculator = ImpliedVol(S, K, T, r, market_price, 'Call', 'Bachelier')
        implied_vol = self.calculator.calculate_implied_vol()
        
        # Should recover the original volatility
        self.assertAlmostEqual(implied_vol, true_sigma, places=6)

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)