---
title: "G23 三角剖分"
publishDate: 2026-08-08
description: "计算几何：多边形三角剖分。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

多边形三角剖分：把 $n$ 边形用不相交的对角线分成 $n-2$ 个三角形。

### 算法解析：

多边形三角剖分：把 $n$ 边形用不相交的对角线分成 $n-2$ 个三角形。凸多边形的剖分方案数与卡特兰数相关；最优化剖分（如面积/周长和最小）可用区间 DP：$dp[l][r]=\min(dp[l][k]+dp[k][r]+cost(l,k,r))$。

![image-20250930175859818](/images/算法竞赛/G/G23-1.png)

### C++代码

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
#define x first
#define y second
using namespace std;

typedef pair<double,double> Point;
const double eps=1e-8;
const double PI=acos(-1.0);
double R;
Point p[4],o; //顶点和圆心

Point operator+(Point a,Point b){ //向量+
  return Point(a.x+b.x,a.y+b.y);
}
Point operator-(Point a,Point b){ //向量-
  return Point(a.x-b.x,a.y-b.y);
}
Point operator*(Point a,double t){ //数乘
  return Point(a.x*t,a.y*t);
}
Point operator/(Point a,double t){ //数除
  return Point(a.x/t,a.y/t);
}
double operator*(Point a,Point b){ //叉积
  return a.x*b.y-a.y*b.x;
}
double operator&(Point a,Point b){ //点积
  return a.x*b.x+a.y*b.y;
}
double len(Point a){ //模长
  return sqrt(a&a);
}
double dis(Point a,Point b){ //距离
  return len(b-a);
}
Point getNode(Point a,Point u,Point b,Point v){ //直线交点
  double t=(a-b)*v/(v*u);
  return a+u*t;
}
Point rotate(Point a,double b){ //逆转角
  return Point(a.x*cos(b)-a.y*sin(b),a.x*sin(b)+a.y*cos(b));
}
bool onSegment(Point p,Point a,Point b){ //p在线段ab上
  return fabs((a-p)*(b-p))<eps && ((a-p)&(b-p))<=0;
}
Point norm(Point a){ //单位向量
  return a/len(a);
}
double getDP2(Point a,Point b,Point& pa,Point& pb){
  Point e=getNode(a,b-a,o,rotate(b-a,PI/2)); //垂足
  double d=dis(o,e);
  if(!onSegment(e,a,b)) d=min(dis(o,a),dis(o,b));
  if(R<=d) return d; //线段在圆外
  double len=sqrt(R*R-dis(o,e)*dis(o,e));
  pa=e+norm(a-b)*len;
  pb=e+norm(b-a)*len; //pa,pb:线段与圆的两交点
  return d;           //d:圆心到线段的最近距离
}
double sector(Point a,Point b){ //扇形面积
  double angle=acos((a&b)/len(a)/len(b)); //[0,Pi]
  if(a*b<0) angle=-angle;
  return R*R*angle/2;
}
double getArea(Point a,Point b){ //面积的交
  if(fabs(a*b)<eps) return 0; //共线
  double da=dis(o,a),db=dis(o,b);
  if(R>=da && R>=db) return a*b/2; //ab在圆内
  Point pa,pb;
  double d=getDP2(a,b,pa,pb); //d:圆心到线段的最近距离
  if(R<=d) return sector(a,b); //ab在圆外
  if(R>=da) return a*pb/2+sector(pb,b); //a在圆内
  if(R>=db) return sector(a,pa)+pa*b/2; //b在圆内
  return sector(a,pa)+pa*pb/2+sector(pb,b); //ab是割线
}
int main(){
  while(scanf("%lf%lf%lf%lf%lf%lf%lf%lf%lf",
  &p[0].x,&p[0].y,&p[1].x,&p[1].y,&p[2].x,&p[2].y,&o.x,&o.y,&R)!=-1){
    for(int i=0;i<3;i++) p[i].x-=o.x,p[i].y-=o.y; //三角形顶点平移
    o=Point(0,0); //圆心平移到原点
    double res=0;
    for(int i=0;i<3;i++) res+=getArea(p[i],p[(i+1)%3]);
    printf("%.2lf\n",fabs(res)); //点可能顺时针
  }
  return 0;
}
```
