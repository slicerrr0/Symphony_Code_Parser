# Source
This symphony code is sourced from the following url: 

## Code
```
(defsymphony
 "Copy of Holy Grail simplified"
 {:rebalance-threshold 0.03}
 (weight-equal
  [(if
    (> (current-price "TQQQ") (moving-average-price "TQQQ" 200))
    [(weight-equal
      [(if (> (rsi "QQQ" 10) 80) [(asset "UVXY")] [(asset "TQQQ")])])]
    [(weight-equal
      [(if
        (< (rsi "TQQQ" 10) 31)
        [(asset "TECL")]
        [(weight-equal
          [(if
            (< (rsi "UPRO" 10) 31)
            [(asset "UPRO")]
            [(weight-equal
              [(if
                (>
                 (current-price "TQQQ")
                 (moving-average-price "TQQQ" 20))
                [(asset "TQQQ")]
                [(weight-equal
                  [(filter
                    (rsi "10")
                    (select-top 1)
                    [(asset "TLT") (asset "SQQQ")])])])])])])])])])]))
```