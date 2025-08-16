from backend.src.parser_prescription import PrescriptionParser
import pytest

@pytest.fixture
def doc_1_maria():
    
    document_text =  '''
       
        Dr John Smith, M.D
        2 Non-Important Street,
        New York, Phone (000)-111-2222

        Name: Marta Sharapova Date: 5/11/2022

        Address: 9 tennis court, new Russia, DC

        Prednisone 20 mg
        Lialda 2.4 gram

        Directions:

        Prednisone, Taper 5 mig every 3 days,
        Finish in 2.5 weeks a
        Lialda - take 2 pill everyday for 1 month

        Refill: 2 times
    
        '''

    return PrescriptionParser(document_text)


@pytest.fixture
def doc_2_virat():
    
    document_text = '''

        Dr John Smith, M.D

        2 Non-Important street,
        New York, Phone (900)-323- ~2222

        Name:  Virat Kohli Date: 2/05/2022

        Address: 2 cricket blvd, New Delhi

        | Omeprazole 40 mg

        Directions: Use two tablets daily for three months

        Refill: 3 times

        '''
    
    return PrescriptionParser(document_text)


@pytest.fixture
def doc_3_empty():
    doc_text = ''
    return PrescriptionParser(doc_text)

def test_get_name(doc_1_maria,doc_2_virat,doc_3_empty):
 
    assert doc_1_maria.get_field('patient_name') == 'Marta Sharapova'
    assert doc_2_virat.get_field('patient_name') == 'Virat Kohli'
    assert doc_3_empty.get_field('patient_name') == None

def test_get_address(doc_1_maria,doc_2_virat,doc_3_empty):

    assert doc_1_maria.get_field('patient_address') == "9 tennis court, new Russia, DC"
    assert doc_2_virat.get_field('patient_address') == "2 cricket blvd, New Delhi"
    assert doc_3_empty.get_field('patient_address') == None

def test_get_medicines(doc_1_maria,doc_2_virat,doc_3_empty):

    assert doc_1_maria.get_field('medicines') == 'Prednisone 20 mg\nLialda 2.4 gram'
    assert doc_2_virat.get_field('medicines') == "| Omeprazole 40 mg"
    assert doc_3_empty.get_field('medicines') == None

def test_get_directions(doc_1_maria,doc_2_virat,doc_3_empty):

    assert doc_1_maria.get_field('directions') == 'Prednisone, Taper 5 mig every 3 days,\nFinish in 2.5 weeks a\nLialda - take 2 pill everyday for 1 month'
    assert doc_2_virat.get_field('directions') == "Use two tablets daily for three months"
    assert doc_3_empty.get_field('directions') == None

def test_get_refill(doc_1_maria,doc_2_virat,doc_3_empty):

    assert doc_1_maria.get_field('refill') == "2"
    assert doc_2_virat.get_field('refill') == "3"
    assert doc_3_empty.get_field('refill') == None

def test_parse(doc_1_maria,doc_2_virat,doc_3_empty):

    assert doc_1_maria.parse() == {'patient_name': 'Marta Sharapova', 'patient_address': '9 tennis court, new Russia, DC', 'medicines': 'Prednisone 20 mg\nLialda 2.4 gram', 'directions': 'Prednisone, Taper 5 mig every 3 days,\nFinish in 2.5 weeks a\nLialda - take 2 pill everyday for 1 month', 'refill': '2'}
    
    record_virat = doc_2_virat.parse()

    assert record_virat['patient_name'] == 'Virat Kohli'
    assert record_virat['patient_address'] == "2 cricket blvd, New Delhi"
    assert record_virat['medicines'] == "| Omeprazole 40 mg"
    assert record_virat['directions'] == "Use two tablets daily for three months"
    assert record_virat['refill'] == "3"

    record_empty = doc_3_empty.parse()

    assert record_empty == {'patient_name': None,
                            'patient_address': None,
                            'medicines': None,
                            'directions': None,
                            'refill': None}