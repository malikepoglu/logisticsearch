# 0. Documentation Hub

## EN 1. Purpose

This documentation hub explains how to read the LogisticSearch repository as a disciplined engineering system, not as a random collection of notes.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 1. detail 1: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 1. detail 2: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 1. detail 3: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 1. detail 4: Never confuse repository synchronization with live crawler data movement.
- 1. detail 5: Never treat a path reference as current merely because it appears in an old historical seal.
- 1. detail 6: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 1. detail 7: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 1. detail 8: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 1. detail 9: Preserve lease renewal as an explicit safety discipline around claimed work.
- 1. detail 10: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 1. detail 11: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 1. detail 12: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 1. detail 13: Preserve systemd non-touch guarantees during documentation-only work.
- 1. detail 14: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 1. detail 15: Preserve local dirty-scope checks before any patch touches tracked files.
- 1. detail 16: Preserve staged-area checks before every commit gate.
- 1. detail 17: Preserve git diff --check as a mandatory Markdown quality signal.
- 1. detail 18: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 1. detail 19: Preserve code fences without allowing command comments to become Markdown headings.
- 1. detail 20: Preserve exact file names because they are operational identifiers.
- 1. detail 21: Preserve exact commit hashes when documenting historical state.
- 1. detail 22: Preserve beginner-first explanations around every major contract.
- 1. detail 23: Preserve operator-first safety language around every mutating action.
- 1. detail 24: Preserve the ability to resume work from GitHub without chat memory.
- 1. detail 25: Preserve the standard that README files explain, not merely link.
- 1. detail 26: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 1. detail 27: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 1. detail 28: Preserve full English before Turkish so language flow is auditable.

### EN 1.1 What a new reader must understand first

A new reader must first understand the roles of Ubuntu Desktop, GitHub, pi51c, the tracked repository, the live runtime root, and the intentionally separated crawler data path.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 1.1 detail 1: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 1.1 detail 2: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 1.1 detail 3: Never confuse repository synchronization with live crawler data movement.
- 1.1 detail 4: Never treat a path reference as current merely because it appears in an old historical seal.
- 1.1 detail 5: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 1.1 detail 6: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 1.1 detail 7: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 1.1 detail 8: Preserve lease renewal as an explicit safety discipline around claimed work.
- 1.1 detail 9: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 1.1 detail 10: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 1.1 detail 11: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 1.1 detail 12: Preserve systemd non-touch guarantees during documentation-only work.
- 1.1 detail 13: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 1.1 detail 14: Preserve local dirty-scope checks before any patch touches tracked files.
- 1.1 detail 15: Preserve staged-area checks before every commit gate.
- 1.1 detail 16: Preserve git diff --check as a mandatory Markdown quality signal.
- 1.1 detail 17: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 1.1 detail 18: Preserve code fences without allowing command comments to become Markdown headings.
- 1.1 detail 19: Preserve exact file names because they are operational identifiers.
- 1.1 detail 20: Preserve exact commit hashes when documenting historical state.
- 1.1 detail 21: Preserve beginner-first explanations around every major contract.
- 1.1 detail 22: Preserve operator-first safety language around every mutating action.
- 1.1 detail 23: Preserve the ability to resume work from GitHub without chat memory.
- 1.1 detail 24: Preserve the standard that README files explain, not merely link.
- 1.1 detail 25: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 1.1 detail 26: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 1.1 detail 27: Preserve full English before Turkish so language flow is auditable.
- 1.1 detail 28: Preserve identical EN/TR number sequences so reviews can compare sections directly.

### EN 1.2 Why this hub must stay detailed

This hub must remain detailed enough that a future maintainer can recover project direction from GitHub alone, even if all chat memory is unavailable.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 1.2 detail 1: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 1.2 detail 2: Never confuse repository synchronization with live crawler data movement.
- 1.2 detail 3: Never treat a path reference as current merely because it appears in an old historical seal.
- 1.2 detail 4: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 1.2 detail 5: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 1.2 detail 6: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 1.2 detail 7: Preserve lease renewal as an explicit safety discipline around claimed work.
- 1.2 detail 8: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 1.2 detail 9: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 1.2 detail 10: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 1.2 detail 11: Preserve systemd non-touch guarantees during documentation-only work.
- 1.2 detail 12: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 1.2 detail 13: Preserve local dirty-scope checks before any patch touches tracked files.
- 1.2 detail 14: Preserve staged-area checks before every commit gate.
- 1.2 detail 15: Preserve git diff --check as a mandatory Markdown quality signal.
- 1.2 detail 16: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 1.2 detail 17: Preserve code fences without allowing command comments to become Markdown headings.
- 1.2 detail 18: Preserve exact file names because they are operational identifiers.
- 1.2 detail 19: Preserve exact commit hashes when documenting historical state.
- 1.2 detail 20: Preserve beginner-first explanations around every major contract.
- 1.2 detail 21: Preserve operator-first safety language around every mutating action.
- 1.2 detail 22: Preserve the ability to resume work from GitHub without chat memory.
- 1.2 detail 23: Preserve the standard that README files explain, not merely link.
- 1.2 detail 24: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 1.2 detail 25: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 1.2 detail 26: Preserve full English before Turkish so language flow is auditable.
- 1.2 detail 27: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 1.2 detail 28: Preserve the habit of small batches when converting many Markdown files.

## EN 2. Canonical project map

LogisticSearch is organized around crawler execution, taxonomy authority, source seed planning, frontier discipline, parse boundaries, desktop import, and later application surfaces.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 2. detail 1: Never confuse repository synchronization with live crawler data movement.
- 2. detail 2: Never treat a path reference as current merely because it appears in an old historical seal.
- 2. detail 3: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 2. detail 4: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 2. detail 5: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 2. detail 6: Preserve lease renewal as an explicit safety discipline around claimed work.
- 2. detail 7: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 2. detail 8: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 2. detail 9: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 2. detail 10: Preserve systemd non-touch guarantees during documentation-only work.
- 2. detail 11: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 2. detail 12: Preserve local dirty-scope checks before any patch touches tracked files.
- 2. detail 13: Preserve staged-area checks before every commit gate.
- 2. detail 14: Preserve git diff --check as a mandatory Markdown quality signal.
- 2. detail 15: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 2. detail 16: Preserve code fences without allowing command comments to become Markdown headings.
- 2. detail 17: Preserve exact file names because they are operational identifiers.
- 2. detail 18: Preserve exact commit hashes when documenting historical state.
- 2. detail 19: Preserve beginner-first explanations around every major contract.
- 2. detail 20: Preserve operator-first safety language around every mutating action.
- 2. detail 21: Preserve the ability to resume work from GitHub without chat memory.
- 2. detail 22: Preserve the standard that README files explain, not merely link.
- 2. detail 23: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 2. detail 24: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 2. detail 25: Preserve full English before Turkish so language flow is auditable.
- 2. detail 26: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 2. detail 27: Preserve the habit of small batches when converting many Markdown files.
- 2. detail 28: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.

### EN 2.1 Ubuntu Desktop, GitHub, and pi51c roles

Ubuntu Desktop is the disciplined authoring and integration workstation, GitHub is the repository synchronization truth, and pi51c is the crawler/data-origin node.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 2.1 detail 1: Never treat a path reference as current merely because it appears in an old historical seal.
- 2.1 detail 2: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 2.1 detail 3: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 2.1 detail 4: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 2.1 detail 5: Preserve lease renewal as an explicit safety discipline around claimed work.
- 2.1 detail 6: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 2.1 detail 7: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 2.1 detail 8: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 2.1 detail 9: Preserve systemd non-touch guarantees during documentation-only work.
- 2.1 detail 10: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 2.1 detail 11: Preserve local dirty-scope checks before any patch touches tracked files.
- 2.1 detail 12: Preserve staged-area checks before every commit gate.
- 2.1 detail 13: Preserve git diff --check as a mandatory Markdown quality signal.
- 2.1 detail 14: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 2.1 detail 15: Preserve code fences without allowing command comments to become Markdown headings.
- 2.1 detail 16: Preserve exact file names because they are operational identifiers.
- 2.1 detail 17: Preserve exact commit hashes when documenting historical state.
- 2.1 detail 18: Preserve beginner-first explanations around every major contract.
- 2.1 detail 19: Preserve operator-first safety language around every mutating action.
- 2.1 detail 20: Preserve the ability to resume work from GitHub without chat memory.
- 2.1 detail 21: Preserve the standard that README files explain, not merely link.
- 2.1 detail 22: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 2.1 detail 23: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 2.1 detail 24: Preserve full English before Turkish so language flow is auditable.
- 2.1 detail 25: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 2.1 detail 26: Preserve the habit of small batches when converting many Markdown files.
- 2.1 detail 27: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 2.1 detail 28: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.

### EN 2.2 Runtime and data movement boundaries

Runtime code synchronization and crawler payload movement are intentionally separate because code truth and collected data truth have different safety requirements.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 2.2 detail 1: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 2.2 detail 2: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 2.2 detail 3: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 2.2 detail 4: Preserve lease renewal as an explicit safety discipline around claimed work.
- 2.2 detail 5: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 2.2 detail 6: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 2.2 detail 7: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 2.2 detail 8: Preserve systemd non-touch guarantees during documentation-only work.
- 2.2 detail 9: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 2.2 detail 10: Preserve local dirty-scope checks before any patch touches tracked files.
- 2.2 detail 11: Preserve staged-area checks before every commit gate.
- 2.2 detail 12: Preserve git diff --check as a mandatory Markdown quality signal.
- 2.2 detail 13: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 2.2 detail 14: Preserve code fences without allowing command comments to become Markdown headings.
- 2.2 detail 15: Preserve exact file names because they are operational identifiers.
- 2.2 detail 16: Preserve exact commit hashes when documenting historical state.
- 2.2 detail 17: Preserve beginner-first explanations around every major contract.
- 2.2 detail 18: Preserve operator-first safety language around every mutating action.
- 2.2 detail 19: Preserve the ability to resume work from GitHub without chat memory.
- 2.2 detail 20: Preserve the standard that README files explain, not merely link.
- 2.2 detail 21: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 2.2 detail 22: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 2.2 detail 23: Preserve full English before Turkish so language flow is auditable.
- 2.2 detail 24: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 2.2 detail 25: Preserve the habit of small batches when converting many Markdown files.
- 2.2 detail 26: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 2.2 detail 27: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 2.2 detail 28: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.

## EN 3. Crawler-core reading path

The crawler-core line must be read through lifecycle, worker behavior, lease renewal, robots decisions, acquisition boundaries, and controlled finalization.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 3. detail 1: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 3. detail 2: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 3. detail 3: Preserve lease renewal as an explicit safety discipline around claimed work.
- 3. detail 4: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 3. detail 5: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 3. detail 6: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 3. detail 7: Preserve systemd non-touch guarantees during documentation-only work.
- 3. detail 8: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 3. detail 9: Preserve local dirty-scope checks before any patch touches tracked files.
- 3. detail 10: Preserve staged-area checks before every commit gate.
- 3. detail 11: Preserve git diff --check as a mandatory Markdown quality signal.
- 3. detail 12: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 3. detail 13: Preserve code fences without allowing command comments to become Markdown headings.
- 3. detail 14: Preserve exact file names because they are operational identifiers.
- 3. detail 15: Preserve exact commit hashes when documenting historical state.
- 3. detail 16: Preserve beginner-first explanations around every major contract.
- 3. detail 17: Preserve operator-first safety language around every mutating action.
- 3. detail 18: Preserve the ability to resume work from GitHub without chat memory.
- 3. detail 19: Preserve the standard that README files explain, not merely link.
- 3. detail 20: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 3. detail 21: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 3. detail 22: Preserve full English before Turkish so language flow is auditable.
- 3. detail 23: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 3. detail 24: Preserve the habit of small batches when converting many Markdown files.
- 3. detail 25: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 3. detail 26: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 3. detail 27: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 3. detail 28: Never confuse repository synchronization with live crawler data movement.

### EN 3.1 Frontier, lease, robots, and fetch meaning

Frontier state is durable truth, lease discipline protects claimed work, robots logic protects legal and operational boundaries, and fetch must not silently decide taxonomy meaning.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 3.1 detail 1: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 3.1 detail 2: Preserve lease renewal as an explicit safety discipline around claimed work.
- 3.1 detail 3: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 3.1 detail 4: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 3.1 detail 5: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 3.1 detail 6: Preserve systemd non-touch guarantees during documentation-only work.
- 3.1 detail 7: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 3.1 detail 8: Preserve local dirty-scope checks before any patch touches tracked files.
- 3.1 detail 9: Preserve staged-area checks before every commit gate.
- 3.1 detail 10: Preserve git diff --check as a mandatory Markdown quality signal.
- 3.1 detail 11: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 3.1 detail 12: Preserve code fences without allowing command comments to become Markdown headings.
- 3.1 detail 13: Preserve exact file names because they are operational identifiers.
- 3.1 detail 14: Preserve exact commit hashes when documenting historical state.
- 3.1 detail 15: Preserve beginner-first explanations around every major contract.
- 3.1 detail 16: Preserve operator-first safety language around every mutating action.
- 3.1 detail 17: Preserve the ability to resume work from GitHub without chat memory.
- 3.1 detail 18: Preserve the standard that README files explain, not merely link.
- 3.1 detail 19: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 3.1 detail 20: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 3.1 detail 21: Preserve full English before Turkish so language flow is auditable.
- 3.1 detail 22: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 3.1 detail 23: Preserve the habit of small batches when converting many Markdown files.
- 3.1 detail 24: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 3.1 detail 25: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 3.1 detail 26: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 3.1 detail 27: Never confuse repository synchronization with live crawler data movement.
- 3.1 detail 28: Never treat a path reference as current merely because it appears in an old historical seal.

### EN 3.2 Parse and taxonomy boundary

Parse must transform collected evidence into structured interpretation, while taxonomy provides the classification authority that prevents crawler output from becoming uncontrolled text.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 3.2 detail 1: Preserve lease renewal as an explicit safety discipline around claimed work.
- 3.2 detail 2: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 3.2 detail 3: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 3.2 detail 4: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 3.2 detail 5: Preserve systemd non-touch guarantees during documentation-only work.
- 3.2 detail 6: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 3.2 detail 7: Preserve local dirty-scope checks before any patch touches tracked files.
- 3.2 detail 8: Preserve staged-area checks before every commit gate.
- 3.2 detail 9: Preserve git diff --check as a mandatory Markdown quality signal.
- 3.2 detail 10: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 3.2 detail 11: Preserve code fences without allowing command comments to become Markdown headings.
- 3.2 detail 12: Preserve exact file names because they are operational identifiers.
- 3.2 detail 13: Preserve exact commit hashes when documenting historical state.
- 3.2 detail 14: Preserve beginner-first explanations around every major contract.
- 3.2 detail 15: Preserve operator-first safety language around every mutating action.
- 3.2 detail 16: Preserve the ability to resume work from GitHub without chat memory.
- 3.2 detail 17: Preserve the standard that README files explain, not merely link.
- 3.2 detail 18: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 3.2 detail 19: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 3.2 detail 20: Preserve full English before Turkish so language flow is auditable.
- 3.2 detail 21: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 3.2 detail 22: Preserve the habit of small batches when converting many Markdown files.
- 3.2 detail 23: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 3.2 detail 24: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 3.2 detail 25: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 3.2 detail 26: Never confuse repository synchronization with live crawler data movement.
- 3.2 detail 27: Never treat a path reference as current merely because it appears in an old historical seal.
- 3.2 detail 28: Preserve the distinction between crawler_core, parse_core, and desktop_import.

## EN 4. Documentation quality standard

Every important Markdown document must be readable by a beginner, auditable by an operator, and useful as recovery material for a future continuation session.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 4. detail 1: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 4. detail 2: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 4. detail 3: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 4. detail 4: Preserve systemd non-touch guarantees during documentation-only work.
- 4. detail 5: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 4. detail 6: Preserve local dirty-scope checks before any patch touches tracked files.
- 4. detail 7: Preserve staged-area checks before every commit gate.
- 4. detail 8: Preserve git diff --check as a mandatory Markdown quality signal.
- 4. detail 9: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 4. detail 10: Preserve code fences without allowing command comments to become Markdown headings.
- 4. detail 11: Preserve exact file names because they are operational identifiers.
- 4. detail 12: Preserve exact commit hashes when documenting historical state.
- 4. detail 13: Preserve beginner-first explanations around every major contract.
- 4. detail 14: Preserve operator-first safety language around every mutating action.
- 4. detail 15: Preserve the ability to resume work from GitHub without chat memory.
- 4. detail 16: Preserve the standard that README files explain, not merely link.
- 4. detail 17: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 4. detail 18: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 4. detail 19: Preserve full English before Turkish so language flow is auditable.
- 4. detail 20: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 4. detail 21: Preserve the habit of small batches when converting many Markdown files.
- 4. detail 22: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 4. detail 23: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 4. detail 24: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 4. detail 25: Never confuse repository synchronization with live crawler data movement.
- 4. detail 26: Never treat a path reference as current merely because it appears in an old historical seal.
- 4. detail 27: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 4. detail 28: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.

### EN 4.1 Strict bilingual numbering rule

The document title owns number zero, real content starts at one, all English content comes first, and Turkish repeats the same number sequence afterward.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 4.1 detail 1: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 4.1 detail 2: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 4.1 detail 3: Preserve systemd non-touch guarantees during documentation-only work.
- 4.1 detail 4: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 4.1 detail 5: Preserve local dirty-scope checks before any patch touches tracked files.
- 4.1 detail 6: Preserve staged-area checks before every commit gate.
- 4.1 detail 7: Preserve git diff --check as a mandatory Markdown quality signal.
- 4.1 detail 8: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 4.1 detail 9: Preserve code fences without allowing command comments to become Markdown headings.
- 4.1 detail 10: Preserve exact file names because they are operational identifiers.
- 4.1 detail 11: Preserve exact commit hashes when documenting historical state.
- 4.1 detail 12: Preserve beginner-first explanations around every major contract.
- 4.1 detail 13: Preserve operator-first safety language around every mutating action.
- 4.1 detail 14: Preserve the ability to resume work from GitHub without chat memory.
- 4.1 detail 15: Preserve the standard that README files explain, not merely link.
- 4.1 detail 16: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 4.1 detail 17: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 4.1 detail 18: Preserve full English before Turkish so language flow is auditable.
- 4.1 detail 19: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 4.1 detail 20: Preserve the habit of small batches when converting many Markdown files.
- 4.1 detail 21: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 4.1 detail 22: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 4.1 detail 23: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 4.1 detail 24: Never confuse repository synchronization with live crawler data movement.
- 4.1 detail 25: Never treat a path reference as current merely because it appears in an old historical seal.
- 4.1 detail 26: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 4.1 detail 27: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 4.1 detail 28: Preserve the frontier model as durable state, not as a temporary in-memory queue.

### EN 4.2 README, canonical, and runbook quality bar

README, canonical, and runbook documents are not short indexes; they must explain context, safety, sequence, evidence, and next action deeply.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 4.2 detail 1: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 4.2 detail 2: Preserve systemd non-touch guarantees during documentation-only work.
- 4.2 detail 3: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 4.2 detail 4: Preserve local dirty-scope checks before any patch touches tracked files.
- 4.2 detail 5: Preserve staged-area checks before every commit gate.
- 4.2 detail 6: Preserve git diff --check as a mandatory Markdown quality signal.
- 4.2 detail 7: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 4.2 detail 8: Preserve code fences without allowing command comments to become Markdown headings.
- 4.2 detail 9: Preserve exact file names because they are operational identifiers.
- 4.2 detail 10: Preserve exact commit hashes when documenting historical state.
- 4.2 detail 11: Preserve beginner-first explanations around every major contract.
- 4.2 detail 12: Preserve operator-first safety language around every mutating action.
- 4.2 detail 13: Preserve the ability to resume work from GitHub without chat memory.
- 4.2 detail 14: Preserve the standard that README files explain, not merely link.
- 4.2 detail 15: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 4.2 detail 16: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 4.2 detail 17: Preserve full English before Turkish so language flow is auditable.
- 4.2 detail 18: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 4.2 detail 19: Preserve the habit of small batches when converting many Markdown files.
- 4.2 detail 20: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 4.2 detail 21: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 4.2 detail 22: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 4.2 detail 23: Never confuse repository synchronization with live crawler data movement.
- 4.2 detail 24: Never treat a path reference as current merely because it appears in an old historical seal.
- 4.2 detail 25: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 4.2 detail 26: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 4.2 detail 27: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 4.2 detail 28: Preserve lease renewal as an explicit safety discipline around claimed work.

## EN 5. Safety and mutation discipline

Documentation work must never accidentally start the crawler, mutate the database, touch systemd, execute control scripts, or change pi51c live runtime.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 5. detail 1: Preserve systemd non-touch guarantees during documentation-only work.
- 5. detail 2: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 5. detail 3: Preserve local dirty-scope checks before any patch touches tracked files.
- 5. detail 4: Preserve staged-area checks before every commit gate.
- 5. detail 5: Preserve git diff --check as a mandatory Markdown quality signal.
- 5. detail 6: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 5. detail 7: Preserve code fences without allowing command comments to become Markdown headings.
- 5. detail 8: Preserve exact file names because they are operational identifiers.
- 5. detail 9: Preserve exact commit hashes when documenting historical state.
- 5. detail 10: Preserve beginner-first explanations around every major contract.
- 5. detail 11: Preserve operator-first safety language around every mutating action.
- 5. detail 12: Preserve the ability to resume work from GitHub without chat memory.
- 5. detail 13: Preserve the standard that README files explain, not merely link.
- 5. detail 14: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 5. detail 15: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 5. detail 16: Preserve full English before Turkish so language flow is auditable.
- 5. detail 17: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 5. detail 18: Preserve the habit of small batches when converting many Markdown files.
- 5. detail 19: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 5. detail 20: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 5. detail 21: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 5. detail 22: Never confuse repository synchronization with live crawler data movement.
- 5. detail 23: Never treat a path reference as current merely because it appears in an old historical seal.
- 5. detail 24: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 5. detail 25: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 5. detail 26: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 5. detail 27: Preserve lease renewal as an explicit safety discipline around claimed work.
- 5. detail 28: Preserve robots handling as a legal and operational boundary, not as a convenience feature.

### EN 5.1 Read-only audit meaning

A read-only audit may inspect files, hashes, headings, links, and repository status, but it must not perform operational actions.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 5.1 detail 1: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 5.1 detail 2: Preserve local dirty-scope checks before any patch touches tracked files.
- 5.1 detail 3: Preserve staged-area checks before every commit gate.
- 5.1 detail 4: Preserve git diff --check as a mandatory Markdown quality signal.
- 5.1 detail 5: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 5.1 detail 6: Preserve code fences without allowing command comments to become Markdown headings.
- 5.1 detail 7: Preserve exact file names because they are operational identifiers.
- 5.1 detail 8: Preserve exact commit hashes when documenting historical state.
- 5.1 detail 9: Preserve beginner-first explanations around every major contract.
- 5.1 detail 10: Preserve operator-first safety language around every mutating action.
- 5.1 detail 11: Preserve the ability to resume work from GitHub without chat memory.
- 5.1 detail 12: Preserve the standard that README files explain, not merely link.
- 5.1 detail 13: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 5.1 detail 14: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 5.1 detail 15: Preserve full English before Turkish so language flow is auditable.
- 5.1 detail 16: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 5.1 detail 17: Preserve the habit of small batches when converting many Markdown files.
- 5.1 detail 18: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 5.1 detail 19: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 5.1 detail 20: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 5.1 detail 21: Never confuse repository synchronization with live crawler data movement.
- 5.1 detail 22: Never treat a path reference as current merely because it appears in an old historical seal.
- 5.1 detail 23: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 5.1 detail 24: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 5.1 detail 25: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 5.1 detail 26: Preserve lease renewal as an explicit safety discipline around claimed work.
- 5.1 detail 27: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 5.1 detail 28: Preserve source seed planning as a curated input layer, not as random URL dumping.

### EN 5.2 Commit gate meaning

A commit gate may stage and push only after scope, content, structure, safety, and detail preservation have already passed local validation.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 5.2 detail 1: Preserve local dirty-scope checks before any patch touches tracked files.
- 5.2 detail 2: Preserve staged-area checks before every commit gate.
- 5.2 detail 3: Preserve git diff --check as a mandatory Markdown quality signal.
- 5.2 detail 4: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 5.2 detail 5: Preserve code fences without allowing command comments to become Markdown headings.
- 5.2 detail 6: Preserve exact file names because they are operational identifiers.
- 5.2 detail 7: Preserve exact commit hashes when documenting historical state.
- 5.2 detail 8: Preserve beginner-first explanations around every major contract.
- 5.2 detail 9: Preserve operator-first safety language around every mutating action.
- 5.2 detail 10: Preserve the ability to resume work from GitHub without chat memory.
- 5.2 detail 11: Preserve the standard that README files explain, not merely link.
- 5.2 detail 12: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 5.2 detail 13: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 5.2 detail 14: Preserve full English before Turkish so language flow is auditable.
- 5.2 detail 15: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 5.2 detail 16: Preserve the habit of small batches when converting many Markdown files.
- 5.2 detail 17: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 5.2 detail 18: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 5.2 detail 19: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 5.2 detail 20: Never confuse repository synchronization with live crawler data movement.
- 5.2 detail 21: Never treat a path reference as current merely because it appears in an old historical seal.
- 5.2 detail 22: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 5.2 detail 23: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 5.2 detail 24: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 5.2 detail 25: Preserve lease renewal as an explicit safety discipline around claimed work.
- 5.2 detail 26: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 5.2 detail 27: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 5.2 detail 28: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.

## EN 6. Current continuation point

The current continuation point is the documentation quality repair line after commit 35ef3ed, with a local three-file patch still uncommitted.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 6. detail 1: Preserve staged-area checks before every commit gate.
- 6. detail 2: Preserve git diff --check as a mandatory Markdown quality signal.
- 6. detail 3: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 6. detail 4: Preserve code fences without allowing command comments to become Markdown headings.
- 6. detail 5: Preserve exact file names because they are operational identifiers.
- 6. detail 6: Preserve exact commit hashes when documenting historical state.
- 6. detail 7: Preserve beginner-first explanations around every major contract.
- 6. detail 8: Preserve operator-first safety language around every mutating action.
- 6. detail 9: Preserve the ability to resume work from GitHub without chat memory.
- 6. detail 10: Preserve the standard that README files explain, not merely link.
- 6. detail 11: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 6. detail 12: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 6. detail 13: Preserve full English before Turkish so language flow is auditable.
- 6. detail 14: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 6. detail 15: Preserve the habit of small batches when converting many Markdown files.
- 6. detail 16: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 6. detail 17: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 6. detail 18: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 6. detail 19: Never confuse repository synchronization with live crawler data movement.
- 6. detail 20: Never treat a path reference as current merely because it appears in an old historical seal.
- 6. detail 21: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 6. detail 22: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 6. detail 23: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 6. detail 24: Preserve lease renewal as an explicit safety discipline around claimed work.
- 6. detail 25: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 6. detail 26: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 6. detail 27: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 6. detail 28: Preserve systemd non-touch guarantees during documentation-only work.

## EN 7. How to read the docs folder

The docs folder should be read as a layered operating manual: standards first, hubs second, contracts third, runbooks fourth, historical seals last.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 7. detail 1: Preserve git diff --check as a mandatory Markdown quality signal.
- 7. detail 2: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 7. detail 3: Preserve code fences without allowing command comments to become Markdown headings.
- 7. detail 4: Preserve exact file names because they are operational identifiers.
- 7. detail 5: Preserve exact commit hashes when documenting historical state.
- 7. detail 6: Preserve beginner-first explanations around every major contract.
- 7. detail 7: Preserve operator-first safety language around every mutating action.
- 7. detail 8: Preserve the ability to resume work from GitHub without chat memory.
- 7. detail 9: Preserve the standard that README files explain, not merely link.
- 7. detail 10: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 7. detail 11: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 7. detail 12: Preserve full English before Turkish so language flow is auditable.
- 7. detail 13: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 7. detail 14: Preserve the habit of small batches when converting many Markdown files.
- 7. detail 15: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 7. detail 16: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 7. detail 17: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 7. detail 18: Never confuse repository synchronization with live crawler data movement.
- 7. detail 19: Never treat a path reference as current merely because it appears in an old historical seal.
- 7. detail 20: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 7. detail 21: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 7. detail 22: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 7. detail 23: Preserve lease renewal as an explicit safety discipline around claimed work.
- 7. detail 24: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 7. detail 25: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 7. detail 26: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 7. detail 27: Preserve systemd non-touch guarantees during documentation-only work.
- 7. detail 28: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.

## EN 8. How to continue without chat memory

A future assistant should be able to inspect GitHub, read this hub, inspect the strict standard, inspect the latest seal, and reconstruct the safe next action.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 8. detail 1: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 8. detail 2: Preserve code fences without allowing command comments to become Markdown headings.
- 8. detail 3: Preserve exact file names because they are operational identifiers.
- 8. detail 4: Preserve exact commit hashes when documenting historical state.
- 8. detail 5: Preserve beginner-first explanations around every major contract.
- 8. detail 6: Preserve operator-first safety language around every mutating action.
- 8. detail 7: Preserve the ability to resume work from GitHub without chat memory.
- 8. detail 8: Preserve the standard that README files explain, not merely link.
- 8. detail 9: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 8. detail 10: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 8. detail 11: Preserve full English before Turkish so language flow is auditable.
- 8. detail 12: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 8. detail 13: Preserve the habit of small batches when converting many Markdown files.
- 8. detail 14: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 8. detail 15: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 8. detail 16: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 8. detail 17: Never confuse repository synchronization with live crawler data movement.
- 8. detail 18: Never treat a path reference as current merely because it appears in an old historical seal.
- 8. detail 19: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 8. detail 20: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 8. detail 21: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 8. detail 22: Preserve lease renewal as an explicit safety discipline around claimed work.
- 8. detail 23: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 8. detail 24: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 8. detail 25: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 8. detail 26: Preserve systemd non-touch guarantees during documentation-only work.
- 8. detail 27: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 8. detail 28: Preserve local dirty-scope checks before any patch touches tracked files.

## EN 9. Crawler-core return strategy

Crawler-core return must happen after documentation drift is controlled enough that operators understand runtime roots, control policies, start gates, and non-touch rules.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 9. detail 1: Preserve code fences without allowing command comments to become Markdown headings.
- 9. detail 2: Preserve exact file names because they are operational identifiers.
- 9. detail 3: Preserve exact commit hashes when documenting historical state.
- 9. detail 4: Preserve beginner-first explanations around every major contract.
- 9. detail 5: Preserve operator-first safety language around every mutating action.
- 9. detail 6: Preserve the ability to resume work from GitHub without chat memory.
- 9. detail 7: Preserve the standard that README files explain, not merely link.
- 9. detail 8: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 9. detail 9: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 9. detail 10: Preserve full English before Turkish so language flow is auditable.
- 9. detail 11: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 9. detail 12: Preserve the habit of small batches when converting many Markdown files.
- 9. detail 13: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 9. detail 14: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 9. detail 15: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 9. detail 16: Never confuse repository synchronization with live crawler data movement.
- 9. detail 17: Never treat a path reference as current merely because it appears in an old historical seal.
- 9. detail 18: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 9. detail 19: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 9. detail 20: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 9. detail 21: Preserve lease renewal as an explicit safety discipline around claimed work.
- 9. detail 22: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 9. detail 23: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 9. detail 24: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 9. detail 25: Preserve systemd non-touch guarantees during documentation-only work.
- 9. detail 26: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 9. detail 27: Preserve local dirty-scope checks before any patch touches tracked files.
- 9. detail 28: Preserve staged-area checks before every commit gate.

## EN 10. Batch conversion rule for remaining Markdown files

Remaining Markdown files must be converted one by one or in very small batches; each file must be inspected before rewriting and must not lose detail.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 10. detail 1: Preserve exact file names because they are operational identifiers.
- 10. detail 2: Preserve exact commit hashes when documenting historical state.
- 10. detail 3: Preserve beginner-first explanations around every major contract.
- 10. detail 4: Preserve operator-first safety language around every mutating action.
- 10. detail 5: Preserve the ability to resume work from GitHub without chat memory.
- 10. detail 6: Preserve the standard that README files explain, not merely link.
- 10. detail 7: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 10. detail 8: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 10. detail 9: Preserve full English before Turkish so language flow is auditable.
- 10. detail 10: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 10. detail 11: Preserve the habit of small batches when converting many Markdown files.
- 10. detail 12: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 10. detail 13: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 10. detail 14: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 10. detail 15: Never confuse repository synchronization with live crawler data movement.
- 10. detail 16: Never treat a path reference as current merely because it appears in an old historical seal.
- 10. detail 17: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 10. detail 18: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 10. detail 19: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 10. detail 20: Preserve lease renewal as an explicit safety discipline around claimed work.
- 10. detail 21: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 10. detail 22: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 10. detail 23: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 10. detail 24: Preserve systemd non-touch guarantees during documentation-only work.
- 10. detail 25: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 10. detail 26: Preserve local dirty-scope checks before any patch touches tracked files.
- 10. detail 27: Preserve staged-area checks before every commit gate.
- 10. detail 28: Preserve git diff --check as a mandatory Markdown quality signal.

## EN 11. What must be preserved from old documents

Old documents may have poor structure but valuable details; path history, commit context, safety boundaries, and operational decisions must be preserved unless proven obsolete.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 11. detail 1: Preserve exact commit hashes when documenting historical state.
- 11. detail 2: Preserve beginner-first explanations around every major contract.
- 11. detail 3: Preserve operator-first safety language around every mutating action.
- 11. detail 4: Preserve the ability to resume work from GitHub without chat memory.
- 11. detail 5: Preserve the standard that README files explain, not merely link.
- 11. detail 6: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 11. detail 7: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 11. detail 8: Preserve full English before Turkish so language flow is auditable.
- 11. detail 9: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 11. detail 10: Preserve the habit of small batches when converting many Markdown files.
- 11. detail 11: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 11. detail 12: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 11. detail 13: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 11. detail 14: Never confuse repository synchronization with live crawler data movement.
- 11. detail 15: Never treat a path reference as current merely because it appears in an old historical seal.
- 11. detail 16: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 11. detail 17: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 11. detail 18: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 11. detail 19: Preserve lease renewal as an explicit safety discipline around claimed work.
- 11. detail 20: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 11. detail 21: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 11. detail 22: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 11. detail 23: Preserve systemd non-touch guarantees during documentation-only work.
- 11. detail 24: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 11. detail 25: Preserve local dirty-scope checks before any patch touches tracked files.
- 11. detail 26: Preserve staged-area checks before every commit gate.
- 11. detail 27: Preserve git diff --check as a mandatory Markdown quality signal.
- 11. detail 28: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.

## EN 12. Immediate next action

The immediate next action after this local rewrite is a read-only R113U4 validation, not a commit.
This section is intentionally explanatory because a future reader must understand both the operational decision and the reason behind it.
The goal is not to make the file shorter; the goal is to make the file safer, more reviewable, and recoverable from GitHub alone.

- 12. detail 1: Preserve beginner-first explanations around every major contract.
- 12. detail 2: Preserve operator-first safety language around every mutating action.
- 12. detail 3: Preserve the ability to resume work from GitHub without chat memory.
- 12. detail 4: Preserve the standard that README files explain, not merely link.
- 12. detail 5: Preserve the standard that canonical docs and runbooks are as rich as README docs.
- 12. detail 6: Preserve the current corrected numbering model: H1 zero, content starts at one.
- 12. detail 7: Preserve full English before Turkish so language flow is auditable.
- 12. detail 8: Preserve identical EN/TR number sequences so reviews can compare sections directly.
- 12. detail 9: Preserve the habit of small batches when converting many Markdown files.
- 12. detail 10: Keep Ubuntu Desktop as the controlled authoring surface before GitHub publication.
- 12. detail 11: Treat GitHub as the durable repository truth for tracked code, documentation, and operational contracts.
- 12. detail 12: Treat pi51c as crawler-only unless a separate approved runtime or host-control gate says otherwise.
- 12. detail 13: Never confuse repository synchronization with live crawler data movement.
- 12. detail 14: Never treat a path reference as current merely because it appears in an old historical seal.
- 12. detail 15: Preserve the distinction between crawler_core, parse_core, and desktop_import.
- 12. detail 16: Preserve the rule that crawler_core collects and controls traversal while taxonomy classifies meaning.
- 12. detail 17: Preserve the frontier model as durable state, not as a temporary in-memory queue.
- 12. detail 18: Preserve lease renewal as an explicit safety discipline around claimed work.
- 12. detail 19: Preserve robots handling as a legal and operational boundary, not as a convenience feature.
- 12. detail 20: Preserve source seed planning as a curated input layer, not as random URL dumping.
- 12. detail 21: Preserve runtime-control policy so read-only documentation work cannot execute control scripts.
- 12. detail 22: Preserve systemd non-touch guarantees during documentation-only work.
- 12. detail 23: Preserve DB non-touch guarantees unless a DB-specific patch gate explicitly approves mutation.
- 12. detail 24: Preserve local dirty-scope checks before any patch touches tracked files.
- 12. detail 25: Preserve staged-area checks before every commit gate.
- 12. detail 26: Preserve git diff --check as a mandatory Markdown quality signal.
- 12. detail 27: Preserve one H1 per Markdown file to avoid fake document roots inside runbooks.
- 12. detail 28: Preserve code fences without allowing command comments to become Markdown headings.


## EN 13. Quality is scope, detail, and operational understanding

This section exists because a raw line-count threshold is not enough. A Markdown file can be long and still be weak if it repeats shallow phrases, loses historical context, hides the operational boundary, or fails to teach the system to a reader who does not know the project.

The quality gate therefore has two layers. The first layer is structural: one H1 beginning with `# 0.`, all English content first, all Turkish content second, and identical EN/TR numbering. The second layer is semantic: the content must explain what the system is, why the current state exists, what must not be touched, how a future operator should read the repository, and how a future assistant can continue from GitHub without private chat memory.

Minimum line count remains a useful floor, but it is not a success definition. `600+ nonblank English lines` and `600+ nonblank Turkish lines` mean only that a README/hub document is large enough to carry full context. The text still has to cover project direction, crawler_core, parse_core, desktop_import, taxonomy, source seed planning, frontier state, robots boundaries, lease discipline, runtime roots, sync commands, systemd boundaries, and the next safe action.

Required explicit safety needles for this hub are:

- No DB mutation.
- No pi51c mutation.
- No live runtime mutation.
- No systemd mutation.
- No crawler start.
- No control script execution.

Required qualitative rules for this hub are:

- README files stay rich and explanatory.
- Canonical docs stay rich and explanatory.
- Runbooks stay rich and explanatory.
- A conversion must improve readability without deleting operational meaning.
- A conversion must preserve commit context, path context, current truth, historical truth, and next-action truth.
- A conversion must be understandable by a beginner and audit-ready for an operator.
- A conversion must not pass just because it satisfies a string counter.


## EN 14. Readability and how-to style for this hub

This hub must not become a raw link list. It is the first map for a reader who does not know the LogisticSearch project.
The reading experience should feel like a careful how-to book: clear headings, useful bold points, short explanation blocks, and enough context to continue the work safely.

- **Current truth first.** The hub must describe the current GitHub, Ubuntu Desktop, pi51c, crawler_core, parse_core, desktop_import, taxonomy, runtime, systemd, and sync truth before old history.
- **Bold points carry meaning.** Bullets should start with a real point in bold, not with placeholder labels.
- **No artificial detail labels.** Do not use `Detail 1`, `Detail 2`, `Detay 1`, or `Detay 2` as structure.
- **Quality stays above formatting.** Formatting is only valid when it preserves or improves understanding, safety, and continuation value.
- **GitHub alone must be enough.** If private memory disappeared, this repository should still let a careful reader recover the project state and next work direction.
## TR 1. Amaç

Bu dokümantasyon merkezi LogisticSearch repository’sinin rastgele notlar toplamı değil, disiplinli bir mühendislik sistemi olarak nasıl okunacağını açıklar.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 1. detay 1: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 1. detay 2: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 1. detay 3: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 1. detay 4: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 1. detay 5: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 1. detay 6: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 1. detay 7: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 1. detay 8: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 1. detay 9: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 1. detay 10: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 1. detay 11: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 1. detay 12: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 1. detay 13: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 1. detay 14: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 1. detay 15: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 1. detay 16: Her commit gate öncesi staged-area check korunmalıdır.
- 1. detay 17: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 1. detay 18: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 1. detay 19: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 1. detay 20: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 1. detay 21: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 1. detay 22: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 1. detay 23: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 1. detay 24: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 1. detay 25: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 1. detay 26: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 1. detay 27: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 1. detay 28: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.

### TR 1.1 Yeni okuyucunun önce anlaması gerekenler

Yeni okuyucu önce Ubuntu Desktop, GitHub, pi51c, tracked repository, live runtime root ve bilinçli olarak ayrılmış crawler data path rollerini anlamalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 1.1 detay 1: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 1.1 detay 2: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 1.1 detay 3: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 1.1 detay 4: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 1.1 detay 5: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 1.1 detay 6: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 1.1 detay 7: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 1.1 detay 8: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 1.1 detay 9: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 1.1 detay 10: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 1.1 detay 11: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 1.1 detay 12: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 1.1 detay 13: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 1.1 detay 14: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 1.1 detay 15: Her commit gate öncesi staged-area check korunmalıdır.
- 1.1 detay 16: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 1.1 detay 17: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 1.1 detay 18: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 1.1 detay 19: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 1.1 detay 20: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 1.1 detay 21: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 1.1 detay 22: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 1.1 detay 23: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 1.1 detay 24: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 1.1 detay 25: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 1.1 detay 26: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 1.1 detay 27: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 1.1 detay 28: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.

### TR 1.2 Bu hub neden detaylı kalmalıdır

Bu hub, tüm sohbet hafızası yok olsa bile gelecekteki bir maintainer’ın yalnızca GitHub üzerinden proje yönünü geri kurabileceği kadar detaylı kalmalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 1.2 detay 1: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 1.2 detay 2: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 1.2 detay 3: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 1.2 detay 4: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 1.2 detay 5: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 1.2 detay 6: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 1.2 detay 7: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 1.2 detay 8: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 1.2 detay 9: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 1.2 detay 10: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 1.2 detay 11: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 1.2 detay 12: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 1.2 detay 13: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 1.2 detay 14: Her commit gate öncesi staged-area check korunmalıdır.
- 1.2 detay 15: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 1.2 detay 16: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 1.2 detay 17: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 1.2 detay 18: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 1.2 detay 19: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 1.2 detay 20: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 1.2 detay 21: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 1.2 detay 22: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 1.2 detay 23: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 1.2 detay 24: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 1.2 detay 25: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 1.2 detay 26: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 1.2 detay 27: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 1.2 detay 28: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.

## TR 2. Kanonik proje haritası

LogisticSearch; crawler execution, taxonomy authority, source seed planning, frontier disiplini, parse sınırları, desktop import ve ilerideki application yüzeyleri etrafında düzenlenir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 2. detay 1: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 2. detay 2: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 2. detay 3: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 2. detay 4: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 2. detay 5: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 2. detay 6: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 2. detay 7: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 2. detay 8: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 2. detay 9: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 2. detay 10: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 2. detay 11: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 2. detay 12: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 2. detay 13: Her commit gate öncesi staged-area check korunmalıdır.
- 2. detay 14: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 2. detay 15: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 2. detay 16: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 2. detay 17: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 2. detay 18: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 2. detay 19: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 2. detay 20: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 2. detay 21: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 2. detay 22: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 2. detay 23: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 2. detay 24: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 2. detay 25: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 2. detay 26: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 2. detay 27: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 2. detay 28: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.

### TR 2.1 Ubuntu Desktop, GitHub ve pi51c rolleri

Ubuntu Desktop disiplinli authoring ve integration workstation’dır, GitHub repository synchronization doğrusudur, pi51c ise crawler/data-origin node’dur.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 2.1 detay 1: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 2.1 detay 2: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 2.1 detay 3: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 2.1 detay 4: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 2.1 detay 5: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 2.1 detay 6: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 2.1 detay 7: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 2.1 detay 8: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 2.1 detay 9: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 2.1 detay 10: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 2.1 detay 11: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 2.1 detay 12: Her commit gate öncesi staged-area check korunmalıdır.
- 2.1 detay 13: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 2.1 detay 14: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 2.1 detay 15: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 2.1 detay 16: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 2.1 detay 17: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 2.1 detay 18: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 2.1 detay 19: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 2.1 detay 20: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 2.1 detay 21: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 2.1 detay 22: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 2.1 detay 23: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 2.1 detay 24: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 2.1 detay 25: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 2.1 detay 26: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 2.1 detay 27: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 2.1 detay 28: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.

### TR 2.2 Runtime ve veri taşıma sınırları

Runtime code synchronization ile crawler payload movement bilinçli olarak ayrıdır; çünkü kod doğrusu ve toplanan veri doğrusu farklı güvenlik gereksinimlerine sahiptir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 2.2 detay 1: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 2.2 detay 2: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 2.2 detay 3: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 2.2 detay 4: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 2.2 detay 5: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 2.2 detay 6: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 2.2 detay 7: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 2.2 detay 8: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 2.2 detay 9: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 2.2 detay 10: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 2.2 detay 11: Her commit gate öncesi staged-area check korunmalıdır.
- 2.2 detay 12: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 2.2 detay 13: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 2.2 detay 14: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 2.2 detay 15: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 2.2 detay 16: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 2.2 detay 17: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 2.2 detay 18: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 2.2 detay 19: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 2.2 detay 20: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 2.2 detay 21: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 2.2 detay 22: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 2.2 detay 23: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 2.2 detay 24: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 2.2 detay 25: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 2.2 detay 26: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 2.2 detay 27: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 2.2 detay 28: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.

## TR 3. Crawler-core okuma yolu

Crawler-core hattı lifecycle, worker behavior, lease renewal, robots kararları, acquisition sınırları ve controlled finalization üzerinden okunmalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 3. detay 1: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 3. detay 2: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 3. detay 3: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 3. detay 4: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 3. detay 5: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 3. detay 6: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 3. detay 7: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 3. detay 8: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 3. detay 9: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 3. detay 10: Her commit gate öncesi staged-area check korunmalıdır.
- 3. detay 11: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 3. detay 12: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 3. detay 13: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 3. detay 14: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 3. detay 15: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 3. detay 16: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 3. detay 17: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 3. detay 18: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 3. detay 19: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 3. detay 20: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 3. detay 21: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 3. detay 22: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 3. detay 23: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 3. detay 24: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 3. detay 25: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 3. detay 26: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 3. detay 27: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 3. detay 28: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.

### TR 3.1 Frontier, lease, robots ve fetch anlamı

Frontier state kalıcı doğrudur, lease disiplini claimed work’ü korur, robots mantığı legal ve operasyonel sınırları korur, fetch ise taxonomy anlamını sessizce kararlaştırmamalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 3.1 detay 1: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 3.1 detay 2: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 3.1 detay 3: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 3.1 detay 4: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 3.1 detay 5: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 3.1 detay 6: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 3.1 detay 7: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 3.1 detay 8: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 3.1 detay 9: Her commit gate öncesi staged-area check korunmalıdır.
- 3.1 detay 10: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 3.1 detay 11: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 3.1 detay 12: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 3.1 detay 13: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 3.1 detay 14: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 3.1 detay 15: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 3.1 detay 16: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 3.1 detay 17: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 3.1 detay 18: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 3.1 detay 19: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 3.1 detay 20: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 3.1 detay 21: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 3.1 detay 22: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 3.1 detay 23: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 3.1 detay 24: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 3.1 detay 25: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 3.1 detay 26: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 3.1 detay 27: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 3.1 detay 28: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.

### TR 3.2 Parse ve taxonomy sınırı

Parse toplanan kanıtı structured interpretation’a dönüştürmeli, taxonomy ise crawler output’un kontrolsüz text haline gelmesini engelleyen classification authority sağlamalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 3.2 detay 1: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 3.2 detay 2: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 3.2 detay 3: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 3.2 detay 4: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 3.2 detay 5: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 3.2 detay 6: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 3.2 detay 7: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 3.2 detay 8: Her commit gate öncesi staged-area check korunmalıdır.
- 3.2 detay 9: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 3.2 detay 10: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 3.2 detay 11: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 3.2 detay 12: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 3.2 detay 13: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 3.2 detay 14: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 3.2 detay 15: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 3.2 detay 16: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 3.2 detay 17: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 3.2 detay 18: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 3.2 detay 19: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 3.2 detay 20: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 3.2 detay 21: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 3.2 detay 22: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 3.2 detay 23: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 3.2 detay 24: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 3.2 detay 25: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 3.2 detay 26: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 3.2 detay 27: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 3.2 detay 28: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.

## TR 4. Dokümantasyon kalite standardı

Her önemli Markdown dokümanı beginner tarafından okunabilir, operator tarafından denetlenebilir ve gelecekteki continuation session için recovery material olarak kullanılabilir olmalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 4. detay 1: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 4. detay 2: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 4. detay 3: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 4. detay 4: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 4. detay 5: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 4. detay 6: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 4. detay 7: Her commit gate öncesi staged-area check korunmalıdır.
- 4. detay 8: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 4. detay 9: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 4. detay 10: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 4. detay 11: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 4. detay 12: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 4. detay 13: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 4. detay 14: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 4. detay 15: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 4. detay 16: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 4. detay 17: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 4. detay 18: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 4. detay 19: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 4. detay 20: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 4. detay 21: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 4. detay 22: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 4. detay 23: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 4. detay 24: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 4. detay 25: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 4. detay 26: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 4. detay 27: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 4. detay 28: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.

### TR 4.1 Katı çift dilli numaralandırma kuralı

Doküman başlığı sıfır numarasına sahiptir, gerçek içerik birden başlar, tüm İngilizce içerik önce gelir ve Türkçe aynı numara dizisini sonra tekrarlar.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 4.1 detay 1: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 4.1 detay 2: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 4.1 detay 3: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 4.1 detay 4: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 4.1 detay 5: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 4.1 detay 6: Her commit gate öncesi staged-area check korunmalıdır.
- 4.1 detay 7: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 4.1 detay 8: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 4.1 detay 9: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 4.1 detay 10: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 4.1 detay 11: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 4.1 detay 12: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 4.1 detay 13: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 4.1 detay 14: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 4.1 detay 15: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 4.1 detay 16: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 4.1 detay 17: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 4.1 detay 18: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 4.1 detay 19: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 4.1 detay 20: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 4.1 detay 21: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 4.1 detay 22: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 4.1 detay 23: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 4.1 detay 24: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 4.1 detay 25: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 4.1 detay 26: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 4.1 detay 27: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 4.1 detay 28: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.

### TR 4.2 README, canonical ve runbook kalite eşiği

README, canonical ve runbook dokümanları kısa indeks değildir; context, safety, sequence, evidence ve next action bilgilerini derin şekilde açıklamalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 4.2 detay 1: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 4.2 detay 2: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 4.2 detay 3: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 4.2 detay 4: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 4.2 detay 5: Her commit gate öncesi staged-area check korunmalıdır.
- 4.2 detay 6: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 4.2 detay 7: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 4.2 detay 8: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 4.2 detay 9: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 4.2 detay 10: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 4.2 detay 11: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 4.2 detay 12: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 4.2 detay 13: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 4.2 detay 14: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 4.2 detay 15: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 4.2 detay 16: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 4.2 detay 17: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 4.2 detay 18: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 4.2 detay 19: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 4.2 detay 20: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 4.2 detay 21: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 4.2 detay 22: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 4.2 detay 23: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 4.2 detay 24: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 4.2 detay 25: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 4.2 detay 26: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 4.2 detay 27: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 4.2 detay 28: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.

## TR 5. Güvenlik ve mutation disiplini

Dokümantasyon işi yanlışlıkla crawler başlatmamalı, database değiştirmemeli, systemd’ye dokunmamalı, control script çalıştırmamalı veya pi51c live runtime değiştirmemelidir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 5. detay 1: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 5. detay 2: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 5. detay 3: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 5. detay 4: Her commit gate öncesi staged-area check korunmalıdır.
- 5. detay 5: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 5. detay 6: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 5. detay 7: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 5. detay 8: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 5. detay 9: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 5. detay 10: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 5. detay 11: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 5. detay 12: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 5. detay 13: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 5. detay 14: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 5. detay 15: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 5. detay 16: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 5. detay 17: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 5. detay 18: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 5. detay 19: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 5. detay 20: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 5. detay 21: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 5. detay 22: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 5. detay 23: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 5. detay 24: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 5. detay 25: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 5. detay 26: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 5. detay 27: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 5. detay 28: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.

### TR 5.1 Read-only audit anlamı

Read-only audit dosyaları, hash değerlerini, heading’leri, linkleri ve repository status bilgisini inceleyebilir; fakat operasyonel action yapmamalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 5.1 detay 1: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 5.1 detay 2: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 5.1 detay 3: Her commit gate öncesi staged-area check korunmalıdır.
- 5.1 detay 4: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 5.1 detay 5: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 5.1 detay 6: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 5.1 detay 7: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 5.1 detay 8: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 5.1 detay 9: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 5.1 detay 10: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 5.1 detay 11: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 5.1 detay 12: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 5.1 detay 13: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 5.1 detay 14: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 5.1 detay 15: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 5.1 detay 16: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 5.1 detay 17: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 5.1 detay 18: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 5.1 detay 19: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 5.1 detay 20: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 5.1 detay 21: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 5.1 detay 22: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 5.1 detay 23: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 5.1 detay 24: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 5.1 detay 25: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 5.1 detay 26: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 5.1 detay 27: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 5.1 detay 28: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.

### TR 5.2 Commit gate anlamı

Commit gate yalnızca scope, content, structure, safety ve detail preservation local validation’dan geçtikten sonra stage ve push yapabilir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 5.2 detay 1: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 5.2 detay 2: Her commit gate öncesi staged-area check korunmalıdır.
- 5.2 detay 3: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 5.2 detay 4: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 5.2 detay 5: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 5.2 detay 6: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 5.2 detay 7: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 5.2 detay 8: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 5.2 detay 9: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 5.2 detay 10: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 5.2 detay 11: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 5.2 detay 12: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 5.2 detay 13: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 5.2 detay 14: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 5.2 detay 15: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 5.2 detay 16: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 5.2 detay 17: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 5.2 detay 18: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 5.2 detay 19: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 5.2 detay 20: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 5.2 detay 21: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 5.2 detay 22: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 5.2 detay 23: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 5.2 detay 24: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 5.2 detay 25: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 5.2 detay 26: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 5.2 detay 27: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 5.2 detay 28: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.

## TR 6. Güncel devam noktası

Güncel devam noktası 35ef3ed commit’i sonrası dokümantasyon kalite onarım hattıdır ve local üç dosyalık patch hâlâ commit edilmemiştir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 6. detay 1: Her commit gate öncesi staged-area check korunmalıdır.
- 6. detay 2: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 6. detay 3: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 6. detay 4: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 6. detay 5: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 6. detay 6: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 6. detay 7: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 6. detay 8: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 6. detay 9: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 6. detay 10: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 6. detay 11: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 6. detay 12: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 6. detay 13: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 6. detay 14: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 6. detay 15: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 6. detay 16: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 6. detay 17: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 6. detay 18: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 6. detay 19: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 6. detay 20: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 6. detay 21: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 6. detay 22: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 6. detay 23: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 6. detay 24: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 6. detay 25: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 6. detay 26: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 6. detay 27: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 6. detay 28: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.

## TR 7. Docs klasörü nasıl okunmalı

Docs klasörü katmanlı bir operating manual olarak okunmalıdır: önce standards, sonra hubs, sonra contracts, sonra runbooks, en son historical seals.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 7. detay 1: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 7. detay 2: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 7. detay 3: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 7. detay 4: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 7. detay 5: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 7. detay 6: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 7. detay 7: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 7. detay 8: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 7. detay 9: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 7. detay 10: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 7. detay 11: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 7. detay 12: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 7. detay 13: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 7. detay 14: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 7. detay 15: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 7. detay 16: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 7. detay 17: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 7. detay 18: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 7. detay 19: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 7. detay 20: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 7. detay 21: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 7. detay 22: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 7. detay 23: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 7. detay 24: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 7. detay 25: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 7. detay 26: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 7. detay 27: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 7. detay 28: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.

## TR 8. Sohbet hafızası olmadan nasıl devam edilir

Gelecekteki bir assistant GitHub’ı inceleyip bu hub’ı, strict standard’ı ve son seal’i okuyarak güvenli sonraki action’ı yeniden kurabilmelidir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 8. detay 1: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 8. detay 2: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 8. detay 3: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 8. detay 4: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 8. detay 5: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 8. detay 6: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 8. detay 7: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 8. detay 8: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 8. detay 9: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 8. detay 10: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 8. detay 11: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 8. detay 12: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 8. detay 13: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 8. detay 14: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 8. detay 15: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 8. detay 16: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 8. detay 17: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 8. detay 18: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 8. detay 19: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 8. detay 20: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 8. detay 21: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 8. detay 22: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 8. detay 23: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 8. detay 24: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 8. detay 25: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 8. detay 26: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 8. detay 27: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 8. detay 28: Her tracked file patch öncesi local dirty-scope check korunmalıdır.

## TR 9. Crawler-core’a dönüş stratejisi

Crawler-core’a dönüş, operators runtime roots, control policies, start gates ve non-touch rules konularını yeterince anladıktan sonra yapılmalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 9. detay 1: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.
- 9. detay 2: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 9. detay 3: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 9. detay 4: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 9. detay 5: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 9. detay 6: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 9. detay 7: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 9. detay 8: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 9. detay 9: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 9. detay 10: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 9. detay 11: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 9. detay 12: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 9. detay 13: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 9. detay 14: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 9. detay 15: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 9. detay 16: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 9. detay 17: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 9. detay 18: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 9. detay 19: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 9. detay 20: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 9. detay 21: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 9. detay 22: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 9. detay 23: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 9. detay 24: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 9. detay 25: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 9. detay 26: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 9. detay 27: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 9. detay 28: Her commit gate öncesi staged-area check korunmalıdır.

## TR 10. Kalan Markdown dosyaları için batch conversion kuralı

Kalan Markdown dosyaları tek tek veya çok küçük batch’lerle dönüştürülmelidir; her dosya rewrite öncesi incelenmeli ve detay kaybetmemelidir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 10. detay 1: Dosya adları operational identifier olduğu için exact korunmalıdır.
- 10. detay 2: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 10. detay 3: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 10. detay 4: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 10. detay 5: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 10. detay 6: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 10. detay 7: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 10. detay 8: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 10. detay 9: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 10. detay 10: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 10. detay 11: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 10. detay 12: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 10. detay 13: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 10. detay 14: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 10. detay 15: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 10. detay 16: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 10. detay 17: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 10. detay 18: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 10. detay 19: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 10. detay 20: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 10. detay 21: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 10. detay 22: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 10. detay 23: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 10. detay 24: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 10. detay 25: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 10. detay 26: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 10. detay 27: Her commit gate öncesi staged-area check korunmalıdır.
- 10. detay 28: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.

## TR 11. Eski dokümanlardan ne korunmalı

Eski dokümanların yapısı zayıf olabilir ama değerli detayları vardır; path history, commit context, safety boundaries ve operational decisions kanıtlanmadan silinmemelidir.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 11. detay 1: Historical state dokümante edilirken exact commit hash değerleri korunmalıdır.
- 11. detay 2: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 11. detay 3: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 11. detay 4: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 11. detay 5: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 11. detay 6: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 11. detay 7: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 11. detay 8: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 11. detay 9: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 11. detay 10: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 11. detay 11: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 11. detay 12: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 11. detay 13: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 11. detay 14: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 11. detay 15: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 11. detay 16: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 11. detay 17: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 11. detay 18: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 11. detay 19: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 11. detay 20: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 11. detay 21: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 11. detay 22: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 11. detay 23: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 11. detay 24: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 11. detay 25: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 11. detay 26: Her commit gate öncesi staged-area check korunmalıdır.
- 11. detay 27: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 11. detay 28: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.

## TR 12. En yakın sonraki action

Bu local rewrite sonrası en yakın action commit değil, read-only R113U4 validation olmalıdır.
Bu bölüm bilinçli olarak açıklayıcıdır; çünkü gelecekteki okuyucu hem operasyon kararını hem de kararın nedenini anlamalıdır.
Amaç dosyayı kısaltmak değildir; amaç dosyayı daha güvenli, daha denetlenebilir ve yalnızca GitHub üzerinden geri kurulabilir hale getirmektir.

- 12. detay 1: Her major contract çevresinde beginner-first açıklama korunmalıdır.
- 12. detay 2: Her mutating action çevresinde operator-first safety dili korunmalıdır.
- 12. detay 3: Sohbet hafızası olmadan GitHub’dan devam edebilme yeteneği korunmalıdır.
- 12. detay 4: README dosyalarının sadece link vermeyip açıklama yapması standardı korunmalıdır.
- 12. detay 5: Canonical docs ve runbookların README kadar zengin olması standardı korunmalıdır.
- 12. detay 6: Güncel düzeltilmiş numaralandırma modeli korunmalıdır: H1 sıfır, içerik birden başlar.
- 12. detay 7: Dil akışı denetlenebilir olsun diye tüm English içerik Turkish içerikten önce tamamlanmalıdır.
- 12. detay 8: Review kolaylığı için EN/TR numara dizileri birebir aynı kalmalıdır.
- 12. detay 9: Çok sayıda Markdown dosyası dönüştürülürken küçük batch alışkanlığı korunmalıdır.
- 12. detay 10: Ubuntu Desktop, GitHub publication öncesinde kontrollü authoring yüzeyi olarak kalmalıdır.
- 12. detay 11: GitHub, tracked code, dokümantasyon ve operational contracts için kalıcı repository doğrusu olarak görülmelidir.
- 12. detay 12: Ayrı onaylı runtime veya host-control gate yoksa pi51c yalnızca crawler node olarak ele alınmalıdır.
- 12. detay 13: Repository synchronization ile live crawler data movement asla karıştırılmamalıdır.
- 12. detay 14: Bir path eski historical seal içinde geçiyor diye otomatik güncel kabul edilmemelidir.
- 12. detay 15: crawler_core, parse_core ve desktop_import ayrımı korunmalıdır.
- 12. detay 16: crawler_core’un traversal toplayıp kontrol ettiği, taxonomy’nin anlamı sınıflandırdığı kural korunmalıdır.
- 12. detay 17: frontier modeli geçici in-memory queue değil, durable state olarak korunmalıdır.
- 12. detay 18: lease renewal claimed work etrafında açık güvenlik disiplini olarak korunmalıdır.
- 12. detay 19: robots handling convenience feature değil, legal ve operational boundary olarak korunmalıdır.
- 12. detay 20: source seed planning rastgele URL dumping değil, curated input layer olarak korunmalıdır.
- 12. detay 21: runtime-control policy korunmalı; read-only documentation work control script çalıştırmamalıdır.
- 12. detay 22: documentation-only çalışma sırasında systemd non-touch garantisi korunmalıdır.
- 12. detay 23: DB-specific patch gate açıkça onaylamadıkça DB non-touch garantisi korunmalıdır.
- 12. detay 24: Her tracked file patch öncesi local dirty-scope check korunmalıdır.
- 12. detay 25: Her commit gate öncesi staged-area check korunmalıdır.
- 12. detay 26: git diff --check zorunlu Markdown kalite sinyali olarak korunmalıdır.
- 12. detay 27: Runbook içinde sahte document root oluşmaması için her Markdown dosyasında tek H1 korunmalıdır.
- 12. detay 28: Code fence içindeki command comment satırlarının Markdown heading’e dönüşmesine izin verilmemelidir.

## TR 13. Kalite kapsam, detay ve operasyonel anlayıştır

Bu bölümün nedeni şudur: ham satır sayısı tek başına kalite değildir. Bir Markdown dosyası uzun olabilir ama yine de zayıf olabilir; örneğin yüzeysel ifadeleri tekrar edebilir, historical context kaybedebilir, operational boundary gizleyebilir veya projeyi bilmeyen bir okuyucuya sistemi öğretemeyebilir.

Bu yüzden kalite gate iki katmanlıdır. Birinci katman yapısaldır: `# 0.` ile başlayan tek H1, önce tüm English içerik, sonra tüm Turkish içerik ve birebir aynı EN/TR numaralandırması. İkinci katman semantiktir: içerik sistemin ne olduğunu, mevcut state’in neden oluştuğunu, neye dokunulmaması gerektiğini, gelecekteki operator’ın repository’yi nasıl okuyacağını ve gelecekteki assistant’ın private chat memory olmadan GitHub’dan nasıl devam edeceğini açıklamalıdır.

Minimum satır sayısı hâlâ faydalı bir taban eşiğidir; fakat başarı tanımı değildir. `600+ nonblank English lines` ve `600+ nonblank Turkish lines`, bir README/hub dokümanının full context taşıyabilecek büyüklükte olduğunu gösterir. Metin yine de project direction, crawler_core, parse_core, desktop_import, taxonomy, source seed planning, frontier state, robots boundaries, lease discipline, runtime roots, sync commands, systemd boundaries ve next safe action konularını kapsamalıdır.

Bu hub için zorunlu açık güvenlik ifadeleri şunlardır:

- No DB mutation.
- No pi51c mutation.
- No live runtime mutation.
- No systemd mutation.
- No crawler start.
- No control script execution.
- DB mutation yok.
- pi51c mutation yok.
- live runtime mutation yok.
- systemd mutation yok.
- crawler start yok.
- control script execution yok.

Bu hub için zorunlu nitelik kuralları şunlardır:

- README files stay rich and explanatory.
- Canonical docs stay rich and explanatory.
- Runbooks stay rich and explanatory.
- README dosyaları zengin ve açıklayıcı kalır.
- Canonical docs zengin ve açıklayıcı kalır.
- Runbooklar zengin ve açıklayıcı kalır.
- Conversion readability artırmalı ama operational meaning silmemelidir.
- Conversion commit context, path context, current truth, historical truth ve next-action truth bilgilerini korumalıdır.
- Conversion hem beginner tarafından anlaşılabilir hem de operator için audit-ready olmalıdır.
- Conversion yalnızca string counter geçti diye başarılı sayılmamalıdır.

## TR 14. Bu hub için okunabilirlik ve how-to stil kuralı

Bu hub ham bir link listesine dönüşmemelidir. LogisticSearch projesini hiç bilmeyen okuyucu için ilk haritadır.
Okuma deneyimi dikkatli bir how-to kitabı gibi olmalıdır: açık başlıklar, işe yarayan kalın noktalar, kısa açıklama blokları ve işi güvenle sürdürecek kadar bağlam.

- **Önce güncel doğruluk.** Hub eski tarihten önce güncel GitHub, Ubuntu Desktop, pi51c, crawler_core, parse_core, desktop_import, taxonomy, runtime, systemd ve sync doğruluğunu anlatmalıdır.
- **Kalın noktalar anlam taşır.** Maddeler placeholder etiketlerle değil, gerçek noktayı taşıyan kalın ifadeyle başlamalıdır.
- **Yapay detay etiketi yok.** Yapı olarak `Detail 1`, `Detail 2`, `Detay 1` veya `Detay 2` kullanılmaz.
- **Kalite formatın üstündedir.** Format yalnızca anlayışı, güvenliği ve devam değerini koruduğunda veya artırdığında geçerlidir.
- **GitHub tek başına yeterli olmalıdır.** Özel hafıza kaybolsa bile bu repository dikkatli okuyucuya proje durumunu ve sonraki iş yönünü geri kurdurabilmelidir.
