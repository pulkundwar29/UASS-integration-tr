from numpy import character
import pandas as pd
#enter the raw file name
file1 = open("15Dec2020_16_27.raw", errors="ignore")
#file1 = open("15Dec2020_12_29.raw", errors="ignore")
#file1 = open("16Dec2020_12_24.raw", errors="ignore")
#file1 = open("16Dec2020_16_39.raw", errors="ignore")
#file1 = open("17Dec2020_12_9.raw", errors="ignore")
lines = file1.readlines()
# print(lines)
#file2 = open("text.txt")
# file2.write(str(lines))

# print(lines)
#print(len(lines))
s1 = ['P', 'I', 'E', 'U', 'X', "t", 'l', 'x', 'o', 'y', 's', 'h']
e1 = ['I', 'E', 'U', 'X', "123456789", 'l', 'x', 'o', 'y', 'q1s', 'h', 'P0']
p1 = ["Pressure", "Int_temp", "Ext_temp", "Humidity", "Voltage", "GPS time",
      "Latitutde", "direction n/s", "Longitude", "direction e/w", "No. of satelite", "GPS altitude"]
len1 = [5, 5, 5, 5, 2, 8, 9, 1, 9, 1, 2, 8]
div = [10, 100, 100, 100, 10, 1, 1, 1, 1, 1, 1, 1]
mylist = []
t = len(s1)


def find_data(s1=s1, e1=e1, p1=p1, div=div):
    for line in lines:
        # print(line)
        output = {}
        for i in range(t):
            # output = {}
            # pressure
            beg = line.find(s1[i])
            end = line.find(e1[i])
            if beg == -1 or end == -1:
                continue
            val = line[beg+1:end]
            if len(val) <= len1[i]:
                try:

                    value = int(val)/div[i]
                    # output = {"Pressure": value}
                    output[p1[i]] = value
                    # print(output)
                    # mylist.append(output)
                except:
                    # try:
                    #     value = float(val)/div[i]
                    #     output[p1[i]] = value
                    # except:
                    try:
                        value = val
                        output[p1[i]] = value
                    except:
                        continue
            else:
                continue
        mylist.append(output)


find_data()
# find_data('P', 'I', "Pressure", 10)
# find_data('I', 'E', "Ext_temp", 100)
# find_data('E', 'U', "Int_Temp", 100)
# find_data('U', 'X', "Humidity", 100)
# find_data('X', "123456789", "Voltatage", 10)
# print(mylist)
data = pd.DataFrame(mylist)
#print(data.head())
data.to_csv("data1.csv")
df = pd.read_csv("data1.csv")
df=df.mean().interpolate(method='linear',limit_direction='forward')
#df1 = df.dropna(thresh=6)
print(df.head())
#data1 = df1.fillna(value='-')
#data1.to_csv("cleandata.csv")
# data1.to_csv("cleandata_15dec_12_29.csv")
# data1.to_csv("cleandata_16dec_12_24.csv")
# data1.to_csv("cleandata_16dec_16_39.csv")
# data1.to_csv("cleandata_17dec_12_9.csv")
