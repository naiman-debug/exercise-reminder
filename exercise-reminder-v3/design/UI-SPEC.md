# UI 设计规范

## 1. 整体风格

- **风格定位**：深色科技风，现代感，对比强烈
- **视觉特点**：紫色渐变主题、半透明毛玻璃效果、高对比度文字
- **参考图**：`design/reference-style.png`

---

## 2. 配色方案

### 2.1 主界面（深色模式）

```css
/* 背景色：深蓝紫渐变 */
--bg-gradient-start: #1a1a2e;
--bg-gradient-end: #16213e;

/* 主色调：紫色渐变 */
--primary-gradient-start: #7C3AED;
--primary-gradient-end: #A855F7;

/* 卡片背景：半透明毛玻璃 */
--card-bg: rgba(255, 255, 255, 0.1);
--card-blur: backdrop-filter: blur(10px);

/* 文字颜色 */
--text-primary: #FFFFFF;
--text-secondary: rgba(255, 255, 255, 0.7);
--text-tertiary: rgba(255, 255, 255, 0.5);

/* 边框颜色 */
--border-color: rgba(255, 255, 255, 0.2);
--border-focus: #A855F7;
```

### 2.2 提醒弹窗（浅色模式）

```css
/* 背景色：半透明白色 */
--modal-bg: rgba(255, 255, 255, 0.95);

/* 文字颜色 */
--modal-text-primary: #333333;
--modal-text-secondary: #666666;

/* 主按钮：与主界面一致的紫色渐变 */
--button-bg: linear-gradient(135deg, #7C3AED, #A855F7);
```

---

## 3. 字号层级

| 用途 | 字号 | 字重 | 颜色 | 说明 |
|------|------|------|------|------|
| 页面大标题 | 24px（标准）<br>32px（重要页面） | 700-800（加粗） | 白色 | 首页等重要页面可使用 32px 增强视觉冲击力 |
| 卡片标题/区块标题 | 18px | 700（加粗） | 白色 | - |
| 列表项主文字 | 16px | 500（中等） | 白色 | - |
| 正文/说明文字 | 14px | 400（常规） | rgba(255,255,255,0.7) | - |
| 次要信息（标签、时间、删除） | 12px | 400（常规） | rgba(255,255,255,0.5) | - |

**说明：**
- **标准页面**（如设置、详情页）：使用 24px 大标题
- **重要页面**（如首页、统计页）：可使用 28-32px 大标题，增强品牌识别度和视觉层次

---

## 4. 间距规则

```css
/* 页面内边距 */
--page-padding: 24px;

/* 卡片内边距 */
--card-padding: 20px;

/* 卡片之间间距 */
--card-gap: 16px;

/* 表单项之间间距 */
--form-item-gap: 16px;

/* 紧凑元素间距 */
--compact-gap: 8px;
```

---

## 5. 圆角规则

```css
/* 大卡片/弹窗 */
--radius-large: 16px;

/* 按钮/输入框 */
--radius-medium: 8px;

/* 小标签 */
--radius-small: 4px;
```

---

## 6. 按钮规则

### 6.1 主要按钮

```css
background: linear-gradient(135deg, #7C3AED, #A855F7);
color: #FFFFFF;
border: none;
border-radius: 8px;
height: 48px;  /* 推荐使用 48px，更易点击 */
padding: 0 24px;
font-weight: 600;
cursor: pointer;
transition: all 0.3s ease;

/* Hover 状态 */
box-shadow: 0 4px 16px rgba(168, 85, 247, 0.4);
transform: translateY(-2px);
```

### 6.2 次要按钮

```css
background: transparent;
color: #FFFFFF;
border: 1px solid rgba(255, 255, 255, 0.3);
border-radius: 8px;
height: 48px;  /* 推荐使用 48px，更易点击 */
padding: 0 24px;
font-weight: 500;
cursor: pointer;
transition: all 0.3s ease;

/* Hover 状态 */
border-color: #A855F7;
background: rgba(168, 85, 247, 0.1);
```

**说明：**
- **标准高度**：48px（推荐）
  - 符合现代设计趋势
  - 更易点击，提升用户体验
  - 视觉更平衡
- **紧凑场景**：44px（可选）
  - 空间受限时使用
  - 保持与输入框高度一致

### 6.3 文字按钮/链接

```css
background: transparent;
color: #A855F7;
border: none;
font-size: 12px;
cursor: pointer;
text-decoration: none;
transition: all 0.2s ease;

/* Hover 状态 */
text-decoration: underline;
```

### 6.4 危险操作（删除）

```css
background: transparent;
color: rgba(255, 255, 255, 0.5);
border: none;
font-size: 12px;
cursor: pointer;
text-decoration: none;
transition: all 0.2s ease;

/* Hover 状态 */
color: #EF4444;
text-decoration: underline;
```

---

## 7. 列表项布局

```css
/* 标准列表项（紧凑型） */
.list-item {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 内容丰富的列表项（舒适型） */
.list-item-rich {
  min-height: 60px;
  padding: 16px;
  /* 实际高度根据内容调整，通常 70-76px */
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 布局结构 */
/* 左侧：主信息（运动名称） */
/* 右侧：标签 + 操作按钮 */
/* 删除按钮放在最右侧，与标签间距 12px */

.list-item-left {
  flex: 1;
  font-size: 16px;
  font-weight: 500;
}

.list-item-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 悬停效果 */
.list-item:hover {
  background: rgba(255, 255, 255, 0.05);
}
```

**说明：**
- **标准高度 60px**：适用于内容简单的列表项（如设置页的运动库列表）
  - 只包含：图标 + 名称 + 标签 + 操作按钮
  - 使用固定 `height: 60px`
- **舒适型 70-76px**：适用于内容丰富的列表项（如首页活动详情）
  - 包含：大图标 + 多行信息 + 额外数据（热量、时间等）
  - 使用 `padding: 16px`，让高度自然适应内容
  - 提供更好的视觉呼吸感

---

## 8. 输入框规则

```css
.input-field {
  height: 44px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 0 16px;
  color: #FFFFFF;
  font-size: 14px;
  transition: all 0.3s ease;
}

/* 聚焦状态 */
.input-field:focus {
  outline: none;
  border-color: #A855F7;
  box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.1);
}

/* 占位符 */
.input-field::placeholder {
  color: rgba(255, 255, 255, 0.4);
}
```

### 8.1 输入框宽度规则

根据输入内容类型设置合理宽度：

| 输入类型 | 宽度 | CSS 类名 | 示例 |
|---------|------|----------|------|
| 短数字（1-2位）| 70px | `.input-extra-small` | 年龄（30） |
| 短数字（1-3位）| 80px | `.input-small` | 体重（70）、间隔时间 |
| 中等数字（3-4位）| 100px | `.input-fit-height` | 身高（175） |
| 中等数字（3-4位）| 120px | `.input-medium`, `.input-fit-goal` | 热量目标（300）、单次时长（120） |
| 长数字/文本 | 200px 或更宽 | `.input-wide` | 运动名称 |
| 范围输入（两个框）| 每个 80px | `.input-small` | 10 — 20 |

```css
/* 输入框宽度类 */
.input-extra-small {
  width: 70px;
}

.input-small {
  width: 80px;
}

.input-fit-height {
  width: 100px;
}

.input-medium {
  width: 120px;
}

.input-fit-goal {
  width: 120px;
}

.input-wide {
  width: 200px;
}
```

**重要原则：**
- 数字输入框**不要撑满整行**，保持紧凑
- 输入框**左对齐**，右留空白
- 宽度应该刚好容纳预期内容 + 适当留白
- 避免输入框过大导致视觉空洞

---

## 9. 标签样式

```css
/* 高强度标签 */
.tag-high {
  background: #EF4444;
  color: #FFFFFF;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

/* 中强度标签 */
.tag-medium {
  background: #F97316;
  color: #FFFFFF;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

/* 低强度标签 */
.tag-low {
  background: #22C55E;
  color: #FFFFFF;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}
```

---

## 10. 卡片样式

```css
.card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* 卡片标题 */
.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #FFFFFF;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
```

---

## 11. 特殊效果

### 11.1 毛玻璃效果（Glassmorphism）

```css
.glass-effect {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
}
```

### 11.2 渐变背景

```css
.gradient-bg {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.gradient-primary {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
}
```

### 11.3 发光效果

```css
.glow {
  box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
}

/* 文字发光 */
.text-glow {
  text-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
}
```

---

## 12. 动画规则

```css
/* 通用过渡 */
.transition-all {
  transition: all 0.3s ease;
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 卡片悬停效果 */
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  border-color: rgba(168, 85, 247, 0.3);
}
```

---

## 13. 响应式设计

```css
/* 移动端适配 */
@media (max-width: 640px) {
  :root {
    --page-padding: 16px;
    --card-padding: 16px;
  }

  /* 列表项改为垂直布局 */
  .list-item {
    height: auto;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }

  /* 按钮全宽 */
  .btn {
    width: 100%;
  }
}
```

---

## 14. 可访问性

- 文字与背景对比度至少达到 **4.5:1**（WCAG AA 标准）
- 所有交互元素（按钮、链接）必须有清晰的 **focus 状态**
- 焦点可见性：`outline: 2px solid #A855F7`
- 图标必须配合文字标签使用，或提供 `aria-label`

---

## 15. 使用说明

### ✅ 必须遵循

1. **所有页面设计必须严格遵循此规范**
2. **设计前先阅读本文档**
3. **使用 CSS 变量统一管理颜色和间距**
4. **保持视觉一致性**

### 🎯 设计原则

1. **对比强烈**：深色背景 + 亮色文字 + 紫色强调
2. **现代科技感**：毛玻璃效果 + 渐变 + 发光
3. **清晰易读**：合理的字号层级和间距
4. **流畅交互**：平滑的过渡动画

### 📋 设计检查清单

- [ ] 背景使用深蓝紫渐变
- [ ] 主按钮使用紫色渐变
- [ ] 卡片使用半透明毛玻璃效果
- [ ] 字号层级清晰（标准 24/18/16/14/12，重要页面标题可用 32px）
- [ ] 圆角规则统一（16/8/4px）
- [ ] 按钮高度 48px（推荐）或 44px（紧凑场景）
- [ ] 输入框高度 44px
- [ ] 列表项行高 60px（标准）或 70-76px（内容丰富时）
- [ ] 所有交互元素有 hover 效果

---

**文档版本**：v1.1
**最后更新**：2026-01-30
**维护者**：设计团队
**本次更新**：
- 按钮高度调整为 48px（推荐），提升点击体验
- 列表项高度支持 60-76px，根据内容复杂度选择
- 页面大标题支持 24-32px，重要页面可使用更大字号

---

> 💡 **提示**：将此规范作为设计系统的核心文档。所有新页面和组件都应基于此规范创建，以确保产品视觉的一致性和专业性。
>
> 📝 **注意**：本规范基于实际设计验证，已纳入首页原型的优化经验。规范中的灵活选项（如按钮高度、列表项高度、标题字号）应根据具体场景选择，以在一致性和用户体验之间取得平衡。
