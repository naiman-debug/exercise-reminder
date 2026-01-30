# 本地开发网页截图分析 - 快速工作流程

## 问题

本地开发服务器 (localhost) 的截图无法直接被 GLM API 访问，因为：
- GLM API 需要公开可访问的图片 URL
- localhost 只在本地可访问

## 解决方案

### 方案 A: 使用 Vision MCP（推荐 - 最简单）

Vision MCP 已配置 SiliconFlow，可能支持本地文件或 base64：

```javascript
// 在 Claude Code 对话中直接使用：
"请分析本地截图 F:/claude-code/temp/inbox/screenshot.png 的布局设计"
```

Claude 会自动调用 `mcp__vision-mcp__analyze_image` 工具。

### 方案 B: GitHub 图床（推荐 - 稳定免费）

1. **创建 GitHub 仓库用于存放截图**
   ```bash
   # 在 GitHub 创建新仓库: screenshots
   # 克隆到本地
   cd F:/claude-code
   git clone https://github.com/YOUR_USERNAME/screenshots.git
   ```

2. **截图并提交**
   ```bash
   # 使用任意工具截图到 screenshots 目录
   # 例如使用 Playwright:
   mcp__playwright__browser_take_screenshot({
     path: "F:/claude-code/screenshots/screenshot.png"
   })

   # 提交到 GitHub
   cd F:/claude-code/screenshots
   git add .
   git commit -m "Add screenshot"
   git push
   ```

3. **获取图片 URL**
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/screenshots/main/screenshot.png
   ```

4. **使用 GLM-Flash 分析**
   ```javascript
   mcp__glm-flash__analyze_image({
     imageUrl: "https://raw.githubusercontent.com/YOUR_USERNAME/screenshots/main/screenshot.png",
     prompt: "分析这个网页的 UI 设计"
   })
   ```

### 方案 C: 免费图床 API（自动化）

使用 imgbb 等免费图床的 API：

```javascript
// upload-image.js
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

async function uploadToImgBB(imagePath, apiKey) {
  const form = new FormData();
  form.append('image', fs.createReadStream(imagePath));

  const response = await fetch(
    `https://api.imgbb.com/1/upload?key=${apiKey}`,
    { method: 'POST', body: form }
  );

  const data = await response.json();
  return data.data.url;
}

// 使用示例
const imageUrl = await uploadToImgBB(
  'F:/claude-code/temp/inbox/screenshot.png',
  'YOUR_IMGBB_API_KEY'
);

console.log('图片 URL:', imageUrl);
```

获取 imgbb API key: https://api.imgbb.com/

### 方案 D: 本地 HTTP 服务器（临时解决）

使用 Python 快速启动本地服务器：

```bash
# 在截图目录启动服务器
cd F:/claude-code/temp/inbox
python -m http.server 8080

# 使用 ngrok 或类似工具暴露到公网
# 下载: https://ngrok.com/
ngrok http 8080

# 得到公网 URL，例如:
# https://abc123.ngrok.io/screenshot.png
```

## 完整工作流程示例

### 在 Claude Code 中使用

**场景**: 分析本地开发服务器上的网页

```
你: 请帮我分析 http://localhost:3000 这个页面的 UI 设计

Claude:
[自动执行以下步骤]

1. [使用 Playwright 导航到页面]
2. [截取屏幕保存到本地]
3. [上传到图床/GitHub]
4. [使用 GLM-Flash 分析]
5. [返回分析结果]

分析结果：
[详细的 UI 设计分析...]
```

### 手动操作步骤

如果需要手动操作：

```bash
# 1. 截图（使用 Playwright）
# 通过 MCP 工具完成

# 2. 上传到 GitHub
cp F:/claude-code/temp/inbox/screenshot.png F:/claude-code/screenshots/
cd F:/claude-code/screenshots
git add .
git commit -m "Add screenshot"
git push

# 3. 获取 URL
# https://raw.githubusercontent.com/YOUR_USERNAME/screenshots/main/screenshot.png

# 4. 在 Claude Code 中分析
# "请分析 https://raw.githubusercontent.com/.../screenshot.png 这个网页"
```

## 优缺点对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| Vision MCP | 最简单，可能支持本地文件 | 依赖 SiliconFlow 配置 | ⭐⭐⭐⭐⭐ |
| GitHub 图床 | 稳定、免费、永久保存 | 需要手动提交 | ⭐⭐⭐⭐ |
| 图床 API | 可自动化 | 有流量限制，依赖第三方 | ⭐⭐⭐ |
| 本地服务器+内网穿透 | 快速临时解决 | 需要额外工具，URL 会变 | ⭐⭐ |

## 推荐配置

**对于日常开发**：使用方案 A (Vision MCP) 或方案 B (GitHub 图床)

**对于自动化测试**：使用方案 C (图床 API) 或结合 CI/CD 使用方案 B

## 获取免费图床 API Key

### ImgBB
1. 访问 https://imgbb.com/
2. 注册账号
3. 进入 https://api.imgbb.com/
4. 创建 API Key

### Imgur
1. 访问 https://imgur.com/
2. 注册账号
3. 进入 https://api.imgur.com/
4. 创建 Application
5. 获取 Client ID

### Cloudinary (免费额度大)
1. 访问 https://cloudinary.com/
2. 注册账号
3. 获取 API Key 和 Cloud Name
