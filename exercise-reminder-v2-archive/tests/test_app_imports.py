# -*- coding: utf-8 -*-
"""
测试应用模块导入
"""
import pytest
import ast


def test_app_imports_qdialog():
    """Test that app.py imports QDialog correctly"""
    with open('src/core/app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if QDialog is imported from PySide6.QtWidgets
    has_qdialog_import = 'QDialog' in content and 'from PySide6.QtWidgets import' in content

    # More precise check: parse the import statement (handles multi-line imports)
    lines = content.split('\n')

    # Find all lines that are part of the from import statement
    import_lines = []
    in_import = False
    for line in lines:
        if 'from PySide6.QtWidgets import' in line:
            in_import = True
            import_lines.append(line)
        elif in_import:
            import_lines.append(line)
            if ')' in line:
                break

    import_statement = '\n'.join(import_lines)

    if import_statement:
        # Check if QDialog is in the import statement
        assert 'QDialog' in import_statement, f"QDialog not found in import statement"
    else:
        raise AssertionError("No PySide6.QtWidgets import line found")
