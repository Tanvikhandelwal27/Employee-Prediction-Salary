import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('salary_data.csv')

le_edu = LabelEncoder()
le_role = LabelEncoder()
df['Education_Level'] = le_edu.fit_transform(df['Education_Level'])
df['Job_Role'] = le_role.fit_transform(df['Job_Role'])

X = df[['Experience', 'Education_Level', 'Job_Role']]
y = df['Salary']
model = LinearRegression()
model.fit(X, y)

pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(le_edu, open('edu_encoder.pkl', 'wb'))
pickle.dump(le_role, open('role_encoder.pkl', 'wb'))
