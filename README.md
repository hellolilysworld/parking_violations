# NYC Parking Violations

## Part 1: Python Scripting	

### File Structure

  ```console
  $ tree
  ```

  ```console
  .
  ├── Dockerfile
  ├── main.py
  ├── requirements.txt
  └── src
      └── bigdata1
          └── api.py

  2 directories, 4 files
  ```

### Packages 
- Specified in `requirements.txt`
  - `requests`
  - `pandas`
  - `numpy`
  - `sklearn`
  - `pytest`
  - `pyyaml`
  - `matplotlib`
  - `pygithub`
  - `scipy`
  - `sodapy`
  - `pprint`

### Docker

  - `Dockerfile`

  ```
  FROM python:3.7

  WORKDIR /app

  COPY requirements.txt /app

  RUN pip install -r requirements.txt
  ```

  - `docker build`
  
    - `-t bigdata1:1.0`
    
      ```console
      $ docker build -t bigdata1:1.0 .
      ```

  - `docker run`
  
    - `-v $(pwd):/app`
    - `-e APP_KEY={*Insert Token Here*}`
    - `-it bigdata1:1.0 /bin/bash`
    
    
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 /bin/bash
      ```
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main
      ```
      
    - `$soda_token` = environment variable set in `.bash_profile`
  
### Python Scripts

`main.py`
 ```py
  import argparse

  from src.bigdata1.api import get_results, add_record

  if __name__ == "__main__":
      parser = argparse.ArgumentParser()
      parser.add_argument("--page_size", type=int)
      parser.add_argument("--num_pages", default=None, type=int)
      parser.add_argument("--output", default=None)
      args = parser.parse_args()

      get_results(args.page_size, args.num_pages, args.output)
 ```

`src/bigdata1/api.py`
```py
import os
import json 
import pprint
from sodapy import Socrata

data_id = 'nc67-uf89'
client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))
count = int(client.get(data_id, select='COUNT(*)')[0]['COUNT'])

def get_results(page_size, num_pages, output):
    if not num_pages:
        num_pages = count // page_size + 1

    if output:
        create_records(output)

    for page in range(num_pages):
        offset = page * page_size
        page_records = client.get(data_id, limit=page_size, offset=offset)

        for record in page_records:
            if output:
                add_record(record, output)
            else:
                pprint.pprint(record, indent=4)

def create_records(output):
    with open(output, 'w') as json_file:
        init = {'results': []}
        json.dump(init, json_file, indent=4)


def add_record(record, output):

    with open(output) as json_file: 
        data = json.load(json_file) 
        records = data['results'] 
        records.append(record) 
    
    with open(output, 'w') as json_file:
        json.dump(data, json_file, indent=4)
```

  
### Usage

#### Arguments

- `--page_size`: 
  - Required 
  - How many records to request from the API per call.
- `--num_pages`: 
  - Optional
  - If not provided, continue requesting data until the entirety of the content has been exhausted. 
  - If provided, continue querying for data `num_pages` times.
- `--output`: 
  - Optional 
  - If not provided, print results to stdout. 
  - If provided, write the data to the file `output`.


```console
$ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main --page_size=3 --num_pages=2 
```


### EC2

#### ssh into EC2

- Change directory to the folder containing `.pem` file

```console
ssh -i 9760_ubuntu.pem ubuntu@{*Insert Public IP*}
```

## Part 2: Loading into ElasticSearch	


## Part 3: Visualizing and Analysis on Kibana	


## Part 4: Deploying to EC2 Instance	

