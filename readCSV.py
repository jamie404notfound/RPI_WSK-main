import csv
# Print all existing entries from CSV file in console window
with open("./sensor_readings.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        print(row)