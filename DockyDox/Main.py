from Database import Database

import DocumentReader
import DocumentRepo

connection_string = ''
database = Database(connection_string)
database.open_connection()

# Iterate while DocumentRepo has documents OR kill command is received:
document_data_by_type = {}
while DocumentRepo.has_next():
    # Load document into memory.
    document = DocumentRepo.get_next()
    data, document_type = DocumentReader.read_document(document)
    database.write_data(
        document_type,
        data.keys(),
        data.values())

database.close_connection()
