---
name: hyperframes-cli-runtime-contract
description: HyperFrames 首次 init 慢与 check 项目约定(根 index.html、timed elements 必须 class="clip"、中文字体需 @font-face local 声明)——踩过一遍即可避坑
type: resource-lesson
status: in-flight
owner: investagent-video-by-hyperframes
asset: hyperframes
tags: [hyperframes, cli, check, composition-contract]
---

# Experience: hyperframes-cli-runtime-contract

## 来源证据

- 项目：investment-research-video · 2026-08-20 试点(贵州茅台 600519,investagent-video-by-hyperframes 首跑)
- 运行记录：`outputs/companies/贵州茅台/2026-08-20/video/hyperframes-execution.md`
- 资源 installed_ref：hyperframes skill c32b804;CLI npm 0.8.4(npx 解析)

## 触发场景

- 任何 HyperFrames 项目首次 scaffold 与 check 验证时

## 问题与归属判定

- 问题：①`npx hyperframes init` 首次拉取 ~15 分钟(npm 依赖含 onnxruntime-node,postinstall 下载大体积运行时,国内网络慢;资产记录此前实测 auth 8m10s);`--example=data-chart` 有缺陷(安装后缺 index.html,报错但不影响项目骨架生成);②`hyperframes check` 期望**项目根 index.html**(参数传文件路径报 "Not a directory";`compositions/` 目录是 registry 子项不是主 composition);③所有带 `data-start` 的视觉元素必须 `class="clip"`(首轮 check 18 个 timed_element_missing_clip_class 错误);④中文字体栈(Noto Sans SC/PingFang SC/Microsoft YaHei)不在渲染器自动解析列表,必须 `@font-face { src: local('...') }` 声明否则回退泛型字体
- 归属（owner）：investagent-video-by-hyperframes workflow SOP Phase 4/5 Known Issues;hyperframes 资源记录注意事项

## 可复用结论（resolution）

- init 慢是常态:预留 10-15 分钟或提前预拉取;`--example` 有缺陷时忽略示例,骨架(项目目录 + hyperframes.lock.json)仍可用
- check/渲染命令在**项目根目录**运行(`npx hyperframes check .` / `render .`);主 composition 放根 `index.html`,registry 安装项才放 `compositions/`
- 所有 timed 视觉元素(clip 语义元素)加 `class="clip"`,runtime 才按 data-start/duration 控制显隐
- 中文字体加 `@font-face { font-family: "Noto Sans SC"; src: local("Noto Sans SC"); }` 等声明
- 对比度警告(2.63:1 需 3:1)低成本修复:ink-faint #9A9A9A→#8F8F8F、gold 上文字 #B08D57→#AC8A55

## 回写目标

- investagent-video-by-hyperframes workflow SOP Phase 4/5 Known Issues;hyperframes 资产记录注意事项(init 慢已记,补 check 约定与 clip class)

## 适用范围

- HyperFrames CLI 0.8.x 项目 scaffold 与 check 流程

## 不适用范围

- 渲染管线(render)本身的失败排查;composition 动画实现细节(属 hyperframes-animation)

## 关联资产

- hyperframes、investagent-video-by-hyperframes
