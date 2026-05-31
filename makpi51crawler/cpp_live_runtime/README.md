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

## Current modules

### `byte_metrics`

Small deterministic byte statistics helper for raw/evidence-oriented pipelines.

Initial fields:

- `byte_count`
- `zero_byte_count`
- `newline_count`
- `ascii_printable_count`
- `high_bit_byte_count`
- `fnv1a64_non_crypto`

Security note: `fnv1a64_non_crypto` is intentionally non-cryptographic and must not be used as a deduplication identity or trust boundary.

### `file_byte_metrics`

Regular-file byte metrics helper that reads a file in bounded chunks and applies the existing `byte_metrics` model.

Initial result fields:

- `ok`
- `error_code`
- `metrics`
- `bytes_read`
- `chunks_read`

Safety notes:

- Only regular files are accepted.
- Chunk size must be between 1 byte and 16 MiB.
- The helper does not mutate files.
- `fnv1a64_non_crypto` remains non-cryptographic and must not be used as a deduplication identity or trust boundary.

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
