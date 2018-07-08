from jenkinsapi.jenkins import Jenkins
import sqlite3
from datetime import datetime

def get_server_instance():
    jenkins-url = 'http://localhost:8080/'
    jenkins-username = ''
    jenkins-password = ''

    server = Jenkins(jenkins-url, jenkins-username, jenkins-password)
    return server

def get_job_details():
    jobs = []

    server = get_server_instance()
    for job_name, job_instance in server.get_jobs():
        if job_instance.is_enabled():
            status = "ENABLED"
        else:
            status = 'DISABLED'

        if job_instance.is_running():
            status = 'RUNNING'

        jobs.append([job_name, status, datetime.now().strftime('%Y/%m/%d %H:%M:%S')])

    return jobs

def get_db_connection():
    db_name = 'jenkins-jobs.db'
    conn = sqlite3.connect(db_name)
    return conn

def create_jobs_table():
    conn = get_db_connection()

    query = '''CREATE TABLE JOBS
     (NAME           TEXT    NOT NULL,
     STATUS          TEXT    NOT NULL,
     CHECKTIME       TEXT    NOT NULL);'''
    conn.execute(query);

    conn.commit()
    conn.close()

def add_jobs_to_db(jobs):
    conn = get_db_connection()

    for job_name, job_status, check_time in jobs:
        query = "INSERT INTO JOBS (NAME,STATUS,CHECKTIME) \
          VALUES ('" + job_name + "', '" + job_status + "', '" + check_time + "')"
        conn.execute(query);

    conn.commit()
    conn.close()

jobs = get_job_details()
create_jobs_table()
add_jobs_to_db(jobs)
