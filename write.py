"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
from helpers import datetime_to_str
import csv
import json

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    # Save the results in a CSV file according to the specifications provided in the instructions.
    with open(filename, 'w', newline="") as outfile:
        w = csv.DictWriter(outfile, fieldnames = fieldnames)
        w.writeheader()

        for row in results:
            row_data = {**row.serialize(), **row.neo.serialize()}
            if row_data['diameter_km'] not in row_data:
                row_data['diameter_km'] = ''
            row_data['name'] = row_data['name'] or ''
            row_data['potentially_hazardous'] = 'True' if row_data['potentially_hazardous'] else 'False'
            w.writerow(row_data)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    data = []

    # Loop through each dict in the results
    for ca in results:
        entry = {
            'datetime_utc': ca.time.strftime('%Y-%m-%d %H:%M'),
            'distance_au': ca.distance,
            'velocity_km_s': ca.velocity,
            'neo': {
                'designation': ca.neo.designation,
                'name': ca.neo.name if ca.neo.name else '',
                'diameter_km': float('nan') if ca.neo.diameter is None else ca.neo.diameter,
                'potentially_hazardous': True if ca.neo.hazardous else False
            }
        }

        data.append(entry)

    # Open the output file in write mode ('w')
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)
