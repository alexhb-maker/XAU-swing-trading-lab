# Strategy v2 — Adapted from backtest findings

> This is not a new indicator. It's an execution, risk-management, and behavioral overlay on top of the same [EMA Gold Trader 2026](./ema-gold-trader-2026.pine) script, built directly from what the [17-trade backtest](../analysis/statistical-summary.md) actually showed — not from theory.

## 0. Why this version exists

[Strategy v1](./strategy-v1.md) defines the indicator and the 4 technical confluences. The backtest surfaced three things the indicator alone cannot resolve:

1. Long and Short performance are **not symmetric**, even though the same confluence logic is applied to both.
2. Some Short losses were **not analytical errors** — they were stop-placement errors.
3. The single biggest source of losses was **not the market** — it was what happened in the days after a loss.

v2 doesn't replace v1; it adds the layer that can only be learned by trading and reviewing the actual log.

## 1. Guiding principle: structure over indicator

Already present as a comment in the original trading rules, formalized here as an explicit rule:

> The 4 confluences are a guide, not a hard rule. The market sometimes breaks the confluence structure specifically to invalidate algorithmic setups. When my structural/contextual reading conflicts with what the indicator shows, structure wins.

The indicator filters candidates; the final entry decision stays discretionary, informed by what's actually on the chart, not an automatic execution of signals.

## 2. Timeframe framework

- **Execution: 1H.** Where the EMA/DEMA logic lives and where I actually trade.
- **Context: EMA 200 on the 1H chart as a 4H proxy**, to avoid constantly switching charts.
- **New in v2:** for higher-conviction trades (planned R:R > 2.5, or when the proxy and my discretionary read disagree), confirm with an actual glance at the 4H chart before entering. The proxy is a speed tool, not a guarantee — it doesn't always faithfully represent the higher timeframe.

## 3. The 4 confluences — with a validated entry threshold

Same four checks, 1 point each:

1. **Market structure** — market structure in the technical-analysis / SMC sense: price patterns, liquidity zones, structure breaks (BOS/CHoCH), order blocks, and general trend context. Independent of whether the EMAs happen to be aligned — this is always a discretionary read, not a script output.
2. **EMA alignment** — price respects the expected EMA 60 / DEMA 60 / EMA 200 positioning (`Price > DEMA > EMA > EMA200` for longs, inverted for shorts).
3. **Indicator signal** — BUY/SELL Signal active per the Pine Script logic.
4. **Liquidity Sweep** — detected by the indicator.

**Entry threshold (data-backed):**

- **0 confluences → do not trade, no exceptions.** In the backtest, 0-confluence trades had a 0% win rate (2/2 losses), both also rule-violating and logged with a non-neutral emotional state. The simplest and best-validated filter in the whole system.
- **2 confluences → exceptional case, not standard practice.** One winning trade exists (op #7) but was self-flagged at the time as "rushed" and "risky." If taken, requires a written structural justification in the trade log *before* the outcome is known — not a post-hoc rationalization.
- **3–4 confluences → standard entry threshold.**

## 4. Direction-specific rules

The most important addition in v2 — **Long and Short don't behave the same in my trading, even under the identical rule set.**

### 4.1 Long

- Track record with full rule compliance: 6/6 — **100% win rate**.
- **No changes to the current Long rule set** — validated within the available sample.
- **Regime warning:** that 100% was built during an exceptionally clean, sustained uptrend (Jan–Apr 2026). Do not assume the edge holds equally well in a range-bound or corrective regime — there is no data yet for Long trades under those conditions. Treat the 100% as "validated in trend," not "validated in all contexts."

### 4.2 Short

- Track record with full rule compliance: 3/6 — **50% win rate**.
- Reviewing the chart images for the losing trades showed that **2 of the 3 losses were not directional misreads** — the trend read was correct — but **stop-placement failures**: price stopped me out via the sweep's own wick before the anticipated move completed.
- **New stop rule for shorts:** place the stop beyond the *entire* sweep zone that triggered the entry, not at the first technical invalidation level. More conservative alternative: wait for the sweep candle to **close** before entering, instead of entering during the sweep itself.
- **Sizing note (suggestion, not yet a hard rule):** while more sample accumulates on shorts with the adjusted stop, consider a slightly reduced position size on shorts relative to longs, given the current n (6 trades) is too small to treat 50% as a stable number.

## 5. EMA 200 as a conviction multiplier, not a standalone signal

The hypothesis that price touching/rejecting EMA 200 raises win probability was visually confirmed in at least one clean case (op #12: repeated rejection before a strong drop). It is not infallible — op #9 shows price breaking a resistance at the EMA200 zone because the underlying trend was stronger than the level.

**Rule:** a visible touch/rejection at EMA 200 is **not a fifth confluence** and does not replace the original four. It's a conviction multiplier applied *after* already having 3–4 confluences — it increases position conviction, it doesn't enable the trade on its own. Before treating an EMA200 rejection as valid, confirm the underlying trend isn't clearly dominant against the trade (the specific error in op #9).

## 6. Emotional circuit breaker — the single most important rule in v2

The clearest, best-supported conclusion of the whole backtest: the biggest source of losses isn't an analytical failure — it's what happens in the 1–2 weeks after a real loss.

**Evidence:** the only losing streak in the 17-trade log (May 5–19) starts with a clean loss and turns into a chain of indiscipline — including a trade explicitly logged as "revenge" and another annotated directly on the chart with *"why don't you follow the plan!!!"*. The two only non-neutral emotional states in the entire log fall exactly in this window.

**Rules:**

- After any real loss (does not apply to "No entry"): **mandatory 24h minimum pause** before the next entry, real or paper.
- During that pause: zero new positions, including "just to test something."
- **Emotional veto rule:** if the emotional state logged before entry is not Neutral, do not trade — no exceptions, even with all 4 confluences present. Emotional state is logged *before* entry, not as a post-hoc justification.
- If the "I need to win this back now" pattern shows up, that's the signal to activate the pause, not to look for the next entry.

## 7. Structured patience — reinforcing what already works

Not everything in the backtest is a failure. One behavior pattern is worth explicitly protecting: **op #15 → op #16.** An entry never triggered ("didn't happen, was a good idea"), and instead of forcing an immediate substitute, I waited and came back to the same thesis days later via a different structural confirmation. Result: a win.

**Rule:** when an entry doesn't trigger, the next step is to wait, not substitute. If the same thesis reappears later via a different confirmation, document the link via `setup_reference` (`_v` suffix for a variation of the same setup, or `ref_op_n.XX` for a direct continuation of a trade that didn't trigger).

## 8. Setup families to prioritize

From the current track record, these are the patterns with the best history and worth recognizing faster in real time:

- **ref_01** (3/3 wins) — the most consistent setup so far.
- **ref_02 and ref_03** (4/4 confluences, both winners, the highest ratios in the log) — "complete" entries tend to be the best-performing.
- **ref_00 → ref_00_v** — evidence the refinement process itself works: the original version never triggered, the variation did, and won. Keep documenting variations with `_v` instead of treating them as unrelated trades.

## 9. v2 Entry checklist

- [ ] At least 3 of 4 confluences present? (0 = don't trade, 2 = exceptional and justified in writing)
- [ ] Emotional state = Neutral, logged before entry?
- [ ] At least 24h since the last real loss?
- [ ] If Short: stop placed beyond the full sweep zone, or waited for candle close?
- [ ] If Short: confirmed not trading against a clearly dominant underlying trend?
- [ ] If EMA200 rejection present: treated as a conviction boost, not a substitute for the 4 confluences?
- [ ] Pre-trade comment written before knowing the outcome (thesis, discretionary read, setup reference)?

## 10. When to revisit this version

These rules are based on a small sample (17 trades, 6 per direction on the short side). Revisit and adjust v2 once 15–20 additional trades accumulate under this rule set, specifically comparing:

- Whether Short win rate improves with the new stop placement.
- Whether the emotional circuit breaker reduces or eliminates losing streaks caused by indiscipline.
- Whether the 100% Long win rate holds outside a strong-trend regime, or where the first crack appears.

The goal of v2 is not to predict the market better — it's to execute the reads I already know how to make with fewer process leaks.
