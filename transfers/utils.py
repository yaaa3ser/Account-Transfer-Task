import csv
import json
import xml.etree.ElementTree as ET
from io import StringIO

def import_accounts_from_file(file):
    file_type = file.name.split('.')[-1].lower()
    data = file.read().decode('utf-8')
    file_io = StringIO(data)

    if file_type == 'csv':
        reader = csv.reader(file_io)
        next(reader)  # Skip header row
        return list(reader)
    elif file_type == 'json':
        return json.load(file_io)
    
    # we can add more file types
    
    else:
        raise ValueError("Unsupported file type.")
