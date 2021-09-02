
class Database:

    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def open_connection(self):
        pass
    
    def close_connection(self):
        pass

    def write_data(self,
        table,
        columns,
        data):
        additional_columns, additional_data = self.get_additional_column_data()
        columns = columns + additional_columns
        data = columns + additional_data
        # Form SQL query from columns + data + table.
        # Execute query.
        print('Implement Database.write_data()!!!')

    # Method to account for hardcoded data (such as data provider initials = 'GS')
    def get_additional_column_data(self):
        return [ 'FILL ME IN' ], [ 'SOME DATA?' ]
