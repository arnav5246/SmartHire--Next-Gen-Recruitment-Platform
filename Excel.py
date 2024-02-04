import csv

def convert_to_excel(data):

    # Writing data to CSV in append mode
    with open('arnav_jain_data.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        
        # If the file is empty, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write data to a new row
        writer.writerow(data)
