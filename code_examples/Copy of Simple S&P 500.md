# Source
This symphony code is sourced from the following url: https://app.composer.trade/symphony/PdgUAAy4GmEQvGyKsYZt/details

## Code
```
(defsymphony
 "Copy of Simple S&P 500"
 {:rebalance-frequency :daily}
 (weight-equal
  [(if
    (>
     (moving-average-price "SPY" 21)
     (moving-average-price "SPY" 210))
    [(asset "QQQ")]
    [(weight-equal
      [(if
        (< (rsi "QQQ" 10) 30)
        [(asset "QQQ")]
        [(weight-equal
          [(if
            (> (current-price "SPY") (moving-average-price "SPY" 31))
            [(asset "QQQ")] 
            [(asset "SHY")])])])])])]))

```