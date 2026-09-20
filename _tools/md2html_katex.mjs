// 用 unified + remark-math + rehype-katex 把 算法竞赛合集.md 转成含渲染公式的 HTML
import { readFileSync, writeFileSync } from 'fs'
import { unified } from 'unified'
import remarkParse from 'remark-parse'
import remarkMath from 'remark-math'
import remarkRehype from 'remark-rehype'
import rehypeKatex from 'rehype-katex'
import rehypeStringify from 'rehype-stringify'

const md = readFileSync('算法竞赛合集.md', 'utf-8')

// 修正图片路径：/images -> 指向 public 的实际 file 路径，让浏览器能加载
// 保留为绝对路径但在打印前通过 --allow-file-access 或本地 server 提供。
// 这里转成相对 public 的 file 引用：从 src 之外不行，直接指向 public 目录
const mdFixed = md.replace(
  /!\[([^\]]*)\]\((\/images\/[^)]+)\)/g,
  (_m, alt, path) => `![${alt}](public${path})`
)

const file = await unified()
  .use(remarkParse)
  .use(remarkMath)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeKatex, { throwOnError: false })
  .use(rehypeStringify)
  .process(mdFixed)

const body = String(file)

// 引入本地 katex CSS（字体相对 katex/dist/fonts）
const katexCss = readFileSync('node_modules/katex/dist/katex.min.css', 'utf-8')

const css = `
<style>
${katexCss}
body { font-family: "Microsoft YaHei","SimSun",sans-serif; font-size: 10.5pt; line-height: 1.55; margin: 2cm 1.6cm; }
h1 { font-size: 20pt; color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 4px; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 14pt; color: #1f618d; border-left: 4px solid #2980b9; padding-left: 8px; margin-top: 20px; }
h3 { font-size: 12pt; color: #2c3e50; }
code { font-family: Consolas,monospace; background: #f4f4f4; padding: 1px 3px; border-radius: 3px; font-size: 9pt; }
pre { background: #f7f8fa; border: 1px solid #e1e4e8; border-radius: 5px; padding: 8px 10px; font-size: 8.5pt; line-height: 1.4; white-space: pre-wrap; word-break: break-word; }
pre code { background: none; padding: 0; }
blockquote { color: #57606a; border-left: 4px solid #d0d7de; margin: 6px 0; padding: 2px 12px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0; }
th, td { border: 1px solid #bbb; padding: 3px 8px; font-size: 9.5pt; }
img { max-width: 100%; height: auto; }
hr { border: none; border-top: 1px solid #e1e4e8; margin: 14px 0; }
a { color: #0969da; text-decoration: none; }
</style>
`
const html = `<!DOCTYPE html><html><head><meta charset="utf-8">${css}</head><body>${body}</body></html>`
writeFileSync('算法竞赛合集.html', html, 'utf-8')
console.log('HTML 生成 KB:', Math.round(html.length / 1024))
