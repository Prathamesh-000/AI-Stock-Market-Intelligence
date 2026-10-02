import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class BacktestEngine:
    """
    Simulates a trading strategy based on AI signals to calculate PnL and risk metrics.
    """
    def __init__(self, initial_capital: float = 100000.0, transaction_cost: float = 0.001):
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost # 0.1% slippage/commission per trade
        self.portfolio_value = initial_capital
        self.trade_history = []
        
    def run(self, df: pd.DataFrame, signal_col: str = 'AI_Signal', return_col: str = 'Fwd_Ret_1d'):
        """
        Executes the backtest over a dataframe containing historical AI signals and actual forward returns.
        """
        logger.info(f"Starting backtest with ${self.initial_capital:,.2f}")
        
        # We need chronological order for a proper equity curve
        if 'Timestamp' in df.columns:
            df = df.sort_values('Timestamp').reset_index(drop=True)
            
        capital = self.initial_capital
        equity_curve = [capital]
        daily_returns = []
        
        winning_trades = 0
        total_trades = 0

        for i, row in df.iterrows():
            signal = row[signal_col]
            actual_return = row[return_col]
            
            if pd.isna(actual_return):
                continue
                
            trade_return = 0.0
            
            if signal == 'BUY':
                # Go Long
                trade_return = actual_return - self.transaction_cost
                total_trades += 1
                if trade_return > 0: winning_trades += 1
                
            elif signal == 'SELL':
                # Go Short
                trade_return = -actual_return - self.transaction_cost
                total_trades += 1
                if trade_return > 0: winning_trades += 1
                
            else:
                # UNCERTAIN / HOLD
                trade_return = 0.0
                
            # Update Capital (Simple non-compounding for this basic simulation)
            daily_pnl = capital * trade_return
            capital += daily_pnl
            
            equity_curve.append(capital)
            daily_returns.append(trade_return)
            
            self.trade_history.append({
                'index': i,
                'signal': signal,
                'market_return': actual_return,
                'trade_return': trade_return,
                'capital': capital
            })
            
        self.portfolio_value = capital
        
        # Calculate Quant Metrics
        returns_array = np.array(daily_returns)
        
        total_return_pct = (self.portfolio_value - self.initial_capital) / self.initial_capital * 100
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        
        # Annualized Sharpe Ratio (assuming roughly 252 trading days)
        if len(returns_array) > 0 and returns_array.std() > 0:
            sharpe_ratio = (returns_array.mean() / returns_array.std()) * np.sqrt(252)
        else:
            sharpe_ratio = 0.0
            
        # Max Drawdown
        equity_series = pd.Series(equity_curve)
        rolling_max = equity_series.cummax()
        drawdown = (equity_series - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100
        
        metrics = {
            "Initial Capital": f"${self.initial_capital:,.2f}",
            "Final Capital": f"${self.portfolio_value:,.2f}",
            "Total Return": f"{total_return_pct:.2f}%",
            "Total Trades": total_trades,
            "Win Rate": f"{win_rate:.2f}%",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Max Drawdown": f"{max_drawdown:.2f}%"
        }
        
        return metrics, pd.DataFrame(self.trade_history)
