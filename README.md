# mimic2 데이터를 이용한 패혈증 환자 분류

## 1. 패혈증에 대해서
- 패혈증은 미생물 감염에 대한 전신적인 반응으로 주요 장기에 장애를 유발하는 질환입니다.

### 1-1. 증상
- 빈백
- 빈호흡
- 심부전
- 오한
- 열
- 의식 저하
- 소변량 감소
- 저혈압
- 반점
- 근육통
- 구역 및 반점
- 등등 여러가지가 있습니다.
> 저는 위의 __증상들과 매칭이 되는 ItemId__ 를 사용해서 패혈증을 분류 했습니다.

## 2. 전처리
### 2-1. 패혈증이 한번이라도 걸린 적이 있는 환자의 subject_id를 가져왔습니다.
![image](https://user-images.githubusercontent.com/74887218/174982385-aef64565-6d09-4a54-9b40-3a5873e9c385.png)
***

### 2-2. 위 증상에 맞는 ItemId를 해시와 맵 형태로 저장했습니다. 
![image](https://user-images.githubusercontent.com/74887218/174982490-1a44cb04-9236-4dcd-9113-bd6be8f71c68.png)
***

### 2-3. 환자들의 나이를 구해줬습니다.
![image](https://user-images.githubusercontent.com/74887218/174983234-3442bb85-0b0e-4479-a434-fd781466adbb.png)   
   
나이는 DOD(data of death)에서 DOB(date of birth)를 빼서 구했습니다
***

### 2-4. 위에서 구한 증상들만 있을 수 있게 필터링을 해줬습니다. 또한 필터링을 함으로서 데이터의 크기를 줄여줬습니다. 
![image](https://user-images.githubusercontent.com/74887218/174983895-a85ff90d-e5c1-4072-8cd0-cc329e57ff8d.png)
***

### 2-5. 그 후 에는 필요 없는 열을 다 제거해주고, ItemId을 원핫이코딩을 해주었습니다.
![image](https://user-images.githubusercontent.com/74887218/174984223-a63c0441-69e3-4ded-92ea-8aeb409a93df.png)

## 3. 모델 및 사용 결과
### 3-1. RF
<img src = "https://user-images.githubusercontent.com/74887218/174984390-9c62542a-298f-439f-9ecc-b33ec73d5717.png" width="30%" height="30%">
너무 높게 나왔습니다. 아마도 전처리 하는 과정에서 문제가 생긴 것 같습니다.
***

### 3-2. DT
<img src = "https://user-images.githubusercontent.com/74887218/174984562-27543084-2d48-4a3f-b2cc-5667cc059c98.png" width="10%" height="10%">   
RF모델과 같이 전처리 과정에서 문제가 생긴 것 같습니다. 
***

### 3-3. ANN
<img src = "https://user-images.githubusercontent.com/74887218/174984736-1e4f9cd8-076c-4ffe-85bb-5afd9f90a8d1.png" width="70%" height="70%">   
- batch size = 100, epoch = 100 으로 했습니다.
***

### 3-4. MLP
<img src = "https://user-images.githubusercontent.com/74887218/174986347-ba75af0c-ecb7-474f-a73b-f90e651491b2.png" width="30%" height="30%">   
*** 

