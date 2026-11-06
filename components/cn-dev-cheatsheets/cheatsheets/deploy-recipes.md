# 部署与验收配方

## 静态服务

一条命令起本地服务（锁 127.0.0.1，别暴露局域网）：

```bash
python -m http.server 8899 --bind 127.0.0.1
```

- 坑：目录内容更新后 URL 还返回旧内容 → serve 进程持着旧快照，杀掉重起
- 多个静态站用不同端口隔离，端口写死在组件 start.bat 里

## start.bat 模板（双击即开）

```bat
@echo off
cd /d "%~dp0"
start "server" /min python -m http.server 8899 --bind 127.0.0.1
timeout /t 1 >nul
start "" "http://localhost:8899/入口页.html?参数=1"
```

- `cd /d "%~dp0"` 保证从任意位置双击都切到 bat 所在目录
- 交付验收标准之一：把整个文件夹拷到别人电脑，双击 bat 能开

## nginx 子域（已有泛域名证书时）

- 加子站只写一个 server 块：新 subdomain → 新 upstream/root，证书走现成通配符
- 改完 `nginx -t` 验配置再 reload

## 交付验收三连（提交前必做）

1. **curl 200**：`curl -s -o /dev/null -w "%{http_code}" <URL>`，线上地址自己验过才算活
2. **手机开**：扫码或局域网地址真机过一遍，横竖屏不崩
3. **干净机开**：无开发环境的机器（或至少新浏览器 profile）能跑，本地依赖全打包进文件夹

## 无头截图 / HTML→PDF

- 无头浏览器截图用**独立的 user-data-dir**，别污染日常浏览器档案；被默认档案占用端口坑过
- HTML→PDF 走无头 Chromium 打印；复杂学术排版（公式/上下标）走 Word COM 转 PDF 更稳
- 截图脚本参数化：`--url --out --wait`，做成可复用小工具存进项目

## WebGL 页面黑屏排查（三步定位）

1. 打开浏览器控制台看有没有 `WebGL context lost` / 着色器编译错误
2. 确认纹理/数据文件路径 200（404 静默失败最常见）
3. 换一台机器/关闭硬件加速对照，区分代码问题和驱动问题
