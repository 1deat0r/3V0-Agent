def group_anagrams(words):
    groups = {}
    for w in words:
        key = str(sorted(w))
        groups.setdefault(key, []).append(w)
    return list(groups.values())
assert sum(len(g) for g in group_anagrams(['eat','tea','tan','ate','nat','bat'])) == 6
assert group_anagrams([]) == []
assert group_anagrams(['a']) == [['a']]
assert group_anagrams(['ab','ba','ab']) == [['ab','ba','ab']]
print("anagram assertions OK")
