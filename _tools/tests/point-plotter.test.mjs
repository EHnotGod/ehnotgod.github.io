// Run with Node 22.18+: node --test _tools/tests/point-plotter.test.mjs
import assert from 'node:assert/strict'
import test from 'node:test'

import {
  edgeCount,
  EXAMPLE_POINTS,
  fitPoints,
  gridTicks,
  MAX_POINTS,
  parsePoints
} from '../../src/utils/point-plotter.ts'

test('parses the supplied example and backslash-separated paste', () => {
  const result = parsePoints(EXAMPLE_POINTS)
  assert.equal(result.points.length, 9)
  assert.deepEqual(result.points.at(-1), { x: 60, y: 5 })
  assert.deepEqual(parsePoints(EXAMPLE_POINTS.replaceAll('\n', '\\')), result)
  assert.deepEqual(parsePoints(EXAMPLE_POINTS.replaceAll('\n', '\\\n')), result)
})

test('supports whitespace, commas, decimals, negatives, and scientific notation', () => {
  assert.deepEqual(parsePoints('\n -2.5, +3\r\n\n.5\t1e2\n0，-4.2E-1 ').points, [
    { x: -2.5, y: 3 },
    { x: 0.5, y: 100 },
    { x: 0, y: -0.42 }
  ])
  assert.deepEqual(parsePoints('  \n\t').points, [])
})

test('reports invalid rows without silently drawing partial data', () => {
  for (const invalid of ['1', '1 2 3', 'NaN 2', 'Infinity 3', '0x10 2', '<script> 0']) {
    assert.deepEqual(parsePoints(`0 0\n\n${invalid}`), { error: 'invalid', line: 3 })
  }
  assert.deepEqual(parsePoints('1e999 0'), { error: 'range', line: 1 })
  assert.equal(parsePoints('0 0\n'.repeat(MAX_POINTS)).points.length, MAX_POINTS)
  assert.equal(parsePoints('0 0\n'.repeat(MAX_POINTS + 1)).error, 'limit')
})

test('connection modes handle empty, single, two-point, and closed plots', () => {
  assert.equal(edgeCount(0, true, true), 0)
  assert.equal(edgeCount(1, true, true), 0)
  assert.equal(edgeCount(2, true, true), 1)
  assert.equal(edgeCount(9, true, false), 8)
  assert.equal(edgeCount(9, true, true), 9)
  assert.equal(edgeCount(9, false, true), 0)
})

test('preserves equal scale and upward y on desktop and mobile', () => {
  const points = parsePoints(EXAMPLE_POINTS).points
  for (const width of [240, 360, 720]) {
    const fit = fitPoints(points, width, 440)
    const origin = fit.project({ x: 0, y: 0 })
    const unitX = fit.project({ x: 1, y: 0 })
    const unitY = fit.project({ x: 0, y: 1 })
    assert.ok(Math.abs(unitX.x - origin.x - (origin.y - unitY.y)) < 1e-10)
    for (const point of points.map(fit.project)) {
      assert.ok(point.x >= 55 && point.x <= width - 55)
      assert.ok(point.y >= 55 && point.y <= 385)
    }
    const ticks = gridTicks(fit.xMin, fit.xMax, fit.scale)
    assert.ok(ticks.length > 0 && ticks.length < 200)
    assert.ok(ticks.every(Number.isFinite))
  }
})

test('fits empty, coincident, collinear, negative, and large-offset points', () => {
  for (const points of [
    [],
    [{ x: 0, y: 0 }],
    [
      { x: 3, y: 4 },
      { x: 3, y: 4 }
    ],
    [
      { x: -10, y: -5 },
      { x: -10, y: 5 }
    ],
    [
      { x: -10, y: 0 },
      { x: 10, y: 0 }
    ],
    [
      { x: 1e12, y: 1e12 },
      { x: 1e12 + 10, y: 1e12 + 10 }
    ]
  ]) {
    const fit = fitPoints(points, 600, 440)
    assert.ok(fit)
    assert.ok(Number.isFinite(fit.scale) && fit.scale > 0)
    for (const point of points.map(fit.project)) {
      assert.ok(Number.isFinite(point.x) && Number.isFinite(point.y))
    }
  }
  assert.equal(
    fitPoints(
      [
        { x: -1e308, y: 0 },
        { x: 1e308, y: 0 }
      ],
      600,
      440
    ),
    null
  )
})
