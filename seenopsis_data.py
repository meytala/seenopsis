# -*- coding: utf-8 -*-
import pandas as pd
import webbrowser, os, subprocess
import paths, errors, variable_info

DATA_TYPE_DF = 0
DATA_TYPE_CSV = 1
DATA_TYPE_DB = 2

# csv
CSV_ENCODINGS = ['utf-8', 'ANSI', 'ISO-8859-1', 'ISO-8859-8']
CSV_DELIMITERS = [",", "|"]
CSV_NA_VALUES = ["", "NULL"]

# print messages:
UPLOAD_FROM_CSV_SUCCEEDED = '''The data uplode from csv file "{csv_file_path}" scucceeded. The csv file is encoded with {encoding}, and the delimiter is {delimiter}.'''
UPLOAD_FROM_CSV_FAILED = '''The data upload from csv file "{csv_file_path}" failed. Please make sure the file is a valid csv file with comma delimiter (not excel).'''
UPLOAD_FROM_CSV_UNKNOWN_ENCODING_OR_DELIMITER = '''The data upload from csv file "{csv_file_path}" failed. Please make sure the encoding is one of the following: {encodings}, and the delimiter os one of the following: {delimiters}'''

# to pdf
CHROME_DIR = r"C:\Program Files (x86)\Google\Chrome\Application"

class SeenopsisData(object):
    def __init__(self, data, output_file_path, data_type=DATA_TYPE_CSV, export_to_pdf=True):
        # input
        self.csv_file_path = None
        self.query_file_path = None # for future use
        # output
        self.output_file_path = output_file_path
        self.export_to_pdf = export_to_pdf
        # data
        self.df = pd.DataFrame()
        self.columns = []
        self.encoding = 'unkown' # we can't know the encoding yet
        
        if data_type == DATA_TYPE_DF:
            self.df = data.copy(deep=True)
            
        if data_type == DATA_TYPE_CSV:
            self.csv_file_path = data
            self.upload_df_from_csv()

        # proccess df
        self.df = self.df.dropna(how='all', axis=0)
        self.df = self.df.dropna(how='all', axis=1)
        
        # get df statistics
        self.record_count =  max(self.df.count())
        self.columns_names = list(self.df)
        
        # get columns
        self.columns = self.create_columns()

    def upload_df_from_csv(self):
        for encoding in CSV_ENCODINGS:
            for delimiter in CSV_DELIMITERS:
                try:
                    self.df = pd.read_csv(self.csv_file_path, parse_dates=True, infer_datetime_format=True,
                                            date_parser=pd.to_datetime, encoding=encoding, delimiter=delimiter, na_values=CSV_NA_VALUES)
                    self.encoding = encoding
                    print(UPLOAD_FROM_CSV_SUCCEEDED.format(csv_file_path=self.csv_file_path, encoding=self.encoding, delimiter=delimiter))
                    return
                except UnicodeDecodeError:
                    pass
                except pd.errors.ParserError:
                    pass
                except OSError:
                    print(UPLOAD_FROM_CSV_FAILED.format(csv_file_path=self.csv_file_path))
                    raise errors.UploadCSVFailed
            
        print(UPLOAD_FROM_CSV_UNKNOWN_ENCODING_OR_DELIMITER.format(csv_file_path=self.csv_file_path, encodings=str(CSV_ENCODINGS), delimimters=str(CSV_DELIMITERS)))
        raise errors.UploadCSVUnknownEncoding
        
    def create_columns(self):
        columns = []
        for index, name in enumerate(self.columns_names):
            values = self.df[name]
            var = variable_info.get_variable_info(name, values, index)
            columns.append(var)

        return columns
    
    def split_by_binary(self, binary_column_name):
        binary_column = self.find_column_by_name(binary_column_name)
        if binary_column.var_type == "Binary Variable":
            for val in binary_column.unique_values:
                data = self.df[self.df[binary_column.name] == val]
                new_output_file_path, extention = os.path.splitext(self.output_file_path)
                new_output_file_path += "_{column_name}-{val}{extention}".format(column_name=binary_column_name, val=val, extention=extention)
                sd = SeenopsisData(data, new_output_file_path, data_type=DATA_TYPE_DF)
                sd.export_to_html()
            return True
        else:
            return False
    
    def find_column_by_name(self, name):
        for column in self.columns:
            if column.name == name:
                return column

    def export_to_html(self):
        html_template = paths.HTML_TEMPLATE_STR
    
        body_list = []
        html_body = paths.HTML_BODY_STR
        for column in self.columns:
            html_row_body = html_body.format\
                (column_name=column.name,
                 column_np_type=column.np_type,
                 column_graph=column.export_graph(),
                 column_statistics="<br>".join(column.list_statistics()),
                 column_null_data=column.str_null_data(),
                 column_outliers=column.str_number_of_outliers(3))
            body_list.append(html_row_body)
        
        body_list = "".join(body_list)
        merged_html = html_template.format(columns_count=len(self.columns_names), lines_count=self.record_count, table_body=body_list)
    
        with open(self.output_file_path, "w") as html_file:
            html_file.write(merged_html)
            html_file.close()
    
        if self.export_to_pdf:
            os.chdir(CHROME_DIR)
            pdf_file_path, html_extention = os.path.splitext(self.output_file_path)
            pdf_file_path += ".pdf"
            subprocess.call('chrome --headless --print-to-pdf="{pdf_file_path}" "{html_file_path}"'.format(pdf_file_path=pdf_file_path, html_file_path=self.output_file_path), shell=True, creationflags=0x08000000)
            os.chdir(paths.SCRIPT_DIR)

    def get_columns(self, filter_by_var_type=None):
        all_columns = []
        for column in self.columns:  
            if filter_by_var_type != None:
                if column.var_type == filter_by_var_type:
                    all_columns.append(column)
        return all_columns