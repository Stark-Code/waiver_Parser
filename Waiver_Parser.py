from pdfminer.high_level import extract_text  # pdfminer.six
from tkinter import *
from tkinter import filedialog
import os


class Waiver_Parser:
    def __init__(self):
        self.member_Core = {}
        self.member_Common = {}
        self.waiver_Text = None
        self.core_Filters = {
            'first_Name': '(.*)\n?(?=First Name\\*)', 'middle_Name': '(.*)\n?(?=Middle Name)',
            'last_Name': '(.*)\n?(?=Last Name\\*)', 'dob': '[0-1]?[0-9] ? - ?(.* \\d{4})'
        }
        self.common_Filters = {
            'creation': '(?<=Completed:) ?\\d{4}-\\d{2}-\\d{2}', 'phone': '.*\n?(?=Phone\\*)',
            'address_1': '(?<=Address Line 1:\\*\n)\n?.*', 'address_2': '(?<=Address Line 2:\n)\n?.*',
            'country': '(?<=Country:\\*\n)\n?.*', 'city': '(?<=City:\\*\n)\n?.*',
            'state': '(?<=State/Province:\\*\n)\n?.*', 'zip': '(?<=Zip/Postal:\\*\n)\n?.*',
            'email': '(?<=Email Address\n)\n?.*', 'emergency_Contact': ".*\n?(?=Emergency Contact's Name\\*)",
            'emergency_Contact_Number': ".*\n*(?=.?Emergency Contact's Phone Number\\*)"
        }

    def clean_Text(self, waiver_Text, _filter):
        if re.search(_filter, waiver_Text) is None:
            return waiver_Text
        waiver_Text = re.sub(_filter, '', waiver_Text)
        return self.clean_Text(waiver_Text, _filter)

    def load_Waiver(self, waiver):  # OCR/ Pre-Filter
        self.waiver_Text = extract_text(waiver)
        for _filter in [r"IP: \d{2}.*", r"Page .*"]:
            self.waiver_Text = self.clean_Text(self.waiver_Text, _filter)

    def extract_Data(self):
        for filter_Key in self.core_Filters:
            self.member_Core[filter_Key] = list(filter(lambda x: x != '', re.findall(self.core_Filters[filter_Key],
                                                                                     self.waiver_Text)))
        for filter_Key in self.common_Filters:
            self.member_Common[filter_Key] = re.search(self.common_Filters[filter_Key], self.waiver_Text).group(
                0).strip()

    def create_Member(self):
        member_Data = {}
        for member_Idx in range(len(self.member_Core['dob'])):
            for key in self.member_Core:
                member_Data[key] = self.member_Core[key][member_Idx]
            member_Data = {**member_Data, **self.member_Common}
            self.print_Member_Info(member_Data)
            # Return or Export member_Data

    @staticmethod
    def print_Member_Info(member_Data):
        for key in member_Data:
            print(f'{key}: {member_Data[key]}')
        print('')


def static_Test():
    tests = ["/home/john/Downloads/Starkweather-John-20210922-33pw72b3LgYYABmDFJNY7Y.pdf",
         "/home/john/Downloads/archive/Bernens-Jim-adult-with-two-minors.pdf",
         '/home/john/Downloads/archive/Bernens-Kate-20210923-minor.pdf',
         '/home/john/Downloads/archive/Computer-Test-20210914-adult.pdf',
         '/home/john/Downloads/archive/Kiosk-Test-20210914-adult.pdf',
         '/home/john/Downloads/archive/Phone-Test-20210914-adult.pdf']

    waiver_Parser = Waiver_Parser()

    for test in tests:
        waiver_Parser.load_Waiver(test)
        waiver_Parser.extract_Data()
        waiver_Parser.create_Member()


def browseFiles():  # Single File
    waiver_Parser = Waiver_Parser()
    filename = filedialog.askopenfilename(initialdir="/home/john/Documents/",
                                          title="Select a File",
                                          filetypes=(("PDF Files", "*.pdf*"), ("Text Files", "*.txt*")))
    waiver_Parser.load_Waiver(filename)
    waiver_Parser.extract_Data()
    waiver_Parser.create_Member()


def bulk_Import(root_Dir):
    waiver_Parser = Waiver_Parser()
    waiver_Paths = list(os.listdir(root_Dir))
    print(waiver_Paths)
    for waiver_Path in waiver_Paths:
        filename = f'{root_Dir}/{waiver_Path}'
        waiver_Parser.load_Waiver(filename)
        waiver_Parser.extract_Data()
        waiver_Parser.create_Member()


bulk_Import('/home/john/Downloads/archive/')
