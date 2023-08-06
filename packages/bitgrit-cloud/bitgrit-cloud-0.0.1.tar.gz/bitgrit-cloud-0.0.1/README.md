# bitgrit-cloud
Library to interact with our cloud service(GCP)

### Run tests inside a docker container
```bash
docker-compose run test
```

### Build inside a docker container
```bash
docker-compose run build
```
> Note: look inside `./dist/` folder to see the latest build `.whl` file.

# How to setup the Library:
### Install Dependencies/Packages:

### Run this command:
```bash
pip install -r requirements.txt
```

### Import the Library:
```python
from dsn.bitgrit.gcp.dataset_api import DatasetAPI
from dsn.bitgrit.datasets.dataset import DatasetType
```

### To checkout documentation:
```bash
pydoc dataset
```

### To set the environment variable
```bash
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/settings.json"
```

### To run the test
```bash
python -m unittest
```
### To package the library
```bash
python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```