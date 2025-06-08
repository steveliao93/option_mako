import implied_vol
import math

def test_pricing_models():
    S = 0.2817    # Spot price
    K = 0.3065   # Strike price
    T = 0.093758     # Time to maturity
    r = -0.0027     # Risk-free rate
    sigma_bs = 0.2    # Vol for BS
    sigma_bach = 0.2 * S   # Vol for Bachelier
    
    # Black-Scholes model
    bs_model = implied_vol.BSModel()
    bs_call = bs_model.calculate_price(S, K, T, r, sigma_bs, 'Call')
    bs_put = bs_model.calculate_price(S, K, T, r, sigma_bs, 'Put')    
    print(f"BS Call Price: {bs_call:.6f}")
    print(f"BSPut Price:  {bs_put:.6f}")
    
    # Verify put-call parity
    parity_check = bs_call - bs_put - (S - K * math.exp(-r * T))
    print(f"BS Put-Call Parity Check: {parity_check:.10f}")

    # Bachelier model
    bach_model = implied_vol.BachelierModel()
    bach_call = bach_model.calculate_price(S, K, T, r, sigma_bach, 'Call')
    bach_put = bach_model.calculate_price(S, K, T, r, sigma_bach, 'Put')
                                                    
    print(f"Bachelier Call Price: {bach_call:.6f}")
    print(f"Bachelier Put Price:  {bach_put:.6f}")

    # Verify put-call parity
    parity_check = bach_call - bach_put - (S - K * math.exp(-r * T))
    print(f"Bachelier Put-Call Parity Check: {parity_check:.10f}")

def test_implied_vol():
    
    
    # BS
    S, K, T, r = 1.4840, 1.5856, 0.081119, -0.0015
    market_price = 1.744341

    calculator_bs = implied_vol.ImpliedVol(S, K, T, r, market_price, 'Put', 'BlackScholes')

    implied_vol_bs = calculator_bs.calculate_implied_vol()
    
    print(f"\nBlack-Scholes Example:")
    print(f"Market Price: {market_price}")
    print(f"Implied Volatility: {implied_vol_bs:.6f}")
    
    # Verify by recalculating price
    if not math.isnan(implied_vol_bs):
        bs_model = implied_vol.BSModel()
        recalc_price = bs_model.calculate_price(S, K, T, r, implied_vol_bs, 'Put')
        print(f"Recalculated Price: {recalc_price:.6f}")
        print(f"Price Difference: {abs(recalc_price - market_price):.8f}")
    
    # Bachelier
    S, K, T, r = 1.4840, 1.5856, 0.081119, -0.0015
    market_price = 1.744341

    calculator_bach = implied_vol.ImpliedVol(S, K, T, r, market_price, 'Put', 'Bachelier')
    
    implied_vol_bach = calculator_bach.calculate_implied_vol()
    
    print(f"\nBachelier Example:")
    print(f"Market Price: {market_price}")
    print(f"Implied Volatility: {implied_vol_bach:.6f}")

    if not math.isnan(implied_vol_bach):
        bach_model = implied_vol.BachelierModel()
        recalc_price = bach_model.calculate_price(S, K, T, r, implied_vol_bach, 'Put')
        print(f"Recalculated Price: {recalc_price:.6f}")
        print(f"Price Difference: {abs(recalc_price - market_price):.8f}")


if __name__ == "__main__":
    test_pricing_models()
    test_implied_vol()