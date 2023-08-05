from datetime import datetime, date
from marqeta.response_models import datetime_object
import json
import re

class CronJobInfo(object):

    def __init__(self, json_response):
        self.json_response = json_response

    def __str__(self):
        return json.dumps(self.json_response, default=self.json_serial)

    @staticmethod
    def json_serial(o):
        if isinstance(o, datetime) or isinstance(o, date):
            return o.__str__()

    @property
    def schedule(self):
        return self.json_response.get('schedule', None)


    @property
    def group(self):
        return self.json_response.get('group', None)


    @property
    def id(self):
        return self.json_response.get('id', None)


    @property
    def class(self):
        return self.json_response.get('class', None)


    @property
    def is_running(self):
        return self.json_response.get('is_running', None)

    @property
    def last_run_duration_millis(self):
        return self.json_response.get('last_run_duration_millis', None)

    @property
    def next_run(self):
        if 'next_run' in self.json_response:
            return datetime_object('next_run', self.json_response)


    @property
    def last_run(self):
        if 'last_run' in self.json_response:
            return datetime_object('last_run', self.json_response)


    @property
    def timezone(self):
        return self.json_response.get('timezone', None)


    @property
    def start_time(self):
        if 'start_time' in self.json_response:
            return datetime_object('start_time', self.json_response)


    def __repr__(self):
         return '<Marqeta.response_models.cron_job_info.CronJobInfo>' + self.__str__()
