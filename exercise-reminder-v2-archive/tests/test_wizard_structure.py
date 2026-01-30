# -*- coding: utf-8 -*-
"""
测试向导模块结构
"""
import pytest


def test_wizard_module_exists():
    """Test wizard module can be imported"""
    from src.ui.wizards import FirstRunWizard
    assert FirstRunWizard is not None
