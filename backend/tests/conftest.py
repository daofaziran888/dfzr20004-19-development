"""pytest 配置：确保测试运行目录在 backend/ 下，Python 路径包含当前目录。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))