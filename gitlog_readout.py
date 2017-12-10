"""Extract and plot the timeline of commits from the Donders Hackathon.
First save git log to file:
``git log --data=raw > git_log.txt``
"""

import re
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import pandas as pd

logfile = "git_log.txt"
with open(logfile) as f:
    lines = [line.strip() for line in f]

commit = []
author = []
date = []

for line in lines:
    if line.startswith("commit "):
        commit_string = re.search("[0-9a-f]{40}", line)
        if bool(commit_string):
            commit.append(commit_string.group())
    elif line.startswith("Author: "):
        try:
            auth_start = line.find(":") + 1
            auth_end = line.find("<") - 1
            author_string = line[auth_start:auth_end].strip()
            author.append(author_string)
        except:
            pass
    elif line.startswith("Date: "):
        try:
            date_start = line.find(":") + 1
            date_end = line.find("+") - 1
            date_string = line[date_start:date_end].strip()
            date.append(int(date_string))
        except:
            pass

commit_data = pd.DataFrame(
    {'commit': commit,
     'author': author,
     'date': date})

# exclude commits from after Hackathon
commit_data = commit_data[commit_data.date.values < 1511701200]

# reverse commits order because git log goes from newest to oldest
commit_data.reindex(index=commit_data.index[::-1])

# time frame for commits
starttime = min(commit_data.date)
endtime = max(commit_data.date)
timeline = range(starttime, endtime, 1)
commit_tracker = [0] * len(timeline)
commit_count = [0] * len(timeline)
count = 0
for t, time in enumerate(timeline):
    if time in commit_data.date.values:
        count += 1
        commit_tracker[t] = 1
        commit_count[t] = count

# unix datetime into human datetime
timeline = [dt.datetime.fromtimestamp(ts) for ts in timeline]

plt.figure()

# set time ticks on x-axis
ax=plt.gca()
xfmt = md.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(xfmt)
locator = md.HourLocator(byhour=range(0, 24, 2))
ax.xaxis.set_major_locator(locator)

plt.plot(timeline, commit_count)
plt.xlabel('time')
plt.ylabel('total number of commits')
plt.title('Progression of git commits\nduring Donders Hackathon')

# annotate plot with arrows and text
ax.annotate('dinner', xy=(md.date2num(dt.datetime(2017, 11, 25, 18, 0)), 10),
            xytext=(md.date2num(dt.datetime(2017, 11, 25, 17, 0)), 20),
            arrowprops=dict(arrowstyle="->"))
ax.annotate('halfway\nannouncement', xy=(md.date2num(dt.datetime(2017, 11, 26, 0, 3)), 20),
            xytext=(md.date2num(dt.datetime(2017, 11, 25, 21, 30)), 30),
            arrowprops=dict(arrowstyle="->"))
ax.annotate('coffee', xy=(md.date2num(dt.datetime(2017, 11, 26, 3, 30)), 30),
            xytext=(md.date2num(dt.datetime(2017, 11, 26, 2, 30)), 40),
            arrowprops=dict(arrowstyle="->"))
ax.annotate('breakfast', xy=(md.date2num(dt.datetime(2017, 11, 26, 8, 30)), 50),
            xytext=(md.date2num(dt.datetime(2017, 11, 26, 6, 30)), 60),
            arrowprops=dict(arrowstyle="->"))
ax.annotate('wrapup\nannouncement', xy=(md.date2num(dt.datetime(2017, 11, 26, 10, 30)), 65),
            xytext=(md.date2num(dt.datetime(2017, 11, 26, 6, 30)), 75),
            arrowprops=dict(arrowstyle="->"))
plt.show()
