import csv


def open_csv(filename):
    csvfile = open(filename, newline='')
    return csv.DictReader(csvfile)
