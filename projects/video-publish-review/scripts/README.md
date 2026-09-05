# Project scripts

项目级脚本只保留无法跨项目复用、且直接服务本项目产物的工具。可跨项目复用的选题信号扫描已沉淀为 `topic-forward-signal-scanner` Skill，调用其资源目录下的脚本。

当前脚本：

- `build-topic-candidates.py`：读取可选 `signals.json`，并可通过 `--leads` 接收按 `topic-forward-candidate` 模板填写、有来源的事件、产品、行业、观众问题或比较线索，输出 `candidate-pool.json`。行情种子的观众问题保持为空，交策划轻量核验后形成；脚本不把价格变化自动解释成财务问题。

批准卡随后交给 `topic-research`；本目录脚本不负责研究、审批或生成视频。
