#%% 필요한 라이브러리 호출
import pandas as pd
from datetime import datetime
import numpy as np


#%%
"""
    icd9 데이터에서 패혈증에 맞는 코드 찾기
"""
#%% icd9 데이터 읽기
icd_9 = pd.read_csv("icd9.csv")

#%% 패혈증에 맞는 코드 찾아주기
print(icd_9["subject_id"])

# "SEPTICEMIA"는 패혈증임
word = "SEPTICEMIA"
# 패혈증이 포함된 문장을 찾음 -> True, False로 나옴
contain_word = icd_9["description"].str.contains(word)
# 위에서 나온 True, False를 조건으로 함
condition = (contain_word == True)

# 위 조건에서 맞는 조건을 word_sub_id에 넣음
word_sub_id = icd_9[condition]["subject_id"]

# 위에서 구한 값은 패혈증이 있는 환자이기 때문에 그냥 1을 넣어줌
label = pd.DataFrame([str(1) for _ in range(len(word_sub_id))], 
                     columns = ['label'])

# 조건으로 필터링 해서 인덱스가 안맞음 -> 인덱스 번호를 초기화 해줌
word_sub_id = word_sub_id.reset_index(drop=True)

# 라벨과 붙여
word_sub_id = pd.concat([word_sub_id, label], axis = 1)

print(word_sub_id["subject_id"])


#%%
"""
    chartitem 데이터에서 패혈증과 관련된 데이터 가져오기
"""
#%% chartitem 불러오기
chartitem = pd.read_csv("d_chartitems.csv")

#%% 원하는 증상 고르기

def chart_times_item_id(data, name: str) -> list:
    """
        chart_times에 대해서 병명을 넣으면 그에 맞는 item_id를 반환해주는 함수
        
        <info parameters>
        data : dataFrame
        name : string
        yield : int
        
    """
    
    # 진단 명을 소문자로 바꿔줌
    name = name.lower()
    
    # 쉽게 접근하기 위해서 label, item_id를 따로 만들어줌
    label = data["label"]
    item_id = data["itemid"]
    
    # 반복문을 돌려서 해당 이름에 해당하는 item_id를 반환해줌
    for x in range(len(label)):
        check = label[x].lower().strip()
        if name == check:
            yield item_id[x]

# 증상들 -> 위 함수의 name이 될것임
symptoms = ["pulse", "heart rate", "Low pressure", "orientation", "nausea",
         "fever", "Nausea and Vomiting", "1.Nausea &vomitting",
         "1. Nausea and Vomit."]
           
# 빈 hash 와 map을 생성함
item_id_dict = {}

# 위에서 만든 hash와 map에 해당하는 item_id(eky)와 증상(value)을 넣어
for symptom in symptoms:
    item_id_num = list(chart_times_item_id(chartitem, symptom))
    for num in item_id_num:
        item_id_dict[num] = symptom
        
#%%
"""
    d_patient에서 나이와 성별 가져오기
"""
#%% d_patient 불러오기
patient = pd.read_csv("d_patients.csv")

#%%
print(patient.head())

# 나이를 담을 빈 리스트를 생성
patient_age = []

# 나이는 dod - dob로 구했고, 해당 문자가 날짜로 되어 있어서 해당하는 연도만 따로 구해서 나이를 구함
for idx in range(len(patient)):
    patient_age.append(int(patient['dod'][idx][-13:-9]) - int(patient['dob'][idx][-13:-9]))

# 위에서 구한 나이를 데이터 프레임으로 만들어줌
patient_age = pd.DataFrame(data = patient_age, columns=['Age'])

# 필요 없어진 열을 제거해줌
del patient['dob']
del patient['dod']
del patient['hospital_expire_flg']

# 필요 없어진 열을 제거한 데이터 프레임에 나이 데이터 프레임을 붙여
patient = pd.concat([patient, patient_age], axis = 1)
print(patient.head())
        

#%% 
"""
    chart_event 데이터 최대한 줄이기
"""
#%% chart_event 불러오기
chart_event = pd.read_csv("chartevents.csv")

#%% item id dict에 value 값으로 필터링 해줌
chart_event = chart_event.loc[(chart_event["itemid"] == 1332) | (chart_event["itemid"] == 1341)
                  | (chart_event["itemid"] == 1725) | (chart_event["itemid"] == 211)
                  | (chart_event["itemid"] == 2027) | (chart_event["itemid"] == 6107)
                  | (chart_event["itemid"] == 6417) | (chart_event["itemid"] == 6944)
                  | (chart_event["itemid"] == 479) | (chart_event["itemid"] == 6852)
                  | (chart_event["itemid"] == 3433) | (chart_event["itemid"] == 1430)
                  | (chart_event["itemid"] == 1922) | (chart_event["itemid"] == 1932)]

#%% 문자로 되어 있는 시간을 datetime 타입으로 변경

# 위에서 필터링이 되어서 인덱스를 초기화 해줌
chart_event = chart_event.reset_index(drop=True)
print(type(chart_event["charttime"][0]))

# 시간을 apply에 익명함수를 적용해서 날짜로 바꾼 후 정렬을 해줌, 정렬 과정에서 인덱스가 섞이기 때문에 인덱스를 다시 초기화 해줌
chart_event["charttime"] = chart_event["charttime"].apply(lambda _: datetime.strptime(_,'%d/%m/%Y %H:%M:%S'))
chart_event = chart_event.sort_values(by = ["subject_id", "charttime"])
chart_event = chart_event.reset_index(drop=True)

print(type(chart_event["charttime"][0]))


#%%
"""
    chart_event에 위에서 한거 다 붙이고, 증상을 0과1로 바꾸기
"""
#%% 결측치 및 필요없는 값 제거

print("chartevent_head")
print(chart_event.head())
print("chartevent_columns")
print(chart_event.columns)

# del temp["Unnamed: 0"]
del chart_event["icustay_id"]
del chart_event["elemid"]
del chart_event["realtime"]
del chart_event["cgid"]
del chart_event["cuid"]
del chart_event["value1num"]
del chart_event["value1uom"]
del chart_event["value2"]
del chart_event["value2num"]
del chart_event["value2uom"]
del chart_event["resultstatus"]
del chart_event["stopped"]
del chart_event["charttime"]

chart_event["value1"] = chart_event["value1"].dropna()

chart_event = chart_event.loc[(chart_event["value1"] != "Unable to Assess")]

print("chartevent_head")
print(chart_event.head())
print("chartevent_columns")
print(chart_event.columns)

#%% 더미 변수화 및 나이 성별 붙여주기

# item id를 더미 변수화 해줌
chart_event = pd.get_dummies(chart_event, columns = ["itemid"])

# 위에서 만들었던 것들을 다 합쳐줌
chart_event = pd.merge(chart_event, patient, on = 'subject_id', how = 'inner')
chart_event = pd.merge(chart_event, word_sub_id, on = 'subject_id', how = 'outer')

# outer조인으로 합쳤기 때문에 빈 공간에는 NaN값이 들어가 있음 -> 이 사람들은 패혈증이 걸린 사람이 아니라는 소리 -> 0으로 바꿔줌
chart_event["label"] = chart_event["label"].fillna(0)
# 필요 없는 열과 결측치를 제거해줌
del chart_event["value1"]
chart_event = chart_event.dropna()

print(chart_event.isnull().sum())

# 성별을 여자는 1, 남자는 0으로 해줌
chart_event["sex"] = np.where(chart_event["sex"] == 'F', '1', '0')

print("chartevent_head")
print(chart_event.head())
print("chartevent_columns")
print(chart_event.columns)

#%% 더미 변수화된 데이티 타입 변경

# 더미 변수화 된 데이터를 문자형을 바꿔주는데, 보기 이쁘게 하기 위해서 int로 바꾼 후 해줌
for idx in range(1,10):
    column = chart_event.columns[idx]
    chart_event[column] = chart_event[column].astype("int")
    chart_event[column] = chart_event[column].astype("str")



#%% 최종 chart_event 내보내기
chart_event.to_csv("modeling.csv")

