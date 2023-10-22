from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

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
    result = conn.execute(text("SELECT * FROM jobs WHERE (`id` = :id)"),{"id": id})

    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(
          zip([
              'id', 'title', 'location', 'salary', 'currency',
              'responsibilities', 'requirements', 'time1', 'time2'
          ], rows[0]))


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


def add_job_to_db(data):
  try:
        with engine.connect() as conn:
            query = text(
                "INSERT INTO jobs (`title`, `location`, `salary`, `currency`) VALUES (:title, :location, :salary, :currency)"
            )
    
            conn.execute(
                query, {
                    "title": data['title'],
                    "location": data['location'],
                    "salary": data['salary'],
                    "currency": data['currency']
                })
            conn.execute("COMMIT")
        print("Added" +str(data))
        return True  # Return True on successful execution
  except Exception as e:
    print(f"Error: {e}")
    return False
      

def update_job_in_db(data):
  try:
    with engine.connect() as conn:
      query = text(
          "UPDATE jobs SET `title` = :title, `location` = :location, `salary` = :salary, `currency` = :currency WHERE (`id` = :id)"
      )
  
      conn.execute(
          query, {
              "title": data['title'],
              "location": data['location'],
              "salary": data['salary'],
              "currency": data['currency'],
              "id": data['id']
          })
      conn.execute("COMMIT")
      return True  # Return True on successful execution
  except Exception as e:
    print(f"Error: {e}")
    return False

def delete_job_in_db(id):
  try:
    with engine.connect() as conn:
      query = text(
          "DELETE FROM `jobs` WHERE (`id` = :id)"
      )
  
      conn.execute(
          query, {"id": id})
      conn.execute("COMMIT")
      return True  # Return True on successful execution
  except Exception as e:
    print(f"Error: {e}")
    return False
