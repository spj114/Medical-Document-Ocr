from backend.src.parser_patient_details import PatientDetailParser
import pytest

@pytest.fixture
def doc_1_kathy():
    document_text = '''
    17/12/2020
    
    Patient Medical Record . : :
    
    Patient Information
    
    Birth Date
    Kathy Crawford May 6 1972
    (737) 988-0851 Weight:
    9264 Ash Dr 95
    New York City, 10005 a
    United States Height:
    190
    In Case of Emergency
    en oe
    Simeone Crawford 9266 Ash Dr
    New York City, New York, 10005
    Home phone United States
    (990) 375-4621
    Work phone
    Genera! Medical History
    I a
    Chicken Pox (Varicella): Measies:
    IMMUNE IMMUNE
    
    Have you had the Hepatitis B vaccination?
    
    No
    
    List any Medical Problems (asthma, seizures, headaches):
    
    Migraine
    | : ‘Name of Insurance Company:
    Random Insuarance Company - 4789 Bollinger Rd
    Jersey City, New Jersey, 07030
    
     - policy Number:
    oo 30 December 2020
    Do you have medical insurance?
    
    Yes -
    
    Medical Insurance Details
    
    List any allergies:
    
    Peanuts
    
    List any medication taken regularly:
    
    Triptans
    '''

    return PatientDetailParser(document_text)

@pytest.fixture
def doc_2_jerry():
    document_text = '''
        Patient Medical Record
    
    Patient Information
    Jerry Lucas
    
    (279) 920-8204
    
    4218 Wheeler Ridge Dr
    Buffalo, New York, 14201
    United States
    
    In Case of Emergency
    
    -_ OC -- OO eee
    
    Joe Lucas
    
    Home phone
    
    General Medical History
    
    Chicken Pox (Varicelia):
    IMMUNE
    Have you had the Hepatitis B vaccination?
    Yes
    
    Birth Date
    May 2 1998
    
    Weight:
    57
    
    Height:
    170
    
    4218 Wheeler Ridge Dr
    Buffalo, New York, 14201
    United States
    
    Work phone
    
    Measles: .
    
    NOT IMMUNE
    
    List any Medical Problems (asthma, seizures, headaches):
    
    N/A
    
    17/12/2020
    
    —_—
    
    Name of Insurance Company:
    Random Insuarance Company
    
    Policy Number:
    5638746258
    
    Do you have medical insurance?
    
    Yes
    
    Medical Insurance Details
    
    List any allergies:
    N/A
    
    List any medication taken regularly:
    
    N/A
    
    4218 Smeeler Ridge Dr
    Buffalo, New York, 14206
    United States
    
    Expiry Date:
    31 December 2020
    '''

    return PatientDetailParser(document_text)

def test_get_patient_name(doc_1_kathy, doc_2_jerry):
    assert doc_1_kathy.get_patient_name() == 'Kathy Crawford'
    assert doc_2_jerry.get_patient_name() == 'Jerry Lucas'

def test_get_patient_phone_number(doc_1_kathy, doc_2_jerry):
    assert doc_1_kathy.get_patient_phone_number() == '(737) 988-0851'
    assert doc_2_jerry.get_patient_phone_number() == '(279) 920-8204'


def test_get_hepatitis_b_vaccination(doc_1_kathy, doc_2_jerry):
    assert doc_1_kathy.get_hepatitis_b_vaccination() == 'No'
    assert doc_2_jerry.get_hepatitis_b_vaccination() == 'Yes'


def test_get_medical_problems(doc_1_kathy, doc_2_jerry):
    assert doc_1_kathy.get_medical_problems_history() == 'Migraine'
    assert doc_2_jerry.get_medical_problems_history() == 'N/A'

def test_parse(doc_1_kathy, doc_2_jerry):
    record_kathy = doc_1_kathy.parse()
    assert record_kathy['patient_name'] == 'Kathy Crawford'
    assert record_kathy['phone_number'] == '(737) 988-0851'
    assert record_kathy['medical_problems_history'] == 'Migraine'
    assert record_kathy['hepatitis_b_vaccination'] == 'No'