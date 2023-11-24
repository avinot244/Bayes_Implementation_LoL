import csv

with open("temp.csv", "w", newline='') as f:
    writer = csv.writer(f)
    header = ['name', 'greeting']
    data = ['AV', 'yo']
    writer.writerow(header)
    writer.writerow(data)