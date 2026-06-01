# LogisticSearch — AI / Ranking / Neural / Crawling Dependency Decision

Date: 2026-06-01  
Gate: KOD_BLOGU_067 / AI_RANKING_DEPENDENCY_DECISION_DOC_LOCAL_ONLY_R1  
Status: LOCAL_ONLY_DECISION_DOC  
Canonical HEAD: 61465250a30a1e37799f84c91bd2a744384c6c69  
Previous issue: KOD_BLOGU_066 was too aggressive because it moved toward install before a written dependency decision and sync plan.

## 1. Purpose

This document defines the dependency scope for LogisticSearch AI/ranking/crawling extensions across Python, C, and C++.

The goal is not to blindly install every possible package. The goal is to create a strict, documented, staged, auditable dependency plan for:

- web crawling support
- static HTML extraction
- dynamic page support boundary
- raw/evidence reading
- compression/decompression helpers
- classical ranking
- taxonomy-aware ranking
- neural reranking
- vector indexing
- Python/C/C++ integration
- future Hailo acceleration

## 2. Hard rules

1. System Python must not be polluted by pip.
2. Python dependencies must be installed only into an explicit venv.
3. The venv must not live inside `/logisticsearch/repo`.
4. The venv must not live inside `/logisticsearch/makpi51crawler`.
5. Preferred pi51c Python venv path: `/logisticsearch/makpi51crawler/.venv`.
6. No Hailo driver/runtime/package before physical Hailo device is visible.
7. No crawler service start during dependency installation.
8. No DB mutation during dependency installation.
9. No raw/evidence deletion during dependency installation.
10. No hidden apt/pip install outside explicit mutation gates.
11. C and C++ surfaces remain separate:
    - `makpi51crawler/c_live_runtime/`
    - `makpi51crawler/cpp_live_runtime/`
12. Forbidden mixed runtime surfaces remain absent:
    - `makpi51crawler/native_live_runtime/`
    - `makpi51crawler/c_cpp_live_runtime/`

## 3. Dependency layers

### Layer A — System build/runtime foundation

Purpose:
- compile Python wheels if needed
- compile C/C++ helper probes
- provide stable compression, parsing, regex, JSON, DB, and numeric headers

Apt package manifest:
- tracked separately at `makpi51crawler/python_live_runtime/requirements/ai_ranking_py312.apt-packages.txt`

Allowed later:
- apt install only in a mutation gate after audit
- no system service mutation
- no DB mutation
- no crawler start

### Layer B — Python venv foundation

Purpose:
- isolated Python runtime
- no system Python pollution
- reproducible pip package scope

Python venv path:
- `/logisticsearch/makpi51crawler/.venv`

Forbidden venv paths:
- `/logisticsearch/repo/.venv`
- `/logisticsearch/makpi51crawler/.venv`

Important existing issue:
- previous inventory saw `/logisticsearch/makpi51crawler/.venv`.
- this must be inspected and classified before creating the new canonical venv.
- it must not be reused blindly.

### Layer C — Crawling and extraction packages

Purpose:
- HTTP support
- HTML parsing
- article/main-content extraction
- URL/domain normalization
- robust retry behavior
- compressed body processing

Python candidate packages:
- requests
- httpx
- aiohttp
- urllib3
- tenacity
- beautifulsoup4
- lxml
- html5lib
- selectolax
- trafilatura
- readability-lxml
- courlan
- tldextract
- orjson
- pysimdjson / simdjson package variant
- zstandard
- brotli
- lz4

Dynamic browser boundary:
- playwright package and browser binaries are not part of this initial dependency gate.
- browser binaries require a separate browser/runtime gate.
- crawler service must stay inactive during dependency work.

### Layer D — Classical ranking packages

Purpose:
- deterministic lexical ranking
- BM25
- taxonomy-weighted scoring
- feature pipelines
- audit-friendly scoring output

Python candidate packages:
- numpy
- scipy
- pandas
- pydantic
- scikit-learn
- rank-bm25
- rapidfuzz
- lightgbm
- xgboost

Initial recommended ranking sequence:
1. BM25 baseline
2. taxonomy keyword/alias weighted score
3. source-family quality score
4. URL/title/body field weighting
5. language/locale fit
6. LightGBM/XGBoost learning-to-rank only after labelled training data exists

### Layer E — Neural and neural ranking packages

Purpose:
- embedding generation
- reranking
- ONNX CPU inference
- later accelerator migration

Python candidate packages:
- onnx
- onnxruntime
- tokenizers
- safetensors
- huggingface-hub
- transformers
- sentence-transformers
- torch CPU-only baseline

Strict policy:
- neural packages are heavy.
- initial install must be CPU-only unless a separate GPU gate is opened.
- model download/cache must be separate from dependency install.
- Hailo conversion/runtime is separate and blocked until hardware is visible.

### Layer F — Vector index packages

Purpose:
- approximate nearest-neighbor lookup
- embedding/reranking experiments

Python candidate packages:
- hnswlib
- faiss-cpu optional
- annoy optional later

Policy:
- hnswlib is preferred first due small scope.
- faiss-cpu is platform-sensitive and optional.
- failure to install faiss-cpu must not fail the entire dependency strategy.

### Layer G — Python/C/C++ binding packages

Purpose:
- expose C/C++ deterministic helpers to Python orchestration
- keep crawler_core thin
- avoid mixing C and C++ runtime surfaces

Python candidate packages:
- pybind11
- nanobind
- cffi
- Cython

Recommended order:
1. cffi/ctypes for C helper smoke
2. pybind11 or nanobind for C++ helper smoke
3. package/build integration only after ABI and venv are pinned
4. no crawler_core integration until smoke tests are sealed

### Layer H — C libraries

Purpose:
- low-level runtime helper support

C header/library candidate families:
- libcurl
- OpenSSL
- zlib
- zstd
- brotli
- lz4
- libxml2
- libxslt
- sqlite3
- libpq
- OpenBLAS/LAPACK when numeric/native scoring requires it

Policy:
- C runtime remains under `makpi51crawler/c_live_runtime/`.
- C smoke tests must compile and run before Python binding work.
- no C/C++ mixed runtime folder.

### Layer I — C++ libraries

Purpose:
- deterministic parsing, byte metrics, JSON, regex, vector/math support

C++ header/library candidate families:
- CMake
- Ninja
- pkg-config
- clang/gcc toolchain
- simdjson
- nlohmann-json
- RE2
- ICU
- Gumbo parser
- Eigen
- OpenBLAS/LAPACK if required by native math
- libcurl/OpenSSL/zstd/brotli/lz4/libxml2 as shared foundations

Policy:
- C++ runtime remains under `makpi51crawler/cpp_live_runtime/`.
- C++ smoke tests must compile and run before Python binding work.
- no `native_live_runtime/`.
- no `c_cpp_live_runtime/`.

### Layer J — Hailo / accelerator packages

Blocked until hardware visible:
- hailort
- hailo_platform
- HailoRT driver/runtime
- TAPPAS
- Hailo Model Zoo runtime install
- Hailo kernel modules

Required before any Hailo install:
1. Seeed HAT installed
2. NVMe still visible
3. Hailo device visible in `lspci`
4. PCIe link speed/width audited
5. service/crawler/browser process count 0
6. separate Hailo driver/runtime plan doc
7. separate mutation gate

## 4. Install staging plan

### Stage 0 — current state
- KOD_BLOGU_065 inventory passed.
- all relevant Python packages were missing on Desktop and pi51c.
- pi51c has Python 3.12.3.
- pi51c architecture is arm64/aarch64.
- Hailo is absent.
- Hailo packages are forbidden.

### Stage 1 — local documentation
Gate:
- KOD_BLOGU_067

Creates:
- this decision document
- Python requirements candidate manifest
- apt package candidate manifest

No install.

### Stage 2 — local audit
Gate:
- KOD_BLOGU_068

Checks:
- document exists
- requirements files exist
- no forbidden Hailo package in manifests
- no venv inside repo/live path
- no git staged content yet unless intentionally staged in later gate
- package groups are complete enough for project scope

### Stage 3 — commit/push
Gate:
- KOD_BLOGU_069

Allowed:
- git add exactly the three documentation/manifest files
- commit
- push

Forbidden:
- apt
- pip
- venv
- pi51c mutation

### Stage 4 — pi51c repo sync
Gate:
- KOD_BLOGU_070

Allowed:
- sync pi51c `/logisticsearch/repo` to GitHub HEAD

Forbidden:
- install
- live runtime copy unless explicitly needed
- DB/crawler/systemd mutation

### Stage 5 — post-sync read-only seal
Gate:
- KOD_BLOGU_071

Checks:
- Ubuntu Desktop = GitHub = pi51c repo
- docs/manifests identical

### Stage 6 — old live `.venv` classification
Gate:
- KOD_BLOGU_072

Purpose:
- inspect `/logisticsearch/makpi51crawler/.venv`
- classify as legacy/unused/active/unknown
- no delete yet

### Stage 7 — canonical venv creation plan
Gate:
- KOD_BLOGU_073

Purpose:
rejected context: - create `/logisticsearch/makpi51crawler/venvs/ai_ranking_py312`
- no package install yet, unless explicitly approved by a later gate

### Stage 8 — dependency install in canonical venv
Gate:
- KOD_BLOGU_074 or later

Allowed:
- apt install from approved manifest
- pip install from approved requirements inside canonical venv only

Forbidden:
- Hailo packages
- crawler start
- DB mutation
- service mutation

## 5. KOD_BLOGU_068B corrected audit truth

Marker: `KOD_BLOGU_068B_CORRECTED_AUDIT_TRUTH`

KOD_BLOGU_068 initially returned `REVIEW_REQUIRED` only because the audit constants expected the wrong active package counts. KOD_BLOGU_068B corrected the audit constants and sealed the same file content as valid.

Corrected sealed counts:

- Active Python requirements: 41
- Active apt packages: 38
- Duplicate active Python requirements: 0
- Duplicate active apt packages: 0
- Active Hailo pip requirements: 0
- Active Hailo apt/Hailo patterns: 0
- Deferred/inactive Python package entries: `faiss-cpu`, `playwright`, `hailo_platform`, `hailort`
- Dirty scope before commit: exactly three files
- Staged files before commit: 0

Active Python requirements sealed by KOD_BLOGU_068B:

1. `numpy`
2. `scipy`
3. `pandas`
4. `pydantic`
5. `scikit-learn`
6. `rank-bm25`
7. `rapidfuzz`
8. `lightgbm`
9. `xgboost`
10. `requests`
11. `urllib3`
12. `httpx`
13. `aiohttp`
14. `tenacity`
15. `beautifulsoup4`
16. `lxml`
17. `html5lib`
18. `selectolax`
19. `trafilatura`
20. `readability-lxml`
21. `courlan`
22. `tldextract`
23. `orjson`
24. `zstandard`
25. `brotli`
26. `lz4`
27. `psycopg[binary]`
28. `SQLAlchemy`
29. `onnx`
30. `onnxruntime`
31. `tokenizers`
32. `safetensors`
33. `huggingface-hub`
34. `transformers`
35. `sentence-transformers`
36. `torch`
37. `hnswlib`
38. `pybind11`
39. `nanobind`
40. `cffi`
41. `Cython`

Active apt packages sealed by KOD_BLOGU_068B:

1. `python3-full`
2. `python3-venv`
3. `python3-pip`
4. `python3-dev`
5. `python3-setuptools`
6. `python3-wheel`
7. `build-essential`
8. `gcc`
9. `g++`
10. `clang`
11. `lld`
12. `gdb`
13. `valgrind`
14. `cmake`
15. `ninja-build`
16. `pkg-config`
17. `git`
18. `curl`
19. `ca-certificates`
20. `libssl-dev`
21. `libcurl4-openssl-dev`
22. `zlib1g-dev`
23. `libzstd-dev`
24. `libbrotli-dev`
25. `liblz4-dev`
26. `libxml2-dev`
27. `libxslt1-dev`
28. `libgumbo-dev`
29. `libre2-dev`
30. `libicu-dev`
31. `libsimdjson-dev`
32. `nlohmann-json3-dev`
33. `libsqlite3-dev`
34. `libpq-dev`
35. `libopenblas-dev`
36. `liblapack-dev`
37. `libeigen3-dev`
38. `libomp-dev`

Policy conclusion:

- The active Python dependency scope is documented and intentionally limited to the 41 entries above.
- The active apt dependency scope is documented and intentionally limited to the 38 entries above.
- Hailo remains blocked until physical Hailo hardware is visible and a separate hardware audit passes.
- Browser binaries and Playwright runtime installation remain blocked until a separate dynamic crawling gate.
- `faiss-cpu` remains optional/platform-sensitive and must not fail the whole dependency strategy if ARM64 support is unavailable.
- C and C++ dependency boundaries remain separate.

## 6. Edge AI architecture discussion for LogisticSearch

Marker: `KOD_BLOGU_069B_EDGE_AI_ARCHITECTURE_TRUTH`

This section records the current hardware and neural-processing design decision for understanding and ranking collected LogisticSearch data.

### 6.1 Current hardware assumption

Target edge node:

- Raspberry Pi 5
- 16GB RAM
- 512GB NVMe SSD
- PCIe Gen3 preparation already applied
- future Seeed PCIe 3.0 Dual M.2 HAT
- future Hailo-8 M.2 accelerator
- current Hailo software/runtime install remains blocked until hardware is visible

### 6.2 Core opinion

The Raspberry Pi 5 16GB + NVMe + Hailo-8 setup is a good and realistic first production-edge platform for LogisticSearch data understanding, if it is used correctly.

It should be treated as:

- crawler/runtime orchestration node
- raw evidence and parse staging node
- deterministic ranking node
- taxonomy-aware feature extraction node
- edge inference node
- small/medium model inference and reranking node

It should not be treated as:

- large model training machine
- large LLM fine-tuning machine
- unlimited transformer batch-processing server
- Hailo driver/runtime experimentation surface before hardware audit

### 6.3 Python / C / C++ role split

Python remains the orchestration layer:

- queue-level ranking experiments
- BM25 and lexical scoring
- taxonomy matching orchestration
- ONNXRuntime baseline
- model input/output preparation
- audit output
- glue between crawler, parse, ranking and future Hailo inference

C remains the low-level deterministic helper layer:

- byte metrics
- raw body scanning
- compression/decompression helpers
- stable ABI helper functions
- fast hashing / counters / small native routines
- ctypes/cffi boundary candidates

C++ remains the higher-level native acceleration layer:

- fast parser helpers
- simdjson-backed JSON helpers
- RE2/ICU text helpers
- vector/math helpers
- pybind11/nanobind boundary candidates
- later taxonomy matching acceleration

C and C++ must remain separate:

- `makpi51crawler/c_live_runtime/`
- `makpi51crawler/cpp_live_runtime/`

The following surfaces remain forbidden:

- `makpi51crawler/native_live_runtime/`
- `makpi51crawler/c_cpp_live_runtime/`

### 6.4 Data understanding pipeline

The collected LogisticSearch data should become meaningful through a staged pipeline:

1. raw evidence collection
2. raw retention and integrity seal
3. HTML/text extraction
4. language/locale/source-family normalization
5. taxonomy keyword and alias matching
6. BM25 and lexical ranking
7. source quality and freshness scoring
8. neural classification and reranking
9. vector/embedding indexing where useful
10. Hailo-accelerated inference only after HEF/runtime gate

### 6.5 Transportation and logistics focus

The AI/ranking layer must stay domain-specific. The main target is transportation and logistics, including related branches:

- freight forwarding
- road freight
- sea freight
- air freight
- rail freight
- warehousing
- customs brokerage
- cold chain
- project cargo
- dangerous goods
- container logistics
- port/terminal services
- courier/parcel
- last-mile delivery
- intermodal and multimodal transport
- fleet, route, and carrier services
- logistics associations and directories

Generic web ranking is not the goal. The goal is logistics-aware search and company/service understanding.

### 6.6 Recommended AI sequence

Phase 1: deterministic baseline

- BM25
- taxonomy weighted keyword score
- title/body/url/source-family field weighting
- language and locale fit score
- source freshness and trust score

Phase 2: classical ML

- scikit-learn feature pipeline
- LightGBM/XGBoost later, only after labelled data exists
- explicit feature audit output

Phase 3: CPU neural baseline

- ONNXRuntime
- small transformer/reranker experiments
- sentence-transformer embeddings
- no hidden model downloads during dependency install gates

Phase 4: Hailo candidate pipeline

- choose model
- export to ONNX when appropriate
- compile/convert to Hailo HEF in a separate model build gate
- run HailoRT only after Hailo PCI device is visible
- compare CPU baseline vs Hailo inference output

Phase 5: production edge inference

- Hailo inference workers
- CPU fallback
- deterministic audit output
- no crawler_core bloat

### 6.7 Capacity judgement

The Pi 5 16GB + 512GB NVMe + Hailo-8 platform should be enough for the first real LogisticSearch semantic/ranking stack if we keep the workload bounded and staged.

Expected good fit:

- crawler orchestration
- parsing and extraction
- BM25/taxonomy ranking
- small neural classification
- small/medium reranking
- embedding generation in controlled batches
- edge inference with compiled Hailo models
- local evaluation and audit loops

Expected weak fit:

- training large neural networks
- fine-tuning large language models
- running large generative models as the main production inference path
- heavy parallel browser automation
- uncontrolled transformer batch jobs
- Hailo compilation/runtime work before hardware audit

### 6.8 Design decision

The project will proceed with the Pi 5 + NVMe + Hailo-8 path, but with strict boundaries:

- first document and seal dependencies
- then sync GitHub/pi51c repo
- then classify the old live `.venv`
- then create the canonical venv
- then install approved dependencies
- then run CPU baseline
- then add Hailo only after hardware visibility
- then benchmark and compare CPU vs Hailo behavior

This keeps LogisticSearch realistic, stable, and extensible without turning the crawler node into an uncontrolled AI lab.

## 7. KOD_BLOGU_072 old live venv classification

Marker: `KOD_BLOGU_072_OLD_LIVE_VENV_CLASSIFICATION_TRUTH`

KOD_BLOGU_072 classified the existing live runtime virtual environment.

### 7.1 Classification result

Old live venv path:

- `/logisticsearch/makpi51crawler/.venv`

Python AI/ranking source-code surface:

- `/logisticsearch/makpi51crawler/python_live_runtime/ai_ranking`

Classification:

- `EXISTING_LIVE_RUNTIME_VENV_REFERENCED_DO_NOT_REUSE_FOR_AI_RANKING_DO_NOT_DELETE`

Decision:

- The old live `.venv` is an existing referenced live runtime venv.
- It must not be reused for AI/ranking dependency installation.
- It must not be deleted.
- It must not be renamed.
- It must not be moved.
- It must not be chowned/chmodded during AI/ranking work.
- The AI/ranking Python packages must use the existing live Python venv, while AI/ranking source code must live under `python_live_runtime/`.

### 7.2 Observed old live venv facts

KOD_BLOGU_072 observed:

- old live venv exists: yes
- old live venv is directory: yes
- old live venv is symlink: no
- canonical AI venv exists: no
- Python version: 3.12.3
- SOABI: `cpython-312-aarch64-linux-gnu`
- venv path in `pyvenv.cfg`: `/logisticsearch/makpi51crawler/.venv`
- package distribution count: 10
- old venv has `playwright`
- old venv has `psycopg`
- old venv does not have the new AI/ranking stack packages such as numpy, scipy, pandas, sklearn, torch, onnxruntime, transformers, or sentence-transformers
- old venv does not have Hailo packages

### 7.3 Old live venv reference facts

KOD_BLOGU_072 found:

- old venv reference file count: 18
- live root reference file count: 2
- active user systemd service references `/logisticsearch/makpi51crawler/.venv/bin/python`
- sync runbooks reference `/logisticsearch/makpi51crawler/.venv/bin/python`
- existing docs intentionally describe `/logisticsearch/makpi51crawler/.venv`

Therefore the old live venv is part of the current crawler/runtime surface and must be preserved.

### 7.4 New AI/ranking venv policy

The single Python venv path remains:

- `/logisticsearch/makpi51crawler/.venv`

Hard policy:

- no install into `/usr`
- no install into `/logisticsearch/repo/.venv`
- no install into `/logisticsearch/makpi51crawler/.venv`
- no reuse of old live venv
- no deletion or cleanup of old live venv
- no Hailo package before physical Hailo hardware is visible
- no browser binary install in the AI/ranking dependency gate
- no crawler start during venv creation or dependency installation

### 7.5 Next gate consequence

The next safe gate must be a canonical venv creation plan or audit for:

rejected context: - `/logisticsearch/makpi51crawler/venvs/ai_ranking_py312`

The gate must treat `/logisticsearch/makpi51crawler/.venv` as preserved live runtime infrastructure.



## 8. KOD_BLOGU_082B runtime topology repair

Marker: `KOD_BLOGU_082B_ACTIVE_REJECTED_PATH_REPAIR_TRUTH`

KOD_BLOGU_082B repairs the wording after KOD_BLOGU_082. The topology decision was correct, but the rejected paths were still listed in a form that the active-topology audit could count as active. This section makes every rejected path explicit.

### 8.1 Final Python decision

There will be one Python virtual environment:

- `/logisticsearch/makpi51crawler/.venv`

This path is a Python runtime environment, not a source-code directory.

It contains Python interpreter/runtime files such as:

- `bin/`
- `include/`
- `lib/`
- `lib64/`
- `pyvenv.cfg`

It must not be used as an application source-code tree.

### 8.2 Python source-code surface

Python source code belongs here:

- `/logisticsearch/makpi51crawler/python_live_runtime`

AI/ranking Python source code may be added here later:

- `/logisticsearch/makpi51crawler/python_live_runtime/ai_ranking`

This is a source-code/runtime surface. It is not a virtualenv.

### 8.3 C working environment

C does not need a Python-style `.venv`.

The C project working surface is:

- `/logisticsearch/makpi51crawler/c_live_runtime`

C source/build/runtime substructure may later be standardized inside that existing surface:

- `/logisticsearch/makpi51crawler/c_live_runtime/src/`
- `/logisticsearch/makpi51crawler/c_live_runtime/include/`
- `/logisticsearch/makpi51crawler/c_live_runtime/build/`
- `/logisticsearch/makpi51crawler/c_live_runtime/bin/`
- `/logisticsearch/makpi51crawler/c_live_runtime/lib/`

System C toolchain and headers remain OS-managed under paths such as `/usr/bin`, `/usr/include`, and `/usr/lib/aarch64-linux-gnu`.

### 8.4 C++ working environment

C++ does not need a Python-style `.venv`.

The C++ project working surface is:

- `/logisticsearch/makpi51crawler/cpp_live_runtime`

C++ source/build/runtime substructure may later be standardized inside that existing surface:

- `/logisticsearch/makpi51crawler/cpp_live_runtime/src/`
- `/logisticsearch/makpi51crawler/cpp_live_runtime/include/`
- `/logisticsearch/makpi51crawler/cpp_live_runtime/build/`
- `/logisticsearch/makpi51crawler/cpp_live_runtime/bin/`
- `/logisticsearch/makpi51crawler/cpp_live_runtime/lib/`

System C++ toolchain and headers remain OS-managed under paths such as `/usr/bin`, `/usr/include`, and `/usr/lib/aarch64-linux-gnu`.

### 8.5 Rejected environment paths

The following paths are rejected and must not become canonical:

- rejected path: `/logisticsearch/venvs/ai_ranking_py312`
- rejected path: `/logisticsearch/makpi51crawler/venvs/ai_ranking_py312`
- rejected path: `/logisticsearch/makpi51crawler/.venv_ai_ranking_py312`
- rejected path: `/logisticsearch/makpi51crawler/.venvs`
- rejected path: `/logisticsearch/makpi51crawler/venvs`
- rejected path: `/logisticsearch/makpi51crawler/.cenv`
- rejected path: `/logisticsearch/makpi51crawler/.cppenv`
- rejected path: `/logisticsearch/makpi51crawler/c_env`
- rejected path: `/logisticsearch/makpi51crawler/cpp_env`
- rejected path: `/logisticsearch/makpi51crawler/native_live_runtime`
- rejected path: `/logisticsearch/makpi51crawler/c_cpp_live_runtime`

### 8.6 Cleanup consequence

KOD_BLOGU_080 created one rejected temporary venv.

- rejected cleanup target: `/logisticsearch/venvs/ai_ranking_py312`
- rejected cleanup parent root: `/logisticsearch/venvs`

The rejected temporary venv was sealed as a baseline venv containing only `pip==24.0`, with no AI/ranking packages and no Hailo packages.

The next safe sequence is:

1. audit this document repair
2. commit/push this document repair
3. sync pi51c repo
4. verify the rejected temporary venv still contains only baseline pip and no AI/Hailo packages
5. delete only the rejected temporary venv path `/logisticsearch/venvs/ai_ranking_py312`
6. delete only the rejected temporary root `/logisticsearch/venvs` if it is empty after removing the rejected venv
7. preserve `/logisticsearch/makpi51crawler/.venv`
8. plan any package installation into `/logisticsearch/makpi51crawler/.venv` separately

No apt install, pip install, Hailo runtime, crawler start, DB mutation, systemd mutation, raw mutation, or live runtime copy is allowed during the topology repair and cleanup sequence.

## 9. Current recommendation

Do not install everything immediately.

The correct next gate after KOD_BLOGU_067 is:

KOD_BLOGU_068 / AI_RANKING_DEPENDENCY_DECISION_DOC_AUDIT_READONLY_R1

Only after documentation audit passes should we commit/push/sync.
