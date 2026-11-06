# Windows 中文环境坑手册

## Git Bash

**MSYS 路径转换吃掉斜杠参数**
- 症状：`robocopy src dst /E /XD .git` 报"无效参数 #3"，`/E` 被转成 `E:/`
- 原因：Git Bash（MSYS2）把 `/xxx` 当 Unix 路径转成 Windows 路径
- 正解：`MSYS_NO_PATHCONV=1 robocopy ... /E /XD .git`

**robocopy 退出码语义**
- 0-7 都是成功（1=有文件拷贝，2=有多余文件检测……），8+ 才是错误
- bash 按 `!=0` 判失败会误报，用 `[ $? -le 7 ]`

## 编码

**curl 传中文 JSON 丢码**
- 症状：中文变问号/乱码，服务端收到废字符
- 正解：中文 JSON 一律用 Python `httpx`（或 requests）发，别用 curl 拼

**curl 访问带中文文件名的 URL**
- 正解：先 URL 编码中文段再拼 URL

**剪贴板中文（clip）**
- 症状：`echo 中文 | clip` 出去变乱码
- 原因：clip 按 GBK 解
- 正解：`chcp 65001` 后再 clip，或用 Python `subprocess` 写 UTF-8

**heredoc 里的反斜杠**
- 症状：heredoc 里写 `C:\Users\x` 变成 `C:Usersx`
- 原因：`\U` `\x` 被当转义处理
- 正解：heredoc 内路径全用正斜杠 `C:/Users/x`

**.bat 批处理**
- 坑：UTF-8 无 BOM + LF 保存的 bat 中文乱码、行为怪
- 正解：bat 存 GBK(ANSI) + CRLF；要 UTF-8 就第一行 `chcp 65001 >nul`

**中文路径操作**
- mv/重命名中文文件在 Git Bash 下偶发编码异常；大批量中文文件操作用 `robocopy`（配 MSYS_NO_PATHCONV）或 Python `shutil`

## 进程与目录

**目录删不掉**
- 原因：几乎总是有进程占用（含资源管理器预览、后台 python/node）
- 正解：先定位占用者（进程名不直观的用窗口标题/命令行匹配），关进程再删；别硬 rm -rf 循环重试

**静态服务目录被删后还活着**
- 症状：serve 的目录删了，URL 还能返回旧内容
- 原因：serve 进程持有已删除目录的快照句柄
- 正解：杀 serve 进程重起，别信返回内容

## 嵌套 git

- 把别处 clone 来的目录拷进自己仓库前，先 `find . -name ".git" -type d` 检查，嵌套 .git 会把子目录当成 submodule 引用导致 push 后别人拉不到内容
