import pandas as pd
from omero.gateway import BlitzGateway
import tkinter as tk
from tkinter import filedialog, simpledialog


def connect_to_omero():
    """Connect to OMERO with user credentials."""
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    host = simpledialog.askstring("OMERO Login", "Enter OMERO Host:", initialvalue="xxx") #Put your initial host
    username = simpledialog.askstring("OMERO Login", "Enter OMERO Username:")
    password = simpledialog.askstring("OMERO Login", "Enter OMERO Password:", show="*")

    conn = BlitzGateway(username, password, host=host, port=4064, secure=True)
    if not conn.connect():
        raise ConnectionError("Failed to connect to OMERO. Check your credentials.")

    print("Successfully connected to OMERO.")

    # Retrieve available groups
    groups = conn.getGroupsMemberOf()
    group_dict = {g.getId(): g.getName() for g in groups}

    if not group_dict:
        raise ValueError("No groups available.")

    # Display list of groups for selection
    group_options = "\n".join([f"ID: {g_id} - {g_name}" for g_id, g_name in group_dict.items()])
    selected_group_ids = simpledialog.askstring(
        "Select Groups",
        f"Available Groups:\n{group_options}\n\nEnter Group IDs separated by commas:"
    )

    if not selected_group_ids:
        raise ValueError("No group ID entered.")

    selected_group_ids = [int(g.strip()) for g in selected_group_ids.split(",") if g.strip().isdigit()]

    for group_id in selected_group_ids:
        if group_id not in group_dict:
            raise ValueError(f"Invalid group ID: {group_id}")

    print(f"Selected Group IDs: {selected_group_ids}")
    return conn, selected_group_ids


def select_datasets(conn, group_id):
    """Allows the user to select multiple datasets from a given group."""
    conn.setGroupForSession(group_id)  # Switch to the group
    datasets = list(conn.getObjects("Dataset"))

    if not datasets:
        print(f"No datasets available in Group ID: {group_id}")
        return []

    dataset_dict = {dataset.getId(): dataset.getName() for dataset in datasets}

    # Display dataset list for selection
    dataset_options = "\n".join([f"ID: {d_id} - {name}" for d_id, name in dataset_dict.items()])
    selected_dataset_ids = simpledialog.askstring(
        "Select Datasets",
        f"Available Datasets in Group {group_id}:\n{dataset_options}\n\nEnter Dataset IDs separated by commas:"
    )

    if not selected_dataset_ids:
        return []

    selected_dataset_ids = [int(d.strip()) for d in selected_dataset_ids.split(",") if d.strip().isdigit()]

    selected_datasets = []
    for dataset_id in selected_dataset_ids:
        if dataset_id in dataset_dict:
            selected_datasets.append(conn.getObject("Dataset", dataset_id))
        else:
            print(f"Invalid dataset ID: {dataset_id}")

    return selected_datasets


def get_project_id(dataset):
    """Retrieve the project ID associated with the selected dataset."""
    project = dataset.getParent()  # Get the parent project
    return project.getId() if project else "N/A"


def get_images_from_datasets(datasets, group_id):
    """Retrieves the ID and name of all images within the selected datasets."""
    results = []
    for dataset in datasets:
        dataset_id = dataset.getId()
        project_id = get_project_id(dataset)

        for image in dataset.listChildren():
            results.append({
                "group_id": group_id,
                "project_id": project_id,
                "dataset_id": dataset_id,
                "image_id": image.getId(),
                "image_name": image.getName()
            })

    return results


def save_results_to_csv(results):
    """Saves the results to a CSV file in the user-selected location."""
    if not results:
        print("No images found in the selected datasets.")
        return

    df = pd.DataFrame(results)

    # Show file save dialog
    file_path = filedialog.asksaveasfilename(
        title="Save CSV File",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    df.to_csv(file_path, index=False)
    print(f"Results saved to: {file_path}")


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter window

    try:
        conn, group_ids = connect_to_omero()

        all_results = []
        for group_id in group_ids:
            # Select multiple datasets within the chosen group
            datasets = select_datasets(conn, group_id)
            if datasets:
                all_results.extend(get_images_from_datasets(datasets, group_id))

        # Save results to CSV
        save_results_to_csv(all_results)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()
