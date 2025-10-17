# 雪花生成器实现文档 / Snowflake Generator Implementation

## 概述 / Overview

本项目实现了一个基于程序化生成的雪花生成引擎，具有径向对称性、星系效果和自适应画布等高级特性。

This project implements a procedural snowflake generation engine with radial symmetry, galaxy effects, and responsive canvas features.

## 核心模块 / Core Modules

### 1. SnowflakeGenerator 类 (src/snowflakeGenerator.js)

**职责 / Responsibilities:**
- 管理画布的渲染循环
- 处理画布的响应式调整
- 控制动画状态（播放/暂停）
- 维护渲染状态（角度、脉冲相位、时间）

**关键方法 / Key Methods:**
- `constructor(canvas)` - 初始化生成器并启动渲染循环
- `handleResize()` - 响应式调整画布大小以适应容器
- `setState(state, options)` - 应用新的雪花状态
- `toggleAnimation()` - 切换动画的播放/暂停
- `getRenderSnapshot()` - 获取当前渲染状态的快照（用于导出）
- `loop(timestamp)` - 主渲染循环

**特性 / Features:**
- 使用 `ResizeObserver` 监听容器尺寸变化
- 支持高 DPI 显示（通过 `devicePixelRatio`）
- 防抖优化的 resize 处理（80ms 延迟）
- 最小画布尺寸限制（360px）

### 2. 径向对称系统 / Radial Symmetry System

**实现细节 / Implementation Details:**

对称选项：
- 6-fold symmetry（6 重对称）
- 8-fold symmetry（8 重对称）
- 12-fold symmetry（12 重对称）

```javascript
const SYMMETRY_OPTIONS = [6, 8, 12];

function chooseSymmetry(preferred, random) {
    // 选择最接近期望值的对称度
    // Choose the symmetry closest to the preferred value
}

function withRadialSymmetry(ctx, count, draw) {
    // 围绕中心旋转绘制指定次数
    // Rotate and draw around center for specified count
    for (let i = 0; i < count; i++) {
        ctx.save();
        ctx.rotate((TAU / count) * i);
        draw();
        ctx.restore();
    }
}
```

### 3. 星系效果 / Galaxy Effects

#### 3.1 星空背景 / Star Field

**生成函数:** `generateStarField(params, random)`

- 基于种子的确定性随机生成
- 星星数量根据画布大小和星系密度参数调整
- 每颗星星具有独特的属性：
  - 位置 (x, y)
  - 大小 (size)
  - 亮度 (brightness)
  - 光晕衰减 (falloff)
  - 闪烁速度和相位 (twinkleSpeed, twinklePhase)

**渲染特性:**
- 径向渐变光晕效果
- 基于时间的闪烁动画
- 距离衰减（越远越暗）

```javascript
const twinkle = 0.6 + 0.4 * Math.sin(time * star.twinkleSpeed * 6 + star.twinklePhase);
const alpha = clamp(star.brightness * twinkle, 0, 1);
```

#### 3.2 星云层 / Nebula Layers

**生成函数:** `generateNebulaLayers(params, random)`

- 多层星云渐变
- 每层具有独特的颜色方案：
  - 内核色 (inner) - 最亮的中心
  - 中间色 (mid) - 过渡区域
  - 外部色 (outer) - 边缘渐隐
- 动态参数：
  - 拉伸比例 (stretch)
  - 漂移速度 (drift)
  - 初始相位 (phase)

**渲染特性:**
- 慢速旋转和呼吸效果
- 椭圆形渐变（通过 scale 变换）
- 半透明混合

#### 3.3 粒子系统 / Particle System

**类型 / Types:**

1. **Sparkles（闪光点）**
   - 围绕雪花分布的发光粒子
   - 受脉冲动画影响
   - 径向渐变光晕

2. **Particles（粒子）**
   - 更小、更分散的光点
   - 独立的闪烁频率
   - 添加景深效果

### 4. 渲染管线 / Rendering Pipeline

**渲染顺序 / Render Order:**

```
1. drawBackground() - 基础背景渐变
2. drawNebula() - 星云层
3. drawStarfield() - 星空背景
4. drawParticles() - 粒子效果
5. drawSparkles() - 闪光点
6. drawRings() - 装饰环
7. withRadialSymmetry() - 径向对称的雪花主体
   - drawArm() - 单个雪花臂
```

## 性能优化 / Performance Optimizations

### 1. 画布响应式调整 / Responsive Canvas Resizing

- 使用 `ResizeObserver` API（现代浏览器）
- 回退到 `window.resize` 事件（旧版浏览器）
- 防抖处理避免频繁 resize
- 高 DPI 适配（`devicePixelRatio`）

### 2. 渲染优化 / Rendering Optimizations

- 条件渲染：仅在动画运行或状态改变时渲染
- Canvas 状态管理：正确使用 `save()` / `restore()`
- 梯度缓存：在循环外创建渐变对象
- 早期退出：空数组检查避免无效循环

### 3. 内存管理 / Memory Management

- 临时 canvas 用于导出后立即清理
- Blob URL 使用后立即撤销
- Gallery 大小限制（24 个项目）
- 缩略图压缩（200x200）

## 参数系统 / Parameter System

### 核心参数 / Core Parameters

```javascript
{
    seed: number,                    // 随机种子
    branches: number,                 // 实际臂数（可能与 radialSymmetry 不同）
    radialSymmetry: number,           // 径向对称度（6/8/12）
    complexity: number,               // 复杂度（1-12）
    radius: number,                   // 半径（120-380）
    lineWidth: number,                // 线宽（0.6-6）
    color: string,                    // 主色调
    accentColor: string,              // 强调色
    coreColor: string,                // 核心色
    background: string,               // 背景色
    
    // 星系效果参数
    galaxyDensity: number,            // 星系密度（0.45-1.0）
    starBrightness: number,           // 星星亮度（0.55-0.9）
    starFalloff: number,              // 星光衰减（1.8-3.2）
    nebulaIntensity: number,          // 星云强度（0.35-0.75）
    nebulaScale: number,              // 星云规模（1.1-2.0）
    
    // 动画参数
    animate: boolean,                 // 是否启用动画
    spinSpeed: number,                // 旋转速度
    pulseSpeed: number,               // 脉冲速度
    pulseStrength: number,            // 脉冲强度
    glow: number,                     // 发光强度
}
```

## 随机化与可重复性 / Randomization and Reproducibility

### 种子系统 / Seed System

使用线性同余生成器（LCG）确保可重复性：

```javascript
function createRandom(seed) {
    let state = seed >>> 0;
    return () => {
        state = (state * 1664525 + 1013904223) >>> 0;
        return state / 4294967296;
    };
}
```

**特点 / Features:**
- 确定性：相同种子产生相同结果
- 快速：比 Math.random() 更高效
- 独立：每个生成阶段使用派生种子

### 种子派生 / Seed Derivation

```javascript
const structureSeed = (params.seed ^ 0x9e3779b9) >>> 0;
const starfieldSeed = (params.seed ^ 0xDEADBEEF) >>> 0;
```

## 使用示例 / Usage Examples

### 基础生成 / Basic Generation

```javascript
const generator = new SnowflakeGenerator(canvas);
const params = createParameters({ branches: 6, complexity: 5 });
const state = createSnowflakeState(params);
generator.setState(state);
```

### 自定义星系效果 / Custom Galaxy Effects

```javascript
const params = createParameters({
    galaxyDensity: 0.8,      // 更密集的星空
    starBrightness: 0.9,      // 更亮的星星
    nebulaIntensity: 0.6,     // 更强的星云
    nebulaScale: 1.5          // 更大的星云范围
});
```

### 导出高分辨率图像 / Export High-Resolution Image

```javascript
const exportCanvas = document.createElement('canvas');
exportCanvas.width = 2400;
exportCanvas.height = 2400;
const ctx = exportCanvas.getContext('2d');
const snapshot = generator.getRenderSnapshot();
renderSnowflake(ctx, state, snapshot);
```

## 浏览器兼容性 / Browser Compatibility

### 必需特性 / Required Features
- Canvas API
- ES6+ JavaScript (class, arrow functions, template literals)
- Blob API
- RequestAnimationFrame

### 可选特性 / Optional Features
- ResizeObserver (fallback to window.resize)
- Clipboard API (fallback to execCommand)
- Crypto.getRandomValues (fallback to Math.random)

### 测试环境 / Tested Environments
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 未来增强 / Future Enhancements

1. **更多对称选项** / More Symmetry Options
   - 3-fold, 4-fold, 5-fold 等
   - 混合对称（不同臂使用不同对称度）

2. **高级星系效果** / Advanced Galaxy Effects
   - 旋臂结构
   - 尘埃带
   - 黑洞效果

3. **性能提升** / Performance Improvements
   - WebGL 渲染器
   - Web Worker 用于结构生成
   - OffscreenCanvas 支持

4. **交互增强** / Interaction Enhancements
   - 手势控制（缩放、旋转）
   - 实时编辑预览
   - 动画时间轴控制

## 贡献指南 / Contributing Guidelines

保持代码风格一致：
- 使用 4 空格缩进
- 添加 JSDoc 注释
- 遵循现有命名约定
- 中英文双语注释

Maintain consistent code style:
- Use 4-space indentation
- Add JSDoc comments
- Follow existing naming conventions
- Bilingual comments (Chinese/English)

## 许可证 / License

MIT License - 详见 LICENSE 文件
MIT License - See LICENSE file for details

---

**开发者 / Developer:** Nivalis Starway Studio (牧星雪缘工作室)
**最后更新 / Last Updated:** 2025
