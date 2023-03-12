import cv2
import pytesseract
import datetime
import re

# Load image
idType = input("ID Type to Test (Passport/Drivers): ")
if idType == "Passport" or "passport":
    idType = "passport.jpg"
else:
    idType = "Drivers.jpg"
image = cv2.imread(idType)

# Extract text from image using OCR
text = pytesseract.image_to_string(image)
print(text)

# Define regular expressions to match date patterns for UK driver's license and passport
ukdl_date_pattern = r"\d{2}\.\d{2}\.\d{4}"  # pattern for dd.mm.yyyy format
passport_dob_pattern = r"\d{2}\s\w{3}\s\d{4}"  # pattern for dd mmm yyyy format
passport_exp_pattern = r"\d{2}\s\w{3}\s/\s\w{3}\s\d{2}(\d{2})?"  # pattern for dd mmm / mmm yy format

# Look for date of birth and expiration date in text using regular expressions
exp_date = None
dob = None
id_type = None
for line in text.split("\n"):
    # Check if this line contains a date pattern for UK driver's license
    match = re.search(ukdl_date_pattern, line)
    if match:
        date_str = match.group()
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        if not exp_date:
            exp_date = date
            id_type = "UK driver's license"
        elif not dob:
            dob = date

    # Check if this line contains a date of birth pattern for a passport
    match = re.search(passport_dob_pattern, line)
    if match:
        date_str = match.group()
        date = datetime.datetime.strptime(date_str, "%d %b %Y").date()
        if not dob:
            dob = date
            id_type = "passport"

    # Check if this line contains an expiration date pattern for a passport
    match = re.search(passport_exp_pattern, line)
    if match:
        date_str = match.group()
        date_str = date_str.replace(" / ", " ")
        if len(date_str) == 11:
            date = datetime.datetime.strptime(date_str, "%d %b %Y").date()
        else:
            date = datetime.datetime.strptime(date_str, "%d %b %y").date()
        if not exp_date:
            exp_date = date
            id_type = "passport"

# Get current date
today = datetime.date.today()

# Check if ID is expired
if exp_date is None:
    print("Expiration date information not found.")
else:
    if today > exp_date:
        print(f"This {id_type} has expired!")
    else:
        print(f"This {id_type} is not expired.")

# Check if person is of legal age
if dob is None:
    print("Date of birth information not found.")
else:
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age >= 18:
        print(f"This person is of legal age for a {id_type}.")
    else:
        print(f"This person is not of legal age for a {id_type}.")
