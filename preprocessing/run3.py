# This file is used to run the preprocessor locally
import preprocess3
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess Dota 2 match data.")
    parser.add_argument("input_folder", type=str, help="Path to the input folder containing parsed match data.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder for processed CSV files.")
    args = parser.parse_args()

    preprocess3.create_modified_csv(args.input_folder, args.output_folder)