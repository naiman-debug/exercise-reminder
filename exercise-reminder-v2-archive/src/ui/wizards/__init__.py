# -*- coding: utf-8 -*-
"""
首次启动向导模块（3页结构）
"""
from .first_run_wizard import FirstRunWizard
from .profile_page import ProfilePage
from .reminder_settings_page import ReminderSettingsPage
from .experience_page import ExperiencePage

__all__ = ['FirstRunWizard', 'ProfilePage', 'ReminderSettingsPage', 'ExperiencePage']
