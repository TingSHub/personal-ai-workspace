# video-publish-review — Project Context

## Project

video-publish-review (Video Publish Review)

## Goal

Run a standardized retrospective on every published video: traffic data collection → funnel/ratio diagnostics → attribution → improvement items → write-back decision, so the next video measurably improves on publish strategy and content structure. Results are kept per-video and compound into account-level assets.

## Current Status

in_progress

## Workflow

- publish-review (registration check → collection → diagnostics → attribution → improvements → write-back decision)

## Required Resources

- douyin-creator-tools (P1 collection, required)
- experience-curator (P5 write-back decision, required at P5)
- boundary-rewrite (optional, P4 compliant rewrite of sharp claims)
- video-hook-intro (optional, P4 hook design reference)

## Development Rules

- One folder per published video: `outputs/retrospectives/<published_date>-<slug>/`
- Metrics snapshot JSON is the single source of truth for traffic facts; attribution reports cite snapshot data only, never memory
- Collection runs through douyin-creator-tools logged-in automation under its usage constraints (low frequency, no anti-crawl bypass, stop on failure)
- Retrospective reports must state unverified items explicitly; keep inference separate from fact
- No write-back decisions inside this project; candidates go to the user, then experience-curator
- Field lists always come from the workspace `.ai/templates/`
- Project execution records go to `logs/` and never enter the asset library directly; at completion, send reusable candidates to Experience Curator

## Known Issues

- Official exports lack per-video retention curves and audience profiles (page-only), so mid-video drop-off attribution relies on inference; manual screenshots as fallback at T+7
