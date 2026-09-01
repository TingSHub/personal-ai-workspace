# Investment Research HTML MVP — Project Context

## Project

investment-research-html-mvp

## Goal

Validate whether an investagent investment research report can be directly converted into a high-quality investor-reading HTML page (minimal loop: investagent + html-ppt-skill). Results first, optimize process later.

## Current Status

in_progress

## Workflow

investagent-html-report-v0.1 (built-in: Step 1 Research Source → Step 2 HTML Generation)

## Required Resources

- html-ppt-skill (HTML generation)
- investagent (input research report)

## Development Rules

- Preserve the full content of the input report (company intro / business model / moat / financials / industry / current changes / investment view / risks / watch metrics); no re-research, no data verification, no new investment judgments
- Page positioning: investor-reading report, NOT slide deck, marketing page, or video script
- Avoid AI-internal fields, metadata, EV numbering, workflow info, audit info
- Self-contained single file (HTML+CSS+SVG), openable locally, no complex services
- Field lists always come from the workspace `.ai/templates/`
- Project execution records go to `logs/` and never enter the asset library directly; at completion, send reusable candidates to Experience Curator

## Known Issues

- None
