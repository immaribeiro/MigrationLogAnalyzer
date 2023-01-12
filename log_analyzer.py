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
    # Open the log file and the csv file
    with open(log_file_path + log_file_name, 'r') as logfile, open(output_file + "_triages.csv", 'w', newline='') as csvfile_triage, open(output_file + "_queries.csv", 'w', newline='') as csvfile_queries:
        # Create a csv writers object for triages
        writer_triage = csv.writer(csvfile_triage)
        # Write the header row
        writer_triage.writerow(['Worker','SimilarityID', 'Error'])
        # Create a csv writers object for queries
        writer_queries = csv.writer(csvfile_queries)
        # Write the header row
        writer_queries.writerow(['Worker','ProjectID', 'Error'])
        
        for line in logfile:
            try:
                data = json.loads(line)
                if "skipping predicate" in data['msg']:
                    worker = data['worker']
                    similarity_id = data['msg'].split()[2]
                    msg = data['msg']
                    match = re.search(r'id [-\d]+ (.+?),', msg)
                    if match:
                        error = match.group(1)
                    else:
                        error = "No match found."

                    writer_triage.writerow([worker, similarity_id, error])
                    
                elif "skipping group" in data['msg']:
                    project_id = data['msg'].split()[3]
                    worker = data['worker']
                    msg = data['msg']
                    match = re.search(r'ID \d+ (.+?),', msg)
                    if match:
                        error = match.group(1)
                    else:
                        error = "No match found."
                    writer_queries.writerow([worker, project_id, error ])

            except json.decoder.JSONDecodeError:
                # Handle JSONDecodeError in case a line is not in json format
                print("Line is not in JSON format, skipping")
            except KeyError:
                # Handle KeyError in case the json object does not contain the expected keys
                print("Missing keys in JSON object, skipping")

from_log_into_csv("8f860c2c-3b3a-471f-9501-29c23e792bce.log")



# import re

# line = '{"msg":"similarity id 657146215 is not unique, skipping predicate"}'
# data = json.loads(line)
# msg = data['msg']

# match = re.search(r'id \d+ (.+?),', msg)
# if match:
#     text = match.group(1)
#     print(text)
# else:
#     print("No match found.")



# import re
# line = '{"msg":"similarity id 657146215 is not unique, skipping predicate"}'
# data = json.loads(line)
# msg = data['msg']

# text = re.findall(r'id \d+ (.+?),', msg)
# if text:
#     text = text[0]
#     print(text)
# else:
#     print("No match found.")
