# UK Premium Bond Checker

## Introduction

NS&I update their online prize checker the day after the first working day of each month - although, it's not clear by exactly what time of day (but must be early in the morning).

NS&I send out an email if you have won a few days afterwards (4th day after the first working day?) but they don't tell you how much you have won.  You don't get an email if you have not won anything.

API is not published but is pretty simple and appears established.

## Program strategy

Only want to notify a monthly win once. So, the current months JSON isn't saved until you are notified (or not if you didn't win).
Want to check and notify as quickly as possible (i.e. in the early hours after the first working day).
Don't want to have to work out what the day after the first working day of each month is (day after a weekend or bank/public holiday). Or query an API to find out. Or have a list.
No wins are a problem as the JSON doesn't contain the month of the no win.

Saving the JSON saves future calls to the website if you have won this month and therefore stops another notification being sent.
Saving the JSON for debug purposes if the API changes.

## crontab for checking bonds

10 2-6 2-7 * * python3 /home/pi/checkbonds.py >/dev/null 2>&1

Every hour at 10 minutes past 2am to 7am on the 2nd to 6th day of the month. This checks in the early hours of the morning and persists until it gets this months winning bonds. It checks for 5 days after the 1st of the month to ensure it checks the day after the first working day of the month.
