# Implied Volatility Calculator

A Python application that calculates implied volatility for options using Black-Scholes and Bachelier pricing models. This solution processes CSV files containing option market data and outputs implied volatilities.

### Command Line Usage

```bash
$ python run_calculator.py
```

This will process `input.csv` and create `output.csv` in the same directory.

### Unit tests
```bash
$ python unit_test.py
test_call_option_price (__main__.TestBachelierModel) ... ok
test_forward_symmetry (__main__.TestBachelierModel) ... ok
test_put_option_price (__main__.TestBachelierModel) ... ok
test_call_option_price (__main__.TestBlackScholesModel) ... ok
test_put_call_parity (__main__.TestBlackScholesModel) ... ok
test_put_option_price (__main__.TestBlackScholesModel) ... ok
test_zero_volatility (__main__.TestBlackScholesModel) ... ok
test_bachelier_implied_vol (__main__.TestImpliedVolatilityCalculator) ... ok
test_black_scholes_implied_vol (__main__.TestImpliedVolatilityCalculator) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.003s

OK
```

