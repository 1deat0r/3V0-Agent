The test suites — `tests/` (Python; per-file subprocess isolation via
run_tests_parallel), conformance/integration/stress. `3v0/tests/` covers the
sovereign core. The upstream `evals/` harness was pruned (commit 377b41e14b);
run the suites only via `scripts/run_tests.sh`.