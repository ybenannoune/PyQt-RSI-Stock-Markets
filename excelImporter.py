import pandas as pd

def getCollumnInExcelFile(filename,tabName):
    df = pd.read_excel(io=filename)
    return df[tabName].values.tolist()