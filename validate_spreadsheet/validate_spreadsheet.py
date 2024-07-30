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


# Function to validate mandatory columns from json are in sheet
def manda_cols_inside_sheet(df):

    # Iterate over each mandatory column group
    missing_cols = []
    matching_cols = {}
    for column_group in manda_cols['mandatory_columns']:
        column_group_key = list(column_group.keys())[0]

        # Escape parentheses in column names
        escaped_column_names = [re.escape(name) for name in list(column_group.values())[0]]
        equivalents_col = '|'.join(escaped_column_names)
        matches_any = []
        for sheet_col in df.columns:
            match_col = re.fullmatch(equivalents_col, sheet_col, re.IGNORECASE)
            if match_col:
                matches_any.append(match_col.group())
                matching_cols[column_group_key] = match_col.group()
            else:
                continue
        if len(matches_any) == 0:
            missing_cols.append(column_group)
    if len(missing_cols) == 0:
        return True, matching_cols, missing_cols
    else:
        return False, matching_cols, missing_cols


# Function to validate all barcodes from ont are in sheet
def no_missing_barcodes(sheet_df, barcodes_ont_df, mandatory_matches):

    # Get barcode column, drop NaNs, convert to str type, then regex search
    sheet_barcodes = sheet_df[mandatory_matches['barcode']].dropna(axis=0).astype(str).apply(lambda x: re.search(r'\d+', x).group())
    ont_barcodes = barcodes_ont_df['barcode'].dropna(axis=0).astype(str).apply(lambda x: re.search(r'\d+', x).group())

    # Covnert to int type for comparison
    sheet_barcodes = sheet_barcodes.astype(int)
    ont_barcodes = ont_barcodes.astype(int)

    missing_barcodes = set(ont_barcodes) - set(sheet_barcodes)
    if len(missing_barcodes) == 0:
        return True, missing_barcodes
    else:
        return False, missing_barcodes


# Report unnamed columns in sheet_df
def count_unnamed_cols(df):
    unnamed_cols = df.columns.str.contains('Unnamed')
    return unnamed_cols.sum()


def report_validity():
    print('REPORT: Validating spreadsheet')
    print('--------------------------------')
    print('Number of unnamed columns: ', count_unnamed_cols(sheet_df))

    all_manda_matched, mandatory_matches, missing_cols = manda_cols_inside_sheet(sheet_df)
    no_barcode_missed, missing_barcodes = no_missing_barcodes(sheet_df, barcodes_ont_df, mandatory_matches)

    if all_manda_matched:
        print('Mandatory columns are complete:')
        print(mandatory_matches)
    else:
        print('Mandatory columns are incomplete:')
        print(missing_cols)

    if no_barcode_missed:
        print('All barcodes are present')
    else:
        print('Some barcodes are missing')
        print(missing_barcodes)


report_validity()
