import csv
import sys
import math

def split_dataset(input_file, x):
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    total_points = len(data)
    points_per_file = total_points // x
    remainder = total_points % x
    start = 0
    # Split data into x subsets and write to separate files
    for i in range(1, x + 1):
        if i <= remainder:
            end = start + points_per_file + 1
        else:
            end = start + points_per_file
        subset_data = data[start:end]
        # Write each subset to a separate CSV file
        output_file = f'subset{i}.csv'
        with open(output_file, 'w', newline='') as subset_file:
            writer = csv.writer(subset_file)
            writer.writerows(subset_data)
        print(f'{output_file} written with {len(subset_data)} points')
        start = end

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python split_dataset.py <dataset.csv> <x>")
        sys.exit(1)
    input_file = sys.argv[1]
    x = int(sys.argv[2])
    split_dataset(input_file, x)