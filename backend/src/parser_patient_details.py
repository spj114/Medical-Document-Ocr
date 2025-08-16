from parser_generic import  MedicalDocParser
import re 

class PatientDetailParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)

    def parse(self):
        return {
            'patient_name':self.get_patient_name(),
            'phone_number':self.get_patient_phone_number(),
            'medical_problems_history':self.get_medical_problems_history(),
            'hepatitis_b_vaccination':self.get_hepatitis_b_vaccination()
        }
    

    def get_patient_name(self):
        pattern = r"Patient Information(.*?)\(\d{3}\)"
        matches = re.findall(pattern, self.text, flags=re.DOTALL)
        name = ''
        if matches:
            name = self.remove_noise_from_name(matches[0])
        return name


    def remove_noise_from_name(self, name):
        name = name.replace('Birth Date','').strip()
        pattern = r'((Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)[ \d]+)'
        date_matches = re.findall(pattern, name)
        if date_matches:
            date = date_matches[0][0]
            name = name.replace(date,'').strip()
        
        return name

    def get_patient_phone_number(self):
        pattern = r"Patient Information(.*?)(\(\d{3}\) \d{3}-\d{4})"
        matches = re.findall(pattern, self.text, flags=re.DOTALL)
        if matches:
            return matches[0][-1]
        
    def get_hepatitis_b_vaccination(self):
        pattern = r"Have you had the Hepatitis B vaccination\?\s*(Yes|No)"
        matches = re.findall(pattern, self.text, flags=re.DOTALL)
        if matches:
            return matches[0].strip()

    def get_medical_problems_history(self):
        pattern =  r"List any Medical Problems.*?:\s*((?:N\s*/?\s*A)|[\w\s,]+)"
        matches = re.search(pattern, self.text, flags=re.DOTALL)
        if matches:
            return matches.group(1).strip()