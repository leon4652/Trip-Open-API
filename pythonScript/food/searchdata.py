import pandas as pd

csv_file_path = 'searchData_ori.csv'
output_csv_file = 'searchData_new.csv'

# CSV 파일을 pandas로 읽기
df = pd.read_csv(csv_file_path, encoding='cp949')
df = df.dropna(subset=['addr1'])

# 데이터 정제하기
df['title'] = df['title'].str.replace(r'\([^)]*\)|\[[^\]]*\]', '', regex=True)

def custom_modify_address(addr):
    parts = addr.split(' ')
    if(len(parts) <= 3):
      return ' '.join(parts[:3])
    else:
      if parts[-1].isdigit() or'-' in parts[-1]:
        return ' '.join(parts[:-1])
      elif parts[3].isdigit() or'-' in parts[3]: 
        # If the last part is a number, take the first three parts
        return ' '.join(parts[:3])
      else:
        # Otherwise, take the first four parts
        return ' '.join(parts[:4])

# 'addr1' 열을 수정
df['naddr1'] = df['addr1'].apply(custom_modify_address)

# 'addr1' 열을 수정
df['naddr1'] = df['addr1'].apply(custom_modify_address)
df['naddr2'] = df['addr1'].str.split(' ').str[:3].str.join(' ')
df['naddr1'] = df['naddr1'].str.replace(',', '')
df['naddr2'] = df['naddr2'].str.replace(',', '')

df.to_csv(output_csv_file, index=False, encoding='cp949')