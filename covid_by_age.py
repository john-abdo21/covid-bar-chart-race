import csv
import json

def convert_date_format(original):
    date, month, year = original.split('/')
    return year + '-' + month + '-' + date

def create_row_dict(row, cumulative_count):
    age = row[4]
    modified_date = convert_date_format(row[1])
    if age == "":
        age_range = "Unknown"
    else:
        if float(age) >= 1 and float(age) <= 10:
            age_range = "1-10"
        if float(age) >= 11 and float(age) <= 20:
            age_range = "11-20"
        if float(age) >= 21 and float(age) <= 30:
            age_range = "21-30"
        if float(age) >= 31 and float(age) <= 40:
            age_range = "31-40"
        if float(age) >= 41 and float(age) <= 50:
            age_range = "41-50"
        if float(age) >= 51 and float(age) <= 60:
            age_range = "51-60"
        if float(age) >= 61 and float(age) <= 70:
            age_range = "61-70"
        if float(age) > 70:
            age_range = "70+"
        # "1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "70+"

    if age_range not in cumulative_count:
        cumulative_count[age_range] = 0
    cumulative_count[age_range] += 1

    return {
        "date": modified_date,
        "name": age_range,
        "category": age_range,
        "value": cumulative_count[age_range]
        }

data = []
with open("confirmed-cases.csv", encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    cumulative_count = {}
    for row in csv_reader:
        if line == 0:
            pass
        else:
            row_dict = create_row_dict(row, cumulative_count)
            if row_dict["name"] == "" and row_dict["category"] == "":
                row_dict["name"] = "Unknown"
                row_dict["category"] = "Unknown"
            current_index = len(data) - 1
            while current_index >= 0 and data[current_index]["date"] == row_dict["date"]:
                if data[current_index]["name"] == row_dict["name"]:
                    data.pop(current_index)
                current_index -= 1
            data.append(row_dict)
            
        line += 1

with open('covid_by_age.json', 'w') as f:
    json.dump(data, f)