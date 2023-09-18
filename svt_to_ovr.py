import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET

def center_and_convert_svg(svg_path, output_path, name):
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Extract width and height from the SVG
        svg_width = root.get("width")
        svg_height = root.get("height")

        # Calculate the centering offsets
        width_offset = float(svg_width.strip("px")) / 2
        height_offset = float(svg_height.strip("px")) / 2

        # Extract the path data
        path_data = ""
        for path in root.iter("{http://www.w3.org/2000/svg}path"):
            path_data += path.get("d")

        # Create the .ovr file content with the centered path data
        ovr_content = f"name={name}\nwidth={svg_width}\nheight={svg_height}\npath=M{-width_offset},{-height_offset} {path_data}"

        # Save the .ovr file with the specified output filename
        with open(output_path, "w") as ovr_file:
            ovr_file.write(ovr_content)

        return output_path

    except Exception as e:
        return str(e)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if file_path:
        name = name_entry.get()
        
        # Set the output filename to be the same as the entered name with the .ovr extension
        output_filename = f"{name}.ovr"
        result_label.config(text="Processing...")
        output_path = center_and_convert_svg(file_path, output_filename, name)
        
        if output_path:
            result_label.config(text=f"Output file: {output_path}")
        else:
            result_label.config(text="Error processing the file.")

# Create a GUI window
window = tk.Tk()
window.title("SVG to OVR converter tool")

# Create and arrange GUI elements
file_button = tk.Button(window, text="Browse SVG", command=browse_file)
file_button.pack(pady=10)

name_label = tk.Label(window, text="Name:")
name_label.pack()

name_entry = tk.Entry(window)
name_entry.pack()

result_label = tk.Label(window, text="")
result_label.pack(pady=10)

window.mainloop()
