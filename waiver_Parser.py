from pdfminer.high_level import extract_text  # Install via  pip install pdfminer.six
import re


def process_Text(text, _filter):
    if re.search(_filter, text) is None:
        return text
    text = re.sub(_filter, '', text)
    return process_Text(text, _filter)


def parse_Waiver(waiver):
    waiver_Text = extract_text(waiver)

    for _filter in [r"IP: \d{2}.*", r"Page .*"]:  # Pre-Filter
        waiver_Text = process_Text(waiver_Text, _filter)
    # print(waiver_Text)

    origin = re.search('(?<=Completed:) ?\\d{4}-\\d{2}-\\d{2}', waiver_Text)  #LB
    first_Name = list(filter(lambda x: x != '', re.findall('(.*)\n?(?=First Name\\*)', waiver_Text)))
    middle_Name = list(filter(lambda x: x != '', re.findall('(.*)\n?(?=Middle Name)', waiver_Text)))
    last_Name = list(filter(lambda x: x != '', re.findall('(.*)\n?(?=Last Name\\*)', waiver_Text)))
    dob = list(filter(lambda x: x != '', re.findall('[0-1]?[0-9] ? - ?(.* \\d{4})', waiver_Text)))
    phone = re.search('.*\n?(?=Phone\\*)', waiver_Text)  #LF

    address_1 = re.search('(?<=Address Line 1:\\*\n)\n?.*', waiver_Text)  #LB
    address_2 = re.search('(?<=Address Line 2:\n)\n?.*', waiver_Text)  #LB
    country = re.search('(?<=Country:\\*\n)\n?.*', waiver_Text)  #LB
    city = re.search('(?<=City:\\*\n)\n?.*', waiver_Text)  #LB
    state = re.search('(?<=State/Province:\\*\n)\n?.*', waiver_Text)  #LB
    zip_Code = re.search('(?<=Zip/Postal:\\*\n)\n?.*', waiver_Text)  #LB
    email = re.search('(?<=Email Address\n)\n?.*', waiver_Text)  #LB


    emergency_Contact_Name = re.search(".*\n?(?=Emergency Contact's Name\\*)", waiver_Text)  #LF
    emergency_Contact_Number = re.search(".*\n*(?=.?Emergency Contact's Phone Number\\*)", waiver_Text)  #LF

    print(f'Date of origin: {origin.group(0)}')
    print(f'First Name: {first_Name}')
    print(f'Middle Name: {middle_Name}')
    print(f'Last Name: {last_Name}')
    print(f'DOB: {dob}')
    print(f'Phone: {phone.group(0).strip()}')

    print(f'Email: {email.group(0).strip()}')
    print(f'Address 1: {address_1.group(0).strip()}')
    print(f'Address 2: {address_2.group(0).strip()}')
    print(f'Country: {country.group(0).strip()}')
    print(f'City: {city.group(0).strip()}')
    print(f'State: {state.group(0).strip()}')
    print(f'Zip: {zip_Code.group(0).strip()}')

    print(f'Emergency Contact Name: {emergency_Contact_Name.group(0).strip()}')
    print(f'Emergency Contact Number: {emergency_Contact_Number.group(0).strip()}')
    print('\n')


tests = ["/home/john/Downloads/Starkweather-John-20210922-33pw72b3LgYYABmDFJNY7Y.pdf",
         "/home/john/Downloads/archive/Bernens-Jim-adult-with-two-minors.pdf",
         '/home/john/Downloads/archive/Bernens-Kate-20210923-minor.pdf',
         '/home/john/Downloads/archive/Computer-Test-20210914-adult.pdf',
         '/home/john/Downloads/archive/Kiosk-Test-20210914-adult.pdf',
         '/home/john/Downloads/archive/Phone-Test-20210914-adult.pdf']

for test in tests:
    waiver_File = open(test, "rb")
    parse_Waiver(waiver_File)
