# Implied Volatility Calculator

A Python application that calculates implied volatility for options using Black-Scholes and Bachelier pricing models. This solution processes CSV files containing option market data and outputs implied volatilities.

### Project Files
```
option_mako/
├── implied_vol.py           # Main implementation
├── unit_test.py             # Unit tests
├── run_calculator.py        # Main processor
├── README.md                # Documentation
├── input.csv                # Input data file
└── output.csv               # Generated output (after running)
```

### Command Line Usage

```bash
$ python run_calculator.py
```

This will process `input.csv` and create `output.csv` in the same directory.

### Unit Tests
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

### Example Output
```
ID,Spot,Strike,Risk-Free Rate,Years To Expiry,Option Type,Model Type,Implied Volatility,Market Price
0,1.9119,2.0264,-0.0009,0.05304082192,Call,Bachelier,1.597868342,0.096576518
1,0.8731,1.061,-0.0025,0.7623843836,Call,Bachelier,1.413315525,0.40362827
2,1.2286,1.3582,-0.0048,0.5319065753,Put,BlackScholes,0.8660063945,0.39162934
3,1.8405,2.1037,-0.002,0.4444334247,Put,BlackScholes,1.267567612,0.78609423
4,1.7372,1.9397,-0.001,0.7343484932,Call,Bachelier,0.8152012729,0.1886192
5,0.2817,0.3065,-0.0027,0.09375753425,Put,BlackScholes,,0.33722994
```

