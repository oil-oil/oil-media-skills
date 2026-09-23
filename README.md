# oil-media-skills

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="oil-media-skills 全流程自媒体创作 Skill 集合：从文案和视觉素材，到剪辑、字幕、封面和发布。">
</p>

`oil-media-skills` 是一个覆盖自媒体创作全流程的 Skill 集合：从面向观众的文案、演示和插图，到视频剪辑、字幕、封面，再到多平台发布。它不是一键自动流水线；你可以只用其中一个 Skill，也可以按自己的内容制作顺序组合使用。

每个 Skill 仍在自己的仓库维护。这个仓库用 Git submodule 记录来源，不复制代码做二次维护。

## 包含的 Skill

| 环节 | Skill | 能做什么 | 独立仓库 |
| --- | --- | --- | --- |
| 文案 | `oil-tone` | 根据已有事实材料起草或润色口播、文章、演讲和产品介绍，让表达自然、清楚，不编造经历或结果。 | [oil-tone](https://github.com/oil-oil/oil-tone) |
| 演示 | `oil-ppt` | 把讲述内容做成 16:9 HTML 演示页，逐页检查；需要时导出 PPTX。 | [oil-ppt](https://github.com/oil-oil/oil-ppt) |
| 插图 | `oil-visual` | 制作解释概念与流程的漫画墨线图，或供文章、演示和封面排版使用的透明角色插图。 | [oil-visual](https://github.com/oil-oil/oil-visual) |
| 工程剪辑 | `screen-studio-editor` | 整理 `.screenstudio` 工程里的停顿、重讲和补录，也能按口播把屏幕轨替换为 PPT。 | [screen-studio-editor](https://github.com/oil-oil/screen-studio-editor) |
| 成片粗剪 | `video-editor` | 对 MP4、MOV 等已导出视频压缩停顿、清理口误，输出新视频、剪辑计划和审计报告。 | [video-editor](https://github.com/oil-oil/video-editor) |
| 字幕 | `oil-subtitle` | 转录并校对中文字幕，预览后烧录进视频；需要时输出同时间轴的英文 SRT。 | [oil-subtitle](https://github.com/oil-oil/oil-subtitle) |
| 封面 | `oil-cover` | 根据视频或脚本制作小红书与 B 站封面，输出适配不同展示位置的三种画幅。 | [oil-cover](https://github.com/oil-oil/oil-cover) |
| 发布 | `video-publisher` | 上传并验证小红书、抖音、B 站、视频号和 YouTube 草稿；默认停在最终发布前，用户明确要求时才完成发布。 | [video-publisher-skill](https://github.com/oil-oil/video-publisher-skill) |

`auto-publish` 暂未接入：它目前没有独立的公开源仓库。等来源确定后再以 submodule 加入，不复制项目内版本。

## 获取源码

```bash
git clone --recurse-submodules https://github.com/oil-oil/oil-media-skills.git
cd oil-media-skills
python3 scripts/verify_collection.py
```

已经克隆但未拉取子仓库时，运行 `git submodule update --init --recursive`。`vendor/` 是独立源仓库，`skills/` 是指向对应 Skill 子目录的符号链接；完整映射见 [`sources.yaml`](sources.yaml)。更新 Skill 请先到独立仓库维护，再审核并提交这里的 submodule 指针。

当前只发布源码集合，尚不提供从本仓库直接安装全部或单个 Skill 的 `npx skills add` 入口，也不启用版本检查或 Hook。需要单独使用时，请前往上表对应的独立仓库查看安装说明。GitHub 的源码压缩包不会自动拉取 submodule，请使用上面的克隆命令。

本仓库的 README、映射和脚本采用 [MIT 许可](LICENSE)；各 submodule 内容遵循各自仓库的许可，不因被本仓库引用而改变。

修改首页主视觉的布局或人物插图后，可运行 `python3 scripts/build_readme_hero.py` 重新生成 SVG。
