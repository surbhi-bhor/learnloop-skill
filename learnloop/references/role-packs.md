# Role packs

These topic maps and examples are starting points, not verified role
requirements. Check them against current job descriptions and practitioners
before presenting them as requirements.

## Senior data engineer

Topic map:

- Pipeline and system design
- Data modeling, including slowly changing dimensions
- Incremental loads, idempotency, and backfills
- Orchestration and recovery
- Data quality and contracts
- Cost, performance, and observability
- Ownership, incident response, and design trade-offs

Practice patterns to investigate: designing a pipeline for late-arriving data;
choosing a partition and join strategy; deduplicating by a composite key; and
explaining safe retries, backfills, and recovery. These are candidates for
validation, not universal interview requirements.

Production scenarios to develop: duplicate or late data, an upstream schema
change, a backfill that must not double-count, and an unexpected cost increase.

Portfolio-sized exercise: make an incremental pipeline safe to rerun and
backfill, then document the design choices and measured outcomes. Keep outcome
fields blank until the learner supplies real numbers.

## Senior BI or analytics engineer

Topic map:

- Metric definitions and governance
- Semantic layers and dimensional modeling
- Performance at scale
- Stakeholder alignment and data contracts
- Dashboard reliability and reconciliation
- Ownership of metric changes and incident response

Practice patterns to investigate: define a KPI and its edge cases; model
conflicting source systems; diagnose why two dashboards disagree; and explain
how to improve a slow dashboard. Validate each against target JDs.

Production scenarios to develop: two dashboards show different values for one
KPI, a metric definition drifts, or a growing table makes a dashboard slow.

Portfolio-sized exercise: model one pipeline output as a star schema, document
the metric definitions, and chart the learner's own study metrics in a BI
tool. Avoid putting private Learning Log data in a public portfolio without
the learner's choice.

## Software engineer

Topic map: data structures and algorithms, system design, API design,
concurrency, testing, debugging and code review, ownership of production
services.

Practice patterns to investigate: classic algorithm patterns (two pointers,
sliding window, hashing, BFS/DFS, heaps, dynamic programming); designing a
rate limiter, cache or URL shortener; reviewing a pull request for bugs.

Production scenarios to develop: a memory leak, a race condition, a slow
endpoint, a breaking API change.

Portfolio-sized exercise: add tests, logging and one performance fix to a
service the learner owns.

## QA or SDET

Topic map: test design (equivalence classes, boundary values, pairwise), test
automation frameworks, API and UI testing, CI pipelines, flaky-test diagnosis,
test data management, risk-based prioritization.

Practice patterns to investigate: write test cases for a login or payment
flow; automate an API test with assertions on status, schema and data; explain
why a test is flaky and how to fix it.

Production scenarios to develop: a release blocked by flaky tests, a bug that
escaped because of missing boundary tests, test data that leaks between runs.

Portfolio-sized exercise: build an automated test suite with CI for a small
open-source or personal project.

## AI or ML engineer

Topic map: model APIs and prompting, retrieval (embeddings, chunking, vector
search), evaluation, agents and tool use, fine-tuning basics, cost and
latency, safety and monitoring.

Practice patterns to investigate: design a retrieval pipeline and justify the
chunk size; build an evaluation set and metric for an LLM feature; explain how
to cut latency or cost of a model call.

Production scenarios to develop: answers drift after a prompt change,
retrieval returns stale documents, cost spikes after a traffic increase.

Portfolio-sized exercise: build a small retrieval or agent feature with an
evaluation script and a written comparison of two approaches.

## Any other role

If the Profile names a role with no pack here, build a temporary pack from the
Profile and any job descriptions the learner has pasted (Skill Map rows): list
the recurring skills as the topic map, and label every item "derived from your
job descriptions, not verified". Offer to save it as a new section in this
file.

## Interview questions for a topic

When a note needs interview questions, pick well-known question patterns for
the learner's target role, not invented puzzles. Example: after Python lists
for a data engineer or BI target, use deduplicating while keeping order,
flattening nested lists, top-K items, sliding-window sums, merging sorted
lists, and grouping records by key. Give each question a difficulty
(Foundational, Intermediate, Advanced) and one line on why the role cares. If
unsure whether a pattern is really asked for that role, say so.

## Reuse across roles

For every pack, keep senior-level emphasis on ownership, design decisions,
trade-offs, and failure response. Label the pack's examples as hypotheses
until they are checked against real job descriptions. Do not invent employer
expectations, learner achievements, or measured project outcomes.
