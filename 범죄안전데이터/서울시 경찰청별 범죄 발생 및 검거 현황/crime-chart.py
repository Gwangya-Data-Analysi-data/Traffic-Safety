import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import numpy as np
from collections import defaultdict
from dotenv import load_dotenv

# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings("ignore", message="Workbook contains no default style, apply openpyxl's default")

def read_and_extract_city(file_path, year, city='서울', id_col_count=3):
    """
    엑셀 파일을 읽어와 3행을 다중 헤더로 사용하고, 
    범죄 항목(첫 id_col_count 열)에 forward-fill을 적용한 후,
    헤더 레벨 0(연도)가 지정한 year이고, 헤더 레벨 1(도시)가 지정한 city인 열만 추출하여 DataFrame 반환.
    """
    df = pd.read_excel(file_path, header=[0, 1, 2])
    df.iloc[:, :id_col_count] = df.iloc[:, :id_col_count].ffill()
    
    id_cols = df.columns[:id_col_count]
    other_cols = df.columns[id_col_count:]
    target_cols = [col for col in other_cols if str(col[0]).strip() == str(year) and col[1] == city]
    
    df_target = df.loc[:, list(id_cols) + target_cols].copy()
    df_target.columns = ['_'.join(map(str, col)).strip() for col in df_target.columns.values]
    
    return df_target

def read_and_extract_district(file_path, year, district, city='서울', id_col_count=3):
    """
    파일을 읽어와 3행 다중 헤더를 사용하고, 
    범죄 항목(첫 id_col_count 열)에 forward-fill을 적용한 후,
    헤더 레벨 0(연도)가 year, 레벨 1(도시)가 city, 레벨 2(구)가 district인 열만 선택하여 
    식별용 열과 함께 반환하는 함수.
    """
    df = pd.read_excel(file_path, header=[0, 1, 2])
    df.iloc[:, :id_col_count] = df.iloc[:, :id_col_count].ffill()
    
    id_cols = df.columns[:id_col_count]
    other_cols = df.columns[id_col_count:]
    
    target_cols = [col for col in other_cols 
                   if str(col[0]).strip() == str(year) 
                   and col[1] == city 
                   and str(col[2]).strip() == district]
    
    df_target = df.loc[:, list(id_cols) + target_cols].copy()
    df_target.columns = ['_'.join(map(str, col)).strip() for col in df_target.columns.values]
    
    return df_target

load_dotenv()

# 환경 변수 불러오기
file2023_path = os.getenv('FILE2023_PATH')
file_path22_21 = os.getenv('FILE_PATH22_21')
file_path19_20 = os.getenv('FILE_PATH19_20')
file_path17_18 = os.getenv('FILE_PATH17_18')
file_image_crime = os.getenv('File_image_crime')

# 서울 전체 데이터 추출 (연도별)
df2023 = read_and_extract_city(file2023_path, year=2023, city='서울')
df2022 = read_and_extract_city(file_path22_21, year=2022, city='서울')
df2021 = read_and_extract_city(file_path22_21, year=2021, city='서울')
df2020 = read_and_extract_city(file_path19_20, year=2020, city='서울')
df2019 = read_and_extract_city(file_path19_20, year=2019, city='서울')
df2018 = read_and_extract_city(file_path17_18, year=2018, city='서울')
df2017 = read_and_extract_city(file_path17_18, year=2017, city='서울')

# 서울 광진구 데이터 추출 (연도별) - 필요 시 사용
df_2023_guangjingu = read_and_extract_district(file2023_path, year=2023, district='광진')
df_2022_guangjingu = read_and_extract_district(file_path22_21, year=2022, district='광진')
df_2021_guangjingu = read_and_extract_district(file_path22_21, year=2021, district='광진')
df_2020_guangjingu = read_and_extract_district(file_path19_20, year=2020, district='광진')
df_2019_guangjingu = read_and_extract_district(file_path19_20, year=2019, district='광진')
df_2018_guangjingu = read_and_extract_district(file_path17_18, year=2018, district='광진')
df_2017_guangjingu = read_and_extract_district(file_path17_18, year=2017, district='광진')

# 사용할 범죄 유형 및 연도 리스트
categories = list(df2023['범죄별(2)_범죄별(2)_범죄별(2)'].unique())
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]

# 사용자 지정 색상 (요청한 색상 계열)
color_list = [
    "#00008B",  # DarkBlue
    "#0000CD",  # MediumBlue
    "#191970",  # MidnightBlue
    "#1E90FF",  # DodgerBlue
    "#4169E1",  # RoyalBlue
    "#4682B4",  # SteelBlue
    "#5F9EA0",  # CadetBlue
    "#6495ED"   # CornflowerBlue
]
# 연도별 데이터프레임 리스트
year_df = [df2023, df2022, df2021, df2020, df2019, df2018, df2017]

filtered_data = {}

# 데이터 필터링 및 NaN값 처리
for category in categories:
    filtered_data[category] = []
    for df in year_df:
        filtered_df = df[df['범죄별(2)_범죄별(2)_범죄별(2)'] == category]
        filtered_df = filtered_df.drop(columns=['범죄별(2)_범죄별(2)_범죄별(2)'])
        filtered_df = filtered_df.reset_index(drop=True)
        filtered_df = filtered_df.replace("-", 0)
        filtered_data[category].append(filtered_df)

list_total2 = []

# 각 범죄 유형에 대해 연도별 데이터프레임 합산
for i in range(len(year_df)):
    for j in categories:
        list_sum = filtered_data[j][i].iloc[:, 3:].replace("-", 0).astype(int).sum().sum()
        list_total2.append([years[i], j, list_sum])

# 항목별 전체 합계 계산 (파이차트용)
from collections import defaultdict
crime_totals = defaultdict(int)
for _, crime, value in list_total2:
    crime_totals[crime.strip()] += value

labels = list(crime_totals.keys())
values = list(crime_totals.values())
total = sum(values)
percentages = [100 * v / total for v in values]
legend_labels = [f"{label}: {pct:.1f}%" for label, pct in zip(labels, percentages)]

# 데이터프레임 변환 (누적 막대 그래프용)
df_chart = pd.DataFrame(list_total2, columns=['년도', '범죄유형', '건수'])
df_pivot = df_chart.pivot(index='년도', columns='범죄유형', values='건수')

# 한 Figure 안에 파이차트와 누적 막대 그래프를 서브플롯으로 표시
fig, axs = plt.subplots(1, 2, figsize=(16, 8))

# ----- 파이차트 서브플롯 -----
wedges, _ = axs[0].pie(values, labels=None, startangle=140, colors=color_list)
axs[0].legend(wedges, legend_labels, title="범죄 유형", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
axs[0].set_title('범죄 유형별 비율', fontsize=14)

# ----- 누적 막대 그래프 서브플롯 -----
df_pivot.plot(kind='bar', stacked=True, color=color_list, ax=axs[1])
axs[1].set_title('연도별 형법범죄 발생 추이', fontsize=16)
axs[1].set_xlabel('년도')
axs[1].set_ylabel('발생 건수')
axs[1].legend(title='범죄유형', bbox_to_anchor=(1.02, 1), loc='upper left')

# 레이아웃 조정 및 출력
plt.tight_layout()
# plt.show()

plt.savefig(file_image_crime, format="png", dpi=300)