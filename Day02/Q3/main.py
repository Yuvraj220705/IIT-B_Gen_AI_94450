import requests
import json

url = "https://jsonplaceholder.typicode.com/todos/1"
response = requests.get(url)

if response.status_code == 200:
    fetched_data = response.json() 

    output_filename = 'api_output.json'
    
    with open(output_filename, 'w') as f:
        
        json.dump(fetched_data, f, indent=4) 
        
    print(f"Data successfully saved to {output_filename}")

else:
    print(f"Error fetching data. Status code: {response.status_code}")