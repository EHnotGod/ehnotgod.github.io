/**
 * 博客分类的唯一来源（single source of truth）。
 *
 * 站点分类是白名单式的：只有这里列出的分类才会出现在导航下拉和分类页里，
 * 文章 frontmatter 的 `category` 必须是其中之一。
 *
 * 原先 Header 与两个分类页（/blog/[category]、/zh/blog/[category]）各写了一份
 * categoryMap + categoryOrder，改一个分类要动 3 个文件，现统一到这里。
 */

export interface CategoryDef {
  /** frontmatter 里 category 的取值，同时进 URL：/blog/<slug> */
  slug: string
  /** 英文显示名（站点默认语言为 en） */
  en: string
  /** 中文显示名（/zh 路由下使用） */
  zh: string
}

export const CATEGORIES: CategoryDef[] = [
  { slug: 'algo', en: 'Algorithm Contest', zh: '算法竞赛' },
  { slug: 'technical', en: 'Technical', zh: '技术笔记' },
  { slug: 'daily-life', en: 'Daily Life', zh: '日常随笔' }
]

/**
 * “全部”是虚拟分类：文章 frontmatter 里永远不会写它，
 * 只用于导航下拉的第一个入口与 /blog/all 列表页。
 */
export const ALL_CATEGORY: CategoryDef = { slug: 'all', en: 'All', zh: '全部' }

/** 导航与分类页的展示顺序（不含 All，All 由调用方单独置顶） */
export const CATEGORY_ORDER: string[] = CATEGORIES.map(category => category.slug)

/** 按预设顺序筛出真实存在的分类 */
export function orderCategories(allCategories: string[]): string[] {
  return CATEGORY_ORDER.filter(slug => allCategories.includes(slug))
}

/** 单个分类的显示名，未知分类回退成 slug 本身 */
export function categoryName(slug: string, locale?: string): string {
  if (slug === ALL_CATEGORY.slug) return locale === 'zh' ? ALL_CATEGORY.zh : ALL_CATEGORY.en
  const found = CATEGORIES.find(category => category.slug === slug)
  if (!found) return slug
  return locale === 'zh' ? found.zh : found.en
}

/** slug -> 显示名 的映射（含 All），供分类页通过 props 传递 */
export function categoryNameMap(locale?: string): Record<string, string> {
  return Object.fromEntries(
    [ALL_CATEGORY, ...CATEGORIES].map(category => [
      category.slug,
      categoryName(category.slug, locale)
    ])
  )
}
