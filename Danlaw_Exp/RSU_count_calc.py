import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

Outfile = 'Unique_RSU_Count.csv'
Inputfile = 'Umtri_ServerLog.csv'
RsuInputfile = 'Unique_RSU_Id.csv'

VisitCounter = 0

df1 = pd.read_csv(RsuInputfile)
rsu_data = df1[["RSU_ID"]]

df2 = pd.read_csv(Inputfile)
server_data = df2[["RsuLocation"]]

df_out = pd.DataFrame({"RSU_ID": [0], "VisitCount": [0]})

for j in range(len(rsu_data)):
    VisitCounter = 0
    for i in range(len(server_data)) :
        NewRsu_Id = str(rsu_data.loc[j, "RSU_ID"])
        if (server_data.loc[i, "RsuLocation"] == NewRsu_Id):
            VisitCounter += 1
# if(VisitCounter == 0):
#     print(j , "RSU Not found -",NewRsu_Id)
# else:
#     print(j , "RSU Found -",NewRsu_Id, "---", VisitCounter)
    df_out.loc[j, "RSU_ID"] = NewRsu_Id
    df_out.loc[j, "VisitCount"] = VisitCounter
df_out.to_csv(Outfile)

# df_out.plot(kind="bar",title="RSU Visit Count Mapping")
# plt.title("RSU_ID vs Visit Count")
# plt.xlabel("RSU_ID")
# plt.ylabel("Visit Count")
# plt.show()

plt.figure(figsize=(14, 14))
splot=sns.barplot(x="RSU_ID",y="VisitCount",data=df_out)
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.1f'),
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center', va = 'center',
                   xytext = (0, 9),
                   textcoords = 'offset points')
plt.xlabel("RSU_ID", size=14)
plt.ylabel("Visit Count", size=14)
plt.show()
plt.savefig("RSU_ID vs Visit Count.png")