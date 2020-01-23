Cronjob lines:


Runs every 11:55 pm

55 23 * * * [path to python] [path to rainfall data script] >> cron.log
55 23 * * * /usr/bin/python3 /home/nina/rainfall_data/main.py >> /home/nina/rainfall_data/cron.log


Runs every 3 hours from start time

0 */3 * * * [path to python] [path to wunderground data script] >> cron.log
0 */3 * * * /usr/bin/python3 /home/nina/wunderground_processor/main.py >> /home/nina/wunderground_processor/cron.log
