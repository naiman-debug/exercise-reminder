# Evidence 验证脚本
# 验证项目级 Evidence 规范是否被遵守

param(
    [string]$ProjectRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

Write-Host "=" * 60
Write-Host "Evidence 验证脚本"
Write-Host "=" * 60
Write-Host ""

$Passed = 0
$Failed = 0

function Test-Item {
    param(
        [string]$Name,
        [scriptblock]$Test,
        [string]$SuccessMsg
    )

    Write-Host "[$Name] " -NoNewline
    try {
        $result = & $Test
        if ($result) {
            Write-Host "✅ PASS" -ForegroundColor Green
            if ($SuccessMsg) {
                Write-Host "  $SuccessMsg" -ForegroundColor Cyan
            }
            $script:Passed++
            return $true
        } else {
            Write-Host "❌ FAIL" -ForegroundColor Red
            $script:Failed++
            return $false
        }
    } catch {
        Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
        $script:Failed++
        return $false
    }
}

# 1. 检查 Evidence 规范文档存在
Test-Item "Evidence 规范文档" {
    Test-Path "$ProjectRoot/docs/EVIDENCE-SPEC.md"
} "docs/EVIDENCE-SPEC.md 存在"

# 2. 检查归档文档存在
Test-Item "归档文档" {
    Test-Path "$ProjectRoot/CC-ARCHIVE-*.md"
} "CC-ARCHIVE-*.md 存在"

# 3. 检查数据库初始化正常
Test-Item "数据库初始化" {
    $output = python -c "from src.models.database import get_db_manager; db = get_db_manager(); db.initialize_database(); print('OK')" 2>&1
    $output -match "OK"
} "数据库可以正常初始化"

# 4. 检查弹窗可以导入
Test-Item "弹窗导入" {
    $output = python -c "from src.ui.dialogs.stand_dialog import StandReminderDialog; from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog; from src.ui.dialogs.gaze_dialog import GazeReminderDialog; print('OK')" 2>&1
    $output -match "OK"
} "所有弹窗模块可以正常导入"

# 5. 检查音频模块导入
Test-Item "音频模块" {
    $output = python -c "from src.utils.audio_player import AudioManager; print('OK')" 2>&1
    $output -match "OK"
} "音频模块可以正常导入"

# 6. 检查音效目录存在
Test-Item "音效目录" {
    Test-Path "$ProjectRoot/src/resources/sounds"
} "src/resources/sounds 目录存在"

# 7. 检查 demo.py 存在
Test-Item "演示脚本" {
    Test-Path "$ProjectRoot/demo.py"
} "demo.py 演示脚本存在"

# 8. 检查主程序存在
Test-Item "主程序" {
    Test-Path "$ProjectRoot/src/main.py"
} "src/main.py 主程序存在"

Write-Host ""
Write-Host "=" * 60
Write-Host "验证结果: $Passed 通过, $Failed 失败"
Write-Host "=" * 60

if ($Failed -eq 0) {
    Write-Host ""
    Write-Host "🎉 所有检查通过！Evidence 规范已正确实施。" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "⚠️  有 $Failed 项检查失败，请修复后重试。" -ForegroundColor Yellow
    exit 1
}
