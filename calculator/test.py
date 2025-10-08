#!/usr/bin/env python3

import calc

px = [0.4, 0.20, 0.25, 0.15]
m = [
  [0.82, 0.05, 0.08, 0.05],
  [0.25, 0.75, 0.00, 0.00],
  [0.00, 0.08, 0.80, 0.12],
  [0.02, 0.10, 0.00, 0.88]
]

print("p(x) * p(y)")
py = calc.proby(m, px)
print([calc.info(a * b) for a, b in zip(px, py)])

print("p(x)")
print([calc.info(px[i]) for i in range(len(px))])

print("px(y|x)")
print([calc.info(m[i][i]) for i in range(len(px))])

print("px(y|x) * px(x)")
print([calc.info(m[i][i] * px[i]) for i in range(len(px))])

# p = [0.1, 0.2, 0.3, 0.4]
# print([calc.info(x) for x in p])

# X = [
#   ("x1", 0.1, "100"),
#   ("x2", 0.2, "101"),
#   ("x3", 0.3, "11"),
#   ("x4", 0.4, "0")
# ]
# calc.stats(X)
#
# X = [
#   ("x1", 0.1, "00"),
#   ("x2", 0.2, "01"),
#   ("x3", 0.3, "10"),
#   ("x4", 0.4, "11")
# ]
# calc.stats(X)
