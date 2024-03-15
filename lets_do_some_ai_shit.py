import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

import cv2
from fastai.vision.all import *
from fastai.data.all import * 
import logging
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    fnames = get_image_files('cards')
    dblock = DataBlock()
    
    # Load the labels.txt file using pandas
    logging.info('Loading labels.txt file')
    df = pd.read_csv('labels.txt', sep='\t', header=None, names=['image_file', 'label', 'category'])
    
    # Check if image files exist and create a new DataFrame with valid files only
    logging.info('Checking image files and creating valid files DataFrame')
    valid_files = []
    for _, row in df.iterrows():
        image_path = Path(row['image_file'])
        if image_path.exists():
            valid_files.append(row)
        else:
            logging.warning(f"Missing file: {image_path}")
            
    
    df_valid = pd.DataFrame(valid_files, columns=['image_file', 'label', 'category'])
    logging.info(f'Number of valid files: {len(df_valid)}')
    
    # Filter out rows with missing labels
    logging.info('Filtering out rows with missing labels')
    df_valid = df_valid[df_valid['label'].isin(df_valid['image_file'].apply(lambda x: Path(x).stem))]
    logging.info(f'Number of rows after filtering missing labels: {len(df_valid)}')
    
    # Prepare the data
    def get_x(r): return Path(r['image_file'])
    def get_y(r): return f"{r['label']}_{r['category']}"

    logging.info('Creating data block')
    cards = DataBlock(
        blocks=(ImageBlock, MulitCategoryBlock),
        get_x=get_x,
        get_y=get_y,
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        item_tfms=Resize(224),
        batch_tfms=aug_transforms(size=224)
    )

    logging.info('Creating data loaders')
    dls = cards.dataloaders(df_valid)
    logging.info('Data preparation completed')

    # Fine-tune a pre-trained model
    logging.info('Fine-tuning the model')
    learn = vision_learner(dls, resnet34, metrics=accuracy)
    learn.fine_tune(5)
    logging.info('Model fine-tuning completed')

    # Use the trained model for inference
    logging.info('Starting camera capture for inference')
    cap = cv2.VideoCapture(0)  # Use the default camera (index 0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.warning('Failed to capture frame from camera')
            break
        
        # Preprocess the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (224, 224))
        frame_tensor = torch.tensor(frame).permute(2, 0, 1).float() / 255.0
        
        # Make a prediction
        pred, _, probs = learn.predict(frame_tensor.unsqueeze(0))
        logging.info(f'Predicted card: {pred}')
        
        # Display the prediction on the frame
        cv2.putText(frame, str(pred), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Playing Card Recognition', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.info('User terminated the program')
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
    logging.info('Camera capture and window display closed')

except FileNotFoundError as e:
    logging.error(f'File not found: {str(e)}')
except pd.errors.EmptyDataError as e:
    logging.error(f'Empty data error: {str(e)}')
except Exception as e:
    logging.error(f'An error occurred: {str(e)}')