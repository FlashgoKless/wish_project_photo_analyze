import pandas as pd
import openpyxl
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import face_recognition as fr
import PySimpleGUI as sg

layout = [  [sg.Text('Путь до фотографии:')],
            [sg.Input(), sg.FileBrowse()],
            [sg.OK(), sg.Cancel()]]

window = sg.Window('Выберите фотографию', layout)

event, jpg_list = window.read()
value1 = jpg_list[0]
window.close()

list_name_img = value1

for i in range(len(list_name_img)):
    for j in range(i+1, len(list_name_img)):
        if (list_name_img[i][0:-4]) > (list_name_img[j][0:-4]):
            list_name_img[i],list_name_img[j] = list_name_img[j],list_name_img[i]


list_lovations_for_cv = []
list_encodings = []
col = 2

xl_file = openpyxl.load_workbook('encodings.xlsx')
sheet = xl_file.active


image_fr = fr.load_image_file(str(list_name_img))
list_lovations_for_cv.append(fr.face_locations(image_fr))
list_encodings = fr.face_encodings(image_fr)
for row in range(128):
    sheet.cell(column = row+1, row = col).value = list_encodings[0][row]
col += 1

xl_file.save('encodings.xlsx')


df = pd.read_excel('encodings_learn.xlsx')

X = df.drop('target', axis = 1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.8,random_state=1)


example=pd.read_excel('encodings.xlsx')


model = RandomForestRegressor()
model.fit(X_train, y_train)
y_pred=model.predict(X_test)
mae=mean_absolute_error(y_test,y_pred)
r_sq = model.score(X_train, y_train)




example_df = pd.DataFrame(example)

if (model.predict(example)[0] >= 6) and (model.predict(example)[0] < 7.2):
    result = 10
elif (model.predict(example)[0] >= 5.5) and (model.predict(example)[0] < 6):
    result = 9
elif (model.predict(example)[0] >= 5.4) and (model.predict(example)[0] < 5.5):
    result = 8
elif (model.predict(example)[0] >= 5.3) and (model.predict(example)[0] < 5.4):
    result = 7
elif (model.predict(example)[0] >= 5.2) and (model.predict(example)[0] < 5.3):
    result = 6
elif (model.predict(example)[0] >= 5.06) and (model.predict(example)[0] < 5.2):
    result = 5
elif (model.predict(example)[0] < 5.06) and (model.predict(example)[0] >= 4.80):
    result = 4
elif (model.predict(example)[0] < 4.80) and (model.predict(example)[0] >= 4.55):
    result = 3
elif (model.predict(example)[0] < 4.55) and (model.predict(example)[0] >= 4):
    result = 2
elif model.predict(example)[0] < 4:
    result = 1


sg.popup('Ваша оценка степени доверия:', result)

print("Техническая оценка: ", model.predict(example)[0])

'''
print('---------------------------------------------------------------------------------------|')
print('mae: ',mae)
print('coefficient of determination:', r_sq)
print('---------------------------------------------------------------------------------------|')
print('Прогноз: ',model.predict(example))
print('---------------------------------------------------------------------------------------|')
'''
