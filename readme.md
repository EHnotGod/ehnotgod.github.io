# EH's Blog

个人博客，基于 [Astro](https://astro.build/) + [Axi-Theme](https://github.com/Axi404/Axi-Theme)（Apache 2.0）构建。

## 本地开发

```bash
pnpm install        # 安装依赖
pnpm dev            # 开发预览 http://localhost:4321
pnpm build          # 构建到 dist/
pnpm preview        # 预览构建产物
pnpm check:content  # 文章规范自检（图片路径 / frontmatter / 分类白名单）
```

## 目录结构

- `src/site.config.ts` — 站点配置（标题、作者、导航、个人信息、域名）
- `src/utils/categories.ts` — **博客分类的唯一来源**（导航下拉、`/blog/[category]`、`/zh/blog/[category]` 都从这里取）
- `src/content/blogs/<slug>/index.md` — 博客文章（`index-en.md` 为同篇英文版，可选）
- `src/content/blogs/<slug>/images/` — 该文章的全部配图（跟文章放一起）
- `src/content/collection/*.md` — 合集（用 `bloglist` 把若干文章串成主题列表）
- `src/pages/` — 页面（首页 / about / projects / links / search / tags / archives）
- `public/` — 站点级静态资源（`avatar/`、`favicon/`、`fonts/`、`icons/`、`site/`、`links.json`、`cv.pdf`）
- `_archive/` — 旧 Hexo 项目存档与迁移期编译产物（不参与构建）
- `_tools/` — 可复用脚本（`localize_images.py`、`check_content.py` 等），历史一次性脚本在 `_tools/archive/`

## 写一篇新文章

1. 在 `src/content/blogs/<slug>/index.md` 新建文件
2. frontmatter 示例：

```md
---
title: "文章标题"
publishDate: 2026-08-22
description: "文章描述"
category: algo        # 取值见 src/utils/categories.ts（algo | technical | daily-life）
tags:
  - 基础算法
language: zh
---
```

3. 正文支持 Markdown、KaTeX 数学公式（`$...$` / `$$...$$`）

## 图片约定

**所有配图放文章自己的 `images/` 目录，正文用相对路径引用：**

```md
![图注](images/A11-1.png)
```

- 不要再写 `public/images/...` 加 `/images/...` 的绝对路径（历史遗留已全部迁移，迁移脚本见 `_tools/localize_images.py`）。
- 相对路径下 Astro 会自动优化图片（转 webp、写入宽高、附带 og:image 用原图），且整篇文章连同图片可以整个目录搬走。
- 命名：算法文章沿用 `<编号>-<序号>.png`（如 `D24-1.png`）；日常随笔用 `01-简短描述.jpg`。
- 新图直接拖进 `src/content/blogs/<slug>/images/` 即可，不需要再往 `public/` 里放。

## 封面图（可选）

`daily-life` 类随笔建议加封面，会同时用于文章顶部横幅、列表卡片和社交分享图：

```yaml
heroImage:
  src: images/02-jinan-venue.jpg
  alt: 一句话描述
```

## 分类

分类是白名单式的，只改 `src/utils/categories.ts` 一处：

```ts
{ slug: 'algo', en: 'Algorithm Contest', zh: '算法竞赛' }
```

`slug` 同时用于 frontmatter 的 `category` 和 URL（`/blog/<slug>`），`en` / `zh` 分别是英文站与 `/zh` 下的显示名。
文字里的分类若不在白名单内，分类页与导航不会收录它（`pnpm check:content` 会报错）。

## 合集（Collection）

在 `src/content/collection/` 下新建一个 `.md`，用 `bloglist` 按想要的顺序列出文章目录名即可：

```yaml
---
title: "算法竞赛模板速查"
title_en: "Competitive Programming Templates Cheatsheet"
description: "一句话介绍"
description_en: "One-line description"
bloglist:
  - a1-高精度加法
  - c4-线段树
---
```

访问路径是 `/collection/<文件名>`（中文站为 `/zh/collection/<文件名>`）。

## 英文版

同一篇文的英文版放 `index-en.md`，与中文版共用一个目录和 `images/`。
没有英文版的文章，英文站会直接回退到中文版（`src/utils/server.ts` 里的 `getBlogCollectionEn`）。

## 提交前自检

```bash
pnpm check:content
```

会检查 frontmatter 必填项、分类是否在白名单、图片是否都在 `images/` 下且真实存在、
有没有外链或孤儿图。硬错误返回非 0，可直接接进 CI。

## 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并发布到 GitHub Pages（`gh-pages` 分支）。

## 更新主题提示

由于 Astro 的一些特性（例如构建产物与自动生成文件等），当你需要更新博客/主题时，建议使用差异对比工具来合并改动，比如 [WinMerge](https://winmerge.org/)。
