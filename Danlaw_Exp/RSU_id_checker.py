import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

Outfile = '09242020_Unique_RSU_Id.csv'
Outfile_c = '09242020_Unique_RSU_Id_count.csv'
Inputfile = '09242020_UmtriServerLogReport.csv'

df1 = pd.read_csv(Inputfile)
rsu_data = df1[df1["RsuLocation"] != "0"]
#print(rsu_data.head())
#
# list(set(rsu_data.RsuLocation))
# unique_rsu = list(rsu_data['RsuLocation'].unique())
#
# df_unique_rsu = pd.DataFrame(unique_rsu,columns=['RSU_ID'])
# print(df_unique_rsu.head())
# df_unique_rsu.to_csv(Outfile)

freq = rsu_data["RsuLocation"].value_counts()
df2 = pd.DataFrame(data=freq)
df2=df2.reset_index()
df2.rename(columns={"index":"RsuLocation", "RsuLocation":"Count"},inplace=True)
print(df2.head())
df2.to_csv(Outfile_c)

df2.plot(kind="bar",title="RSU Visit Count Mapping")
plt.title("RSU_ID vs Visit Count")
plt.xlabel("RSU_ID")
plt.ylabel("Visit Count")
plt.show()

#count_rsu = rsu_data.count()
#print(count_rsu)
#count_rsu.to_csv(Outfile_c)