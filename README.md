# UNSW-Import-Timetable-to-Any-Calendar-App
Import your personal timetable from UNSW website to any timetable app of your choice that supports ICS File. Suported Calendar includes Microsoft Outlook, Google Calendar, Apple Calendar App and more.

# Requirements to use it.
1. You need python 3.x installed on computer.
2. Install <BeautifulSoup4> Python Library: "pip3 install beautifulsoup4"
3. Install <ics> Python Library: "pip3 install ics"
4. Install <arrow> Python Library: "pip3 install arrow"

# How to use it.
1. Go to https://my.unsw.edu.au/active/studentTimetable/timetable.xml
2. Login with your UNSW account.
3. Download the timetable website to your computer, it has to be in HTML format.
4. Rename the downloaded page as "myUNSW.html" #IMPORTANT!!!#IMPORTANT!!!#IMPORTANT!!!
5. Download this project or clone it onto your computer.
6. Inside the project folder, open the folder named "Timetable 2 Calendar"
7. Copy and paste the downloaded timetable website "myUNSW.html" into "Timetable 2 Calendar" folder.
8. Run the file with command "python3 convert.py" and enter the semester start date. Make sure convert.py and myUNSW.html is under the same folder.
9. You can then use the generated .ics file and import it into most calendar app. This includes Outlook, Google Calendar, Apple Calendar and more.
