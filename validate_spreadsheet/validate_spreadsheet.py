import sys

import json
import pandas as pd
import re

# Set variable input to command-line user value
input = sys.argv[1]
sheet_name = sys.argv[2]
barcodes_ont_file = sys.argv[3]

# Read in the spreadsheet
sheet_df = pd.read_excel(f'{input}', sheet_name=sheet_name)
barcodes_ont_df = pd.read_csv(f'{barcodes_ont_file}', sep='\t', header=0)

# Read in the json file
with open('assets/mandatory_columns.json') as f:
    manda_cols = json.load(f)
    print('manda_cols are: ', manda_cols)


# Function to validate that mandatory columns from json are found in the spreadsheet
def manda_cols_inside_sheet(df):

    # Iterate over each mandatory column group
    print(df.columns)
    missing_cols = []
    matching_cols = {}
    for column_group in manda_cols['mandatory_columns']:
        column_group_key = list(column_group.keys())[0]
        # Escape parentheses in column names
        escaped_column_names = [re.escape(name) for name in list(column_group.values())[0]]
        equivalents_col = '|'.join(escaped_column_names)
        print('equivalents_col is: ', equivalents_col)
        matches_any = []
        for sheet_col in df.columns:
            match_col = re.fullmatch(equivalents_col, sheet_col, re.IGNORECASE)
            print(match_col)
            if match_col:
                matches_any.append(match_col.group())
                matching_cols[column_group_key] = match_col.group()
            else:
                continue
        if len(matches_any) == 0:
            missing_cols.append(column_group)
    if len(missing_cols) == 0:
        print(f'There are no missing columns: {missing_cols}')
        print(f'matching_cols: {matching_cols}')
        return matching_cols
    else:
        print(f'There are missing columns: {missing_cols}')
        return False


# Function to validate that no barcodes from barcodes_ont_df are missing from the sheet's barcode column
def no_missing_barcodes(sheet_df, barcodes_ont_df, mandatory_matches):
    print('mandatory_matches is: ', mandatory_matches)
    print('Barcodes in sheet_df are: ', sheet_df[mandatory_matches['barcode']])
    print('Barcodes in barcodes_ont_df are: ', barcodes_ont_df['barcode'])
    # FIXME: Get integer values of barcodes to match between the two dataframes.


# Report unnamed columns in sheet_df
def count_unnamed_cols(df):
    unnamed_cols = df.columns.str.contains('Unnamed')
    return unnamed_cols.sum()


def report_validity():
    print('REPORT: Validating spreadsheet')
    print('--------------------------------')
    print('REPORT: Number of unnamed columns: ', count_unnamed_cols(sheet_df))

    mandatory_matches = manda_cols_inside_sheet(sheet_df)

    if mandatory_matches:
        print('REPORT: Mandatory columns are complete')
    else:
        print('REPORT: Mandatory columns are incomplete')

    if no_missing_barcodes(sheet_df, barcodes_ont_df, mandatory_matches):
        print('REPORT: All barcodes are present')
    else:
        print('REPORT: Some barcodes are missing')


report_validity()
