import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import numpy as np
from scipy.interpolate import make_interp_spline
from dotenv import load_dotenv

# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings("ignore", message="Workbook contains no default style, apply openpyxl's default")

# 환경 변수 로드
load_dotenv()
file_path_subway = os.getenv('FiLE_PATH_subway')

# CSV 파일 읽기
df__subway = pd.read_csv(file_path_subway, encoding='euc-kr')

# 데이터프레임 시간별 목록
time_list = df__subway.columns[4:]

# 시간대별 열 그룹화
one = [col for col in time_list if "00시-01시" in col or "01시-02시" in col or "02시-03시" in col]
two = [col for col in time_list if "03시-04시" in col or "04시-05시" in col or "05시-06시" in col]
three = [col for col in time_list if "06시-07시" in col or "07시-08시" in col or "08시-09시" in col]
four = [col for col in time_list if "09시-10시" in col or "10시-11시" in col or "11시-12시" in col]
five = [col for col in time_list if "12시-13시" in col or "13시-14시" in col or "14시-15시" in col]
six = [col for col in time_list if "15시-16시" in col or "16시-17시" in col or "17시-18시" in col]
seven = [col for col in time_list if "18시-19시" in col or "19시-20시" in col or "20시-21시" in col]
eight = [col for col in time_list if "21시-22시" in col or "22시-23시" in col or "23시-24시" in col]

# 시간대별 합계 계산
time_sums = [
    sum(df__subway[one].sum(axis=1)),    # 00-03시
    sum(df__subway[two].sum(axis=1)),    # 03-06시
    sum(df__subway[three].sum(axis=1)),  # 06-09시
    sum(df__subway[four].sum(axis=1)),   # 09-12시
    sum(df__subway[five].sum(axis=1)),   # 12-15시
    sum(df__subway[six].sum(axis=1)),    # 15-18시
    sum(df__subway[seven].sum(axis=1)),  # 18-21시
    sum(df__subway[eight].sum(axis=1)),  # 21-24시
]

# 시간대 라벨
time_labels = [
    "00-03시", "03-06시", "06-09시", "09-12시",
    "12-15시", "15-18시", "18-21시", "21-24시"
]

x_raw = np.linspace(0, 24, 8)
y_raw = time_sums

# 보간(스플라인) 설정
# 스플라인 범위를 구간 중앙값 최소~최대 사이로 설정
x_smooth = np.linspace(min(x_raw), max(x_raw), 300)
y_smooth = make_interp_spline(x_raw, y_raw)(x_smooth)

# 그래프 생성
plt.figure(figsize=(10, 6))

# 곡선형 라인 차트
plt.plot(x_smooth, y_smooth, color='b', label='총 승차/하차 인원', linewidth=2)

# X축 눈금: 구간 중앙값에 라벨 달기
plt.xticks(x_raw, time_labels)

# X축 범위를 0~24로 지정하면 처음/끝 구간이 더 자연스러워 보임
plt.xlim(0, 24)

# 차트 꾸미기
plt.title("시간대별 승차/하차 합계 (곡선형)", fontsize=15)
plt.xlabel("시간대", fontsize=12)
plt.ylabel("총 인원 수", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

plt.show()
