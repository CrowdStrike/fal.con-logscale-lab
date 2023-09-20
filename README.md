# fal.con-logscale-lab


Welcome to DEV13 (LogScale Lab part 1) and/or DEV22 (LogScale Lab part 2).

For the interactive parts of the sessions please open this link to
[Falcon Encounter](https://falcon.events/landing)
and wait for the entry code to be provided to you.

A script for simulated ingest of logs can be found in the "Lab materials" directory in this repository.

Prerequisits for running the script are:
* Sample events file (events.json)
* Python 3
* 'requests' library (may need to be installed via "pip3 install requests")

Prior to running the "generate_logs.py" script, please replace the ingest token with the generated ingest token for your lab sandbox repository.

The script  will generate randomized events with timestamps to backfill (past 7 days) and send those via a post request to the repository.

The script is only for demo/lab purposes and should not be used for other use cases which rely on accurate information/events.


If you are having issues running the script, submit it [here](https://forms.gle/7kHKhLzeSobfnoVS8)
