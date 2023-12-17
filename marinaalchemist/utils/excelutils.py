import pandas as pd


class ExcelUtils(object):

    def excel_to_df(self, path, excel_sheet):
        df = pd.read_excel(path, sheet_name=excel_sheet)
        return df

