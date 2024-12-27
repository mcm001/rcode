"""
This is chatgpt slop. LOL
"""

import os
import re
from datetime import datetime
import pyexiv2

def extract_date_from_filename(filename):
    # Regular expression to match date in the format DDMMMYY
    date_pattern = r"(\d{2}\s?[A-Za-z]+\d{2})"
    match = re.search(date_pattern, filename)
    if match:
        raw_date = match.group(1).replace(" ", "")

        # normalize weird names
        raw_date = raw_date.replace("Sept","Sep")

        try:
            parsed_date = datetime.strptime(raw_date, "%d%b%y")
            return parsed_date.strftime("%Y:%m:%d %H:%M:%S")  # EXIF date format
        except ValueError:
            print(f"Error parsing date for file: {filename} got: {raw_date}")
    return None

def update_exif_date(filepath, exif_date):
    try:
        name = filepath.split(os.path.sep)[-1]
        with pyexiv2.Image(filepath) as img:
            data = img.read_exif()

            # The date and time when the image was stored as digital data.
            DIGITIZED = "Exif.Photo.DateTimeDigitized"
            # The date and time when the original image data was generated. For a digital still camera the date and time the picture was taken are recorded.
            TAKEN = "Exif.Photo.DateTimeOriginal"

            new_exif = {}
            if DIGITIZED not in data:
                print(f"Time digitized not in {name} - changing to {exif_date}")
                new_exif[DIGITIZED] = exif_date
            # else:
            #     print(f"Image {filepath} digitized at {data[DIGITIZED]}")

            if TAKEN not in data:
                print(f"Time taken not in {name} - changing to {exif_date}")
                new_exif[TAKEN] = exif_date

            if len(new_exif):
                print("WILL MODIFY")
                img.modify_exif(new_exif)
                return True
            
            return False
            # else:
            #     print(f"Image {filepath} taken at {data[TAKEN]}")

            # # Update EXIF DateTimeOriginal and DateTimeDigitized tags
            # exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = exif_date
            # exif_data["Exif"][piexif.ExifIFD.DateTimeDigitized] = exif_date
            # # Save the updated EXIF data back to the image
            # exif_bytes = piexif.dump(exif_data)
            # if False:
            #     img.save(filepath, "jpeg", exif=exif_bytes)
            #     print(f"Updated EXIF date for: {filepath}")
    except RuntimeError as e:
        print(f"ERROR READING {filepath}: {e}") 
        return None

def process_images(directory):
    unchanged = 0
    updated = 0
    errors = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".jpeg")):
            filepath = os.path.join(directory, filename)
            exif_date = extract_date_from_filename(filename)
            if exif_date:
                success = update_exif_date(filepath, exif_date)
                match success:
                    case None: errors += 1
                    case True: updated += 1
                    case False: unchanged += 1
            else:
                print(f"No valid date found in filename: {filename}")
        else:
            print(f"File not an image? {filename}")

    print(f"Updated {updated} left {unchanged} unchanged with {errors} errors")

# Set the directory containing the images
image_directory = "/home/matt/Documents/GitHub/rcode/python/smugmug_exif_updater/batch_3"

# Process the images
process_images(image_directory)
