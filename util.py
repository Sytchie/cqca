#!/usr/local/bin/python3

def list_to_str(l):
    return "\t".join([str(e) for e in l])


def len_min_max(a, b):
    a_len = len(a)
    b_len = len(b)

    min_val = None
    max_val = None

    if a_len > 0 and b_len > 0:
        min_val = min(a[0], b[0])
        max_val = max(a[-1], b[-1])
    elif a_len > 0:
        min_val = a[0]
        max_val = a[-1]
    else:
        min_val = b[0]
        max_val = b[-1]

    return a_len, b_len, min_val, max_val
