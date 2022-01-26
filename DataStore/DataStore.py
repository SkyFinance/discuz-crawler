import csv

class DataStore:
    def ReadLines(self,path):
        lines = []
        with open(path,'r+',encoding='utf_8_sig') as f: 
            csvReader = csv.DictReader(f)
            for row in csvReader:
                lines.append(row)
        return lines

    def SaveLines(self,path,headers:list,lines:list) -> None :
        with open(path,'w+',encoding='utf_8_sig') as f:
            csvWriter = csv.DictWriter(f,fieldnames=headers)
            csvWriter.writeheader()
            csvWriter.writerows(lines)
