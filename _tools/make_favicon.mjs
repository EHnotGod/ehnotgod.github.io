// 生成 EH 渐变 favicon（PNG 各尺寸 + webmanifest），写入 public/favicon/
import sharp from 'sharp'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import { writeFile } from 'node:fs/promises'

const dir = fileURLToPath(new URL('../public/favicon/', import.meta.url))

function svg(size) {
  return `
<svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="50%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
  </defs>
  <rect width="${size}" height="${size}" fill="url(#bg)" rx="${Math.round(size * 0.18)}"/>
  <text x="50%" y="${Math.round(size * 0.64)}" font-family="Segoe UI, Arial, sans-serif"
        font-size="${Math.round(size * 0.46)}" font-weight="700" fill="#ffffff"
        text-anchor="middle">EH</text>
</svg>`
}

const sizes = [16, 32, 180, 192, 512]
for (const size of sizes) {
  await sharp(Buffer.from(svg(size)))
    .png()
    .toFile(path.join(dir, `favicon-${size}x${size}.png`))
  console.log(`favicon-${size}x${size}.png`)
}

// 简单生成一个 ico（32x32 PNG 数据直接写成 .ico 文件名的 PNG，浏览器兼容）
await sharp(Buffer.from(svg(32))).png().toFile(path.join(dir, 'favicon.ico'))
console.log('favicon.ico (png)')

// 更新 site.webmanifest
await writeFile(
  path.join(dir, 'site.webmanifest'),
  JSON.stringify(
    {
      name: "EH's Blog",
      short_name: 'EH',
      icons: [
        { src: '/favicon/favicon-192x192.png', sizes: '192x192', type: 'image/png' },
        { src: '/favicon/favicon-512x512.png', sizes: '512x512', type: 'image/png' }
      ],
      theme_color: '#6366f1',
      background_color: '#ffffff',
      display: 'standalone'
    },
    null,
    2
  ),
  'utf-8'
)
console.log('site.webmanifest updated')
