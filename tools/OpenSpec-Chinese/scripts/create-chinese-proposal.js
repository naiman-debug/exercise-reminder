#!/usr/bin/env node

/**
 * 中文提案创建工具
 * 自动创建符合格式要求的中文提案模板
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = join(__dirname, '..');

function getChangeId() {
  try {
    // 尝试从命令行参数获取
    const args = process.argv.slice(2);
    if (args.length > 0) {
      return args[0];
    }

    // 如果没有参数，提示用户输入
    console.log('请输入change-id (格式: verb-noun-description, 例如: add-user-auth):');
    process.stdout.write('> ');

    // 简单的同步输入读取 (在实际使用中可能需要更好的解决方案)
    const changeId = require('readline-sync').question('');

    if (!changeId || !/^[a-z][a-z0-9-]*$/.test(changeId)) {
      console.error('❌ 无效的change-id格式。请使用kebab-case格式。');
      process.exit(1);
    }

    return changeId;
  } catch (error) {
    console.error('❌ 无法获取change-id:', error.message);
    console.log('使用方法: node create-chinese-proposal.js <change-id>');
    process.exit(1);
  }
}

function loadTemplate(templateName) {
  const templatePath = join(projectRoot, 'openspec', 'templates', 'zh-CN', `${templateName}-template.md`);

  if (!existsSync(templatePath)) {
    console.error(`❌ 模板文件不存在: ${templatePath}`);
    process.exit(1);
  }

  return readFileSync(templatePath, 'utf8');
}

function createProposalDirectory(changeId) {
  const changesDir = join(projectRoot, 'openspec', 'changes', changeId);

  if (existsSync(changesDir)) {
    console.error(`❌ 提案目录已存在: ${changesDir}`);
    process.exit(1);
  }

  // 创建目录结构
  mkdirSync(changesDir, { recursive: true });
  mkdirSync(join(changesDir, 'specs'), { recursive: true });

  return changesDir;
}

function createFiles(changeId, changesDir) {
  // 创建proposal.md
  const proposalTemplate = loadTemplate('proposal');
  const proposalContent = proposalTemplate.replace(
    '# 提案模板',
    `# ${changeId} 提案`
  );

  writeFileSync(
    join(changesDir, 'proposal.md'),
    proposalContent
  );

  // 创建tasks.md
  const tasksTemplate = loadTemplate('tasks');
  writeFileSync(
    join(changesDir, 'tasks.md'),
    tasksTemplate
  );

  // 创建示例spec文件
  const specsDir = join(changesDir, 'specs');
  const specTemplate = loadTemplate('spec');

  // 创建一个示例capability目录和spec文件
  const capabilityDir = join(specsDir, 'example-capability');
  mkdirSync(capabilityDir, { recursive: true });

  writeFileSync(
    join(capabilityDir, 'spec.md'),
    specTemplate.replace(
      '## ADDED Requirements',
      `## ADDED Requirements\n\n### Requirement: 示例功能\n系统 MUST 提供示例功能以演示正确的格式。\n\n#### Scenario: 基本场景\n- **WHEN** 用户使用示例功能\n- **THEN** 系统必须正确响应`
    )
  );

  console.log(`✅ 已创建以下文件:`);
  console.log(`  📄 ${join(changesDir, 'proposal.md')}`);
  console.log(`  📄 ${join(changesDir, 'tasks.md')}`);
  console.log(`  📄 ${join(capabilityDir, 'spec.md')}`);
}

function showNextSteps(changeId) {
  console.log(`\n🎉 提案模板创建成功！`);
  console.log(`\n📋 接下来的步骤:`);
  console.log(`1. 编辑 proposal.md 填写具体的提案内容`);
  console.log(`2. 编辑 tasks.md 添加实施任务清单`);
  console.log(`3. 编辑 specs/example-capability/spec.md 添加具体的需求规格`);
  console.log(`4. 运行验证: openspec validate ${changeId} --strict`);
  console.log(`5. 运行中文验证: node scripts/validate-chinese-spec.js`);
  console.log(`\n💡 提示:`);
  console.log(`- 每个 Requirement 必须包含 MUST 或 SHALL 关键字`);
  console.log(`- 每个 Requirement 必须有至少一个 Scenario`);
  console.log(`- Scenario 必须使用正确的格式: #### Scenario: 名称`);
  console.log(`- Gherkin 关键词必须使用粗体: **WHEN**, **THEN**, **AND**`);
}

function main() {
  console.log('🚀 创建中文OpenSpec提案模板\n');

  const changeId = getChangeId();
  console.log(`📝 创建提案: ${changeId}\n`);

  const changesDir = createProposalDirectory(changeId);
  createFiles(changeId, changesDir);

  showNextSteps(changeId);
}

// 如果直接运行此脚本
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { getChangeId, createProposalDirectory, createFiles };