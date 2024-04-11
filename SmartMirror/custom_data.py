import os
import pandas as pd #open-source Python library that provides high-performance, easy-to-use data structures, and data analysis tools.
from torch.utils.data import Dataset
from torchvision.io import read_image

class EyeMovementDataset(Dataset):
    
    

    def __init__(self, annotations_file, img_dir, transform=None):
        annotations_file = os.path.expanduser('~/Documents/python projects/SmartMirror/data/labels.csv')
        img_dir = os.path.expanduser('~/Documents/python projects/SmartMirror/data/images')
        
        self.img_labels = pd.read_csv(annotations_file) # Load the CSV as a DataFrame
        self.img_dir = img_dir                          # Store the image directory path
        self.transform = transform                      # Transformation to be applied to each image

    def __len__(self):
        return len(self.img_labels) # Return the number of items in the dataset

    def __getitem__(self, idx):
        # Construct the full path to the image file
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0]) 
        image = read_image(img_path)
        
        # Retrieve the label from the DataFrame
        label = self.img_labels.iloc[idx, 1]
         
        # Apply the specified transformations to the image
        if self.transform:
            image = self.transform(image)
       
        # Return the image and its label
        return image, label