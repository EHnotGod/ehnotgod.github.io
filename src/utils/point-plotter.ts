export interface Point {
  x: number
  y: number
}

export const EXAMPLE_POINTS = `0 0
5 10
15 10
20 0
25 11
30 0
35 10
50 10
60 5`

export const MAX_POINTS = 5000

type ParseResult =
  | { points: Point[]; error?: never }
  | { points?: never; error: 'invalid' | 'limit' | 'range'; line: number }

const numberPattern = /^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i

export function parsePoints(input: string): ParseResult {
  const points: Point[] = []
  // Also accept the backslash separators used in pasted examples.
  const lines = input.replace(/\\(?:\r?\n)?/g, '\n').split(/\r?\n/)
  for (const [index, line] of lines.entries()) {
    if (!line.trim()) continue
    const values = line.trim().split(/[\s,，]+/)
    if (values.length !== 2 || !values.every((value) => numberPattern.test(value))) {
      return { error: 'invalid', line: index + 1 }
    }
    const [x, y] = values.map(Number)
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      return { error: 'range', line: index + 1 }
    }
    points.push({ x, y })
    if (points.length > MAX_POINTS) return { error: 'limit', line: index + 1 }
  }
  return { points }
}

/** Fit points using the same scale on both axes, preserving geometric angles. */
export function fitPoints(points: Point[], width: number, height: number) {
  const padding = 56
  const xs = points.map((point) => point.x)
  const ys = points.map((point) => point.y)
  const minX = points.length ? Math.min(...xs) : -5
  const maxX = points.length ? Math.max(...xs) : 5
  const minY = points.length ? Math.min(...ys) : -5
  const maxY = points.length ? Math.max(...ys) : 5
  const spanX = maxX - minX
  const spanY = maxY - minY
  const fallback = Math.max(Math.abs(minX), Math.abs(minY)) * 0.1 || 10
  const span = Math.max(spanX, spanY) || fallback
  const scale = Math.min(
    (width - padding * 2) / (spanX || span),
    (height - padding * 2) / (spanY || span)
  )
  if (!Number.isFinite(span) || !Number.isFinite(scale) || scale <= 0) return null
  const left = (width - spanX * scale) / 2
  const bottom = (height + spanY * scale) / 2
  const xMin = minX - left / scale
  const xMax = maxX + left / scale
  const yMin = minY - (height - bottom) / scale
  const yMax = maxY + (height - bottom) / scale
  if (![xMin, xMax, yMin, yMax].every(Number.isFinite)) return null
  return {
    xMin,
    xMax,
    yMin,
    yMax,
    scale,
    project: (point: Point) => ({
      x: left + (point.x - minX) * scale,
      y: bottom - (point.y - minY) * scale
    })
  }
}

export function gridTicks(min: number, max: number, scale: number): number[] {
  const roughStep = 64 / scale
  const power = 10 ** Math.floor(Math.log10(roughStep))
  const fraction = roughStep / power
  const step = (fraction <= 1 ? 1 : fraction <= 2 ? 2 : fraction <= 5 ? 5 : 10) * power
  if (!Number.isFinite(step) || step <= 0) return []
  const first = Math.ceil(min / step)
  const count = Math.min(200, Math.floor(max / step) - first + 1)
  return Array.from({ length: Math.max(0, count) }, (_, index) => (first + index) * step)
}

export function edgeCount(count: number, connect: boolean, close: boolean): number {
  return connect ? Math.max(0, count - 1) + (close && count > 2 ? 1 : 0) : 0
}
