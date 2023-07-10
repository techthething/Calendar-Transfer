# calendar-transfer
Transfers calendar event information from document to Google Calendar

## Table of Contents
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)

## Install

Follow the steps on this website to set up and run this app which runs on Google Calendar API: https://developers.google.com/admin-sdk/directory/v1/quickstart/python

After running the sample, replace the code with the code from c_transfer.py. You are now ready to run/utilize the program.
## Usage

Insert calendar information into a text file.

The first line should be a date of the form: Day of Week, Month Day

Events can (but are not required to) include a time. 
If time is not given, the event is placed very early in the day (at a time that you can modify).
If time is given, the last mentioned time should be designated AM or PM. 
Events don't need to include an end time. If no end time given, the event is assumed to last 1 hour (although you can modify this variable).

Here is an acceptable example input:
```
Wednesday, July 26th
Sarah goes to the park; 8 am
Brenda works on programming exercises
John takes a bike ride; 9 a.m. - 12 p.m.[need to confirm]
Put a bid in for the auction ($369?)

Thursday, July 27th

Friday, July 28th
Sarah has doctor's appointment
John - swim practice (9 A.M.)
```

With input of the above form, the program will populate your desired events into your Google Calendar.
## Contributing

If you would like to contribute to this project, you can follow these guidelines:

* Fork the project on GitHub.
* Create a new branch for your changes.
* Make your changes and commit them.
* Push your changes to your forked repository.
* Create a pull request on the original repository.

Once your pull request is reviewed and approved, your changes will be merged into the master branch.
