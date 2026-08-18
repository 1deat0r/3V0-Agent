# `git bisect`

## (1) Problem it solves
`git bisect` isolates the **specific commit that introduced a regression** when you know a **known-good** commit (older, working) and a **known-bad** commit (current, broken), but not where between them the breakage started. It does a **binary search** over the commit history to find that first bad commit with only ~log2(N) checks instead of checking every commit, each one it checks out for you to test.

## (2) The two labels
- **`good`** — a commit that **does not** have the regression (working / known-good).
- **`bad`** — a commit that **does** have the regression (known-bad).

You mark each checked-out commit as one of these, and bisect narrows the range.

## (3) Trial complexity
It takes about **log2(N)** trials for N candidate commits — a binary search that halves the search range each step. ~10 checks halve a ~1024-commit range.

## (4) Concrete minimal sequence
```
# start, then mark the boundary commits
git bisect start
git bisect good <old-good-rev>      # e.g. the last known-good commit
git bisect bad <current-bad-rev>    # e.g. HEAD (broken)

# bisect checks out a midpoint for you to test; mark each one:
git bisect good    # when the checked-out commit is fine
# or
git bisect bad     # when the checked-out commit is broken

# when bisect reports "first bad commit", clean up:
git bisect reset
```
`git bisect reset` returns the working tree to your original branch/HEAD and ends the session.
