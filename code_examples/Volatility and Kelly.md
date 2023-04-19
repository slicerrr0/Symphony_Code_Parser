# Source
This symphony code is sourced from the following url: https://app.composer.trade/symphony/7CwWAvbHGmWjwXI1Imzj/details

## Code
```
(defsymphony
 "Volatility and Kelly Symphony - Replace SHY w/ TLT, SSO w/TECL, & UPRO w/ CURE + Fund Surfing - Replace TQQQ w/ TECL"
 {:rebalance-frequency :daily}
 (weight-equal
  [(if
    (> (stdev-return "SPY" 21) 3)
    [(asset "TLT") (asset "SPY")]
    [(weight-equal
      [(if
        (> (stdev-return "SPY" 21) 2)
        [(weight-specified "75%" (asset "SPY") "25%" (asset "TLT"))]
        [(weight-equal
          [(if
            (> (stdev-return "SPY" 21) 1)
            [(asset "SPY")]
            [(weight-equal [(asset "TECL") (asset "CURE")])])])])])])
   (group
    "Fund Surfing"
    [(weight-equal
      [(if
        (< (stdev-return "SPY" 21) 1)
        [(weight-equal
          [(filter
            (rsi 21)
            (select-bottom 1)
            [(asset "UPRO") (asset "TECL") (asset "SHY")])])]
        [(weight-equal [(asset "SHY")])])
       (if
        (< (stdev-return "SPY" 21) 2)
        [(weight-equal
          [(filter
            (rsi 21)
            (select-bottom 1)
            [(asset "UPRO") (asset "TECL") (asset "SHY")])])]
        [(weight-equal [(asset "SHY")])])])])]))

```