class Banner:
    content = ""
    def __init__(self) -> None:
        with open ('banner.txt',"r",encoding="utf-8") as f:
            rows = f.readlines()
            self.content = self.CombineRows(rows)
    
    def GetContent(self):
        return self.content

    def CombineRows(self,rows):
        result = ""
        for row in rows:
            result += row
        return result