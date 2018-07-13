import unittest
import seenopsis
import pandas as pd
import numpy as np


# class Test_process_csv(unittest.TestCase):
# ####the function needs to get a csv and transform it to pandas df
# ####it use other functions:
# #   table_as_df()
#     def
#
# ###how to test?
# ###make sure that the user can choos a file
# ##make sure that the output is a pandas.df
# ##try giving the function a csv file and see that it works
# ##see if the pd dataframe is simmilar to the csv file
# ##try to give the function an excel file and not csv - and see if it fails.
#
#
# class Test_process_pandas_df(unittest.TestCase):
# ####this function take the data frame as pandas and the oputput is the html file.
# ##this function use:
# #   list_of_object()
# #   build_html
#     def
# ##how to test?
# ##give a different dataframe - for example a name of non existing datafram - and see the error
# ##give a dataframe without first name of the variables
#
#
#
# class Test_convert_csv_to_pd(unittest.TestCase):
#
# ####build a csv and read it
# ####build similar pandas df
# ####make sure that the csv is similar to the pd
#
# # pd.testing.assert_frame_equal(my_df, expected_df)
# # pd.testing.assert_series_equal(my_series, expected_series)
# # pd.testing.assert_index_equal(my_index, expected_index)
#     def
#
#
#
# class Test_list_of_object(unittest.TestCase):
# ###takes a list with the name of the variables and the dataframe and return a list of object with VariableInfo(name, values, index)
# ###need to create a data frame, and take the list of objects from the df (list(df)) and than turn it to an object in VariableInfo
# ###need to compare the objects from the df (first one) to an object created by myself. or a method of the object is what is expected.
#     def
#
#
#
# class Test_build_html(unittest.TestCase):
# ####can test what happens if one of the objects method is not provided
#     def


###inside class VariableInfo:

#################create a small dataset to test######################
global df
df = pd.DataFrame(np.array([[1,2,3,4,56,6,7],[2,3,4,6,8,7,9]] ).transpose())
print(df)

name_of_variables = list(df) ####creates a list with the name of the variables
print("this is the names of the variables", name_of_variables)


#####create objects to the test dataset based on attributes of VariableInfo
def list_of_object(name_of_variables, df_table):
    list_of_objects = []
    for index, name in enumerate(name_of_variables):
        values = df_table[name]
        list_of_objects.append(seenopsis.VariableInfo(name, values, index))
    return (list_of_objects)


#####create a list of objects for the test dataset
list_of_objects_new_dataset = list_of_object(name_of_variables,df)
print("this is the list of objects", list_of_objects_new_dataset)


############test the attributes of VariableInfo on the dataset:

class Test_var_type(unittest.TestCase):
###test if the var_type is actually the var_type that is expected (int64)
    def test_var_type(self):
        tested = seenopsis.VariableInfo.var_type(list_of_objects_new_dataset)
        print("var type", tested)
        actual = "int64"
        self.assertEqual(tested, actual)

