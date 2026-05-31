# LogisticSearch C++ Live Runtime

Status: candidate-only skeleton.

This directory is the isolated C++ runtime surface for LogisticSearch.

It is intentionally separate from:

- `makpi51crawler/c_live_runtime/`
- `makpi51crawler/c_cpp_live_runtime/`
- `makpi51crawler/native_live_runtime/`
- `makpi51crawler/python_live_runtime/`

## Safety contract

- No crawler service start/stop is performed from this directory.
- No PostgreSQL mutation is performed from this directory.
- No raw evidence deletion is performed from this directory.
- No build output is tracked in git.
- Build artifacts must stay outside the repository or inside ignored build directories.
- C and C++ must remain separate unless a future explicit architecture gate changes that decision.

## Initial role

The first role of this surface is to provide a clean, testable C++ runtime foundation for future high-performance helpers, such as:

- hashing helpers
- raw/evidence reading helpers
- text scanning helpers
- parsing acceleration experiments
- benchmarked worker binaries

This skeleton is not live-activated.
