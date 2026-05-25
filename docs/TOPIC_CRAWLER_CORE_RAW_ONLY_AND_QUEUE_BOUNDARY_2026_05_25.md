# Crawler_Core Raw-Only Boundary and Future Queue Contract — 2026-05-25

## 1. Purpose

This document freezes the responsibility boundary between `crawler_core`, `parse_core`, and `desktop_import` so implementation work does not drift.

This is a design-control document. It is not a runtime activation, database mutation, crawler start, source evaluation, or ranking patch.

## 2. Core decision

`crawler_core` is the raw crawling/fetching layer.

`crawler_core` reads URLs from the current input surface, fetches public web content under robots/politeness/runtime policy, writes raw evidence, and records operational fetch metadata.

`crawler_core` must not become the source-evaluation, pre-ranking, ranking, or new-link-promotion brain.

## 3. Startpoints are bootstrap only

Startpoints are the initial bootstrap/input surface.

Current startpoints are JSON catalogs. They are used to begin controlled crawling and to provide initial source provenance.

After startpoints are processed cleanly, `crawler_core` will continue from a real queue system.

The future real queue system is expected to be JSON-based and structurally compatible with the startpoints catalogs where practical. Values and source references must be synchronized carefully, but the queue system is the long-lived crawl input surface after bootstrap.

## 4. Future queue system

The real queue system will be designed after startpoints can be read cleanly and safely.

The future queue system must preserve provenance needed by later layers, for example:

- source catalog reference
- source language / country / family / surface reference
- seed URL reference
- parent/referrer URL reference
- first-seen evidence
- raw fetch evidence path
- operational status
- retry/dead/robots/redirect classification
- evidence needed by parse_core for pre-ranking

The future queue system may use JSON files or JSON manifests, but `crawler_core` consumes queue entries; it does not decide which newly discovered links become valuable queue entries.

## 5. What crawler_core may do

`crawler_core` may:

- read startpoints or future queue entries
- apply robots, politeness, delay, retry, timeout, and runtime safety rules
- fetch static and dynamic pages
- write raw body evidence
- write fetch JSON / zstd evidence
- record HTTP status, redirect, robots, retry, timeout, SSL/runtime, dead/retry_wait evidence
- preserve raw provenance and referrer evidence when available
- maintain operational frontier state needed to avoid duplicate fetches and unsafe loops
- continue from the future queue system after bootstrap

## 6. What crawler_core must not do

`crawler_core` must not:

- decide source business value
- perform taxonomy-weighted source evaluation
- perform pre-ranking
- perform final ranking
- promote newly found links into the long-lived valuable-source queue
- become the link-expansion brain
- mutate source catalogs as a result of crawl findings
- replace parse_core source-evaluation responsibility
- replace desktop_import final-ranking responsibility

## 7. Parse_Core responsibility

`parse_core` is the source-evaluation and pre-ranking layer.

`parse_core` will read raw evidence produced by `crawler_core`.

`parse_core` will evaluate useful sources and may use:

- variables
- keywords
- taxonomy nodes
- taxonomy keyword weights
- referrers
- discovered relationships
- source provenance
- language/country/family context
- content signals
- network-style scoring logic

`parse_core` is responsible for deciding which new links/sources should be added or promoted into the future queue system.

`parse_core` is where source-value logic, pre-ranking, and new-link addition logic belong.

Hardware acceleration topics such as AI accelerators, PCIe limits, SSD sharing, and model/runtime efficiency belong to future parse_core planning, not crawler_core boundary work.

## 8. Desktop_Import responsibility

`desktop_import` runs on Ubuntu Desktop as the final import/ranking/enrichment layer.

`desktop_import` is not the pre-ranking layer.

`desktop_import` applies the final ranking and final data interpretation after upstream raw crawl and parse_core pre-ranking work are controlled.

## 9. Duplicate seed policy

Duplicate startpoint URLs must not be blindly deleted.

A URL may appear in multiple language catalogs, source families, surfaces, or global directories.

The durable crawl target may be canonicalized to one URL identity, but source references must be preserved for later parse_core and ranking signals.

Potential future model:

- one canonical queue/frontier URL
- multiple source/reference records
- preserved catalog/language/family/surface context
- preserved first-seen and duplicate-reference evidence

## 10. Referrer / provenance policy

Crawler_Core may preserve raw provenance evidence.

Crawler_Core must not turn provenance into source-value decisions.

Raw evidence that may be preserved for later parse_core use includes:

- requested URL
- final URL
- parent/referrer URL if already known in the current input queue/frontier
- root seed URL if already known
- source catalog reference if already known
- fetch evidence paths
- error/retry/dead/robots/redirect classification

Parse_Core will later use this provenance for pre-ranking and queue promotion.

## 11. Test discipline

Before every new crawler test:

- reset test DB target tables and counters using controlled DELETE + sequence reset
- preserve keep tables such as `ops.webcrawler_runtime_control` and `public.spatial_ref_sys`
- clean raw_fetch evidence when the gate explicitly allows raw cleanup
- reactivate seed/frontier input
- then run the foreground or service test

Never start a fresh test on leftover DB counters/state unless the test is explicitly a continuation test.

## 12. Current safe next direction

Immediate crawler_core improvement should focus on:

- reliable raw fetching
- stable retry_wait / dead classification
- redirect evidence
- robots evidence
- raw/zstd evidence completeness
- terminal/log visibility
- safe queue consumption behavior
- test reset discipline

Do not commit crawler_core patches that move parse_core responsibilities into crawler_core.
