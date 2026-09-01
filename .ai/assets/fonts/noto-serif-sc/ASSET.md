# Asset: font.noto-serif-sc

> 位置: `.ai/assets/fonts/noto-serif-sc/`

## 元数据

| 字段 | 值 |
|---|---|
| resource_key | `font.noto-serif-sc` |
| kind | `fonts` |
| description | 中文播客标题和字幕的衬线字体 |
| source | 用户下载并放入 workspace |
| version | 文件随目录指纹验证 |
| license | 同目录 `LICENSE`；使用时保留许可证 |
| files | `NotoSerifSC-Regular.otf`、`NotoSerifSC-Bold.otf`、`LICENSE` |
| requirements | 支持 OTF 嵌入和中文字符渲染 |
| verification | 已用于 HyperFrames 字体加载、截图和中文字符检查 |

## 调用说明

项目 `account-profile/design.md` 通过 `font.noto-serif-sc` 选择 regular/bold 文件；构建器从 `.ai/assets/fonts/noto-serif-sc/` 读取本体。

## 注意事项

未经项目 profile 选择，不自动替换项目字体；缺字或许可证缺失时回退到已声明的系统字体。
