#!/usr/bin/env node

/**
 * MCP 服务器列表更新脚本
 * 用途：扫描当前安装的 MCP 服务器并生成 Markdown 文档
 * 使用：node update-mcp-docs.js
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const OUTPUT_FILE = path.join(__dirname, '../../docs/mcp/MCP_SERVERS.md');
const DATE = new Date().toISOString().split('T')[0];

console.log('🔍 扫描 MCP 服务器...');

try {
    // 获取 MCP 列表
    const output = execSync('claude mcp list', { encoding: 'utf-8' });

    // 解析输出
    const lines = output.split('\n').filter(line => line.trim());
    const servers = [];

    for (const line of lines) {
        // 解析格式: name: command - status
        const match = line.match(/^([^:]+):\s+(.+?)\s+-\s+(✓ Connected|✗ Failed to connect|⚠ Needs authentication)/);
        if (match) {
            const [, name, command, status] = match;
            servers.push({ name, command, status });
        }
    }

    // 分类
    const connected = servers.filter(s => s.status.includes('✓ Connected'));
    const needsAuth = servers.filter(s => s.status.includes('⚠'));
    const failed = servers.filter(s => s.status.includes('✗'));

    // 生成 Markdown
    let markdown = `# MCP 服务器配置文档

> **更新日期**：${DATE}
> **用途**：记录所有已安装的 MCP 服务器及其状态
> **总计**：${servers.length} 个服务器

---

## 一、已安装并连接成功 (${connected.length}个)

`;

    // 已连接的服务器
    for (const server of connected) {
        markdown += `### ${server.name}
- **状态**：✓ 已连接
- **命令**：\`${server.command}\`

`;
    }

    // 需要认证的
    if (needsAuth.length > 0) {
        markdown += `---

## 二、需要认证 (${needsAuth.length}个)

`;
        for (const server of needsAuth) {
            markdown += `### ${server.name}
- **状态**：⚠️ 需要认证
- **命令**：\`${server.command}\`

`;
        }
    }

    // 连接失败的
    if (failed.length > 0) {
        markdown += `---

## 三、连接失败 (${failed.length}个)

`;
        for (const server of failed) {
            markdown += `### ${server.name}
- **状态**：✗ 连接失败
- **命令**：\`${server.command}\`

`;
        }
    }

    // 写入文件
    fs.writeFileSync(OUTPUT_FILE, markdown, 'utf-8');

    console.log(`✅ 文档已更新：${OUTPUT_FILE}`);
    console.log(`📊 统计：`);
    console.log(`   - 已连接：${connected.length}`);
    console.log(`   - 需要认证：${needsAuth.length}`);
    console.log(`   - 连接失败：${failed.length}`);
    console.log(`   - 总计：${servers.length}`);

} catch (error) {
    console.error('❌ 错误：', error.message);
    console.error('提示：请确保 claude 命令可用');
    process.exit(1);
}
