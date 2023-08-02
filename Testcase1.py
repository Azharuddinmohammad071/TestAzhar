# Importing the required libraries
import pandas as pd
import numpy as np
import configparser

# Reading the Excel sheet using pandas
parser = configparser.ConfigParser()
parser.read("config.txt")


def testcase1():
    # Reading source data which is in the form of csv file extension from stored path
    source_data = pd.read_csv(parser.get("config", "source_data_path") + "\\source.csv", keep_default_na=False)

    # Reading target data which is in the form of parquet file extension from stored path
    target_data = pd.read_parquet(parser.get("config", "target_data_path") + "\\target.parquet",
                                  engine='fastparquet')

    # Convert and save the target parquet file to csv file in desired path
    target_data.to_csv(parser.get("config", "target_data_path") + "\\parquetcsv.csv")

    # Reading target data final which is in the form of csv file extension from stored path
    target_data_final = pd.read_csv(parser.get("config", "target_data_path") + "\\parquetcsv.csv",
                                    keep_default_na=False)

    # Storing the columns that are required for our comparison from both source and target dataset
    columns = ['RowID', 'OrderID', 'OrderDate', 'ShipDate', 'ShipMode',
               'CustomerID', 'CustomerName', 'Segment', 'Country', 'City', 'State', 'Region', 'ProductID', 'Category',
               'SubCategory', 'ProductName', 'Sales', 'Quantity', 'Discount', 'Profit']

    # Assigning the columns stored in above variable to both source and target data
    source_data = source_data[columns]
    target_data_final = target_data_final[columns]

    # Comparing the values between source and target values
    compare_values = source_data.values == target_data_final.values

    # Comparing whether all the values are matching or not. If matches return matching else not matching
    if compare_values.all() == True:
        print("Values are matching")
    else:
        print("Values are not matching")

    # Finding the exact change in value by finding the exact location where compared values is false
    rows, cols = np.where(compare_values == False)

    for item in zip(rows, cols):
        source_data.iloc[item[0], item[1]] = '{} ----> {}'.format(source_data.iloc[item[0], item[1]],
                                                                  target_data_final.iloc[item[0], item[1]])

    # Printing the compare values in console
    print(compare_values)

    # Exporting the data comparison in excel sheet to our desired path
    source_data.to_excel(parser.get("config", "output_data_path") + "\\SDTestCase1.xlsx")


testcase1()










