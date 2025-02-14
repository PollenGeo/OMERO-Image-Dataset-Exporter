=========================================
 OMERO Image Dataset Exporter
=========================================

Description:
------------
This Python script connects to an OMERO server and allows users to select multiple 
groups and datasets to retrieve image information, including the dataset, project, 
and group IDs. The extracted data is then saved to a CSV file.

Features:
---------
- Connects to an OMERO server with user-provided credentials.
- Lists available OMERO groups and allows users to select multiple groups.
- Retrieves datasets within the selected groups.
- Extracts image information, including project, dataset, and group IDs.
- Saves results to a CSV file.

CSV Output Format:
------------------
If images are found, the script saves the results in a CSV file with the following columns:

| Column      | Description                                      |
|------------ |--------------------------------------------------|
| group_id    | ID of the OMERO group where the image is stored. |
| project_id  | ID of the project containing the dataset.         |
| dataset_id  | ID of the dataset where the image is located.     |
| image_id    | ID of the OMERO image.                           |
| image_name  | Name of the OMERO image.                         |

Requirements:
-------------
The script requires the following Python libraries:
- pandas
- omero-gateway
- tkinter (built-in for most Python distributions)

Installation:
-------------
Before running the script, install the required dependencies:
1. Install necessary Python packages:
pip install pandas pip install omero-py
2. If `tkinter` is not installed, install it manually (Linux users only):
sudo apt-get install python3-tk

Usage:
------
1. Run the script:
python Id_Labelimages.py
2. Enter OMERO server credentials when prompted.
3. Select one or multiple OMERO groups.
4. Choose datasets within each selected group.
5. The script retrieves all images in the selected datasets.
6. Save the results as a CSV file when prompted.

Author:
-------
This script was developed by **Daurys De Alba**.

For inquiries, contact:
- Email: daurysdealbaherra@gmail.com
- Email: DeAlbaD@si.edu

