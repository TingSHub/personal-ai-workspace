# Asset: font.zhuque-fangsong

> 位置: `.ai/assets/fonts/zhuque-fangsong/`

## 元数据

| 字段 | 值 |
|---|---|
| resource_key | `font.zhuque-fangsong` |
| kind | `fonts` |
| description | 中文仿宋风格标题候选字体 |
| source | 用户提供的朱雀字体包 |
| version | preview `0.107`；同目录保留 source `0.212` |
| license | 同目录 `preview-0.107/LICENSE.txt`；上游声明 SIL Open Font License 1.1 |
| files | `preview-0.107/ZhuqueFangsong-Regular.ttf`、许可证和来源包 |
| requirements | TTF 嵌入；使用时保留上游许可证 |
| verification | 已通过 HyperFrames check、截图和中文字符覆盖检查 |

## 调用说明

项目 `account-profile/design.md` 通过 `font.zhuque-fangsong` 作为候选显示字体；构建器读取 `preview-0.107/ZhuqueFangsong-Regular.ttf`。

## 注意事项

这是候选显示字体，不自动覆盖项目首选字体；启用时继续检查字形覆盖、标题溢出和许可证。
