# PreHack

> Pre-built hackathon wheels and skills library.
>
> 预组装黑客松开发套件与即用型工具合集。

## Introduction

### English

A centralized collection of ready-to-use code assets, utility tools, integration wrappers, and practical delivery kits for hackathons.
The goal is simple: spend less time rebuilding the same infrastructure, and more time on product, logic, and iteration.

### 中文

这里收集的是适合黑客松直接复用的代码资产、工具轮子、接口封装和交付组件。
目标很直接：少重复造轮子，把时间花在产品、逻辑和快速迭代上。

## Components

### 1. `remote-batch-studio`

路径: [remote-batch-studio](./remote-batch-studio)

一个独立的远程批量生成与筛选工具：

- 批量调用远程 API 生成图片或视频
- 先只保存任务状态和远程结果 URL
- 在本地网页里做 `留下 / 淘汰`
- 只下载筛选通过的保留项
- 导出下一轮重生成包

适合需要“大量生成 -> 快速筛选 -> 保留后下载”这一类工作流。

## Content Classification

- General project templates
- Frontend and backend code wheels
- Algorithm and utility tools
- Third-party API wrappers
- Hackathon practical skills
- Quick deployment solutions

## Usage

Clone this repo and reuse the component you need.

如果你只需要某个组件，直接进入对应子目录使用即可。

## Statement

This repository is intended to grow as a toolkit shelf rather than a single project.

这个仓库更像一个组件货架，后面可以继续把别的预组装工具放进来。
