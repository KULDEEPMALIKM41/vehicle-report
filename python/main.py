import pandas as pd
import numpy as np
import os
import json
# import pandas_profiling

# Get Path of data source
def getFilePath():
    path = f"{os.getcwd()}/data/data.csv".replace("/python", "")
    return path

# Checking given string is convetable or not into a number
def checkIsNumber(num): # Uitility function
    try:
        float(num)
        return True
    except Exception as e:
        return False


# Total Count of coulmn items
def get_total_items(frame, column):
    return frame[column].count()

# Total Count of coulmn unique items
def get_total_unique_items(frame, column):
    return frame[column].nunique()

# Total Count of blank/None items
def get_total_missing_items(frame, column):
    return frame[column].isnull().sum()

# Most comman value from column
def get_most_common_item(frame, column):
    return frame[column].mode()[0]

# Count of most comman value from column
def get_count_most_common_item(frame, column, value):
    return (frame[column].values == value).sum()

# Mismatched value
def get_total_mismatched_item(frame, column):
    # columns which are expect string values
    if column in ['Make', 'Model', 'Vehicle Class', 'Transmission', 'Fuel Type']:
        data = list(frame[column].to_dict().values())
        # if not match with expect value
        mismatched = list(filter(lambda x: not isinstance(x, str) and x is not np.nan, data))
        return len(mismatched)

    # columns which are expect numaric, float or int values
    elif column in ['Engine Size(L)', 'Fuel Consumption City (L/100 km)', 'Fuel Consumption Hwy (L/100 km)', 'Fuel Consumption Comb (L/100 km)']:
        data = list(frame[column].to_dict().values())
        # if not match with expect value
        mismatched = list(filter(lambda x: not checkIsNumber(x), data))
        return len(mismatched)

    # columns which are expect complete numbers
    elif column in ['Cylinders', 'Fuel Consumption Comb (mpg)', 'CO2 Emissions(g/km)']:
        data = frame[column].to_dict().values()
        # if not match with expect value
        mismatched = list(filter(lambda x: int(x) != x if not np.isnan(x) and checkIsNumber(x) else False, data))
        return len(mismatched)

    return 0

# Getting column wise report
def column_wise_report(dataFile, analyze):
    # Get the list of all column names from headers
    column_headers = list(dataFile.columns.values)

    # Creating Report for per column
    for column in column_headers:
        total_items = get_total_items(dataFile, column)

        total_unique_items =  get_total_unique_items(dataFile, column)
        total_unique_items_per = f'{round((total_unique_items * 100)/total_items, 2)} %'

        total_missing_items =  get_total_missing_items(dataFile, column)
        total_missing_items_per = f'{round((total_missing_items * 100)/total_items, 2)} %'

        most_common_item = get_most_common_item(dataFile, column)
        count_most_common_item = get_count_most_common_item(dataFile, column, most_common_item)
        most_common_item_per = f'{round((count_most_common_item * 100)/total_items, 2)} %'

        total_mismatched_item = get_total_mismatched_item(dataFile, column)
        total_mismatched_item_per = f'{round((total_mismatched_item * 100)/total_items, 2)} %'

        valid_items = total_items - total_missing_items - total_mismatched_item
        valid_items_per = f'{round((valid_items * 100)/total_items, 2)} %'
        
        analyze[column] = {
            'total_items': total_items,
            'valid_items': valid_items,
            'valid_items_per(%)':valid_items_per,
            'total_unique_items': total_unique_items,
            'total_unique_items_per(%)':total_unique_items_per,
            'total_missing_items': total_missing_items,
            'total_missing_items_per(%)':total_missing_items_per,
            'most_frequent_item': most_common_item,
            'count_most_common_item': count_most_common_item,
            'most_frequent_item_per(%)':most_common_item_per,
            'total_mismatched_item': total_mismatched_item,
            'total_mismatched_item_per(%)':total_mismatched_item_per
        }

def overview_report(dataFile, analyze):

    # Getting Total Rows
    total_rows = dataFile[dataFile.columns[0]].count()

    # Getting Total Rows
    total_vehicle_attributes = len(dataFile.axes[1])

    # Getting duplicate Rows According to all columns
    df2 = dataFile[dataFile.duplicated()]
    total_duplicate_rows = df2[df2.columns[0]].count()  

    # Getting maximum mileage vehicles details with rows index
    df3 = dataFile[dataFile['Fuel Consumption Comb (L/100 km)'] == df['Fuel Consumption Comb (L/100 km)'].min()]
    max_mileage_vehicle_details = df3.to_dict()
    max_mileage = f"{list(max_mileage_vehicle_details['Fuel Consumption Comb (L/100 km)'].values())[0]} L/100km"

    # Getting minimam mileage vehicles details with rows index
    df4 = dataFile[dataFile['Fuel Consumption Comb (L/100 km)'] == df['Fuel Consumption Comb (L/100 km)'].max()]
    min_mileage_vehicle_details = df4.to_dict()
    min_mileage = f"{list(min_mileage_vehicle_details['Fuel Consumption Comb (L/100 km)'].values())[0]} L/100km"

    # Getting maximum CO2 emissions vehicles details with rows index
    df5 = dataFile[dataFile['CO2 Emissions(g/km)'] == df['CO2 Emissions(g/km)'].max()]
    max_co2_emissions_vehicle_details = df5.to_dict()
    max_co2_emissions = f"{list(max_co2_emissions_vehicle_details['CO2 Emissions(g/km)'].values())[0]} g/100km"

    # Getting minimum CO2 emissions vehicles details with rows index
    df5 = dataFile[dataFile['CO2 Emissions(g/km)'] == df['CO2 Emissions(g/km)'].min()]
    min_co2_emissions_vehicle_details = df5.to_dict()
    min_co2_emissions = f"{list(min_co2_emissions_vehicle_details['CO2 Emissions(g/km)'].values())[0]} g/100km"

    analyze['overview'] = {
        "total_rows":total_rows,
        "total_vehicle_attributes(columns)":total_vehicle_attributes,
        "total_duplicate_rows":total_duplicate_rows,
        "max_mileage":max_mileage,
        "max_mileage_vehicle_details":max_mileage_vehicle_details,
        "min_mileage":min_mileage,
        "min_mileage_vehicle_details":min_mileage_vehicle_details,
        "max_co2_emissions":max_co2_emissions,
        "max_co2_emissions_vehicle_details":max_co2_emissions_vehicle_details,
        "min_co2_emissions":min_co2_emissions,
        "min_co2_emissions_vehicle_details":min_co2_emissions_vehicle_details,
    }

# Save generated report
def save_report(data):
    # print(data)
    print(json.dumps(analyze, indent = 2,  default=str))
    with open("custom_report.json", "w") as outfile:
        json.dump(data, outfile, indent = 2, default=str)

# Descriptive statistics
def autoAnalysis(df):
    '''
        this function "autoAnalysis()" is just for genrating auto report in html & json format, 
        Here i am not show any logical skill, just showing awarness about pandas_profiling module.
        if usefull please uncomment lines no. 159, 160, 161 and 5.
        if uncommnet these line plese install "pandas-profiling" module.
    '''
#     profile = pandas_profiling.ProfileReport(df)
#     profile.to_file("report.html")
#     profile.to_file("report.json")

if __name__ == '__main__':
    
    analyze = {}

    # Get file path
    path = getFilePath()

    # reading the CSV file
    df = pd.read_csv(path)

    # All blank values will convert into None
    df.replace(r'^\s*$', np.nan, regex=True)

    # Call function for genrating report
    overview_report(df, analyze)
    column_wise_report(df, analyze)

    # Saving custom report
    save_report(analyze)

    # For Gereration auto report in html & json file
    autoAnalysis(df)