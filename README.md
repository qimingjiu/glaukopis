# Project Glaukopis · 拾遗 Freeshelf

> γλαυκῶπις —— “明眸”，荷马史诗里雅典娜最常用的称号。

一只收集优质免费网站的小书柜：书、公开课、字体、图库、开发工具、音乐、游戏、历史。

- `index.json`：巡逻索引，每条带规范化 `key`，用来查重
- `scripts/patrol.py`：查重 + 链接巡逻；`python scripts/patrol.py --add URL` 检查是否已收录
- `.github/workflows/patrol.yml`：每周一自动巡逻一次
- 纯静态页面，部署在 GitHub Pages
