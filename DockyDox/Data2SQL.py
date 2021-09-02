import json


def create_subdivision(document):
    legal_lines = document['legal_table_1'].split('\n')
    numbers = []
    block = ''
    legals = []
    for line in legal_lines:
        try:
            remove_length = 0
            legal_components = line.split(' ')
            lot = int(legal_components[0])
            numbers.append(lot)
            remove_length = remove_length + len(str(lot)) + 1

            try:
                block = int(legal_components[1])
                remove_length = remove_length + len(str(block)) + 1
            except:
                pass

            line = line[remove_length:]
        except:
            pass
        if line not in legals:
            legals.append(line)
    numbers_text = ''
    while len(numbers) > 0:
        min_number = min(numbers)
        numbers.remove(min_number)
        if numbers_text == '':
            numbers_text = str(min_number)
        else:
            numbers_text = numbers_text + ', ' + str(min_number)
    legals_text = ''
    for legal in legals:
        if legals_text == '':
            legals_text = legal
        else:
            legals_text = legals_text + ', ' + str(legal)
    return '(\'' + \
        legals_text.replace('\'', '\'\'') + '\', \'' + \
        str(block).replace('\'', '\'\'') + '\', \'' + \
        document['document_type'].replace('\'', '\'\'') + '\', \'' + \
        document['document_id'].replace('\'', '\'\'') + '\', \'' + \
        document['grantor_table'].replace('\'', '\'\'').replace('\n', '\\n') + '\', \'' + \
        document['grantee_table'].replace('\'', '\'\'').replace('\n', '\\n') + '\', \'' + \
        document['recording_date'].split(' ')[0].replace('\'', '\'\'') + '\', \'' + \
        numbers_text.replace('\'', '\'\'') + '\' )'

def generate_yearly_subdivision_scripts(years):
    for year in years:
        data_file = open('./o_' + str(year) + '.txt', 'r')
        contents = '[' + data_file.read()[1:] + ']'
        data = json.loads(contents)

        subdivision_tuples = []
        county_tuples = []

        subdivision_header = 'INSERT INTO HuerfanoSubdivision(\'Subdivision\', \'Block\', \'Inst\', \'Reception\', \'Grantor\', \'Grantee\', \'Recording Date\', \'Lots\') VALUES'

        for document in data:
            if len(document['legal_table_1'].strip()) > 0:
                next_tuple = create_subdivision(document)
                subdivision_tuples.append(next_tuple)
            elif len(document['legal_table_2'].strip()) > 0:
                next_tuple = create_county(document)
                county_tuples.append(next_tuple)
            else:
                pass

        subdivision_script = subdivision_header
        for subdivision_tuple in subdivision_tuples:
            subdivision_script = subdivision_script + '\n' + subdivision_tuple + ','
        subdivision_script = subdivision_script[:-1] + ';'
        script_file = open('./subdivisions_' + str(year) + '.sql', 'x')
        script_file.write(subdivision_script)

def create_county(document):
    legal_lines = document['legal_table_2'].split('\n')
    numbers = []
    block = ''
    legals = []
    s1, s2, s3, d1, d2 = '', '', '', '', ''
    []
    for line in legal_lines:
        try:
            segments = line.split(' ')
            s1 = segments[0]
            s2 = segments[1][:-1]
            s3 = segments[2][:-1]
            d1 = segments[1][-1]
            d2 = segments[2][-1]
            i = 0
        except:
            pass
    numbers_text = ''
    while len(numbers) > 0:
        min_number = min(numbers)
        numbers.remove(min_number)
        if numbers_text == '':
            numbers_text = str(min_number)
        else:
            numbers_text = numbers_text + ', ' + str(min_number)
    legals_text = ''
    for legal in legals:
        if legals_text == '':
            legals_text = legal
        else:
            legals_text = legals_text + ', ' + str(legal)
    return '(\'' + \
        legals_text.replace('\'', '\'\'') + '\', \'' + \
        str(block).replace('\'', '\'\'') + '\', \'' + \
        document['document_type'].replace('\'', '\'\'') + '\', \'' + \
        document['document_id'].replace('\'', '\'\'') + '\', \'' + \
        document['grantor_table'].replace('\'', '\'\'').replace('\n', '\\n') + '\', \'' + \
        document['grantee_table'].replace('\'', '\'\'').replace('\n', '\\n') + '\', \'' + \
        document['recording_date'].split(' ')[0].replace('\'', '\'\'') + '\', \'' + \
        numbers_text.replace('\'', '\'\'') + '\' )'

def generate_yearly_county_scripts(years):
    for year in years:
        data_file = open('./o_' + str(year) + '.txt', 'r')
        contents = '[' + data_file.read()[1:] + ']'
        data = json.loads(contents)

        county_tuples = []

        county_header = "INSERT INTO HuerfanoCounty() VALUES"

        for document in data:
            if len(document['legal_table_1'].strip()) > 0:
                # next_tuple = create_subdivision(document)
                # subdivision_tuples.append(next_tuple)
                pass
            elif len(document['legal_table_2'].strip()) > 0:
                next_tuple = create_county(document)
                county_tuples.append(next_tuple)
            else:
                pass

        county_script = county_header
        for county_tuple in county_tuples:
            county_script = county_script + '\n' + county_tuple + ','
        county_script = county_script[:-1] + ';'
        script_file = open('./county_' + str(year) + '.sql', 'x')
        script_file.write(county_script)

generate_yearly_county_scripts([
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021
])