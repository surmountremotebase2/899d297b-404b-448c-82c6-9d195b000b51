from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, EMA
from surmount.logging import log

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
        allocation = {"SOXL": 0.0, "SOXS": 0.0}

        # Corrected approach: Iterate through each asset and compute its indicators and allocation
        for asset in self.assets:
            # Access the OHLCV data for the specific asset
            ohlcv_data = data["ohlcv"][asset]

            # Calculate technical indicators for the asset
            sma_8d = SMA(asset, data["ohlcv"], 8)[-1] if len(ohlcv_data) >= 8 else None
            sma_2d = SMA(asset, data["ohlcv"], 2)[-1] if len(ohlcv_data) >= 2 else None
            ema_3d = EMA(asset, data["ohlcv"], 3)[-1] if len(ohlcv_data) >= 3 else None
            ema_6d = EMA(asset, data["ohlcv"], 6)[-1] if len(ohlcv_data) >= 6 else None

            # Ensure there is enough data to make a decision
            if not (sma_8d and sma_2d and ema_3d and ema_6d):
                log(f"Not enough data for {asset}")
                continue

            # Get the most recent closing price for the asset
            current_price = ohlcv_data[-1]["close"]

            # Strategy logic to set allocation based on computed indicators
            if current_price > sma_8d:
                if ema_3d > ema_6d:
                    allocation["SOXL"] = 1.0  # Buy SOXL
                    break  # Assuming only one can be held at a time
                elif ema_3d < ema_6d:
                    allocation["SOXS"] = 1.0  # Buy SOXS
                    break
            elif current_price < sma_8d and current_price > sma_2d:
                allocation["SOXS"] = 1.0  # Favor SOXS under these conditions
                break

        # Returns a TargetAllocation object with the determined allocations
        return TargetAllocation(allocation)