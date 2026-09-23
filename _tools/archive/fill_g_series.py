# -*- coding: utf-8 -*-
"""G 系列补全：每篇插入「题目情境(有题号才写链接)+算法解析」。
无对应洛谷题号的篇目：题目情境只写描述，链接留空。
G9 修复：Python 代码块误标为 c++。
"""
import os
import re

BASE = os.path.join("src", "content", "blogs")

# 目录名 -> (题目链接或 "", 题目描述, 算法解析)
# 有题号的写 luogu 链接；没有的 link 留空字符串
G = {
    "G1-快速幂": (
        "https://www.luogu.com.cn/problem/P1226",
        "给定 $a,b,p$，求 $a^b \\bmod p$。",
        "快速幂：把指数 $b$ 按二进制拆分，$a^b$ 由 $a^{2^i}$ 的乘积组成。从低位到高位检查 $b$ 的每一位，当前位为 1 就乘上 $a^{2^i}$，同时 $a$ 每次自乘平方（$a^{2^i}=(a^{2^{i-1}})^2$）。每次运算对 $p$ 取模。复杂度 $O(\\log b)$。",
    ),
    "G2-高精度快速幂": (
        "https://www.luogu.com.cn/problem/P1045",
        "给定 $P$，求 $2^P-1$ 的位数及最后 500 位。",
        "麦森数：位数由 $\\lfloor P\\log_{10}2\\rfloor+1$ 计算。后 500 位用高精度数组 + 快速幂：乘法按位逐位计算并进位，幂次按二进制拆分，最后个位减 1（$2^P-1$）。输出分 10 行，每行 50 位。",
    ),
    "G3-矩阵快速幂": (
        "https://www.luogu.com.cn/problem/P3390",
        "给定 $n,k$ 和 $n\\times n$ 矩阵 $A$，求 $A^k \\bmod (10^9+7)$。",
        "矩阵快速幂：把标量快速幂推广到矩阵。初始为单位矩阵，转移矩阵自乘平方，指数 $k$ 按二进制拆分，当前位为 1 则乘上对应矩阵。矩阵乘法三重循环 $O(n^3)$，总复杂度 $O(n^3\\log k)$，模 $10^9+7$。",
    ),
    "G5-gcd及lcm问题": (
        "https://www.luogu.com.cn/problem/P1029",
        "给定 $x,y$，求有多少对正整数 $(p,q)$ 满足 $\\gcd(p,q)=x$ 且 $\\operatorname{lcm}(p,q)=y$。",
        "利用性质 $\\gcd(p,q)\\cdot\\operatorname{lcm}(p,q)=p\\cdot q$：令 $t=x\\cdot y$，枚举 $i$ 满足 $i\\mid t$ 且 $\\gcd(i,t/i)=x$，则 $(i,t/i)$ 为一组解，对称计数加 2；$x=y$ 时去掉重复的一次。复杂度 $O(\\sqrt{t})$。",
    ),
    "G8-线性筛质数": (
        "https://www.luogu.com.cn/problem/P3383",
        "给定 $n,q$ 和 $q$ 次询问，每次询问第 $k$ 小的质数。",
        "欧拉筛（线性筛）：每个合数只被其最小质因子筛掉一次。枚举 $i$，若未被标记则是质数加入表；再枚举已有质数 $p$，标记 $i\\cdot p$，当 $i\\%p==0$ 时 break（保证每个合数只被最小质因子筛）。$O(n)$ 得质数表后直接回答第 $k$ 小质数。",
    ),
    "G9-欧拉函数": (
        "",
        "给定 $n$，输出 $1\\sim n$ 每个数的欧拉函数 $\\varphi(i)$（$1\\sim i$ 中与 $i$ 互质的个数）。",
        "线性筛求欧拉函数：$\\varphi(1)=1$；质数 $p$ 的 $\\varphi(p)=p-1$；对合数 $m=i\\cdot p$：若 $p\\mid i$ 则 $\\varphi(m)=p\\cdot\\varphi(i)$，否则 $\\varphi(m)=(p-1)\\cdot\\varphi(i)$。用数组 $\\varphi$ 记录并输出。复杂度 $O(n)$。",
    ),
    "G10-筛法求因数个数": (
        "",
        "给定 $n$，输出 $1\\sim n$ 每个数的约数个数 $d(i)$。",
        "线性筛求约数个数：额外维护 $a[i]$ 表示 $i$ 的最小质因子次数。质数 $d=2$；合数 $m=i\\cdot p$：若 $p\\mid i$ 则 $a[m]=a[i]+1,\\ d[m]=d[i]/a[m]\\cdot(a[m]+1)$，否则 $a[m]=1,\\ d[m]=2d[i]$。复杂度 $O(n)$。",
    ),
    "G11-筛法求约数和": (
        "",
        "给定 $n$，输出 $1\\sim n$ 每个数的约数和 $\\sigma(i)$。",
        "线性筛求约数和：质数 $\\sigma(p)=p+1$；合数 $m=i\\cdot p$：若 $p\\mid i$ 用 $\\sigma(m)=\\sigma(i)\\cdot(p^{a+1}-1)/(p-1)$ 合并，否则 $\\sigma(m)=\\sigma(i)\\cdot(p+1)$。本篇代码待补充，思路同线性筛维护最小质因子次数。",
    ),
    "G12-莫比乌斯函数": (
        "",
        "给定 $n$，输出 $1\\sim n$ 每个数的莫比乌斯函数 $\\mu(i)$。",
        "线性筛求莫比乌斯函数：$\\mu(1)=1$；质数 $\\mu(p)=-1$；合数 $m=i\\cdot p$：若 $p\\mid i$ 则 $\\mu(m)=0$（含平方因子），否则 $\\mu(m)=-\\mu(i)$。复杂度 $O(n)$，是莫比乌斯反演的基础。",
    ),
    "G13-费马小定理": (
        "",
        "给定 $a,p$（$p$ 为素数且 $a$ 与 $p$ 互质），求 $a$ 在模 $p$ 下的乘法逆元。",
        "费马小定理：$p$ 为素数且 $\\gcd(a,p)=1$ 时 $a^{p-1}\\equiv1\\pmod p$，故 $a\\cdot a^{p-2}\\equiv1\\pmod p$，即逆元 $a^{-1}\\equiv a^{p-2}\\pmod p$。用快速幂求 $a^{p-2}\\bmod p$ 即可。",
    ),
    "G14-拓展欧拉定理-超大幂次取余": (
        "",
        "求超大幂次 $a^b \\bmod m$（$b$ 极大，无法直接读入）。",
        "扩展欧拉定理：当 $b\\ge\\varphi(m)$ 时 $a^b\\equiv a^{b\\bmod\\varphi(m)+\\varphi(m)}\\pmod m$（$a$ 与 $m$ 互质时指数取 $b\\bmod\\varphi(m)$）。用于超大幂次取模降幂：先求 $\\varphi(m)$，再把指数降下来快速幂。",
    ),
    "G17-拓展欧几里得-不定方程": (
        "",
        "给定 $a,b,c$，求解不定方程 $ax+by=c$ 的一组整数解。",
        "扩展欧几里得：递归求 $ax+by=\\gcd(a,b)$ 的一组特解 $(x_0,y_0)$（$b=0$ 时 $x=1,y=0$）。若 $c$ 能被 $\\gcd(a,b)$ 整除，则 $x=c/d\\cdot x_0,\\ y=c/d\\cdot y_0$ 为解，否则无解。复杂度 $O(\\log)$。",
    ),
    "G18-拓展欧几里得-乘法逆元": (
        "",
        "给定 $a,b,m$，求解同余方程 $ax\\equiv b\\pmod m$。",
        "exgcd 求逆元：$ax\\equiv b\\pmod m$ 即 $ax+my=b$。用扩展欧几里得求 $ax+my=\\gcd(a,m)$ 的特解，若 $b$ 能被 $\\gcd$ 整除则 $x=b/d\\cdot x_0\\bmod m$ 为解，否则无解。当 $b=1$ 时即求 $a$ 的乘法逆元。",
    ),
    "G20-扩展中国剩余定理": (
        "https://www.luogu.com.cn/problem/P4777",
        "给定 $n$ 组 $(m_i,r_i)$，求满足 $x\\equiv r_i\\pmod{m_i}$ 的最小非负整数解（模数不保证互质）。",
        "扩展中国剩余定理（EXCRT）：模数不互质时两两合并。对 $x\\equiv r_1\\pmod{m_1}$ 与 $x\\equiv r_2\\pmod{m_2}$，解 $m_1p+m_2q=\\gcd$，若 $(r_2-r_1)\\%d\\ne0$ 无解；否则得特解并合并为 $x\\equiv r'\\pmod{\\operatorname{lcm}(m_1,m_2)}$。逐对合并到只剩一个同余式。",
    ),
    "G22-扩展BSGS算法": (
        "https://www.luogu.com.cn/problem/P4195",
        "多组询问，求解离散对数 $a^x\\equiv b\\pmod p$（$a,p$ 不一定互质）。",
        "扩展 BSGS：模数不互质时，先不断除去 $\\gcd(a,p)$（每除一次指数加 1），化为 $A\\cdot a^{x-k}\\equiv b'\\pmod{p'}$ 且互质，再套用标准 BSGS 分块：$m=\\lceil\\sqrt p\\rceil$，baby step 存 $b'\\cdot a^j$，giant step 查 $a^{im}$，拼接得 $x$。无解返回 -1。",
    ),
    "G23-高斯消元法": (
        "https://www.luogu.com.cn/problem/P3389",
        "给定 $n$ 元线性方程组（增广矩阵），求解或报告无解。",
        "高斯消元：逐列选主元（当前列绝对值最大），与当前行交换，主元行归一化，再用行变换消去下方行的当前列；回代求各变量。若某列找不到非零主元且常数项非零则无解（No Solution），否则唯一解。复杂度 $O(n^3)$。",
    ),
    "G24-矩阵求逆-高斯约旦消元法": (
        "https://www.luogu.com.cn/problem/P4783",
        "给定 $n\\times n$ 矩阵 $A$，求其逆矩阵 $\\bmod(10^9+7)$，或报告不可逆。",
        "高斯-约旦消元求逆：在 $A$ 右侧拼单位矩阵成 $[A\\mid I]$，逐列选非零主元（$\\bmod$ 下用逆元），把主元行归一化并消去**其他所有行**的当前列，使左侧变为单位矩阵，右侧即 $A^{-1}$。主元为 0 则不可逆。复杂度 $O(n^3)$。",
    ),
    "G26-求组合数-线性逆推": (
        "",
        "求组合数 $C(n,k)$（模 $10^9+7$）。",
        "线性逆推求组合数：预处理阶乘 $fac$ 与逆阶乘 $inv$。$fac[n]$ 用快速幂求逆得 $inv[n]$，再倒推 $inv[i-1]=inv[i]\\cdot i$。则 $C(n,k)=fac[n]\\cdot inv[k]\\cdot inv[n-k]\\bmod p$。查询 $O(1)$，预处理 $O(N)$。",
    ),
    "G27-求组合数-卢卡斯": (
        "",
        "求大组合数 $C(n,k)\\bmod p$（$n,k$ 很大，$p$ 为素数）。",
        "Lucas 定理：$C(n,k)\\equiv C(n/p,k/p)\\cdot C(n\\%p,k\\%p)\\pmod p$（$p$ 为素数）。把 $n,k$ 按 $p$ 进制拆分逐位求组合数相乘。复杂度 $O(p\\log_p n)$，适合 $p$ 较小而 $n,k$ 很大的情况。本篇为公式截图笔记，代码待补充。",
    ),
    "G29-隔板法": (
        "",
        "隔板法：组合计数的经典技巧。",
        "隔板法：把 $n$ 个相同物品分成 $k$ 组（每组至少一个），等价于在 $n-1$ 个空隙中选 $k-1$ 个放隔板，方案数 $C(n-1,k-1)$；若允许空组，则先补 $k$ 个虚拟物品再插板，方案数 $C(n+k-1,k-1)$。用于正整数解/非负整数解计数。",
    ),
    "G32-卡特兰数": (
        "",
        "卡特兰数：入栈出栈 / 括号匹配等计数。",
        "卡特兰数：$Cat_n=\\frac{1}{n+1}C(2n,n)=\\sum_{i=0}^{n-1}Cat_i\\cdot Cat_{n-1-i}$，$Cat_0=1$。计数对象包括：$n$ 对括号合法序列、$n$ 个元素入栈出栈序列、$n$ 个节点二叉树形态、凸多边形三角剖分数等。递推式 $Cat_{n+1}=\\frac{4n+2}{n+2}Cat_n$。",
    ),
    "G33-整除分块": (
        "",
        "整除分块：对 $\\lfloor n/i\\rfloor$ 相同的区间合并计算。",
        "整除分块：$\\lfloor n/i\\rfloor$ 的取值只有 $O(\\sqrt n)$ 段，段 $[l,r]$ 内值相同，其中 $r=\\lfloor n/\\lfloor n/l\\rfloor\\rfloor$。对形如 $\\sum_{i=1}^n f(i)\\cdot\\lfloor n/i\\rfloor$ 的求和，可按段累加 $f$ 的区间和。复杂度 $O(\\sqrt n)$。",
    ),
    "G37-迪利克雷卷积": (
        "",
        "狄利克雷卷积：积性函数的卷积运算。",
        "狄利克雷卷积：$(f*g)(n)=\\sum_{d\\mid n}f(d)g(n/d)$，两个积性函数的卷积仍为积性函数。常见恒等式：$\\mu*1=\\epsilon$、$\\varphi*1=id$、$id*\\mu=\\varphi$，是莫比乌斯反演的理论基础。",
    ),
    "G41-FFT-多项式乘法": (
        "https://www.luogu.com.cn/problem/P3803",
        "给定两个多项式系数，求乘积多项式的系数。",
        "FFT 多项式乘法：把系数表示（$O(n^2)$ 相乘）转为点值表示，点值逐位相乘后逆变换（IDFT）回系数。用位逆序置换 + 蝶形迭代实现 DFT/IDFT，$O(n\\log n)$。精度用 double，注意 $n$ 补到 2 的幂。",
    ),
    "G43-NTT-多项式乘法": (
        "https://www.luogu.com.cn/problem/P3803",
        "给定两个多项式系数，求乘积多项式的系数（模 $998244353$）。",
        "NTT 数论变换：用模素数 $P=998244353$ 的原根 $g=3$ 替代复数单位根做 FFT，避免浮点误差，结果取模。实现与 FFT 相同（位逆序 + 蝶形），逆变换时用 $g$ 的逆元。$O(n\\log n)$。",
    ),
    "G45+G46-第一、二类斯特林数": (
        "",
        "第一类斯特林数 $s(n,k)$ 与第二类斯特林数 $S(n,k)$ 的计数。",
        "第一类斯特林数 $s(n,k)$：$n$ 个不同元素分成 $k$ 个非空环排列的方案数，递推 $s(n,k)=s(n-1,k-1)+(n-1)s(n-1,k)$。第二类斯特林数 $S(n,k)$：$n$ 个不同元素分成 $k$ 个非空集合的方案数，递推 $S(n,k)=S(n-1,k-1)+kS(n-1,k)$。本篇为打表找规律笔记。",
    ),
    "G49-向量运算": (
        "",
        "向量的点积、模长与夹角计算。",
        "向量运算：点积 $a\\cdot b=x_ax_b+y_ay_b$，几何意义为模长乘夹角的余弦；模长 $|a|=\\sqrt{x^2+y^2}$；夹角 $\\theta=\\arccos(a\\cdot b/(|a||b|))$。叉积 $a\\times b=x_ay_b-y_ax_b$ 表示有向面积与旋转方向。",
    ),
    "G50-线线关系": (
        "",
        "计算几何：直线/线段位置关系与点在凸多边形内判定。",
        "叉积 $cross(A,B,C)=(B-A)\\times(C-A)$ 判断三点顺序：正为逆时针，负为顺时针，零为共线。点在凸多边形内：遍历每条边，点始终位于边的同一侧（叉积同号）即在内部（边上也算）。",
    ),
    "G51-三角剖分": (
        "",
        "计算几何：多边形三角剖分。",
        "多边形三角剖分：把 $n$ 边形用不相交的对角线分成 $n-2$ 个三角形。凸多边形的剖分方案数与卡特兰数相关；最优化剖分（如面积/周长和最小）可用区间 DP：$dp[l][r]=\\min(dp[l][k]+dp[k][r]+cost(l,k,r))$。本篇笔记，未附代码。",
    ),
    "G52-凸包算法": (
        "https://www.luogu.com.cn/problem/P2742",
        "给定 $n$ 个点，求凸包的周长。",
        "Andrew 凸包：按 $(x,y)$ 排序后，先从左到右构造下凸包，再从右到左构造上凸包，用叉积判断转向（$\\le0$ 弹出栈顶）。最后栈中即凸包顶点，相邻点距离求和得周长。$O(n\\log n)$。",
    ),
    "G53-旋转卡壳": (
        "https://www.luogu.com.cn/problem/P1452",
        "给定 $n$ 个点，求凸包直径（最远点对距离的平方）。",
        "旋转卡壳：先求凸包，再用双指针枚举凸包上的对踵点对：固定一个点，另一个沿凸包顺时针移动，用面积单调性判断卡壳位置，更新最大距离平方。$O(n)$，用于求凸包直径、最远点对。",
    ),
    "G57-自适应辛普森积分": (
        "https://www.luogu.com.cn/problem/P4525",
        "求 $\\int_L^R \\frac{cx+d}{ax+b}\\,dx$，输出 6 位小数。",
        "自适应辛普森积分：用辛普森公式 $\\int_l^r f\\approx\\frac{r-l}{6}(f(l)+4f(m)+f(r))$ 近似积分。递归比较区间整体与左右两半辛普森值的差，误差小于 $\\epsilon$ 时停止，否则递归细分。适用于无法解析积分的一般函数。",
    ),
    "G60-有向图博弈-SG函数": (
        "",
        "给定有向无环图与 $k$ 枚棋子，判断先手是否必胜。",
        "SG 函数：$sg(u)=\\operatorname{mex}\\{sg(v)\\mid v$ 为 $u$ 的后继$\\}$，$sg=0$ 为必败态。记忆化搜索求每个点 $sg$。多枚棋子时各棋子 $sg$ 值异或，非 0 先手胜（win），为 0 后手胜（lose）。",
    ),
    "G61-线性基-max": (
        "https://www.luogu.com.cn/problem/P3812",
        "给定 $n$ 个数，求其中任意多个数异或的最大值。",
        "线性基求最大异或和：把每个数从高位到低位插入线性基，若当前位已有基向量则异或消去，否则放入。构造后用贪心：从高位到低位，若异或该基向量能使结果变大则异或，累加得最大异或和。复杂度 $O(63n)$。",
    ),
    "G62-线性基-k": (
        "",
        "给定若干数，$m$ 次询问第 $k$ 小的异或值。",
        "线性基求第 $k$ 小：构造线性基后（高斯消元形式），把 $k$ 的二进制位对应选取基向量异或。若原集合能异或出 0 则 $k$ 先减 1；$k\\ge2^{s}$（$s$ 为基大小）则无解输出 -1。本题为 HDU 3949 XOR，非洛谷题。",
    ),
    "G74-拉格朗日插值法": (
        "https://www.luogu.com.cn/problem/P4781",
        "给定 $n$ 个点 $(x_i,y_i)$，求 $n-1$ 次多项式在 $k$ 处的取值（模 $998244353$）。",
        "拉格朗日插值：$f(k)=\\sum_{i=1}^n y_i\\prod_{j\\ne i}\\frac{k-x_j}{x_i-x_j}$。对每个 $i$，分子累乘 $(k-x_j)$、分母累乘 $(x_i-x_j)$，分母用逆元（费马小定理）处理模意义除法。$O(n^2)$。",
    ),
    "G99-超级gcd": (
        "",
        "多组询问 $\\gcd(a^b,c^d)\\bmod 998244353$。",
        "超级 gcd：指数巨大，用扩展欧拉定理降幂。递归：$\\gcd(a^b,c^d)=\\gcd(g^{\\min(b,d)}\\cdot\\ldots)$，逐步约去公共因子（$g=\\gcd(a,c)$），指数超出 $\\varphi$ 时取 $\\bmod\\varphi+\\varphi$，快速幂相乘。详见代码。",
    ),
}

# G9 修复：把 Python 代码块误标为 c++ 的地方修正
def fix_g9():
    p = os.path.join(BASE, "G9-欧拉函数", "index.md")
    with open(p, encoding="utf-8") as f:
        c = f.read()
    c2 = c.replace("```c++\nimport sys", "```python\nimport sys")
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(c2)


def insert_for(name, link, desc, analysis):
    p = os.path.join(BASE, name, "index.md")
    with open(p, encoding="utf-8") as f:
        c = f.read()
    link_line = f"题目链接：{link}\n\n" if link else ""
    block = f"### 题目情境\n\n{link_line}**题目描述**\n\n{desc}\n\n**说明/提示**\n\n本页为算法笔记。\n\n### 算法解析：\n\n{analysis}\n\n"
    # 在 frontmatter 结束 (---\n) 之后、第一个 ### 之前插入
    # 找到 language: zh 后的 --- 结束
    m = re.search(r"^(title:.*\n(?:.*\n)*?language: zh\n---\n)", c, re.M)
    if not m:
        print(f"WARN: frontmatter not found in {name}")
        return
    # 在 frontmatter 后插入，去掉多余空行
    rest = c[m.end():].lstrip("\n")
    new = c[:m.end()] + block + rest
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(new)


if __name__ == "__main__":
    for name, (link, desc, analysis) in G.items():
        insert_for(name, link, desc, analysis)
    fix_g9()
    print("G series filled OK")
