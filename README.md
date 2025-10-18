# Nivalis-Starway Studio Monorepo · 牧星雪缘工作室多工具仓库

欢迎来到 **Nivalis-Starway Studio**（牧星雪缘工作室）的多工具创意实验室。这个仓库以 Monorepo 形式管理所有的互动工具与游戏，统一的极光星空视觉风格、共享主题以及协同的开发体验帮助我们快速迭代未来的创意作品。
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Nivalis-Starway-Studio/Nivalis-Starway)
## ✨ Overview 概览
- **多工具架构**：单一仓库管理多个工具/游戏，便于共享主题、组件与资源。
- **统一品牌视觉**：通过 `/shared/styles/theme.css` 定义的星空/极光主题，在所有页面保持一致的体验。
- **扩展性设计**：`/tools` 目录为每个工具提供独立的代码与资源结构，方便持续扩展。

## 📁 Directory Structure 目录结构
```
.
├── index.html                        # 主作品集入口页 · Portfolio Landing Page
├── shared/                           # 跨工具共享资源 · Shared Resources
│   ├── assets/                       # 公共素材占位 · Global Assets (placeholder)
│   ├── components/                   # 公共组件占位 · Shared Components (placeholder)
│   └── styles/
│       └── theme.css                 # 统一主题变量与基础样式 · Global Theme Styles
├── tools/
│   └── snowflake-generator/          # 雪花生成器工具 · Snowflake Generator Tool
│       ├── index.html
│       ├── src/
│       │   ├── gallery.js
│       │   ├── keyboard.js
│       │   ├── main.js
│       │   ├── share.js
│       │   └── snowflake.js
│       ├── styles/
│       │   └── main.css
│       └── FEATURES.md               # 功能说明文档 · Feature Documentation
├── LICENSE
└── README.md
```

## 🏁 Getting Started 快速上手
1. **打开主站 / Open Landing Page**  
   直接在浏览器中打开仓库根目录的 `index.html`，体验品牌主页与工具导航。
2. **进入雪花生成器 / Launch Snowflake Generator**  
   访问 `tools/snowflake-generator/index.html`，即可使用目前提供的互动雪花创作工具。
3. **本地开发 / Local Development**  
   建议通过本地服务器加载（例如 `python3 -m http.server 8000`），确保 ES6 模块正常工作。

## 🎨 Shared Theme 共享主题
- 全部页面均引入 `shared/styles/theme.css`，提供颜色、字体、间距与按钮等基础样式。
- 主题包含自适应断点、极光背景动画与星空细节，为后续工具提供统一视觉语言。

## 🧰 Current Tools 当前工具
| 工具 Tool | 说明 Description | 状态 Status |
|-----------|------------------|-------------|
| [Snowflake Generator · 雪花生成器](tools/snowflake-generator/) | 程序化雪花创作工具，支持画廊、键盘快捷键、分享与高分辨率导出。 | ✅ 已上线 Available |

更多工具正在研发中，敬请期待。

## 🛣️ Roadmap 路线图
1. Star Map Generator · 星图生成器 — 根据时间与地点生成专属星空
2. Aurora Simulator · 极光模拟器 — 交互式极光渲染体验
3. Crystal Generator · 晶体生成器 — 生成多面晶体与光照效果
4. Audio Visualizer · 音乐可视化工具 — 声音与动画的同步表现
5. Particle Art Studio · 粒子艺术工作室 — 粒子系统创意沙盒
6. Fractal Explorer · 分形探索器 — 探索曼德博与 Julia 集
7. Pixel Art Editor · 像素艺术编辑器 — 轻量像素画创作平台
8. Terrain Generator · 地形生成器 — 程序化生成 3D 地形场景
9. Poetry Generator · 诗歌生成器 — AI 辅助的诗歌灵感工具
10. 更多创意项目持续规划中 · More ideas are on the way

## 🤝 Contributing 贡献指南
- 欢迎以 Issues 或 Pull Requests 的形式提交建议。建议遵循现有的目录结构与主题规范。
- 新增工具时，请在 `/tools/<tool-name>/` 下创建独立的目录结构，并复用 `/shared` 中的样式与资源。
- 所有新增内容请优先提供中英文对照，确保全球用户与中文用户都能愉快体验。

## 📄 License 许可协议
本项目遵循 [MIT License](LICENSE)。欢迎自由使用与拓展，只需保留版权声明。

让我们一同在星轨之间，雕刻灵感的雪花。❄️🌌
