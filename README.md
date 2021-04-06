Cronjob lines:


Runs every 11:55 pm

55 23 * * * [path to python] [path to rainfall data script] >> cron.log

55 23 * * * /usr/bin/python3 /home/weather-data-maintenance/rainfall_data.py >> /home/weather-data-maintenance/rainfall.log


Runs every 3 hours from start time

0 */3 * * * [path to python] [path to wunderground data script] >> cron.log

0 */3 * * * /usr/bin/python3 /home/weather-data-maintenance/wunderground_data.py >> /home/weather-data-maintenance/wunderground.log

0 */3 * * * /usr/bin/python3 /home/weather-data-maintenance/seams_data.py >> /home/weather-data-maintenance/seams.log



Change db port and name in scripts according to the database setup.