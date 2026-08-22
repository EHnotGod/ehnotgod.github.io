# EH's Blog

个人博客，基于 [Astro](https://astro.build/) + [Axi-Theme](https://github.com/Axi404/Axi-Theme)（Apache 2.0）构建。

## 本地开发

```bash
pnpm install        # 安装依赖
pnpm dev            # 开发预览 http://localhost:4321
pnpm build          # 构建到 dist/
pnpm preview        # 预览构建产物
```

## 目录结构

- `src/site.config.ts` — 站点配置（标题、作者、导航、个人信息、域名）
- `src/content/blogs/<slug>/index.md` — 博客文章
- `src/pages/` — 页面（首页 / about / projects / links / search / tags / archives）
- `public/` — 静态资源（`images/`、`avatar/`、`favicon/` 等）
- `_archive/` — 旧 Hexo 项目存档（已迁移，仅供参考）
- `_tools/` — 迁移脚本（`migrate_posts.py` 等）

## 写一篇新文章

1. 在 `src/content/blogs/<slug>/index.md` 新建文件
2. frontmatter 示例：

```md
---
title: "文章标题"
publishDate: 2026-08-22
description: "文章描述"
category: algo        # algo | ml | dl
tags:
  - 基础算法
language: zh
---
```

3. 正文支持 Markdown、KaTeX 数学公式（`$...$` / `$$...$$`）

## 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并发布到 GitHub Pages（`gh-pages` 分支）。

## 更新主题提示

由于 Astro 的一些特性（例如构建产物与自动生成文件等），当你需要更新博客/主题时，建议使用差异对比工具来合并改动，比如 [WinMerge](https://winmerge.org/)。
