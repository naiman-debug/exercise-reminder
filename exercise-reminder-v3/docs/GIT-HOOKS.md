# Git Post-Commit Hook 设置说明

## ✅ 已创建文件

- **Hook 脚本**：`.git/hooks/post-commit`
- **权限**：`-rwxr-xr-x` (已设置执行权限)

## ⚠️ Windows 环境注意事项

在 Windows 上，Git hooks 可能不会自动执行，原因是：

1. **文件系统差异**：Windows 不支持直接执行 `.sh` 脚本
2. **Git Bash 路径**：需要 Git Bash 环境才能执行 bash 脚本

## 🔧 解决方案

### 方案 1：使用 Git Bash（推荐）

确保使用 Git Bash 执行 git 操作：

```bash
# 在 Git Bash 中执行
cd F:/claude-code/exercise-reminder-v3
git add .
git commit -m "message"
# hook 会自动执行
```

### 方案 2：手动执行 hook 脚本

每次 commit 后手动执行：

```bash
bash .git/hooks/post-commit
```

### 方案 3：使用 npm 脚本（推荐）

在 `package.json` 中添加脚本：

```json
{
  "scripts": {
    "commit": "git add . && git commit -m \"$(cat /tmp/commit-msg)\" && bash .git/hooks/post-commit"
  }
}
```

### 方案 4：使用 Git Hook 管理工具（最佳）

安装 `husky` 或 `pre-commit`：

```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/post-commit "bash .git/hooks/post-commit"
```

## 📝 Hook 脚本功能

当前 `post-commit` hook 会自动记录：

- ✅ Commit 时间
- ✅ Commit 信息
- ✅ 提交者名称
- ✅ Commit Hash
- ✅ 变更文件列表
- ✅ 自动追加到 `docs/WORK-LOG.md` 末尾

## 🧪 测试结果

- ✅ 脚本语法正确
- ✅ 手动执行成功
- ✅ 路径解析正确
- ⚠️ 自动执行在 Windows 上需要配置

## 📋 建议的实践

1. **使用 Git Bash** 进行所有 git 操作
2. **或使用 husky** 管理 hooks（跨平台兼容）
3. **或手动执行** hook 脚本（不推荐但可行）

---

**创建日期**：2026-01-30
**状态**：✅ 脚本已创建，⚠️ 需配置自动执行
