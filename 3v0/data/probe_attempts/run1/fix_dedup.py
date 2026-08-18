def dedup_preserve(values):
    out = []
    for v in values:
        if v not in out:
            out.append(v)
    return out
assert dedup_preserve([3,1,3,2,1]) == [3,1,2]
assert dedup_preserve([]) == []
assert dedup_preserve(['a','b','a','c']) == ['a','b','c']
orig = [3,1,3,2,1]
dedup_preserve(orig)
assert orig == [3,1,3,2,1]
print("dedup assertions OK")
