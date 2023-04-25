import streamlit as st
from PIL import Image
import os
import shutil
import tempfile
import tarfile

from train import train_model



def save_uploaded_files(uploaded_files, save_path):
    for file in uploaded_files:
        with open(os.path.join(save_path, file.name), "wb") as f:
            f.write(file.getbuffer())


st.title("Autonomous Vehicle Steering Prediction")

# Upload dataset
uploaded_file = st.file_uploader("Upload dataset", type=['tar.gz'])

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded tar.gz file to the temporary directory
        tar_path = os.path.join(temp_dir, "uploaded_dataset.tar.gz")
        with open(tar_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract the tar.gz file to the temporary directory
        dataset_path = os.path.join(temp_dir, "dataset")
        os.makedirs(dataset_path)
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=dataset_path)

# Training parameters
st.sidebar.header("Training Parameters")
epochs = st.sidebar.slider("Number of epochs", 1, 200, 100)
batch_size = st.sidebar.slider("Batch size", 1, 100, 25)
learning_rate = st.sidebar.number_input("Learning rate", min_value=1e-6, max_value=1e-1, value=1e-3, step=1e-6, format="%.6f")

# Train button
if st.button("Train Model"):
    # Call the train_model function
    train_model(dataset_path, epochs, batch_size, learning_rate)

    # Display progress, metrics, and visualization
    # ...

# Download the trained model weights
# ...
