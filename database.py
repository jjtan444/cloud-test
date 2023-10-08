from sqlalchemy import create_engine, text
import os

db_connection_string = "mysql+pymysql://nme7uy7drx9c3my0u0h2:pscale_pw_oEKX2tK0rEg2LxBRFLI2avAnlM9Tqs7A09FoeZfW62o@aws.connect.psdb.cloud/cloud?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))

    jobs = []
    for row in result.all():
      jobs.append(
          dict(
              zip([
                  'id', 'title', 'location', 'salary', 'currency',
                  'responsibilities', 'requirements', 'time1', 'time2'
              ], row)))
    return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"), val=id)
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text(
        "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"
    )

    conn.execute(query,
                 job_id=job_id,
                 full_name=data['full_name'],
                 email=data['email'],
                 linkedin_url=data['linkedin_url'],
                 education=data['education'],
                 work_experience=data['work_experience'],
                 resume_url=data['resume_url'])


