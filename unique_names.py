def extract_unique_names(input_file_path, output_file_path):
    unique_names = set()

    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            name = line.strip()
            unique_names.add(name)

    with open(output_file_path, 'w') as output_file:
        for name in unique_names:
            output_file.write(name + '\n')

if __name__ == "__main__":
    input_file_path = "PATH_TO_INPUT_FILE.txt"    # Update with the actual input file path
    output_file_path = "PATH_TO_OUTPUT_FILE.txt"  # Update with the desired output file path
    extract_unique_names(input_file_path, output_file_path)

    print("Unique names extracted and saved to:", output_file_path)


