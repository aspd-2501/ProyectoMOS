WEEKDAY_MAP = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6
}

def conv_num(x: str):
    hour, minute = tuple(x.split(":"))
    return int(hour)*60+int(minute)

def week_to_day(week: str):
    return WEEKDAY_MAP[week.lower()]

def calculate_distance(start1, end1, start2, end2):
    if end1 < start2 or end2 < start1:  # Non-overlapping case
        return abs(end1 - start2)
    else:  # Overlapping case
        return 9999


horarios = [
    (
        {
            "start": conv_num("9:30"),
            "end": conv_num("10:30"),
            "day": week_to_day("monday")
        },
        {
            "start": conv_num("9:30"),
            "end": conv_num("10:45"),
            "day": week_to_day("thursday")
        }
    ),
    (
        {
            "start": conv_num("11:00"),
            "end": conv_num("12:00"),
            "day": week_to_day("wednesday")
        },
        {
            "start": conv_num("14:00"),
            "end": conv_num("15:15"),
            "day": week_to_day("friday")
        }
    ),
    (
        {
            "start": conv_num("13:30"),
            "end": conv_num("14:30"),
            "day": week_to_day("tuesday")
        },
        {
            "start": conv_num("10:00"),
            "end": conv_num("11:15"),
            "day": week_to_day("saturday")
        }
    ),
    (
        {
            "start": conv_num("10:00"),
            "end": conv_num("11:30"),
            "day": week_to_day("thursday")
        },
        {
            "start": conv_num("16:30"),
            "end": conv_num("17:45"),
            "day": week_to_day("monday")
        }
    ),
]


horas = [
        {
            "start": conv_num("9:30"),
            "end": conv_num("10:30"),
            "day": week_to_day("Monday")
        },
        {
            "start": conv_num("9:30"),
            "end": conv_num("10:45"),
            "day": week_to_day("Thursday")
        },
        {
            "start": conv_num("11:00"),
            "end": conv_num("12:00"),
            "day": week_to_day("Thursday")
        },
        {
            "start": conv_num("14:00"),
            "end": conv_num("15:15"),
            "day": week_to_day("Friday")
        },
        {
            "start": conv_num("13:30"),
            "end": conv_num("14:30"),
            "day": week_to_day("Tuesday")
        },
        {
            "start": conv_num("10:00"),
            "end": conv_num("11:15"),
            "day": week_to_day("Friday")
        },
        {
            "start": conv_num("10:00"),
            "end": conv_num("11:30"),
            "day": week_to_day("Thursday")
        },
        {
            "start": conv_num("16:30"),
            "end": conv_num("17:45"),
            "day": week_to_day("Monday")
        },
        {
            "start": conv_num("12:00"),
            "end": conv_num("13:50"),
            "day": week_to_day("Friday")
        },
        {
            "start": conv_num("14:00"),
            "end": conv_num("16:50"),
            "day": week_to_day("Saturday")
        }
]

# Define dimensions for the matrices
matrix1 = [[0 for _ in range(len(horas))] for _ in range(len(horas))]

# Fill in the matrices with distances
for i in range(len(horas)):
    for j in range(len(horas)):
        start1, end1, day1 = horas[i]["start"], horas[i]["end"], horas[i]["day"]
        start2, end2, day2 = horas[j]["start"], horas[j]["end"], horas[j]["day"]
        if day1 != day2:  # If the ranges are on different days, set distance to 99999
            distance = 9998
        else:  # Calculate the distance based on time overlap
            if i == j:
                distance = 0 # NOTE: Forbid function call of f(i, i) unless no other hour is in the week. Otherwise, we are gifting 
                             # an easy way for the model to break everything. ( Acceptable to spread the hours in a week to abuse this,
                             # since that is what we are telling it to do )
            else:
                distance = calculate_distance(start1, end1, start2, end2)
        matrix1[i][j] = distance
        matrix1[j][i] = distance

# Print the matrices (for demonstration purposes)
print("Matrix 1:")
print(",".join(["@"] + [f"h{i+1}" for i in range(len(horas))]))
for i, row in enumerate(matrix1):
    print(",".join([f"h{i+1}"] + [str(element) for element in row]))
