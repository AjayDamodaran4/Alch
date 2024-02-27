import pandas as pd
from .config_reader import Config

class ExcelUtils(object):

    def excel_to_df(self, path, excel_sheet):
        df = pd.read_excel(path, sheet_name=excel_sheet)
        return df

    
    def opt_cli_laterality(self):
        file_path = Config.get_value_of_config_key("OPT-CLI-002")
        sheet_name = "Specification Version 10"
        df = self.excel_to_df(file_path,sheet_name)
        laterality_df = df[df['localisation_type'] == 'Laterality']

        # Extract values from columns A and E for the filtered rows
        opt_cli_laterality_data = laterality_df['finding_key'].tolist()
        return opt_cli_laterality_data
        
        
