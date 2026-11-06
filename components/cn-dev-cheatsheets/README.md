# cn-dev-cheatsheets · 国内开发速查卡

在国内 Windows 环境做黑客松/快原型时反复踩到的坑与配方，浓缩成三张卡。全部来自实战验证，不是文档搬运。

## 卡片

| 卡 | 内容 | 什么时候查 |
|---|---|---|
| [windows-pits.md](cheatsheets/windows-pits.md) | Git Bash/编码/路径/批处理坑 | 命令行为怪的时候 |
| [api-quick-ref.md](cheatsheets/api-quick-ref.md) | 国产 API/免费档/链上 RPC/代理选路 | 调模型、拿数据被墙的时候 |
| [deploy-recipes.md](cheatsheets/deploy-recipes.md) | 静态服务/nginx 子域/start.bat/截图 | 部署与验收交付的时候 |

## 约定

- 卡里只有两类内容：**实测过的事实** 和 **标准行为**（Windows/工具的固有机制），不写猜测
- 不含任何 API key；密钥一律走环境变量
- 每条坑 = 症状 + 原因 + 正解，能抄的命令直接抄
