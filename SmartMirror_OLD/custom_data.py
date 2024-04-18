import os
import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import read_image

from SettingsManager import SettingsManager 

class EyeMovementDataset(Dataset):
    def __init__(self, transform=None): 
        self.img_labels = pd.read_csv(SettingsManager.get_path('annotations_file'))
        self.img_dir = SettingsManager.get_path('img_dir')
        self.transform = transform                      

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
