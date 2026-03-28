import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def detect_stale_feeds(df, time_threshold_sec=5, consecutive_threshold=10):
    """
    Identifies stale FX feeds in a DataFrame.

    Parameters:
    - df: DataFrame with columns ['symbol', 'bid', 'ask', 'exchange_ts', 'local_ts']
    - time_threshold_sec: Max seconds allowed since last update.
    - consecutive_threshold: Max number of ticks with identical prices.
    """

    # Ensure timestamps are datetime objects
    df['exchange_ts'] = pd.to_datetime(df['exchange_ts'])
    df['local_ts'] = pd.to_datetime(df['local_ts'])

    # Sort by symbol and time to ensure sequence
    df = df.sort_values(by=['symbol', 'exchange_ts'])

    results = []

    for symbol, group in df.groupby('symbol'):
        # 1. Check for Temporal Staleness (Time since last tick)
        latest_tick = group['exchange_ts'].max()
        current_time = datetime.utcnow()  # Or the max timestamp in the dataset
        time_delta = (current_time - latest_tick).total_seconds()
        is_temporally_stale = time_delta > time_threshold_sec

        # 2. Check for Price Stagnation (Frozen Price)
        # Create a combined string of bid+ask to detect any movement in the spread
        group['price_str'] = group['bid'].astype(str) + group['ask'].astype(str)

        # Count consecutive identical values
        # logic: compare current row to previous, cumsum creates groups of identical prices
        price_groups = (group['price_str'] != group['price_str'].shift()).cumsum()
        max_consecutive = group.groupby(price_groups)['price_str'].count().max()
        is_price_stagnant = max_consecutive >= consecutive_threshold

        # 3. Clock Drift Detection
        # Difference between when the exchange says it happened vs when we got it
        group['drift'] = (group['local_ts'] - group['exchange_ts']).dt.total_seconds()
        avg_drift = group['drift'].mean()

        results.append({
            'symbol': symbol,
            'last_update': latest_tick,
            'seconds_since_last': time_delta,
            'max_consecutive_identical_prices': max_consecutive,
            'avg_drift_sec': avg_drift,
            'is_stale': is_temporally_stale or is_price_stagnant
        })

    return pd.DataFrame(results)


# --- Example Usage ---
data = {
    'symbol': ['EUR/USD', 'EUR/USD', 'EUR/USD', 'GBP/JPY', 'GBP/JPY'],
    'bid': [1.0850, 1.0850, 1.0850, 150.10, 150.11],
    'ask': [1.0851, 1.0851, 1.0851, 150.12, 150.13],
    'exchange_ts': [
        '2023-10-27 10:00:00', '2023-10-27 10:00:01', '2023-10-27 10:00:02',
        '2023-10-27 10:00:00', '2023-10-27 10:00:01'
    ],
    'local_ts': [
        '2023-10-27 10:00:00.1', '2023-10-27 10:00:01.1', '2023-10-27 10:00:02.1',
        '2023-10-27 10:00:00.2', '2023-10-27 10:00:01.2'
    ]
}

df_fx = pd.DataFrame(data)
stale_report = detect_stale_feeds(df_fx, time_threshold_sec=2, consecutive_threshold=3)
print(stale_report)