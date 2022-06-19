"""
    모델링 하기
"""
#%% 필요한 라이브러리 불러오기

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import confusion_matrix



#%% 데이터 불러오기
data = pd.read_csv("modeling.csv")
del data["Unnamed: 0"]


#%% train, test로 나누기(8 : 2)
x_train, x_test, y_train, y_test = train_test_split(data.drop("label", axis = 1), 
                                                    data["label"], test_size=0.2,
                                                    stratify = data["label"])

#%% RF
model = RandomForestClassifier(n_estimators=100, max_depth=20)
model.fit(x_train,y_train)

prediction = model.predict(x_test)
print(accuracy_score(y_test,prediction))

#%% DT
model = tree.DecisionTreeClassifier()
model = model.fit(x_train, y_train)

prediction = model.predict(x_test)
print(accuracy_score(y_test,prediction))

#%% MLP
mlp = MLPClassifier()
mlp.fit(x_train, y_train)
print(mlp.score(x_test, y_test)) # 61.2

#%%
"""
    ANN 모델 생성 및 성능 평가
"""
#%% 히든 레이어가 1개가 있는 ANN모델 생성

Classifier = Sequential()

Classifier.add(Dense(units = 6,
                     kernel_initializer="uniform",
                     activation="relu",
                     input_dim=12))

Classifier.add(Dense(units = 6,
                     kernel_initializer="uniform",
                     activation="relu"))

Classifier.add(Dense(units = 1,
                     kernel_initializer="uniform",
                     activation="sigmoid"))

#%% ANN 모델 학습
Classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
Classifier.fit(x_train, y_train, batch_size=100, epochs=100)

#%% ANN 모델 평가
prediction = Classifier.predict(x_test)
prediction = (prediction > 0.5)

result = confusion_matrix(y_test, prediction)
