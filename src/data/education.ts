/**
 * 教育 / 经历列表的唯一来源。
 *
 * 中英文学术页都从这里取；分语言字段用 Bilingual 包一层，
 * zh 缺省时自动回退到 en。加一条经历只需要改这里。
 */

import type { Bilingual } from './publications'

export interface EducationEntry {
  /** 学校 */
  school: Bilingual
  /** 院系 / 实验室 */
  department: Bilingual
  /** 起止时间 */
  period: Bilingual
  /** 学位 / 身份（可选） */
  degree?: Bilingual
  /** 地点（可选） */
  location?: Bilingual
  /** 备注（可选） */
  note?: Bilingual
}

export const education: EducationEntry[] = [
  {
    school: { en: 'Nankai University', zh: '南开大学' },
    department: {
      en: 'College of Computer Science · Media Computing Lab',
      zh: '计算机学院 · 媒体计算实验室'
    },
    period: { en: '2026 – present', zh: '2026 – 至今' },
    location: { en: 'Tianjin, China', zh: '天津' }
  },
  {
    school: { en: 'Shandong University', zh: '山东大学' },
    department: {
      en: 'School of Mathematics and Statistics · Statistics (Data Science & AI)',
      zh: '数学与统计学院 · 统计学（数据科学与人工智能）'
    },
    period: { en: '2023.09 – 2027.06', zh: '2023.09 – 2027.06' },
    location: { en: 'Weihai, China', zh: '威海' }
  }
]

function pickText(value: Bilingual, isZh: boolean): string {
  return isZh ? (value.zh ?? value.en) : value.en
}

function pickOptional(value: Bilingual | undefined, isZh: boolean): string | undefined {
  return value ? pickText(value, isZh) : undefined
}

export function localizeEducation(locale?: string) {
  const isZh = locale === 'zh'
  return education.map((entry) => ({
    school: pickText(entry.school, isZh),
    department: pickText(entry.department, isZh),
    period: pickText(entry.period, isZh),
    degree: pickOptional(entry.degree, isZh),
    location: pickOptional(entry.location, isZh),
    note: pickOptional(entry.note, isZh)
  }))
}
