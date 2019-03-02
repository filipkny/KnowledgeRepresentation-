def decay_sum_update(s, r):
    for literal, val in s.items():
        s[literal] = s[literal]/2 + r[literal]
        r[literal] = 0