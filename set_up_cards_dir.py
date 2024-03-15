import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the current working directory
cwd = os.getcwd()
logging.info(f"Working in the '{cwd}' directory")

# Get the '/cards' directory path
cards_dir = os.path.join(cwd, 'cards')

# Get all the files in the '/cards' directory
try:
    file_names = os.listdir(cards_dir)
except Exception as e:
    logging.error(f"Error getting file names from '{cards_dir}': {str(e)}")
    raise
else:
    logging.info(f"Found {len(file_names)} files in the '{cards_dir}' directory")

# Create a dictionary to store the cards grouped by name and variant
cards = {}

# Iterate through the file names
for file_name in file_names:
    try:
        # Split the file name into name and variant
        parts = file_name.split("_")
        name = "_".join(parts[:-1])
        variant = parts[-1].split(".")[0]  # Remove the file extension

        # Add the file name to the dictionary
        if name not in cards:
            cards[name] = {}
        if variant not in cards[name]:
            cards[name][variant] = []
        cards[name][variant].append(file_name)
    except Exception as e:
        logging.error(f"Error processing file '{file_name}': {str(e)}")

# Create folders for each unique name and variant inside the '/cards' directory
for name, variants in cards.items():
    for variant, files in variants.items():
        variant_folder_name = f"{variant}"
        card_folder_name = f"{name}"
        variant_folder_path = os.path.join(cards_dir, variant_folder_name)
        card_folder_path = os.path.join(cards_dir, card_folder_name)
        try:
            if not os.path.exists(variant_folder_path):
                os.makedirs(variant_folder_path)
                logging.info(f"Created variant folder '{variant_folder_path}'")
            else:
                logging.info(f"Variant Folder '{variant_folder_path}' already exists")

            if not os.path.exists(card_folder_path):
                os.makedirs(card_folder_path)
                logging.info(f"Created card folder '{card_folder_path}'")
            else:
                logging.info(f"Card Folder '{card_folder_path}' already exists")

            # Copy the files to the respective folders
            for file_name in files:
                source_path = os.path.join(cards_dir, file_name)
                variant_destination_path = os.path.join(variant_folder_path, file_name)
                card_destination_path = os.path.join(card_folder_path, file_name)
                shutil.copy(source_path, variant_destination_path)
                logging.info(f"Copied '{file_name}' to '{variant_destination_path}'")
                shutil.copy(source_path, card_destination_path)
                logging.info(f"Copied '{file_name}' to '{card_destination_path}'")
        except Exception as e:
            logging.error(f"Error processing folders '{variant_folder_path}' and '{card_folder_path}': {str(e)}")

logging.info("Script completed successfully")