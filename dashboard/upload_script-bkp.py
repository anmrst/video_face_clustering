from flask import Flask, render_template, request , jsonify
from urllib.parse import urlparse, parse_qs
import os
import requests
from datetime import datetime
from PIL import Image
import asyncio
import json

app = Flask(__name__)

# Set the folder where uploaded images will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['base_dir'] = "/var/www/html/python/face_cluster/ClusteredFaces"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image = request.files['image']

    if image.filename == '':
        return "No selected image", 400

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Get the file extension
    file_extension = os.path.splitext(image.filename)[1]

    # Create a new filename with the timestamp
    new_filename = f"{timestamp}{file_extension}"

    # Save the uploaded image with the new filename
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'videos', new_filename))

    return "Video uploaded successfully"

@app.route('/get_videos', methods=['GET'])
def get_videos():
    directory_path = "/var/www/html/admin/uploads/videos"
    if os.path.exists(directory_path):
        file_list = os.listdir(directory_path)
        file_list = [file for file in file_list if os.path.isfile(os.path.join(directory_path, file))]
        response_data = {'files': file_list,'isexists':1}
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Directory not found','isexists':0})

@app.route('/get_files', methods=['GET'])
def get_images():
    video_name = request.args.get('videoName')
    directory_path = video_name
    if video_name is None:
        return jsonify({'error': 'Please provide a video_name parameter'}), 400

    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']  # Add more extensions as needed

        file_list = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file)) and os.path.splitext(file)[-1].lower() in image_extensions]

        response_data = {'files': file_list,'isexists':1}
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Folder does not exist','isexists':0})

@app.route('/get_first_image', methods=['GET'])
async def get_folder_info():
    video_name = request.args.get('videoName')
    root_directory = app.config['base_dir']
    # Specify the directory containing your folders
    #root_directory = '/path/to/your/root/directory'

    # Call the async function and get the list of folder information and total folder count
    folder_data_list, total_folders = await get_folder_info(root_directory)
    data_to_json = {
        "total_folders": total_folders,
        "folder_data_list": folder_data_list
    }
    # Convert the list to JSON data
    json_data = json.dumps(data_to_json, indent=4)

    return json_data

async def get_folder_info(root_directory):
    # Create an empty list to store folder information in JSON format
    folder_data_list = []

    # Count the total number of folders
    total_folders = 0

    # Asynchronously iterate over each folder in the root directory
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)

        # Check if it's a directory
        if os.path.isdir(folder_path):
            total_folders += 1

            # List all files in the folder
            files = os.listdir(folder_path)

            # Filter for image files (you can add more extensions if needed)
            image_files = sorted([file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])

            if image_files:
                # Get the first image file in the folder
                first_image = image_files[0]

                # Create a dictionary with folder and image information
                folder_info = {
                    "folder_name": folder_name,
                    "first_image": first_image,
                    "folder_path": folder_path
                }

                folder_data_list.append(folder_info)

    return folder_data_list, total_folders

if __name__ == '__main__':
    app.run(debug=True)
