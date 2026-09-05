# Project scripts

项目级脚本只保留无法跨项目复用、且直接服务本项目产物的工具。可跨项目复用的选题信号扫描已沉淀为 `topic-forward-signal-scanner` Skill，调用其资源目录下的脚本。

当前脚本：

- `build-topic-candidates.py`：读取 `signals.json`，按涨停/涨幅信号生成有限规模的公司种子与行业聚集种子，输出 `candidate-pool.json`。重大新闻和公司对比种子必须在新闻证据审阅、产业链归组后由 `topic-forward-lead` 生成，脚本不擅自推断。
