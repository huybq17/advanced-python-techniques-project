"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    
    # Load the NEO data from the specified CSV file.
    try:
        with open(neo_csv_path, 'r') as infile:
            reader = csv.reader(infile)

            # Next to second row
            next(reader) 

            for line in reader:
                # Extract necessary info
                name = line[4]
                diameter = line[15]
                designation = line[3]
                hazardous = line[7].lower() == 'y'

                 # Instantiate NEO
                neo = NearEarthObject(designation = designation, name = name, diameter = diameter, hazardous = hazardous)
                neos.append(neo)

    except FileNotFoundError:
        print("CSV file not found: {neo_csv_path}")
    except ValueError:
        print("Invalid CSV format or missing data")

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    apprs = []

    # Load the close approach data from the specified JSON file.
    try:
        with open(cad_json_path, 'r') as f:
            cad_data = json.load(f)

            # Some necessary attributes in "fields"
            field_indices = {field: cad_data['fields'].index(field) for field in ['des', 'cd', 'dist', 'v_rel']}

            l = 0
            while l < len(cad_data['data']):
                # Extract the data for the corresponding field attribute indexes. 
                # Then, initiate the `CloseApproach()` object.
                data = cad_data['data'][l]
                appr = CloseApproach(designation = data[field_indices['des']], time = data[field_indices['cd']], distance=data[field_indices['dist']], velocity=data[field_indices['v_rel']])
                apprs.append(appr)
                l += 1
    except FileNotFoundError:
        print("JSON file not found: {cad_json_path}")
    
    return apprs
