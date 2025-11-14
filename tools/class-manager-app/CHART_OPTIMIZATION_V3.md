# 图表统计功能优化 v3.0

## 📊 优化概述

本次优化针对班级小码币统计图表窗口进行了全面改进，实现了更好的布局、滚动支持和自适应显示。

## ✨ 核心改进

### 1. 折线图布局优化 - 每行显示2个学生
- **之前**：每行显示1个学生的折线图
- **现在**：每行显示2个学生的折线图，充分利用横向空间
- **实现**：
  ```python
  line_chart_rows = max(1, (num_students + 1) // 2)  # 每行2个学生
  line_gs = fig_line.add_gridspec(line_chart_rows, 2, ...)  # 2列布局
  row = idx // 2  # 行索引
  col = idx % 2   # 列索引
  ```

### 2. 折线图区域滚动支持
- **之前**：所有图表固定在一个Figure中，学生多时图表过长
- **现在**：折线图区域支持鼠标滚轮滚动，适应任意数量学生
- **实现**：
  - 使用`tk.Canvas`和`ttk.Scrollbar`创建可滚动区域
  - 绑定鼠标滚轮事件：`<MouseWheel>`
  - 折线图嵌入到`scrollable_line_frame`中

### 3. 区域划分 - 折线图区域 + 柱状图区域
- **之前**：折线图和柱状图在同一个Figure中，布局耦合
- **现在**：明确划分为两个独立区域
  - **上方区域**：折线图区域（可滚动，expand=True）
  - **下方区域**：柱状图区域（固定高度，fill=X）
- **实现**：
  - 使用`ttk.LabelFrame`区分两个区域
  - 折线图：`fig_line`嵌入`scrollable_line_frame`
  - 柱状图：`fig_bar`嵌入`bar_frame`

### 4. 柱状图x轴标签自适应
- **之前**：固定45度或90度旋转，部分标签可能被截断
- **现在**：根据学生数量自适应调整标签显示
  - ≤5个学生：0度（水平显示）
  - 6-10个学生：45度旋转
  - >10个学生：90度旋转（完整显示）
- **实现**：
  ```python
  if len(student_names) <= 5:
      ax_bar.tick_params(axis='x', rotation=0, labelsize=9)
  elif len(student_names) <= 10:
      ax_bar.tick_params(axis='x', rotation=45, labelsize=9)
      plt.setp(ax_bar.xaxis.get_majorticklabels(), ha='right')
  else:
      ax_bar.tick_params(axis='x', rotation=90, labelsize=8)
      plt.setp(ax_bar.xaxis.get_majorticklabels(), ha='center')
  ```
- **防止截断**：使用`fig_bar.tight_layout(rect=[0, 0.03, 1, 0.97])`

### 5. 细节优化
- 奇数学生时自动隐藏最后一个空位
- 使用`LabelFrame`增强视觉层次感
- 独立的Figure尺寸控制：折线图动态高度、柱状图固定高度6英寸

## 📐 布局结构

```
┌────────────────────────────────────────────────────────────┐
│                    班级小码币统计图表                        │
├────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 学生小码币变化趋势 (LabelFrame)                      │  │
│  │ ┌────────────────────────────────────────────┐ ┌──┐ │  │
│  │ │ [折线图1] [折线图2]                        │ │▲ │ │  │
│  │ │ [折线图3] [折线图4]  <-- 可滚动区域        │ │█ │ │  │
│  │ │ [折线图5] [折线图6]                        │ │▼ │ │  │
│  │ │ ...                                        │ │  │ │  │
│  │ └────────────────────────────────────────────┘ └──┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 班级总小码币统计 (LabelFrame)                        │  │
│  │ [柱状图 - 固定高度，x轴标签完整显示]                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                      [关闭按钮]                            │
└────────────────────────────────────────────────────────────┘
```

## 🎨 优化对比

| 方面 | v2.0版本 | v3.0版本 | 改进 |
|---|---|---|---|
| 折线图布局 | 每行1个学生 | 每行2个学生 | 充分利用横向空间 |
| 滚动支持 | 无，图表过长 | 支持鼠标滚轮滚动 | 适应任意数量学生 |
| 区域划分 | 单一Figure | 独立折线图+柱状图区域 | 布局清晰，功能分离 |
| 柱状图标签 | 固定45/90° | 自适应0/45/90° | 完整显示，不截断 |
| 视觉层次 | 普通Frame | LabelFrame带标题 | 视觉层次更清晰 |

## 🔧 技术细节

### 修改文件
- `tools/class-manager-app/ui/class_detail_view.py`
- 方法：`show_chart_statistics()`
- 修改行数：约190行

### 关键实现

#### 1. 可滚动Canvas设置
```python
line_canvas = tk.Canvas(line_frame, bg='white')
line_scrollbar = ttk.Scrollbar(line_frame, orient="vertical", command=line_canvas.yview)
scrollable_line_frame = ttk.Frame(line_canvas)

scrollable_line_frame.bind(
    "<Configure>",
    lambda e: line_canvas.configure(scrollregion=line_canvas.bbox("all"))
)

line_canvas.create_window((0, 0), window=scrollable_line_frame, anchor="nw")
line_canvas.configure(yscrollcommand=line_scrollbar.set)
```

#### 2. 鼠标滚轮事件
```python
def _on_mousewheel(event):
    line_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
line_canvas.bind_all("<MouseWheel>", _on_mousewheel)
```

#### 3. 每行2列GridSpec
```python
line_gs = fig_line.add_gridspec(
    line_chart_rows, 2,
    hspace=0.35,
    wspace=0.25,
    left=0.06,
    right=0.98,
    top=0.95,
    bottom=0.05
)
```

#### 4. 行列索引计算
```python
for idx, student in enumerate(all_students):
    row = idx // 2  # 行索引
    col = idx % 2   # 列索引
    ax = fig_line.add_subplot(line_gs[row, col])
```

## ✅ 测试验证

运行验证脚本：
```bash
python3 tools/class-manager-app/test_chart_optimization_v3.py
```

验证项目：
- ✓ 每行显示2个学生的折线图
- ✓ 主框架划分两个区域
- ✓ 折线图区域使用Canvas和Scrollbar
- ✓ 绑定鼠标滚轮事件
- ✓ GridSpec每行2列布局
- ✓ 行列索引计算（每行2个）
- ✓ 奇数学生时隐藏空位
- ✓ 折线图和柱状图独立Figure
- ✓ 柱状图独立区域
- ✓ 柱状图x轴标签自适应（0/45/90度）
- ✓ tight_layout防止标签截断
- ✓ 折线图嵌入到滚动区域

## 📱 用户体验提升

1. **空间利用更高效**：每行2个折线图，减少垂直滚动距离
2. **滚动体验流畅**：鼠标滚轮支持，操作直观
3. **视觉层次清晰**：LabelFrame明确标识两个功能区域
4. **标签显示完整**：柱状图x轴标签自适应，不再被截断
5. **适应性更强**：无论学生数量多少，都能良好显示

## 🔄 向后兼容

- ✓ 所有原有功能保持不变
- ✓ 数据处理逻辑不变
- ✓ 颜色主题和样式保持一致
- ✓ 所有现有代码完全兼容

## 📝 使用说明

1. 登录班级管理系统
2. 点击进入班级详情
3. 点击"图表统计"按钮
4. **新功能**：
   - 在折线图区域使用鼠标滚轮上下滚动
   - 每行可以看到2个学生的折线图
   - 柱状图固定在底部，不受滚动影响
   - 学生名字完整显示，不截断

## 🎯 优化成果

本次优化显著提升了图表统计的可用性和用户体验，特别是在学生数量较多的场景下。通过合理的区域划分、滚动支持和自适应布局，使得图表统计功能更加实用和美观。

---

**版本**: v3.0  
**日期**: 2024  
**修改文件**: `tools/class-manager-app/ui/class_detail_view.py`  
**测试状态**: ✓ 所有优化检查通过
