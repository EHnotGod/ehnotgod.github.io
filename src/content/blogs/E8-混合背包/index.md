---
title: "E8 混合背包"
publishDate: 2026-08-08
description: "混合背包：01 / 完全 / 多重背包组合。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1833

### 算法解析：

混合背包包含 01 / 完全 / 多重背包：对每件物品按类型处理——01 背包容量逆序、完全背包正序、多重背包用二进制拆分转 01 背包。本题中 $s=-1$ 表示只能取 1 件（01），$s=0$ 表示无限件（完全），$s>0$ 表示有 $s$ 件（多重）。复杂度 $O(nm\log s)$。

### C++代码实现

```c++
#include <iostream>
using namespace std;

int f[1010];

int main(){
  int n, m, v, w, s;
  scanf("%d %d", &n, &m);
  for(int i=1; i<=n; i++){  //枚举物品种类
    scanf("%d%d%d",&v,&w,&s);
    if(s!=0){               //01背包或多重背包
      if(s==-1) s=1;                
      int num=min(s,m/v);
      for(int k=1; num>0; k<<=1){
        if(k>num) k=num;
        num-=k;
        for(int j=m; j>=v*k; j--)
          f[j]=max(f[j],f[j-v*k]+w*k);
      }
    }
    else{                   //完全背包
      for(int j=v; j<=m; j++)
        f[j]=max(f[j],f[j-v]+w);
    }
  }
  printf("%d\n", f[m]);
}
```
