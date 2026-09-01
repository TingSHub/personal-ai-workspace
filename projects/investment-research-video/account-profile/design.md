# 账本两面 v1 Design Tokens

```yaml
canvas: 1920x1080
visual_style: 'editorial-paper'
background: '#faf7f1'
surface: '#fffdf8'
ink: '#211d18'
ink_secondary: '#6a6354'
accent_red: '#a6192e'
growth_green: '#1e6b4c'
neutral_amber: '#8a5e15'
hairline: '#e7e0d2'
card_radius: 2px
content_density: medium
speaker_pills: false
topic_navigation: true
visual_priority: chart > table > text
font_display_resource: 'font.noto-serif-sc'
font_candidate_resource: 'font.zhuque-fangsong'
font_license: 'SIL Open Font License 1.1; retain LICENSE with asset'
font_fallback: 'Source Han Serif SC, Songti SC, serif'
font_body: 'Noto Sans SC, Source Han Sans SC, Microsoft YaHei, sans-serif'
persistent_navigator: true
persistent_navigator_background: 'transparent'
persistent_navigator_blur: true
persistent_progress_height: 2px
persistent_progress_opacity: 1
```

## Component contract

- `ShowHeader(company, showName, disclaimer)`
- `SpeakerPill(speaker, active)`
- `TopicTitle(index, question)`
- `MetricCard(color, label, value, explanation)`
- `ChartFrame(type, claim, data, source_ids)`
- `AgendaStrip(items)`
- `TableFallback(rows, unit)`
- `OwnershipRoute(steps)`
- `SubtitleRail(text, speaker)`
- `TopicNavigation(topics, activeTopicId)`
- `PersistentNavigator(chapters, activeChapterId, elapsed, total)` — root-level overlay, independent from page scenes

Each component is driven by account/episode data, not by company-specific selectors or hardcoded text. If a claim has a valid chart spec, render a chart first; use a table only when the relationship is not chartable; use text only for context, caveats and conclusions. The persistent navigator is a root-level layer and must remain visible while page scenes change.
