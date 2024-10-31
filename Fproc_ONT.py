#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import argparse
import shutil
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Process selected barcode folders.")
    
    parser.add_argument("start", type=int, help="Starting barcode number")
    parser.add_argument("end", type=int, help="Ending barcode number")
    parser.add_argument("--skip", nargs="*", type=int, default=[], help="Barcode numbers to skip between selected barcodes")
    parser.add_argument("--input-dir", required=True, help="Path to the input directory containing barcode folders")
    parser.add_argument("--output-dir", required=True, help="Path to the output directory")
    parser.add_argument("--output-folder", required=True, help="Name of the output folder")
    
    args = parser.parse_args()

    for barcode in range(args.start, args.end + 1):
        barcode_str = f'barcode{barcode:02}'  # Format the barcode number with leading zeros
        if barcode in args.skip:
            print(f"Skipping {barcode_str}")
            continue
        
        source_path = os.path.join(args.input_dir, barcode_str)
        
        if not os.path.exists(source_path):
            print(f"Folder '{barcode_str}' does not exist in the input directory. Skipping...")
            continue

        destination_path = os.path.join(args.output_dir, args.output_folder, f'{barcode_str}.fastq.gz')
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        command = f"zcat {source_path}/*fastq.gz | gzip -c > {destination_path}"
        subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    main()




# In[ ]:




