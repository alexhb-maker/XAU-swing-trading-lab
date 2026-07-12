# Data Dictionary — `operations.csv`

| Field | Type | Description |
|---|---|---|
| `op_id` | integer | Sequential trade ID, auto-assigned in chronological order of logging. |
| `operation_name` | string | Free-text label given at logging time (kept as originally written, including self-critical notes — see [Methodology](../README.md#methodology-notes)). |
| `setup_reference` | string | Groups trades sharing the same setup/rationale. Convention: `ref_XX` = base setup; `ref_XX_v` = same setup with a variation; `ref_op_n.XX` = direct continuation of a specific trade that did not trigger. |
| `date_start` / `date_end` | date | Trade window (single day if no `date_end` range applies). |
| `direction` | enum | `Long` or `Short`. |
| `confluences_count` | integer (0–4) | Count of the 4 binary confluence checks below. |
| `structure_ok` | boolean | Market structure alignment (trend/EMA stack) supports the trade direction. |
| `ema_alignment_ok` | boolean | EMA 60 / DEMA 60 positioning supports the trade direction. |
| `indicator_signal` | boolean | BUY/SELL Signal fired per the EMA Gold Trader 2026 Pine Script logic. |
| `liquidity_sweep` | boolean | Liquidity Sweep detected by the indicator (wick ≥ 55% of candle range sweeping the prior 10-candle high/low). |
| `norm_compliant` | enum | `Yes` / `No` / `Partial` — whether the trade followed the trader's own written entry rules, independent of the raw confluence count. |
| `emotional_state` | enum | Self-reported state logged **before** entry: `Neutral`, `Ansioso` (anxious), `Confiado` (confident), `Frustrado` (frustrated), `Eufórico` (euphoric). |
| `planned_rr_ratio` | float | Planned risk:reward ratio at entry (e.g. `2.5` = risking 1 to target 2.5). This is the plan, not the realized outcome. |
| `outcome` | enum | `Win` / `Loss` / `BE` (breakeven) / `No entry` (setup identified but order never triggered). |
| `chart_image` | string | Filename of the corresponding annotated TradingView screenshot in `/images`. |
| `comment` | string | Pre/post-trade discretionary reasoning, translated from the original Spanish trading journal. This is the highest-signal field for behavioral analysis — see [Methodology](../README.md#methodology-notes). |

## Notes on data integrity

- All 17 rows are **paper-traded (simulated) operations**, logged as part of a pre-funding discipline audit, not live capital.
- This is a small, live-growing dataset (n=17 at time of publishing). Statistics in `analysis/statistical-summary.md` should be read as directional behavioral signal, not as a statistically significant edge — see the Methodology section in the main README for how this is handled.
