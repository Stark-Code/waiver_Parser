from pdfminer.high_level import extract_text  # Install via  pip install pdfminer.six
import re


def process_Text(text, _filter):
    if re.search(_filter, text) is None:
        return text
    text = re.sub(_filter, '', text)
    return process_Text(text, _filter)


def parse_Waiver(waiver):
    pre_Filters = [r"IP: \d{2}.*", r"Page .*"]
    waiver_Text = extract_text(waiver)

    for filter in pre_Filters:
        waiver_Text = process_Text(waiver_Text, filter)
    print(waiver_Text)
    # print(text)
    origin = re.search('(?<=Completed:) ?\d{4}-\d{2}-\d{2}', waiver_Text)
    first_Name = re.search('.*\n?(?=First Name*)', waiver_Text)
    middle_Name = re.search('.*\n?(?=Middle Name*)', waiver_Text)
    last_Name = re.search('.*\n?(?=Last Name*)', waiver_Text)
    phone = re.search('.*\n?(?=Phone*)', waiver_Text)
    address_1 = re.search('(?<=Address Line 1:\*\n)\n?(.*)', waiver_Text)
    address_2 = re.search('(?<=Address Line 2:\n)\n?(.*)', waiver_Text)
    country = re.search('(?<=Country:\*\n)\n?(.*)', waiver_Text)
    city = re.search('(?<=City:\*\n)\n?(.*)', waiver_Text)
    state = re.search('(?<=State/Province:\*\n)\n?(.*)', waiver_Text)
    zip_Code = re.search('(?<=Zip/Postal:\*\n)\n?(.*)', waiver_Text)
    email = re.search('(?<=Email Address\n)\n?(.*)', waiver_Text)
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


parse_Waiver(waiver_File)
