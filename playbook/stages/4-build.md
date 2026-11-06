# 阶段 4 · 构建

**目的**：把演示脚本变成部署在线的可运行 demo。

**输入**：演示脚本 + 页面清单 + 组件清单。

**输出**：部署 URL + 本地启动方式（一条命令能跑）。

## 任务清单

1. 先搭骨架：空壳部署上线（域名/nginx 配好），从第一小时起就有线上地址
2. 按演示脚本镜头顺序填功能——评委看得到的先做
3. 接入现成组件（galaxy-scene / multiplayer-server / 生图链等），新代码只写胶水层
4. 移动端过一遍：扫码能开、横竖屏不崩
5. 美学打磨（粒子、场景质感）另开一轮做，不阻塞功能

## 退出条件

- **curl 返回 200**，交付必验可达
- 手机能开
- 演示脚本里的每个镜头都有对应画面，缺一个镜头就是没做完
- 本地启动方式写进 README（双击即开）

## 坑与检查点

- WebGL 黑屏用三步定位法；静态服务注意工作目录坑
- 视觉打磨类工作交给专门的工具链/agent，主线别停
- 改数据走 HTML 中间层，别直接动重资产文件
- 部署后每次大改动重新 curl 验一遍

## 工具

- components: `galaxy-scene`（规划中）、`multiplayer-server`（规划中）、`remote-batch-studio`
- skills: `build-frontend`、`gsap-*` 系列、`generate-interactive-web3d`、`img2threejs`、`systematic-debugging`
