#!/usr/bin/env node

/**
 * 中文规格文件验证工具
 * 检查中文规格文件是否符合OpenSpec格式要求
 */

import { readFileSync, readdirSync, statSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = join(__dirname, '..');

// 中文验证规则
const CHINESE_SPEC_RULES = {
  // 必须包含的关键字检查
  mustContainKeywords: [
    'MUST',
    'SHALL'
  ],

  // 必须的标题格式
  requiredHeaders: [
    /^## ADDED Requirements$/,
    /^## MODIFIED Requirements$/,
    /^## REMOVED Requirements$/,
    /^## RENAMED Requirements$/
  ],

  // Requirement块格式
  requirementPattern: /^### Requirement: .+/,

  // Scenario块格式
  scenarioPattern: /^#### Scenario: .+/,

  // Gherkin关键词
  gherkinKeywords: [
    '**WHEN**',
    '**THEN**',
    '**AND**',
    '**GIVEN**',
    '**BUT**'
  ]
};

function validateFile(filePath) {
  try {
    const content = readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const errors = [];
    const warnings = [];

    // 1. 检查是否有MUST或SHALL关键字
    const hasMustOrShall = CHINESE_SPEC_RULES.mustContainKeywords.some(keyword =>
      content.includes(keyword)
    );

    if (!hasMustOrShall) {
      errors.push('❌ 文件缺少MUST或SHALL关键字');
    }

    // 2. 检查是否有Delta sections
    const hasDeltaSection = CHINESE_SPEC_RULES.requiredHeaders.some(pattern =>
      lines.some(line => pattern.test(line))
    );

    if (!hasDeltaSection) {
      errors.push('❌ 文件缺少Delta sections (## ADDED/MODIFIED/REMOVED Requirements)');
    }

    // 3. 检查Requirement格式
    const requirementMatches = content.match(/^### Requirement: .+$/gm);
    if (!requirementMatches || requirementMatches.length === 0) {
      errors.push('❌ 文件没有有效的Requirement块 (格式: ### Requirement: 名称)');
    }

    // 4. 检查Scenario格式
    const scenarioMatches = content.match(/^#### Scenario: .+$/gm);
    if (!scenarioMatches || scenarioMatches.length === 0) {
      errors.push('❌ 文件没有有效的Scenario块 (格式: #### Scenario: 名称)');
    }

    // 5. 检查Gherkin关键词格式
    let currentRequirement = '';
    let scenarioCount = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (CHINESE_SPEC_RULES.requirementPattern.test(line)) {
        currentRequirement = line;
        scenarioCount = 0;
      }

      if (CHINESE_SPEC_RULES.scenarioPattern.test(line)) {
        scenarioCount++;

        // 检查这个scenario是否有Gherkin关键词
        let hasGherkinKeyword = false;
        let j = i + 1;

        while (j < lines.length && !lines[j].startsWith('#')) {
          const scenarioLine = lines[j];

          if (CHINESE_SPEC_RULES.gherkinKeywords.some(keyword =>
            scenarioLine.includes(keyword)
          )) {
            hasGherkinKeyword = true;
          }

          j++;
        }

        if (!hasGherkinKeyword) {
          warnings.push(`⚠️  Scenario缺少Gherkin关键词: ${line}`);
        }
      }
    }

    // 6. 检查每个Requirement是否有至少一个Scenario
    if (requirementMatches && scenarioMatches) {
      const requirementCount = requirementMatches.length;
      const scenarioCountForRequirements = scenarioMatches.length;

      if (scenarioCountForRequirements < requirementCount) {
        warnings.push(`⚠️  有${requirementCount - scenarioCountForRequirements}个Requirement缺少Scenario`);
      }
    }

    // 7. 检查常见的中文格式问题
    const chineseFormatIssues = [];

    // 检查是否混用了中文标点
    if (content.includes('，') && content.includes(',')) {
      chineseFormatIssues.push('混合使用中英文逗号');
    }

    if (content.includes('。') && content.includes('.')) {
      chineseFormatIssues.push('混合使用中英文句号');
    }

    if (chineseFormatIssues.length > 0) {
      warnings.push(`⚠️  中文格式问题: ${chineseFormatIssues.join(', ')}`);
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings,
      stats: {
        requirements: requirementMatches?.length || 0,
        scenarios: scenarioMatches?.length || 0
      }
    };

  } catch (error) {
    return {
      valid: false,
      errors: [`❌ 读取文件失败: ${error.message}`],
      warnings: [],
      stats: { requirements: 0, scenarios: 0 }
    };
  }
}

function findSpecFiles(dir) {
  const files = [];

  function traverse(currentDir) {
    const items = readdirSync(currentDir);

    for (const item of items) {
      const fullPath = join(currentDir, item);
      const stat = statSync(fullPath);

      if (stat.isDirectory()) {
        traverse(fullPath);
      } else if (item === 'spec.md' && fullPath.includes('changes/')) {
        files.push(fullPath);
      }
    }
  }

  traverse(dir);
  return files;
}

function main() {
  const specDir = join(projectRoot, 'openspec');

  if (!existsSync(specDir)) {
    console.error('❌ 找不到openspec目录');
    process.exit(1);
  }

  const specFiles = findSpecFiles(specDir);

  if (specFiles.length === 0) {
    console.log('✅ 没有找到需要验证的规格文件');
    process.exit(0);
  }

  console.log(`🔍 验证 ${specFiles.length} 个中文规格文件...\n`);

  let totalErrors = 0;
  let totalWarnings = 0;

  for (const file of specFiles) {
    const relativePath = file.replace(projectRoot + '/', '');
    console.log(`📄 验证: ${relativePath}`);

    const result = validateFile(file);

    if (result.errors.length > 0) {
      console.log('  错误:');
      result.errors.forEach(error => console.log(`    ${error}`));
      totalErrors += result.errors.length;
    }

    if (result.warnings.length > 0) {
      console.log('  警告:');
      result.warnings.forEach(warning => console.log(`    ${warning}`));
      totalWarnings += result.warnings.length;
    }

    if (result.valid) {
      console.log(`  ✅ 验证通过 (Requirements: ${result.stats.requirements}, Scenarios: ${result.stats.scenarios})`);
    } else {
      console.log(`  ❌ 验证失败`);
    }

    console.log('');
  }

  console.log(`\n📊 验证总结:`);
  console.log(`  文件数量: ${specFiles.length}`);
  console.log(`  错误数量: ${totalErrors}`);
  console.log(`  警告数量: ${totalWarnings}`);

  if (totalErrors > 0) {
    console.log(`\n❌ 验证失败，请修复错误后重试`);
    process.exit(1);
  } else if (totalWarnings > 0) {
    console.log(`\n⚠️  验证通过，但有警告需要注意`);
  } else {
    console.log(`\n✅ 所有文件验证通过！`);
  }
}

// 如果直接运行此脚本
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { validateFile, findSpecFiles };