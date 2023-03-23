from prettytable import PrettyTable


class UassReport:
    def __init__(self, input_filename: str) -> None:
        self.input_filename = input_filename

    def makeReport(self, output_filename):
        self.extractData()

        self.lines = []

        self.addBlock("INDIA METEOROLOGICAL DEPARTMENT", "RS/RW COMPUTATION")

        self.addValue("Balloon Release Time", "00:00")
        data = [[key, self.STATION_DETAILS[key]]
                for key in self.STATION_DETAILS]
        self.addTable(data, "OBSERVATION STATION DETAILS")

        data = [[key, self.FLIGHT_DETAILS[key]]
                for key in self.FLIGHT_DETAILS]
        self.addTable(data, "RADIOSONDE FLIGHT DETAILS")

        data = [[key, self.SURFACE_WEATHER[key]]
                for key in self.SURFACE_WEATHER]
        self.addTable(data, "SURFACE WEATHER DATA")

        self.addBlock("One Minute P.T.U. DATA")

        data = []
        for i in range(0, len(self.dataLogs), 60):
            row_data = self.dataLogs[i]
            data.append([int(i/60), row_data['Pressure'], row_data['Pressure'],
                        row_data['Humidity'], row_data['Extrenal_temp'], row_data['Altitude']])
        fields = ["Time(mins)", "Prs(hPa)", "Air Temp(C)",
                  "Rel Hum(%)", "DpTemp(C)", "Height(m)"]
        self.addTable(data, "One Minute P.T.U. DATA", fields)

        # saving file
        self.lines = ["\t"+line+"\n" for line in self.lines]
        with open(output_filename, 'w') as file:
            file.writelines(self.lines)

    def addBlock(self, header, subheader=None):
        self.lines.append("")
        self.lines.append("_"*120)
        self.lines.append("")
        self.lines.append(f"\t\t\t{header}")
        if subheader != None:
            self.lines.append(f"\t\t\t\t{subheader}")
        self.lines.append("_"*120)

    def addValue(self, name, value):
        self.lines.append("")
        self.lines.append(f"{name}\t\t = {value}")

    def extractData(self):
        text = open(self.input_filename)
        lines = text.readlines()
        lines = [line.replace("\n", "") for line in lines]

        self.STATION_DETAILS = {
            "Station Name": lines[0].replace("\t", ""),
            "Station Index": lines[1].replace("\t", ""),
            "Zonal No.": lines[2].replace("\t", ""),
            "Latitude": lines[3].replace("\t", ""),
            "Longitude": lines[4].replace("\t", ""),
            "Station Ht.": lines[5].replace("\t", ""),
        }

        self.FLIGHT_DETAILS = {
            "Balloon Weight": lines[18].replace("\t", ""),
            "Free Lift": lines[19].replace("\t", ""),
        }

        self.SURFACE_WEATHER = {
            "Surf Pressure": lines[20].replace("\t", "")+" hPa",
            "Dry Bulb Temp": lines[21].replace("\t", "")+" C",
            "Wet Bulb Temp": lines[22].replace("\t", "")+" C",
            "Rel. Humidity": lines[23].replace("\t", "")+" %",
            # "Dew Point Temp": lines[24].replace("\t","") + " C",
            # "Dew Point Dp": lines[20].replace("\t","")+" C",
            "Wnd Direction": lines[24].replace("\t", "")+" deg",
            "Surf WndSpeed": lines[25].replace("\t", "")+" m/s",
            # "Past Weather": lines[20].replace("\t","")+"",
            "Present Weather": lines[29].replace("\t", "")+"",

        }

        Datalog_start = 37

        dataLogs = []

        for i in lines[Datalog_start-1:]:
            data = i.split("\t")
            data_dict = {
                "index": data[0],
                "index2": data[8],
                "IST": data[1],
                "Pressure": data[2],
                "Extrenal_temp": data[3],
                "Internal_temp": data[4],
                "Humidity": data[5],
                "Battery Volatge": data[6],
                "GMT": data[9],
                "Latitude": data[10],
                "n / s": data[11],
                "Longitude": data[12],
                "e / w": data[13],
                "No. of Satellites": data[14],
                "Altitude": data[15],
            }

            dataLogs.append(data_dict)
        self.dataLogs = dataLogs

    def addTable(self, data=None, title=None, field_names=None):

        if data == None:
            self.lines.append("No data available")
            return

        if field_names == None:
            table = PrettyTable()
            table.header = False
        else:
            table = PrettyTable(field_names)

        if title != None:
            table.title = title

        table.add_rows(data)
        data = str(table).split("\n")

        self.lines.append("")
        self.lines += data


def main():
    report_generator = UassReport(
        "data/Cluter Telecom IMD Delhi/15-12-2020 16-30/15Dec2020_16_27.drs")
    report_generator.makeReport("myreport.txt")


if __name__ == '__main__':
    main()
