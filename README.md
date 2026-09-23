# oil-skills-media

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="oil-skills-media 视频创作 Skill 集合：剪辑、字幕、封面和发布前草稿流程，右侧是眼镜小人与暖黄色边牧。">
</p>

这是 oil 的自媒体创作 Skill 源码集合，覆盖演示、插图、剪辑、字幕、封面和发布前草稿。每个 Skill 仍在自己的仓库维护；这里用 Git submodule 固定来源，不复制一份代码做二次维护。

## 包含的 Skill

| Skill | 用途 | 独立仓库 |
| --- | --- | --- |
| `oil-ppt` | 制作 HTML 演示文稿 | [oil-ppt](https://github.com/oil-oil/oil-ppt) |
| `oil-cover` | 生成视频封面 | [oil-cover](https://github.com/oil-oil/oil-cover) |
| `oil-visual` | 制作解释图与透明插图 | [oil-visual](https://github.com/oil-oil/oil-visual) |
| `screen-studio-editor` | 剪辑 Screen Studio 工程 | [screen-studio-editor](https://github.com/oil-oil/screen-studio-editor) |
| `video-editor` | 粗剪普通视频 | [video-editor](https://github.com/oil-oil/video-editor) |
| `oil-subtitle` | 转录、校对和烧录字幕 | [oil-subtitle](https://github.com/oil-oil/oil-subtitle) |
| `video-publisher` | 准备多平台草稿；明确授权时完成发布 | [video-publisher-skill](https://github.com/oil-oil/video-publisher-skill) |
| `oil-tone` | 为面向观众的文案提供文风规范 | [oil-tone](https://github.com/oil-oil/oil-tone) |

`auto-publish` 暂未接入：它目前没有独立的公开源仓库。等来源确定后再以 submodule 加入，不复制项目内版本。

## 获取源码

```bash
git clone --recurse-submodules https://github.com/oil-oil/oil-skills-media.git
cd oil-skills-media
python3 scripts/verify_collection.py
```

已经克隆但未拉取子仓库时，运行 `git submodule update --init --recursive`。`vendor/` 是独立源仓库，`skills/` 是指向对应 Skill 子目录的符号链接；完整映射见 [`sources.yaml`](sources.yaml)。更新 Skill 请先到独立仓库维护，再审核并提交这里的 submodule 指针。

当前只发布源码集合，尚不提供从本仓库直接安装全部或单个 Skill 的 `npx skills add` 入口，也不启用版本检查或 Hook。需要单独使用时，请前往上表对应的独立仓库查看安装说明。GitHub 的源码压缩包不会自动拉取 submodule，请使用上面的克隆命令。

本仓库的 README、映射和脚本采用 [MIT 许可](LICENSE)；各 submodule 内容遵循各自仓库的许可，不因被本仓库引用而改变。

修改首页主视觉的布局或人物插图后，可运行 `python3 scripts/build_readme_hero.py` 重新生成 SVG。
