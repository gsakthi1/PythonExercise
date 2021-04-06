import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

Outfile = '09242020_RSuAnalytics_Output.csv'
Inputfile = '09242020_UmtriServerLogReport.csv'
asd_Outfile = '09242020_AsdAnalytics_Output.csv'
asd_Visitfile ="09242020_AsdVisit_Output.csv"

df1 = pd.read_csv(Inputfile)
rsu_data = df1[df1["RsuLocation"] != "0"]

freq = rsu_data["RsuLocation"].value_counts()
df2 = pd.DataFrame(data=freq)
df2=df2.reset_index()
df2.rename(columns={"index":"RsuLocation", "RsuLocation":"Count"},inplace=True)
print(df2.head())
df2.to_csv(Outfile)

df2.plot(kind="bar",title="RSU Visit Count Mapping")
plt.title("RSU_ID vs Visit Count")
plt.xlabel("RSU_ID")
plt.ylabel("Visit Count")
plt.show()

max_rsu_visit = "200148a868fa10aa0e0a0025000000a1"
asd_data = df1[df1["RsuLocation"] == max_rsu_visit]
asd_freq = asd_data["Serial No"].value_counts()
df3 = pd.DataFrame(data=asd_freq)
df3=df3.reset_index()
df3.rename(columns={"index":"Serial No", "Serial No":"Count"},inplace=True)
print(df3.head())
df3.to_csv(asd_Outfile)

max_asd_visit = "18090898"
max_data = df1[df1["RsuLocation"] == max_rsu_visit]
#print(max_data)
df4 = pd.DataFrame(data=asd_data)
print(df4.head())
df5 = df4.filter(like=max_asd_visit)
print(df5.head())
df4.to_csv(asd_Visitfile)
df5.to_csv("Asd_18090898.csv")