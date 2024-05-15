import pandas as pd
import json
import re

xlsx_file = input("Enter path to the WGS database (.xlsx file): ")
output_file = input("Enter output filename for JSON data (default: wgs_data.json): ") or "wgs_data.json"


def clean_column_name(name):
    """Cleans a column name by removing parenthesis and their content, converting to lowercase, and replacing spaces with underscores"""
    return re.sub(r"\s*\(.*?\)", "", name).lower().replace(" ", "_")


def parse_date(date_str):
    """Attempts to parse a date string in various formats to YYYY-MM-DD format, or returns empty string if parsing fails"""
    if pd.isna(date_str):  # Check for missing values (using isna)
        return ""
    for format in ["%m-%d-%Y", "%d-%m-%Y", "%Y-%m-%d"]:
        try:
            return pd.to_datetime(date_str, format).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""  # If parsing fails, return empty string


def extract_WGS_data(xlsx_file, output_file):
    """Extracts data from the WGS database and writes it to JSON format"""
    data = pd.read_excel(xlsx_file)

    # Clean column names
    data.columns = [clean_column_name(col) for col in data.columns]

    # Handle missing values (consider filling with empty string or a specific value)
    data["barcode"] = data["barcode"].fillna("")  # Replace missing values with empty string (example)

    # Filter for strings representing barcodes
    string_barcodes = data[data["barcode"].notna()]  # Keep rows with non-missing barcode values after filling
    string_barcodes = string_barcodes[string_barcodes["barcode"].str.strip() != "-"]  # Exclude empty strings and "-"
    string_barcodes = string_barcodes[string_barcodes["barcode"].str.len() <= 5]  # Length less than or equal to 5
    string_barcodes = string_barcodes[string_barcodes["barcode"].str.isalnum()]  # Only alphanumeric characters

    # Filter for numeric barcodes (assuming integers)
    numeric_barcodes = data[data["barcode"].apply(lambda x: isinstance(x, int))]

    # Convert string barcodes to integers (if necessary)
    if len(string_barcodes) > 0:  # Check if there are string barcodes
        string_barcodes["barcode"] = string_barcodes["barcode"].astype(int)

    # Combine filtered dataframes (optional)
    data = pd.concat([string_barcodes, numeric_barcodes], ignore_index=True)

    # Select and format desired data
    desired_columns = ["barcode", "sequencing_id", "ritm_lab_id", "age", "sex", "sple_type", "dru", "dru_address"]
    # Use cleaned column names for date of collection (assuming it has parenthesis)
    if "date_of_collection" in data.columns:
        desired_columns.append(clean_column_name("date_of_collection"))

    desired_data = data[desired_columns]

    # Handle empty values
    desired_data = desired_data.fillna("")

    # Parse date (if the column exists)
    if clean_column_name("date_of_collection") in data.columns:
        desired_data[clean_column_name("date_of_collection")] = desired_data[
            clean_column_name("date_of_collection")].apply(parse_date)

    # Convert to JSON format
    json_data = desired_data.to_json(orient="records")

    # Write to file
    with open(output_file, "w") as f:
        f.write(json_data)

extract_WGS_data(xlsx_file, output_file)
print(f"WGS data extracted and saved to: {output_file}")