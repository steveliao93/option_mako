import pandas as pd
import math

import implied_vol

class RunCalculator:
    def process(self, input_file):

        df = pd.read_csv(input_file)

        df['Years To Expiry'] = df['Days To Expiry'] / 365.0

        df['Implied Volatility'] = df.apply(self.calculate_row_iv, axis = 1)

        df['Spot'] = df['Underlying']

        columns_tosave = ['ID', 'Spot', 'Strike', 'Risk-Free Rate', 'Years To Expiry', 'Option Type', 'Model Type', 'Implied Volatility', 'Market Price']

        df.to_csv('output.csv', columns = columns_tosave, index=False, float_format='%.10g')

    def calculate_row_iv(self, row: pd.Series) -> float:
        """
        Calculate implied volatility for a single row.
        """
        calculator = implied_vol.ImpliedVol(
            S=row['Underlying'],
            K=row['Strike'],
            T=row['Years To Expiry'],
            r=row['Risk-Free Rate'],
            market_price=row['Market Price'],
            option_type=row['Option Type'],
            model_type=row['Model Type'])
        
        return calculator.calculate_implied_vol()
        
if __name__ == "__main__":
    runner = RunCalculator()
    runner.process("input.csv")
