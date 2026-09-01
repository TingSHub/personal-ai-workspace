# Chart Spec Contract

每个可视化由 manifest 提供，builder 只负责渲染，不自行补数字或推断结论。

```json
{
  "chart_id": "t01-growth-profit-gap",
  "type": "dumbbell",
  "claim": "收入增速与利润增速存在差距",
  "unit": "%",
  "precision_policy": "exact",
  "data": [
    {"label": "营业收入", "value": 22.43, "period": "2025", "source_ids": ["E1"]},
    {"label": "归母净利润", "value": 7.19, "period": "2025", "source_ids": ["E2"]}
  ],
  "visual_semantics": {"positive": "green", "risk": "red", "neutral": "orange"},
  "animation": "draw-and-highlight",
  "footnote": "公司合并口径；2025 年全年"
}
```

## Selection rules

- Gap/comparison → `dumbbell` or `diverging-bar`.
- Trend → `line`/`multiline`, never connect incompatible metrics.
- Contribution → `waterfall` or `stacked-bar`.
- Peer comparison → `horizontal-bar`.
- Ownership/event changes → `step-line`.
- Forecast/uncertainty → `range-band`, with estimate labels.
- Chain/relationship → `flow-map`.
- Final operating checks → `validation-dashboard`.

The chart title states the finding, not merely the chart type. Every data point carries a source ID, period, unit and confidence/estimate status where relevant.

`precision_policy` is required for every chart or KPI source:

- `exact`: retain the reported value because the comparison, threshold or ranking depends on it.
- `spoken_rounded`: use a natural spoken form while retaining the exact value in the evidence layer.
- `visual_compact`: show a quantity-level label such as `967+ 亿`; geometry and footnote still derive from the exact value.
