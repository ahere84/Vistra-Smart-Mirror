import torch
from torch.optim import Adam
import torch.nn as nn
from model import SimpleCNN
from torch.utils.data import DataLoader
from torchvision.transforms import Compose, Resize, Normalize, ToTensor
from custom_data import EyeMovementDataset

def train_model(num_epochs=10):
    # Initialize dataset and dataloader inside the function
    transform = Compose([
        Resize((224, 224)),
        ToTensor(),
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    dataset = EyeMovementDataset(annotations_file='~/Documents/python projects/SmartMirror/data/labels.csv', 
                                 img_dir='~/Documents/python projects/SmartMirror/data/images', 
                                 transform=transform)
    
    train_loader = DataLoader(dataset, batch_size=64, shuffle=True)

    # Initialize model, loss, and optimizer inside the function
    model = SimpleCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=0.001)

    # Training loop
    for epoch in range(num_epochs):
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    torch.save(model.state_dict(), 'model_weights.pth') # saves weight in a path like file writer

# main function
if __name__ == '__main__':
    train_model()  # This calls the train_model function when the script is run
