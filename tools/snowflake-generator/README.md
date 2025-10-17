# Snowflake Generator · 雪花生成器

一个美观、交互式的雪花生成工具，具备高级功能，包括键盘快捷键、分享功能和画廊管理。

A beautiful, interactive snowflake generator with advanced features including keyboard shortcuts, sharing functionality, and gallery management.

## ✨ Features 功能特性

- **程序化生成 / Procedural Generation**：创建独特的算法生成雪花
- **实时动画 / Real-time Animation**：流畅的旋转和脉冲效果
- **键盘快捷键 / Keyboard Shortcuts**：快速访问常用操作
- **分享功能 / Share Functionality**：复制参数为 JSON 或可分享链接
- **画廊系统 / Gallery System**：保存、管理和导出多个雪花
- **高质量导出 / High-Quality Export**：导出 2400×2400 PNG 图像
- **响应式设计 / Responsive Design**：支持桌面和移动设备

## 🚀 Quick Start 快速入门

1. 在现代浏览器中打开 `index.html`
2. 使用控制滑块调整参数
3. 点击 "Generate New" 或按 `G` 键创建新雪花
4. 按 `C` 键将雪花保存到画廊
5. 按 `E` 键导出为高分辨率 PNG

## ⌨️ Keyboard Shortcuts 键盘快捷键

| 按键 Key | 功能 Action |
|----------|-------------|
| `G` | 生成新雪花 · Generate new snowflake |
| `A` | 切换动画 · Toggle animation on/off |
| `E` | 快速导出 PNG · Quick export as PNG |
| `S` | 打开分享菜单 · Open share menu |
| `C` | 收藏至画廊 · Capture to gallery |
| `V` | 显示/隐藏画廊 · View/hide gallery |

## 🎛️ Parameters 参数说明

- **Branches（分支数）**：对称臂的数量（3-12）
- **Complexity（复杂度）**：细节与复杂程度（1-10）
- **Size（尺寸）**：雪花的整体半径（100-400px）
- **Line Width（线条宽度）**：线条的粗细（1-5px）
- **Color（颜色）**：雪花的基础颜色

## 🌐 Browser Compatibility 浏览器兼容性

需要支持以下功能的现代浏览器：
- HTML5 Canvas API
- ES6+ JavaScript 模块
- LocalStorage（用于画廊持久化）
- Clipboard API（用于分享功能）

已测试浏览器：
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🛠️ Technology Stack 技术栈

- 纯 HTML5、CSS3 和 JavaScript（ES6+）
- 无外部依赖
- Canvas API 用于渲染
- LocalStorage 用于持久化
- ES6 模块用于代码组织

## 📁 Project Structure 项目结构

```
snowflake-generator/
├── index.html          # 主应用页面 · Main application page
├── styles/
│   └── main.css       # 完整样式 · Complete styling
├── src/
│   ├── main.js        # 应用控制器 · Application controller
│   ├── snowflake.js   # 核心雪花生成逻辑 · Core snowflake generation
│   ├── gallery.js     # 画廊管理 · Gallery management
│   ├── keyboard.js    # 键盘快捷键 · Keyboard shortcuts
│   └── share.js       # 分享功能 · Share functionality
├── FEATURES.md        # 详细功能文档 · Detailed feature documentation
└── README.md          # 本文件 · This file
```

## 🔧 Development 开发说明

应用使用 ES6 模块。由于 file:// URLs 的 CORS 限制，本地开发时需要通过本地 Web 服务器提供文件。

简单的选择：
```bash
# Python 3
python3 -m http.server 8000

# Node.js（使用 npx）
npx serve

# PHP
php -S localhost:8000
```

然后在浏览器中打开 `http://localhost:8000`。

## ⚡ Performance Considerations 性能考虑

- 画廊限制为 24 个雪花，以防止内存问题
- 缩略图以 200×200 存储，提高存储效率
- 动画使用 requestAnimationFrame 实现 60fps 性能
- 导出使用临时画布，立即清理

## 📜 License 许可协议

MIT License - 详见 [LICENSE](../../LICENSE) 文件。

## 💝 Credits 致谢

由 **Nivalis Starway Studio**（牧星雪缘工作室）开发。

---

享受创作美丽的雪花吧！❄️ · Enjoy creating beautiful snowflakes! ❄️
