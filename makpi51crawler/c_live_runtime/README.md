# LogisticSearch C Live Runtime

Status: candidate-only skeleton.

This directory is the isolated C runtime surface for LogisticSearch.

It is intentionally separate from:

- `makpi51crawler/cpp_live_runtime/`
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

The first role of this surface is to provide a small, stable, low-level C runtime foundation for future helpers, such as:

- minimal ABI-safe helper functions
- low-level hashing or byte utilities
- worker-safe C components
- future C ABI boundary experiments

This skeleton is not live-activated.

### `byte_histogram`

Deterministic 256-bucket byte distribution helper for future raw/evidence profile analysis.

Initial result fields:

- `buckets`
- `total_count`
- `distinct_byte_count`

Safety notes:

- This module does not compress data.
- This module does not mutate files.
- This module is not a parser.
- This module must not be used as a deduplication identity or trust boundary.
