import sys

import json
import pandas as pd
import re

# Set variable input to command-line user value
input = sys.argv[1]

# Read in the spreadsheet
sheet_df = pd.read_csv(f'{input}', header=0)
barcodes_df = pd.read_csv(f'{input}', header=0)


# Function to validate that mandatory columns from json are found in the spreadsheet
def manda_cols_inside_sheet(df):
    # Read in the json file
    with open('assets/mandatory_columns.json') as f:
        data = json.load(f)

    # Iterate over each mandatory column group
    print(df.columns)
    missing_cols = []
    for column_group in data['mandatory_columns']:
        # Escape parentheses in column names
        escaped_column_names = [re.escape(name) for name in list(column_group.values())[0]]
        equivalents_col = '|'.join(escaped_column_names)
        print(equivalents_col)
        matches_any = []
        for sheet_col in df.columns:
            match_col = re.fullmatch(equivalents_col, sheet_col, re.IGNORECASE)
            print(match_col)
            if match_col:
                matches_any.append(match_col.group())
            else:
                continue
        if len(matches_any) == 0:
            missing_cols.append(column_group)
    if len(missing_cols) == 0:
        print(f'Missing columns: {missing_cols}')
        return True
    else:
        print(f'Missing columns: {missing_cols}')
        return False


# FIXME: matching columns should be returned from manda_cols_inside_sheet func for use in no_missing_barcodes func.
# Function to validate that no barcodes from barcodes_df are missing from the sheet's barcode column
def no_missing_barcodes(df, barcodes_df):
    # Check if all barcodes in barcodes_df are in df
    if barcodes_df['barcode'].isin(df['BARCODE']).all():
        return True
    else:
        return False


# Print df
print(sheet_df.columns.isnull().sum())

if manda_cols_inside_sheet(sheet_df):
    print('Columns are complete')
else:
    print('Columns are incomplete')
