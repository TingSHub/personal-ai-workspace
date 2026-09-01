---
name: capability-manager
description: 管理 Capability 能力契约——创建、查看、修改、关联 Skill/Agent、调整质量优先顺序和验证引用。当用户说“创建能力”“管理 capability”“关联资源”“调整能力候选”时使用。
---

# Capability Manager

Capability 是长期领域能力的可复用质量契约：定义一类专业结果的输入、输出、验收标准、执行契约，以及能够实现它的 Skill/Agent 候选。它不是 Workflow step、工具调用、输出格式、资源说明书、评分表或日志库。

## 目录与约束

- 资产位置：`.ai/capabilities/<name>/capability.yaml`
- 字段只从 `.ai/templates/capability.yaml.template` 读取
- 所有资源和 Experience 使用 by-name 引用
- 不维护综合评分、状态、数值化成本模型、生命周期或使用次数；依赖与维护成本只作定性比较
- 资源选择只遵循 `best_available_resource`：先判断当前项目适配性，再综合实际效果、输出质量、稳定性、依赖成本和维护成本；来源不构成优先级
- 候选发现必须同时覆盖 workspace、已安装外部资源、skill-hub、find-skills 和 agent repository；发现顺序不等于选择顺序
- 每个候选记录来源、版本、优势、劣势、实测结果、推荐用法及依赖/维护成本；未实测必须明确标注
- `role=execution` 表示资源必须真实运行并产生可追踪产物；`role=reference` 只允许提供方法论参考
- `execution_contract.required_resources` 只能引用 `role=execution` 的资源，不能由主 Agent 模拟执行

## create

输入：能力名称、要解决的问题、输入、输出、验收标准和已知项目场景。

创建前依次判断：

1. 结果能否在一个 Workflow 步骤内调用？
2. 能否独立判断合格或不合格？
3. 是否存在跨项目复用价值？
4. 是否已有同义 Capability？
5. 是否代表长期专业领域，而非文件生成、格式转换或单一工具调用？

不满足时，优先将内容放入 Workflow、资源调用说明或项目步骤，不创建新 Capability。

## link-resource / unlink-resource

- 检查 Skill/Agent 资源记录存在。
- 从模板填写候选评估字段，记录适用边界和能够产生高质量结果的证据。
- 明确资源角色；只有能按调用说明真实运行并交付结果的资源才能标为 `execution`。
- 没有项目验证时可以作为候选，但必须如实说明依据，不能宣称“已验证最好”。
- 解除引用前检查相关 Workflow 和 Experience 的影响。

## reorder-resources

- 先按当前项目适配性筛选，再依据实际效果、输出质量、稳定性、依赖成本、维护成本和真实项目证据选择，不计算综合分数。
- 不得因资源位于 workspace 就排在外部资源之前；质量与适配性相当时再比较依赖和维护成本。
- 配置缺失但可安全补齐，不构成降低顺序的理由。
- 外部资源更新改变结果质量时，必须先在真实项目重新验证。

## view / modify / validate

- `view`：显示契约、执行契约、候选角色、适用场景、理由和 Experience 证据。
- `modify`：更新定义、I/O、验收或候选，保持职责边界。
- `validate`：检查模板字段、资源引用、Experience 引用，以及 acceptance 是否可用于判断项目输出。

## Validation

- capability.yaml 包含 name/description/input/output/acceptance/resources/execution_contract/experience_refs
- selection.principle 为 best_available_resource，评估维度与发现来源完整
- 每个 resource 包含模板规定的评估字段，role 仅为 execution/reference，引用的 Skill/Agent 存在
- execution_contract 包含 required_resources/optional_resources/required_outputs/validation
- required_resources 和 optional_resources 均引用本 Capability 资源；required_resources 全部为 execution 角色
- required_outputs 能映射到 Capability output，validation 可判断真实产物和证据是否存在
- acceptance 是可判断的结果条件，不是资源调用步骤
- 不包含 score/status/availability/setup_cost/usage_count/priority
