# 网页截图分析使用指南

## 概述

本指南说明如何在 Claude Code 中使用 MCP 工具进行网页截图分析。

**✅ 最新更新** (2026-01-29): GLM-4.6V-Flash MCP 工具已验证可用！

## 可用的 MCP 工具

### 1. GLM-4.6V-Flash 视觉分析 ✅ 推荐

**工具名称**: `mcp__glm-flash__analyze_image`

**状态**: ✅ 已测试可用

**功能**: 使用智谱 AI GLM-4.6V-Flash 模型分析图片

**参数**:
- `prompt` (必需): 分析提示词
- `imageUrl` (必需): 图片的公开可访问 URL

**优势**:
- ✅ 价格便宜
- ✅ 响应快速
- ✅ 中文友好
- ✅ 已验证可用

**测试结果**:
- 图像分析: ~782 tokens/次
- 响应质量: 优秀

**示例**:
```
分析网页截图中的布局结构
```

### 2. Playwright 浏览器自动化

**相关工具**:
- `mcp__playwright__browser_navigate` - 导航到网页
- `mcp__playwright__browser_take_screenshot` - 截取屏幕截图
- `mcp__playwright__browser_snapshot` - 获取页面快照

### 3. Chrome DevTools 自动化

**相关工具**:
- `mcp__chrome-devtools__navigate_page` - 导航到网页
- `mcp__chrome-devtools__take_screenshot` - 截取屏幕截图
- `mcp__chrome-devtools__take_snapshot` - 获取页面快照

## 典型工作流程

### 方案 1: 分析在线网站截图

如果你要分析的网页可以公开访问，直接使用图片 URL：

```javascript
// 1. 使用 GLM-Flash 分析网页截图
mcp__glm-flash__analyze_image({
  imageUrl: "https://example.com/screenshot.png",
  prompt: "详细描述这个网页的布局结构、配色方案和主要组件"
})
```

### 方案 2: 本地开发服务器截图分析

对于本地开发服务器（localhost），需要先将截图保存到可公开访问的位置：

#### 步骤 1: 截取页面

使用 Playwright 或 Chrome DevTools 截图：

```javascript
// 导航到本地页面
mcp__playwright__browser_navigate({
  url: "http://localhost:3000"
})

// 截取屏幕
mcp__playwright__browser_take_screenshot({
  path: "F:/claude-code/temp/inbox/screenshot.png"
})
```

#### 步骤 2: 上传到图床（可选）

由于 GLM API 需要公开可访问的 URL，你有以下选择：

1. **使用免费的图床服务**（如 imgbb.com、imgur.com）
2. **使用 GitHub 作为图床**
3. **使用云存储服务**（如阿里云 OSS、腾讯云 COS）

#### 步骤 3: 分析图片

```javascript
mcp__glm-flash__analyze_image({
  imageUrl: "https://your-image-host.com/screenshot.png",
  prompt: "分析这个网页的用户界面设计，包括布局、颜色、组件和交互元素"
})
```

### 方案 3: 使用 Vision MCP（支持本地文件）

`mcp__vision-mcp__analyze_image` 工具可能支持本地文件路径：

```javascript
mcp__vision-mcp__analyze_image({
  image: "F:/claude-code/temp/inbox/screenshot.png",
  prompt: "描述这个网页的设计风格和布局"
})
```

## 分析提示词示例

### UI/UX 分析
```
详细分析这个网页的用户界面设计，包括：
1. 整体布局结构
2. 配色方案和视觉层次
3. 主要组件和功能区域
4. 交互设计的优缺点
5. 改进建议
```

### 功能测试
```
检查这个网页是否包含以下元素：
- 导航栏
- 搜索框
- 用户登录入口
- 主要内容区域
- 页脚信息
```

### 响应式设计分析
```
分析这个网页的响应式设计：
- 是否采用了响应式布局
- 使用了什么 CSS 框架或技术
- 移动端适配情况
```

### 可访问性检查
```
评估这个网页的可访问性：
- 颜色对比度是否足够
- 是否有适当的语义化标签
- 表单是否有标签
- 图片是否有 alt 文本
```

## 费用说明

GLM-4.6V-Flash 是智谱 AI 的付费 API：
- 按调用次数计费
- 建议批量分析以提高效率
- 具体价格请参考 [智谱 AI 官网](https://open.bigmodel.cn/)

## 替代方案

如果 GLM API 不可用，可以考虑：

1. **Vision MCP** (已配置): 使用 SiliconFlow 或其他视觉模型
2. **4.5V MCP** (`mcp__4_5v_mcp__analyze_image`): Claude Opus 4.5 的视觉分析
3. **Zai MCP Server** (`mcp__zai-mcp-server__analyze_image`): 通用图像分析

## 故障排除

### 问题: MCP 工具加载失败

检查 `.mcp.json` 配置：
```json
{
  "mcpServers": {
    "glm-flash": {
      "type": "stdio",
      "command": "F:\\claude-code\\temp\\inbox\\mcp-glm-4.6v-flash\\start-server.bat",
      "args": []
    }
  }
}
```

### 问题: API Key 错误

确保环境变量正确设置：
- 检查 `start-server.bat` 中的 `GLM_API_KEY`
- 或者设置系统环境变量 `ZHIPUAI_API_KEY`

### 问题: 图片 URL 无法访问

确保：
- 图片 URL 是公开可访问的（不带认证）
- URL 格式正确（http:// 或 https://）
- 图片格式支持（jpg, png, gif 等）

## 快速开始

1. 确认 MCP 工具已加载（查看可用的 `mcp__glm-flash__*` 工具）
2. 准备好要分析的图片 URL
3. 在对话中直接请求分析，例如：

```
请分析这个网页截图：https://example.com/screenshot.png
重点关注布局结构和用户交互设计
```

Claude Code 会自动调用 GLM-Flash MCP 工具进行分析。
