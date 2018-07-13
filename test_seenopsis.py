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




# class Test_type(unittest.TestCase):
# ###test if the type is actually the var_type that is expected (categorical, because it is less than 10 unique variables)
#     def test_var_type(self):
#         tested = seenopsis.
#         actual = "Categorical variable"
#         self.assertEqual(tested, actual)
#
#
#
#
# class Test_histogram(unittest.TestCase):   ##########????
# class Test_bars(unittest.TestCase):        ##########????
# class Test_graph(unittest.TestCase):       ##########????   test if it returns a bar???
#
# class Test_mean_of_var(unittest.TestCase):
#     ###test if the mean is actually the mean that is expected    (df: 1,2,3,4,56,6,7 mean = 11.3)
#     def test_mean(self):
#         tested = seenopsis.
#         actual = 11.3
#         self.assertEqual(tested, actual)
#
#
# class Test_median_of_var(unittest.TestCase):
#     ###test if the median is actually the median that is expected  (df: 1,2,3,4,56,6,7 median = 4)
#     def test_median(self):
#         tested = seenopsis.
#         actual = 4
#         self.assertEqual(tested, actual)
#
#
#
#
# class Test_lower_iqr(unittest.TestCase):
# ###test if the lower_iqr is actually the lower_iqr that is expected  (df: 1,2,3,4,56,6,7 lower IQR = 2)
#     def test_lower_iqr(self):
#         tested = seenopsis.
#         actual = 2
#         self.assertEqual(tested, actual)
#
# class Test_upper_iqr(unittest.TestCase):
# ###test if the upper_iqr is actually the upper_iqr that is expected  (df: 1,2,3,4,56,6,7 upper IQR = 7)
#     def test_upper_iqr(self):
#         tested = seenopsis.
#         actual = 7
#         self.assertEqual(tested, actual)
#
# class Test_minimum_of_var(unittest.TestCase):
# ###test if the minimum is actually the minimum that is expected  (df: 1,2,3,4,56,6,7 minimum = 1)
#     def test_minimum_of_var(self):
#         tested = seenopsis.
#         actual = 1
#         self.assertEqual(tested, actual)
#
# class Test_maximum_of_var(unittest.TestCase):
# ###test if the maximum is actually the maximum that is expected  (df: 1,2,3,4,56,6,7 maximum = 56)
#     def test_maximum_of_var(self):
#         tested = seenopsis.
#         actual = 56
#         self.assertEqual(tested, actual)
#
#
#
# class Test_sd_of_var(unittest.TestCase):
# ###test if the sd is actually the sd that is expected  (df: 1,2,3,4,56,6,7 sd = 19.8)
#     def test_sd_of_var(self):
#         tested = seenopsis.
#         actual = 19.8
#         self.assertEqual(tested, actual)
#
#
#
# class Test_statistics(unittest.TestCase): ##########????
#     def test_statistics(self):
#         tested = seenopsis.
#         actual =
#         self.assertEqual(tested, actual)
#
#
# class Test_count_null(unittest.TestCase): ##########????
#     def test_count_null(self):
#         tested = seenopsis.
#         actual =
#         self.assertEqual(tested, actual)
#
# class Test_number_of_outliers(unittest.TestCase):
# ###test if the number_of_outliers is actually the number_of_outliersthat is expected  (df: 1,2,3,4,56,6,7 number_of_outliers = 1)
#     def test_number_of_outliers(self):
#         tested = seenopsis.
#         actual = 1
#         self.assertEqual(tested, actual)
#
# class Test_count_binary(unittest.TestCase):
#
#
# class Test_unique_categories(unittest.TestCase):
# ###test if the unique_categories is actually the unique_categories is expected  (df: 1,2,3,4,56,6,7 unique_categories = 7)
#     def test_unique_categories(self):
#         tested = seenopsis.
#         actual = 7
#         self.assertEqual(tested, actual)


if __name__ == '__main__':
    unittest.main()
