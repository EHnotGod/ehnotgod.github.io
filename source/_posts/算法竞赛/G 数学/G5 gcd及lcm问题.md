---
title: "G5 gcd及lcm问题"
categories:
- [算法, G 数学]
tags:
- 数学
---

### Python代码实现

```python
# P1029 [NOIP 2001 普及组] 最大公约数和最小公倍数问题
import math
x, y = map(int, input().split())
t = x * y
ans = 0
for i in range(1, int(t ** 0.5) + 1):
    if t % i == 0 and math.gcd(t // i, i) == x:
        ans += 2
if x == y:
    ans -= 1
print(ans)
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

typedef long long LL;
LL x,y,ans;

LL gcd(LL a, LL b){
  return b==0 ? a : gcd(b,a%b);
}
int main(){
    cin>>x>>y;
    LL t = x*y;
    for(LL i=1; i*i<=t; i++)
        if(t%i==0 && gcd(i,t/i)==x)
          ans += 2;
    if(x==y) ans--;
    cout << ans;
    return 0;
}
```
