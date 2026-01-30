# -*- coding: utf-8 -*-
"""
运行首次启动向导

用于预览和测试向导功能
"""
import sys
from PySide6.QtWidgets import QApplication
from src.ui.wizards import FirstRunWizard


def main():
    app = QApplication(sys.argv)

    # 创建向导
    wizard = FirstRunWizard()

    # 显示向导
    wizard.show()

    # 运行应用
    result = app.exec()

    # 如果用户点击完成，打印数据
    if result == 0:  # QDialog.Accepted
        print("\n" + "=" * 50)
        print("向导完成！用户数据：")
        print("=" * 50)
        user_data = wizard.get_user_data()
        for key, value in user_data.items():
            print(f"  {key}: {value}")
        print("=" * 50 + "\n")

    sys.exit(result)


if __name__ == "__main__":
    main()
