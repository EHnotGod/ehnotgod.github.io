// 生成一个渐变 "EH" 占位头像，写入 src/assets/avatar.png（可随时替换）
import sharp from 'sharp'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const out = fileURLToPath(new URL('../src/assets/avatar.png', import.meta.url))

const svg = `
<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="50%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" fill="url(#bg)" rx="96"/>
  <text x="256" y="316" font-family="Segoe UI, Arial, sans-serif" font-size="220"
        font-weight="700" fill="#ffffff" text-anchor="middle">EH</text>
</svg>
`

await sharp(Buffer.from(svg))
  .png()
  .toFile(out)

console.log('avatar written to', out)
