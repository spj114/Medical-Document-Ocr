from parser_generic import MedicalDocParser
import re

class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)

    def parse(self):
        return {
            'patient_name' : self.get_field('patient_name'),
            'patient_address' : self.get_field('patient_address'),
            'medicines' : self.get_field('medicines'),
            'directions' : self.get_field('directions'),
            'refill' : self.get_field('refill')
        }



    def get_field(self, field_name):

        att_dict = {
            'patient_name' : {'pattern' : 'Name:(.*)Date', 'flags' : 0},
            'patient_address' : {'pattern' : 'Address:(.*)\n', 'flags' : 0},
            'medicines' : {'pattern' : 'Address:[^\n]*(.*)Directions', 'flags' : re.DOTALL},
            'directions' : {'pattern' : 'Directions:(.*)Refill', 'flags' : re.DOTALL},
            'refill' : {'pattern' : 'Refill:(.*)times', 'flags' : 0}
        }

        att_object = att_dict.get(field_name)
        if att_object:
            matches = re.findall(att_object['pattern'], self.text, flags = att_object['flags'])
            if len(matches) > 0:
                result = matches[0].strip()

                if att_object['flags'] & re.DOTALL:
                    lines = result.split('\n')
                    cleaned_lines = [line.strip() for line in lines if line.strip()]
                    result = '\n'.join(cleaned_lines)

                return result