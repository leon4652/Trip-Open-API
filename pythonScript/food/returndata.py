import pandas as pd

csv_file_path = 'travelfood.csv'
output_csv_file = 'travelfood_v1.csv'

df = pd.read_csv(csv_file_path, encoding='cp949')
print(df.size)
df['food_type'] = df['food_type'].str.replace(' ', '', regex=True)
df['food_type'] = df['food_type'].str.replace('.', '/', regex=False) 
df['food_name'] = df['food_name'].str.replace(',', ' ', regex=True)
df['food_name'] = df['food_name'].str.replace('  ', ' ', regex=True)

#컬럼명 변경 
df.rename(columns={'food_id':'attraction_id'},inplace=True)
df.rename(columns={'food_idx':'food_id'},inplace=True)
df.rename(columns={'food_longtitude':'food_longitude'},inplace=True)
df.rename(columns={'food_starUser':'food_staruser'},inplace=True)

print(df[:3].head())
df.to_csv(output_csv_file, index=False, encoding='utf-8-sig')