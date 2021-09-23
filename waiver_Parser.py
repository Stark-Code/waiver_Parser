from pdfminer.high_level import extract_text  # Install via  pip install pdfminer.six
import re


def parse_Waiver(waiver):
    text = extract_text(waiver)
    # print(text)
    origin = re.search('(?<=Completed:) ?\d{4}-\d{2}-\d{2}', text)
    first_Name = re.search('.*\n?(?=First Name*)', text)
    middle_Name = re.search('.*\n?(?=Middle Name*)', text)
    last_Name = re.search('.*\n?(?=Last Name*)', text)
    phone = re.search('.*\n?(?=Phone*)', text)
    address_1 = re.search('(?<=Address Line 1:\*\n)\n?(.*)', text)
    address_2 = re.search('(?<=Address Line 2:\n)\n?(.*)', text)
    country = re.search('(?<=Country:\*\n)\n?(.*)', text)
    city = re.search('(?<=City:\*\n)\n?(.*)', text)
    state = re.search('(?<=State/Province:\*\n)\n?(.*)', text)
    zip_Code = re.search('(?<=Zip/Postal:\*\n)\n?(.*)', text)
    email = re.search('(?<=Email Address\n)\n?(.*)', text)
    print(f'Date of origin: {origin.group(0)}')
    print(f'First Name: {first_Name.group(0).strip()}')
    print(f'Middle Name: {middle_Name.group(0).strip()}')
    print(f'Last Name: {last_Name.group(0).strip()}')
    print(f'Phone: {phone.group(0).strip()}')
    print(f'Email: {email.group(1).strip()}')
    print(f'Address 1: {address_1.group(1).strip()}')
    print(f'Address 2: {address_2.group(1).strip()}')
    print(f'Country: {country.group(1).strip()}')
    print(f'City: {city.group(1).strip()}')
    print(f'State: {state.group(1).strip()}')
    print(f'Zip: {zip_Code.group(1).strip()}')

waiver_File = open("/home/john/Downloads/Starkweather-John-20210922-33pw72b3LgYYABmDFJNY7Y.pdf", "rb")
# waiver_File = open("Paste Path Here", "rb")

parse_Waiver(waiver_File)