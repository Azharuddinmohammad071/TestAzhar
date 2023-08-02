# Importing the required libraries
import pandas as pd
import numpy as np
import configparser

# Reading the Excel sheet using pandas
parser = configparser.ConfigParser()
parser.read("config.txt")


def testcase3():
    # Reading source data which is in the form of parquet file extension from stored path
    source_data = pd.read_parquet(parser.get("config", "source_data_path") + "\\Sourcedata.parquet",
                              engine='fastparquet')

    # Reading 3 different target data files which is in the form of CSV file extension from stored path
    target_data1 = pd.read_csv(parser.get("config", "source_data_path") + "\\Targetsuperstoreaddress.csv")

    target_data2 = pd.read_csv(parser.get("config", "source_data_path") + "\\Target2superstorecontactdim.csv")

    target_data3 = pd.read_csv(parser.get("config", "source_data_path") + "\\Target3superstoredim.csv")

    # merging the target data 1 & target 2 by using common column Row_ID
    target_data4 = target_data1[["Row_ID", "Order_ID"]].merge(target_data2[["Row_ID", "Customer_Name", "Segment",
                                                                      "Country", "City"]],
                                                        on="Row_ID",
                                                        how="left")

    # # merging the target data 4 & target 3 to get the final dataset by using common column Row_ID
    target_data_final = target_data4[["Row_ID", "Order_ID", "Segment",
                      "Country", "City"]].merge(target_data3[["Row_ID", "Customer_Name"]],
                                                on="Row_ID",
                                                how="left")

    # Storing the columns that are required for our comparison from both source and target dataset
    columns = ['Row_ID','Order_ID','Customer_Name','Segment', 'Country', 'City']

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
    source_data.to_excel(parser.get("config", "output_data_path") + "\\SDTestCase3.xlsx")


testcase1()
testcase2()
testcase3()