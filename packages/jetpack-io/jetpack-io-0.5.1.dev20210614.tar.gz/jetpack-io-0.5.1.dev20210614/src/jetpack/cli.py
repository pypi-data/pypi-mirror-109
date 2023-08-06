import json
import sys

import redis
import schedule
from google.protobuf import json_format
from jetpack import utils
from jetpack.models.runtime import cronjob_pb2, describe_pb2


def describe_output(app):
    jobs = []
    for job in schedule.get_jobs():

        if job.at_time is not None:
            target_time = job.at_time.isoformat()
        else:
            target_time = None

        if job.start_day is not None:
            target_day_of_week = cronjob_pb2.DayOfWeek.Value(job.start_day.upper())
        else:
            target_day_of_week = None

        jobs.append(
            cronjob_pb2.CronJob(
                function=utils.job_name(job),
                target_time=target_time,
                target_day_of_week=target_day_of_week,
                unit=cronjob_pb2.Unit.Value(job.unit.upper()),
                interval=job.interval,
            )
        )

    try:
        enum_name = app.__class__.__name__.upper() if app is not None else "NONE"
        framework = describe_pb2.Framework.Value(enum_name)
    except ValueError:
        framework = describe_pb2.Framework.Value("UNKNOWN")

    return describe_pb2.DescribeOutput(cron_jobs=jobs, framework=framework,)


# TODO(Landau): Use a framework? Like https://click.palletsprojects.com/en/7.x/
def handle(app=None):
    """
    Call individual function: `python jetpack_main.py run func_name`
    """
    if len(sys.argv) == 3 and sys.argv[1] == "run":
        target_job_name = sys.argv[2]
        for job in schedule.get_jobs():
            if utils.job_name(job) == target_job_name:
                job.job_func()

    """
    Get all jobs `python jetpack_main.py describe`
    """
    if len(sys.argv) == 2 and sys.argv[1] == "describe":
        print(json_format.MessageToJson(describe_output(app)))

    """
    Get all jobs `python jetpack_main.py describe-to-redis`
    """
    if len(sys.argv) == 4 and sys.argv[1] == "describe-to-redis":
        host = sys.argv[2]
        key = sys.argv[3]
        r = redis.Redis(host=host, port=6379, db=0)
        r.set(key, json_format.MessageToJson(describe_output(app)))
