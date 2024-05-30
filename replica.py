import os
import yaml
import argparse

changed_files = []
skipped_files = []

def update_replica_count(file_path, new_replica_count):
    global changed_files, skipped_files
    try:
        with open(file_path, 'r') as yaml_file:
            content = yaml_file.read()
            # Check for tab characters
            if '\t' in content:
                print(f"Skipping {file_path} because it contains tab characters")
                skipped_files.append(file_path)
                return

            data = yaml.safe_load(content)
            if data is not None and 'replicaCount' in data:
                current_replica_count = data['replicaCount']
                if new_replica_count == 0 and current_replica_count != 0:
                    print(f"Skipping {file_path} because it already has a non-zero replicaCount")
                    skipped_files.append(file_path)
                elif new_replica_count != 0 or current_replica_count != 0:
                    print(f"Updating replicaCount in {file_path} from {current_replica_count} to {new_replica_count}")
                    data['replicaCount'] = new_replica_count
                    with open(file_path, 'w') as yaml_file_write:
                        yaml.dump(data, yaml_file_write, default_flow_style=False)
                    changed_files.append(file_path)
                else:
                    skipped_files.append(file_path)
            else:
                print(f"No replicaCount found in {file_path}, skipping...")
                skipped_files.append(file_path)
    except yaml.YAMLError as exc:
        print(f"Error reading {file_path}: {exc}")
        skipped_files.append(file_path)
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}")
        skipped_files.append(file_path)

def find_and_update_files(root_directory, new_replica_count):
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            if file == 'values.yaml':
                file_path = os.path.join(subdir, file)
                update_replica_count(file_path, new_replica_count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update replicaCount in values.yaml files.')
    parser.add_argument('root_directory', type=str, help='Root directory to search for values.yaml files')
    parser.add_argument('replica_count', type=int, help='New replica count value')
    args = parser.parse_args()

    find_and_update_files(args.root_directory, args.replica_count)

    # Print summary
    print("\nSummary:")
    print("Changed files:")
    for file in changed_files:
        print(f"  - {file}")
    print("Skipped files:")
    for file in skipped_files:
        print(f"  - {file}")
