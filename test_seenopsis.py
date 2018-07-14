import unittest
import seenopsis
import pandas as pd
import numpy as np

df = pd.DataFrame(np.array([[1,2,3,4,56,6,7],[2,3,4,6,8,7,9]], dtype=np.int64).transpose())
df.columns = ['0','1']
print(df)


class TestSeenopsis (unittest.TestCase):

    def test_convert_csv_to_pd(self):
        my_df = seenopsis.convert_csv_to_pd("csv_for_test.csv")
        expected_df = df
        pd.testing.assert_frame_equal(my_df, expected_df)


###inside class VariableInfo:

    def test_mean(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 11.3
        self.assertAlmostEqual(tested.mean_of_var(), actual,1)


    def test_median(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 4
        self.assertAlmostEqual(tested.median_of_var(), actual,1)


    def test_lower_iqr(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 2.5
        self.assertAlmostEqual(tested.lower_iqr(), actual,1)


    def test_upper_iqr(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 6.5
        self.assertAlmostEqual(tested.upper_iqr(), actual, 1)


    def test_minimum_of_var(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 1
        self.assertAlmostEqual(tested.minimum_of_var(), actual,1)


    def test_maximum_of_var(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 56
        self.assertAlmostEqual(tested.maximum_of_var(), actual,1)


    def test_sd_of_var(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 18.35
        self.assertAlmostEqual(tested.sd_of_var(), actual,1)


    def test_unique_categories(self):
        tested = seenopsis.VariableInfo(0, df["0"], 0)
        actual = 7
        self.assertAlmostEqual(tested.unique_categories(), actual)


if __name__ == '__main__':
    unittest.main()
