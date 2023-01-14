import json
import csv
import os
import re

log_file_path = "logs/"
log_file_name = "8f860c2c-3b3a-471f-9501-29c23e792bce.log"

output_file_path = "outputs/"
output_file_name = os.path.splitext(log_file_name)[0]

output_file = output_file_path + output_file_name

def from_log_into_csv(log_file_name):
    csv_file_names = [output_file + "_triages.csv", output_file + "_queries.csv", output_file + "_projects.csv"]
    with open(log_file_path + log_file_name, 'r') as logfile:
        csv_files = [open(f, 'w', newline='') for f in csv_file_names]
        writer_triage = csv.writer(csv_files[0])
        writer_queries = csv.writer(csv_files[1])
        writer_projects = csv.writer(csv_files[2])
        writer_triage.writerow(['Worker','SimilarityID', 'Error'])
        writer_queries.writerow(['Worker','ProjectID', 'Error'])
        writer_projects.writerow(['Projects Imported'])

        for line in logfile:
            try:
                data = json.loads(line)

                #Traiges Logic
                if "skipping predicate" in data['msg']:
                    worker = data['worker']
                    similarity_id = data['msg'].split()[2]
                    msg = data['msg']
                    match = re.search(r'id [-\d]+ (.+?),', msg)
                    if match:
                        error = match.group(1)
                    else:
                        error = "No match found"
                    writer_triage.writerow([worker, similarity_id, error])
                    
                #Queries Logic    
                elif "skipping group" in data['msg']:
                    project_id = data['msg'].split()[3]
                    worker = data['worker']
                    msg = data['msg']
                    match = re.search(r'ID \d+ (.+?),', msg)
                    if match:
                        error = match.group(1)
                    else:
                        error = "No match found"
                    writer_queries.writerow([worker, project_id, error ])
                
                #Projects Imported Logic
                elif "created project" in data['msg']:
                    match = re.search(r'created project (.+)', data['msg'])
                    if match:
                        project_name = match.group(1)
                        writer_projects.writerow([project_name])
                    else:
                        writer_projects.writerow("No project found")

            except json.decoder.JSONDecodeError:
                # Handle JSONDecodeError in case a line is not in json format
                print("Line is not in JSON format, skipping")
            except KeyError:
                # Handle KeyError in case the json object does not contain the expected keys
                print("Missing keys in JSON object, skipping")
        for csv_file in csv_files:
            csv_file.close()


from_log_into_csv("8f860c2c-3b3a-471f-9501-29c23e792bce.log")

#test commit after