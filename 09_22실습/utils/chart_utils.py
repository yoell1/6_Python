"""
    차트 저장 관련 유틸 함수
"""
from pathlib import Path
import matplotlib.pyplot as plt

# 이 파일(chart_utils.py) 기준, 한 단계 위(09_22실습) 안에 output 폴더를 둠
OUTPUT_DIR = Path(__file__).parent.parent / "output"

def out(name):
    """output/ 폴더 내의 파일 경로 반환"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR / name

def save_and_close(filename):
    """그래프를 output/ 폴더에 저장하고 메모리에서 정리"""
    plt.tight_layout()
    plt.savefig(out(filename))
    plt.close()