from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, add_job_to_db, update_job_in_db, delete_job_in_db

import re
import json

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route("/")
def hello_jovian():
  if request.method == 'POST': 
    return redirect(url_for('hello_jovian'))
  
  jobs = load_jobs_from_db()
  return render_template('home.html', 
                         jobs=jobs)

@app.route("/<message>")
def mes_jovian(message):
  if request.method == 'POST': 
    return redirect(url_for('hello_jovian'))
  
  jobs = load_jobs_from_db()
  return render_template('home2.html', 
                         jobs=jobs,
                         message=message)

@app.route("/filter/<jobstring>")
def search(jobstring):
  
  jobs = load_jobs_from_db()
  if jobstring =="None":
    message="Job not found"
    job=None
  else:
    message="Job is found"
    print(jobstring)
    job=json.loads(jobstring)
  return render_template('search.html', 
                         job=job,
                         jobs=jobs,
                         message=message)
  
@app.route("/search", methods=['POST'])
def filtered():
  data = request.form
  print(data.to_dict(flat=False))
  job = load_job_from_db(data['id'])
  print(job)
  if job:
    subset_dict = {key: job[key] for key in list(job)[:4]}
    return redirect(url_for('search', jobstring=json.dumps(subset_dict)))
  else:
    return redirect(url_for('search', jobstring='None'))

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/create", methods=['POST'])
def create_jobs():
  data = request.form

  if not check_title(data['title']):
    return redirect(url_for('mes_jovian', message="Fix Title Input"))

  if not check_location(data['location']):
    return redirect(url_for('mes_jovian', message="Fix Location Input"))

  if not check_currency(data['currency']):
    return redirect(url_for('mes_jovian', message="Fix Currency Input"))

  if not check_salary(data['salary']):
    return redirect(url_for('mes_jovian', message="Fix Salary Input"))
    
  result = add_job_to_db(data)
  
  if result:
    message = f"Job has been added. Job Title:{data['title']},\n \
    Job location: {data['location']},\n \
    Salary: {data['currency']} {data['salary']}"
  else:
    message = "Job not added."
  return redirect(url_for('mes_jovian', message=message))
  

@app.route("/update", methods=['POST'])
def update_jobs():
  data = request.form
  exist = load_job_from_db(data['id'])
  if not exist:
    return redirect(url_for('mes_jovian', message="Job does not exist"))
  
  
  if not check_title(data['title']):
    return redirect(url_for('mes_jovian', message="Fix Title Input"))

  if not check_location(data['location']):
    return redirect(url_for('mes_jovian', message="Fix Location Input"))

  if not check_currency(data['currency']):
    return redirect(url_for('mes_jovian', message="Fix Currency Input"))

  if not check_salary(data['salary']):
    return redirect(url_for('mes_jovian', message="Fix Salary Input"))
    
  result=update_job_in_db(data)

  if result:
    message = f"Job has been updated. Job Title: {data['title']},\n \
    Job location: {data['location']},\n \
    Salary: {data['currency']} {data['salary']}"
  else:
    message = "Job not updated."
  return redirect(url_for('mes_jovian', message=message))

@app.route("/delete", methods=['POST'])
def delete():
  data = request.form
  job = load_job_from_db(data['id'])
  if not job:
    return redirect(url_for('mes_jovian', message="Job does not exist."))
  result=delete_job_in_db(data['id'])
  jobs = load_jobs_from_db()
  if result:
    message = f"Job has been deleted. Job ID = {data['id']}."
  else:
    message = "Job not deleted."
  return redirect(url_for('mes_jovian', message=message))
  

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  
  if not job:
    return "Not Found", 404
  
  return render_template('jobpage.html', 
                         job=job)

@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html', 
                         application=data,
                         job=job)

def check_title(title):
    # Define a regular expression pattern to match alphabets, spaces, and brackets
    pattern = r'^[a-zA-Z\s\[\]]+$'

    # Use re.match to check if the title matches the pattern from the beginning
    if re.match(pattern, title):
        return True
    else:
        return False
      
def check_location(location):
    # Define a regular expression pattern to match alphabets and spaces
    pattern = r'^[a-zA-Z\s]+$'

    # Use re.match to check if the location matches the pattern from the beginning
    if re.match(pattern, location):
        return True
    else:
        return False

def check_currency(currency):
    # Check if the string contains exactly three alphabetic characters and is not empty
    if len(currency) == 3 and currency.isalpha():
        return True
    else:
        return False

def check_salary(salary):
    # Check if the string contains only digits and has a length of up to 8 characters
    if salary.isdigit() and len(salary) <= 8:
        return True
    else:
        return False

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)