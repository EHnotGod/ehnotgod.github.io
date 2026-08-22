// 从 eh.png 生成 favicon，把 eh2.png 设为主头像（avatar）
import sharp from 'sharp'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import { writeFile } from 'node:fs/promises'

const root = fileURLToPath(new URL('..', import.meta.url))
const srcFav = path.join(root, 'eh.png')
const srcAvatar = path.join(root, 'eh2.png')
const favDir = path.join(root, 'public', 'favicon')
const avatarDst = path.join(root, 'src', 'assets', 'avatar.png')

// 1) favicon 各尺寸
const favSizes = [16, 32, 180, 192, 512]
for (const size of favSizes) {
  await sharp(srcFav)
    .resize(size, size, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toFile(path.join(favDir, `favicon-${size}x${size}.png`))
  console.log(`favicon-${size}x${size}.png`)
}
// ico（PNG 内容，兼容现代浏览器）
await sharp(srcFav).resize(32, 32, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toFile(path.join(favDir, 'favicon.ico'))
console.log('favicon.ico')

// 2) 主头像 -> src/assets/avatar.png (512 高清)
await sharp(srcAvatar).resize(512, 512, { fit: 'cover' }).png().toFile(avatarDst)
console.log('avatar.png (from eh2.png)')

// 3) webmanifest
await writeFile(
  path.join(favDir, 'site.webmanifest'),
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
