# Strategy v1 — EMA Gold Trader 2026 (base indicator)

The base system is a custom TradingView (Pine Script v6) indicator built to flag XAUUSD entries on confluence between moving-average trend structure and automatic liquidity-sweep detection. Full source: [`ema-gold-trader-2026.pine`](./ema-gold-trader-2026.pine).

## Core components

### 1. Three moving averages — trend filters

| Line | Type | Period | Purpose |
|---|---|---|---|
| EMA 60 (orange) | Exponential MA | 60 | Fast trend reaction |
| DEMA 60 (blue) | Double Exponential MA | 60 | Earlier momentum shift detection, less lag than a standard EMA |
| EMA 200 (white) | Exponential MA | 200 | Higher-timeframe context / dominant trend filter |

**Reading the stack:**
- Bullish: `Price > DEMA > EMA > EMA200` (or a similar bullish alignment)
- Bearish: `Price < DEMA < EMA < EMA200` (or a similar bearish alignment)
- Indecision: the three lines are interlaced with no clean order

### 2. Entry / confirmation signals

- **BUY Signal** (green triangle) — conservative signal: previous close above both EMA 60 and DEMA 60.
- **EMA > DEMA Cross** (yellow triangle) — momentum accelerating: the fast EMA crosses back above the DEMA.
- Symmetric **SELL Signal** and **Bearish Cross** are computed for short setups.

### 3. Liquidity sweeps

Automatic detection of stop-liquidity grabs:

- **Bull Sweep:** bullish candle, low touches the lowest low of the last 10 candles, and the lower wick is ≥ 55% of the candle's total range.
- **Bear Sweep:** symmetric condition on the high side.

### 4. Live status table

An on-chart table shows EMA 60 / DEMA 60 / EMA 200 values, BUY Signal state, Sweep state, EMA>DEMA cross state, and current price — always for the **most recent bar**, never for a historical bar under the cursor. (This distinction matters for backtesting — see the [Methodology notes](../README.md#methodology-notes).)

## Original entry logic (4 confluences)

> **Terminology note:** "Structure" here means market structure in the technical-analysis / SMC sense — price patterns, liquidity zones, structure breaks (BOS/CHoCH), order blocks, and general trend context — read discretionarily by the trader, not computed by the script. It is a separate confluence from EMA alignment, which is the mechanical positioning of the three moving averages.

A "complete" long setup requires all four:

1. **Market structure** — discretionary read of price action, liquidity, and context (not just the order of the moving averages)
2. **EMA alignment** — `Price > DEMA > EMA > EMA200`
3. **BUY Signal** active
4. **Bull Sweep** detected

Symmetric logic applies to shorts. Each confluence is worth 1 point (0–4 scale). Only "EMA alignment," "BUY/SELL Signal," and "Liquidity Sweep" are computed automatically by the script — "Market structure" is always a discretionary read by the trader.

## Configurable parameters

| Parameter | Default |
|---|---|
| EMA period | 60 |
| DEMA period | 60 |
| EMA 200 period | 200 |
| Liquidity sweep lookback | 10 candles |
| Minimum wick ratio | 0.55 (55%) |

## Known limitations (as designed)

- No volume analysis.
- Prone to false signals in range-bound / no-trend markets.
- Designed to require additional discretionary confirmation, not to be traded as a fully automated system — see [Strategy v2](./strategy-v2.md) for how that discretionary layer is formalized after backtesting.
