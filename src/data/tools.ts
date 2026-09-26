/**
 * About 页「工具」区块的唯一来源。
 *
 * 中英文 About 页都从这里取；`name` 是品牌名（中英一致），
 * 其余可翻译字段用 Bilingual 包一层，zh 缺省时自动回退到 en。
 * 加一个工具 / 加一组工具只需要改这里。
 */

import type { Bilingual } from './publications'

export interface ToolEntry {
  /** 品牌名，中英一致 */
  name: string
  /** 一句话说明 */
  description: Bilingual
  /** 官网链接 */
  href: string
  /** SVG 原始内容（`import('*.svg?raw')`） */
  icon: Promise<typeof import('*.svg?raw')>
}

export interface ToolGroup {
  /** 分组标题 */
  title: Bilingual
  tools: ToolEntry[]
}

export const toolGroups: ToolGroup[] = [
  {
    title: { en: 'Productivity', zh: '生产力工具' },
    tools: [
      {
        name: 'VS Code',
        description: { en: 'Code Editor', zh: '代码编辑器' },
        href: 'https://code.visualstudio.com/',
        icon: import('@/assets/tools/vscode.svg?raw')
      },
      {
        name: 'Cursor',
        description: { en: 'AI-powered Code Editor', zh: 'AI 驱动的代码编辑器' },
        href: 'https://cursor.com',
        icon: import('@/assets/tools/cursor.svg?raw')
      },
      {
        name: 'Chrome',
        description: { en: 'Web Browser', zh: '网页浏览器' },
        href: 'https://www.google.com/chrome/',
        icon: import('@/assets/tools/chrome.svg?raw')
      },
      {
        name: 'Ubuntu',
        description: { en: 'Operating System', zh: '操作系统' },
        href: 'https://ubuntu.com/',
        icon: import('@/assets/tools/ubuntu.svg?raw')
      }
    ]
  }
]

function pickText(value: Bilingual, isZh: boolean): string {
  return isZh ? (value.zh ?? value.en) : value.en
}

/** 按语言把双语字段展开成 ToolSection 需要的扁平结构 */
export function localizeToolGroups(locale?: string) {
  const isZh = locale === 'zh'
  return toolGroups.map((group) => ({
    title: pickText(group.title, isZh),
    tools: group.tools.map((tool) => ({
      name: tool.name,
      description: pickText(tool.description, isZh),
      href: tool.href,
      icon: tool.icon
    }))
  }))
}
