# Project Registry Index

项目登记索引：每个通过 Project Registry 创建的项目在此写入 `<project-name>.yaml` 登记记录。

- 记录字段：`.ai/templates/project-registration.yaml.template`（name/description/workflows[] + `registered:` 时间戳）
- 物理项目位于 `../../projects/`（独立 git），此处仅存元数据，不存项目代码
