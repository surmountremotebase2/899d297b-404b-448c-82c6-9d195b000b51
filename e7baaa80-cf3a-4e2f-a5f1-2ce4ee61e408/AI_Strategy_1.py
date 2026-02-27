from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, EMA

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["SOXL", "SOXS"]
    
    @property
    def interval(self):
        return "1day"  # Using daily intervals for analysis
    
    @property
    def data(self):
        # No additional data sources are required beyond OHLCV
        return []
    
    def run(self, data):
        # Access the OHLCV data for QQQ to compute indicators
        qqq_data = data["ohlcv"]["QQQ"]
        
        # Calculate the 8-day SMA, 2-day SMA, 3-day EMA, and 6-day EMA for QQQ
        sma_8d = SMA("QQQ", data["ohlcv"], 8)[-1]  # Last value of 8-day SMA
        ema_3d = EMA("QQQ", data["ohlcv"], 3)[-1]  # Last value of 3-day EMA
        ema_6d = EMA("QQQ", data["ohlcv"], 6)[-1]  # Last value of 6-day EMA
        sma_2d = SMA("QQQ", data["ohlcv"], 2)[-1]  # Last value of 2-day SMA
        
        # Get the most recent closing price for QQQ
        current_price = qqq_data[-1]["close"]
        
        # Determine allocation based on strategy rules
        allocation = {"SOXL": 0.0, "SOXS": 0.0}
        
        if current_price > sma_8d:
            if ema_3d > ema_6d:
                allocation["SOXL"] = 1.0  # Buy SOXL
            elif ema_3d < ema_6d:
                allocation["SOXS"] = 1.0  # Buy SOXS
        elif current_price < sma_8d and current_price > sma_2d:
            allocation["SOXS"] = 1.0  # Buy SOXS under these conditions
        else:
            allocation["SOXL"] = 1.0  # Default to holding SOXL
        
        return TargetAllocation(allocation)