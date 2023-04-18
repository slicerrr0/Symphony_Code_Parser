# Symphony Code Example

This document contains an example of the syntax and structure used to
define the code that represents the algorithmic logic of a Symphony.

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

## Breakdown

Python-like indentation is used to denote the flow of logic between conditional statements,
and to express a hierarchical order.