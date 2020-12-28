import pandas as pd

name = 'iris.csv'
data = pd.read_csv("media/" + name)

print(list(set(data['Name'])))