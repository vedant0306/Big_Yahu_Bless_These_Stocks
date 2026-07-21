# tests/test_strategy.py
import pandas as pd
from src.strategy import MovingAverageCrossover

def test_moving_average_crossover_buy_signal():
    strategy = MovingAverageCrossover(fast_window=2, slow_window=3)
    
    # Create sample prices where fast MA crosses above slow MA
    data = {'close': [10.0, 10.0, 10.0, 15.0]}
    df = pd.DataFrame(data)
    
    signal = strategy.generate_signal(df)
    assert signal == "BUY"

def test_moving_average_crossover_hold_signal():
    strategy = MovingAverageCrossover(fast_window=2, slow_window=3)
    
    # Not enough data points to compute MAs
    data = {'close': [10.0, 10.0]}
    df = pd.DataFrame(data)
    
    signal = strategy.generate_signal(df)
    assert signal == "HOLD"