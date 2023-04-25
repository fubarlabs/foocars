import streamlit as st
import logging
import glob

from PIL import Image
import os
import shutil
import tempfile
import tarfile
import tensorflow as tf

from train import prepare_and_train_model, train_model_with_config  
from tensorboard import program

# Configure the logging level for TensorBoard
logging.getLogger("tensorboard").setLevel(logging.ERROR)


def count_files_in_directory(directory, file_pattern='*'):
    files = glob.glob(os.path.join(directory, file_pattern))
    return len(files)


def find_data_directories(base_path):
    data_dirs = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.npz'):
                data_dirs.append(root)
                break
    return data_dirs

def save_uploaded_files(uploaded_files, save_path):
    for file in uploaded_files:
        with open(os.path.join(save_path, file.name), "wb") as f:
            f.write(file.getbuffer())

def create_tensorboard_callback(logdir):
    return tf.keras.callbacks.TensorBoard(log_dir=logdir, histogram_freq=1)

#data is not uploaded and extracted yet
data_ready=False

st.title("Autonomous Vehicle Steering Prediction")

# Text input field for car name
car_name = st.text_input("Enter the car name:")

st.header("Specify Data Directories")
data_directories_input = st.text_input("Enter the paths to your data directories (separate them with commas):")

if data_directories_input:
    data_directories = [directory.strip() for directory in data_directories_input.split(',')]
    non_existent_directories = [directory for directory in data_directories if not os.path.isdir(directory)]

    if non_existent_directories:
        st.error(f"Directory(ies) not found: {', '.join(non_existent_directories)}")
    else:
        st.success(f"Data directories set to: {', '.join(data_directories)}")
        data_ready=True

dataset_path = ""

def extract_with_progress(tar, path, total_members):
    progress_bar = st.progress(0)
    extracted_count = 0

    for member in tar.getmembers():
        tar.extract(member, path)
        extracted_count += 1
        progress = extracted_count / total_members
        progress_bar.progress(progress)



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
            total_members = len(tar.getmembers())
            extract_with_progress(tar, dataset_path, total_members)

        # Find data directories containing *.npz files
        data_directories = find_data_directories(dataset_path)


        # Count files in dataset_path
        num_files_dataset_path = count_files_in_directory(dataset_path)
        print(f"Number of files in dataset_path: {num_files_dataset_path}")

        # Count files in data_directories
        for directory in data_directories:
            num_files_directory = count_files_in_directory(directory)
            print(f"Number of files in {directory}: {num_files_directory}")

        # Display dataset_path and data_directories values in Streamlit app
        st.write(f"Dataset path: {dataset_path}")
        st.write(f"Data directories: {data_directories}")
        data_ready = True

# Training parameters
st.sidebar.header("Training Parameters")
epochs = st.sidebar.slider("Number of epochs", 1, 200, 100)
batch_size = st.sidebar.slider("Batch size", 1, 100, 25)
learning_rate = st.sidebar.number_input("Learning rate", min_value=1e-6, max_value=1e-1, value=1e-3, step=1e-6, format="%.6f")
use_tensorboard = st.sidebar.checkbox("Use TensorBoard", value=False)

logdir = 'logs'

def display_tensorboard():
    # Start TensorBoard
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', logdir])
    url = tb.launch()
    
    # Display TensorBoard in Streamlit
    st.write(f"TensorBoard is available at [this link]({url})")

# Only display

if os.path.exists(logdir):
    display_tensorboard()

# Only display TensorBoard if use_tensorboard is True
if use_tensorboard and os.path.exists(logdir):
    display_tensorboard()




# Train button
if data_ready and st.button("Train Model"):
    callbacks = []
    # Only add the TensorBoard callback if use_tensorboard is True
    if use_tensorboard:
        tensorboard_callback = create_tensorboard_callback(logdir)
        callbacks.append(tensorboard_callback)

    # Use the car_name variable in the training process or for saving the model
    # For example, you can use the car_name to create a subdirectory for the model
    model_save_path = os.path.join("models", car_name)
    os.makedirs(model_save_path, exist_ok=True)

    # Call the train_model function (or the new function name you've chosen)
    prepare_and_train_model(epochs, batch_size, learning_rate, dataset_path, data_directories, callbacks=callbacks)

    # Only display TensorBoard again if use_tensorboard is True and data is ready
    if use_tensorboard:
        display_tensorboard()

# Download the trained model weights
# ...
