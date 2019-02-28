from bs4 import BeautifulSoup
import ics
import datetime
import arrow

user_response = input("Enter the date where the semester begin in this format (dd/mm/yyyy):\n")
sem_start = datetime.datetime(int(user_response.split("/")[2]), int(user_response.split("/")[1]), int(user_response.split("/")[0]))

# Converting text based day indicator to digit indicator.
def text2day(text):
    text = text.strip()

    if text == "Mon":
        return 0
    elif text == "Tue":
        return 1
    elif text == "Wed":
        return 2
    elif text == "Thu" or text == "Thur":
        return 3
    elif text == "Fri":
        return 4
    elif text == "Sat":
        return 5
    elif text == "Sun":
        return 6
    else:
        return -1

# Input is in the format: 5:15PM
def text2time(text):
    hour = int(text.split(":")[0])
    minute = int(text.split(":")[1][:2])

    if text[-2:] == "AM":
        return hour, minute
    elif text[-2:] == "PM" and hour == 12:
        return hour, minute
    else:
        return hour + 12, minute

# Input is in the format: 1,3-7,9,10-12
def text2week(text):
    weeks_txt = text.split(",")
    weeks = []

    for item in weeks_txt:
        if item.find("-") != -1:
            for index in range(int(item.split("-")[0]), int(item.split("-")[1]) + 1):
                weeks.append(index)
        else:
            weeks.append(int(item))

    return weeks

# Read downloaded myUNSW class timetable website from local folder.
file = open("myUNSW.html", "r")
file_content = file.read()
file.close()

# Convert to soup file.
soup = BeautifulSoup(file_content, 'html.parser')

# Step 1
# Find the HTML section where timetable schedule is located.
schedule_tables = []

# In a list of tables, for each table...
for table in soup.find_all("table", {"cellspacing":"0", "width":"100%"}):
    # Convert the soup to text so string matching is possible.
    table_in_text = table.prettify()

    # Check if the table contains both section heading and table heading.
    if table_in_text.find("sectionHeading") != -1 or table_in_text.find("tableHeading") != -1:
        schedule_tables.append(table)


# Step 2
# Organise them into a dictionary
# The dictionary should have the format
# {"Course": [{"Activity":"...", "Section":"...", "Day":0-6, "StartH":0-23, "EndH":0-23, "StartM":0-59, "EndM":0-59, "Week":[0,1,2...], "Location":"..."}]}
schedule = {}
currently_processing_course = None
currently_processing_activity = None
currently_processing_section = None

for table in schedule_tables:
    # Add a new course if found.
    if table.prettify().find("sectionHeading") != -1:
        currently_processing_course = table.find("td", {"class":"sectionHeading"}).text.split(" - ")[0]
        schedule.update({currently_processing_course:[]})

    # Add a new schedule of the course otherwise.
    else:
        dirty_rules = table.find_all("tr")
        rules = []

        # Some clean up to get rid of irrelevant tr sections.
        for rule in dirty_rules:
            if rule.prettify().find("data rowLowlight") != -1 or rule.prettify().find("data rowHighlight") != -1:
                rules.append(rule)

        # For each rules.
        for rule in rules:
            activity = None
            section = None
            day = None
            startH = None
            endH = None
            startM = None
            endM = None
            week = None
            location = None

            # Seperate each info from tr tag.
            tds = rule.find_all("td")

            # If there is a second time for same activity.
            if tds[0].prettify().find("colspan") != -1:
                day = text2day(tds[1].text)
                startH, startM = text2time(tds[2].text.split(" - ")[0])
                endH, endM = text2time(tds[2].text.split(" - ")[1])
                week = text2week(tds[3].text)
                location = tds[4].text
                activity = currently_processing_activity
                section = currently_processing_section
                schedule[currently_processing_course].append({"Activity":activity,
                                                                "Section":section,
                                                                "Day":day,
                                                                "StartH":startH,
                                                                "EndH":endH,
                                                                "StartM":startM,
                                                                "EndM":endM,
                                                                "Week":week,
                                                                "Location":location})
            else:
                currently_processing_activity = tds[0].text
                currently_processing_section = tds[1].text
                day = text2day(tds[2].text)
                startH, startM = text2time(tds[3].text.split(" - ")[0])
                endH, endM = text2time(tds[3].text.split(" - ")[1])
                week = text2week(tds[4].text)
                location = tds[5].text
                activity = currently_processing_activity
                section = currently_processing_section
                schedule[currently_processing_course].append({"Activity":activity,
                                                                "Section":section,
                                                                "Day":day,
                                                                "StartH":startH,
                                                                "EndH":endH,
                                                                "StartM":startM,
                                                                "EndM":endM,
                                                                "Week":week,
                                                                "Location":location})

# Step 3
# Convert Schedule to ICS!!!!
new_calendar = ics.Calendar()

# For each course.
for course in schedule:
    plan = schedule[course]
    # For each plan in the course.
    for item in plan:
        # For each week of each plan.
        for week in item["Week"]:
            new_event = ics.Event(name=course + " " + item["Activity"],
                                description="Class " + item["Section"] + " Week " + str(week),
                                location=item["Location"],
                                begin=arrow.get(sem_start + datetime.timedelta(days=(week-1)*7 + item["Day"], hours=item["StartH"], minutes=item["StartM"]), 'Australia/Sydney'),
                                end=arrow.get(sem_start + datetime.timedelta(days=(week-1)*7 + item["Day"], hours=item["EndH"], minutes=item["EndM"]), 'Australia/Sydney'))
            new_calendar.events.add(new_event)

# Step 4
# Export to ICS!!!!!!!!
with open('UNSW_Calendar.ics', 'w') as f:
    f.writelines(new_calendar)

print("\033[92mSuccessfully generated .ics file.\033[0m")
