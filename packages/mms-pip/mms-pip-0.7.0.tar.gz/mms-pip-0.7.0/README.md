# mms-pip
Public Python module from the GDWH-Team of MediaMarktSaturn-Technology.

!!!!!!!! ATTENTION: BETA VERSION !!!!!!!!!!
```
pip install mms-pip
```
Topics:
1. gcp_logger
2. redis_handler
3. bq_handler
4. gcs_handler



## 1. gcp_logger

Log Module for standardized log purposes.

### How to use:

#### 1.1 Import module:

```python
from mms.gcp_logger import Logger
```

#### 1.2 Initalize the logger:

```python
# Cloud Function Logging:
logger = Logger(service_name, run_id, project_id, function_name, resource_type)
logger = Logger(service_name='my-service', run_id='lksjdf2', project_id='my-project-id', function_name='ppx-price-updates-de-gcs-bq', resource_type='cloud_function')

# App Engine Logging:
logger = Logger(service_name, run_id, project_id, module_id, version_id, resource_type)
logger = Logger(service_name='my-service', run_id='lksjdfl98', project_id='v135-5683-alice-ksk-explore', module_id='app-flex-sample-service', version_id='v0.0.1', resource_type='gae_app')

# Compute Engine:
logger = Logger(service_name, run_id, project_id, resource_type)
logger = Logger(service_name='my-service', run_id='lksjdfl98', project_id='v135-5683-alice-ksk-explore', resource_type='gce_instance')

# Kubernetes Engine: 
logger = Logger(service_name, run_id, project_id, cluster_name, container_name, location, namespace_name, resource_type)
logger = Logger(service_name='my-service', run_id='id12345', project_id='v135-5683-alice-ksk-explore', cluster_name='jg-k8-testcluster', container_name=CONTAINER_NAME, location=ZONE, namespace_name='default', resource_type='k8s_container')

# Cloud Run (Serverless):
logger = Logger(service_name, run_id, project_id, revision_version, resource_type)
logger = Logger(service_name='my-service', run_id='lksjdfl98', project_id='v135-5683-alice-ksk-explore', revision_version='my-service-00003', resource_type='cloud_run_revision')

# Dataproc:
logger = Logger(service_name, run_id, project_id, cluster_name, location, resource_type)
logger = Logger(service_name='my-service', run_id='lksjdfl98', project_id='v135-5683-alice-ksk-explore', cluster_name='my-cluster', location='europe-west4', resource_type='cloud_dataproc_cluster')

# Cloud Composer:
logger = Logger(service_name, run_id, project_id, environment_name, location, resource_type)
logger = Logger(service_name='my-service', run_id='lksjdfl98', project_id='v135-5683-alice-ksk-explore', environment_name='my-composer-environment', location='europe-west4', resource_type='cloud_composer_environment')

```


The following resource_types are supported:

- Cloud Function: 'cloud_function'
- App Engine: 'gae_app'
- Compute Engine: 'gce_instance'
- Kubernetes: 'k8s_container'
- Cloud Run (serverless): 'cloud_run_revision'
- Dataproc: 'cloud_dataproc_cluster'
- Cloud Composer: 'cloud_composer_environment'

When resource type is unrecoginzable logs will be processed to 'Global'


#### 1.3 Use the logger:

```python
logger.info('your message')
logger.warning('your message')
logger.error('your message')
logger.critical('your message')
logger.debug('your message')
```

The logs are visible in Stackdriver Logging via:
- GAE Application -> Module_id -> Version_id for App Engine.
- Or under Cloudfunctions -> Function_id
- Or under GCE VM Instance -> Instance_id
- Or under Kubernetes Container -> cluster_name -> namespace_name -> container_name 
- Or under Cloud Run Revision -> service_name -> revision_name 
- Or under Global

### Important

This log tool only works in App Engine Standard/Flexible, Cloud Function, Compute Engine and Kubernetes, Cloud Run (Serverless) environment.

For local testing please set the boolean flag 'local_run' during initialization to 'True'

### How we log

We initialize the logger only in the "app.py" file. From there every log entry will be written - Modules used within app.py need to return the exceptions to the caller so
error etc. get logged at one central point within app.py.


## TODOs
- Adding description of redis_handler
- Adding description of datastore_handler
- Adding BQ and GCS Handler



## CHANGELOG:

### 0.5.3:

 - Local Run option was introduced -> initialization flag can be set


### 0.5.4: 

- Added 'service_name' to Logger class -> needs to be given in the arguments


### 0.5.5:

- Change the logname for each log entry to the specific service_name
- Added Cloud Run (Serverless as new source)

### 0.5.6:

- Logname bugfix

### 0.5.7:

- Cloud run logging code refinement 

### 0.5.9:

- Change default values from None to empty string


### 0.6.0:

- Added Dataproc as new log resource 'cloud_dataproc_cluster'


### 0.6.1:

- Added Cloud Composer as new log resource 'cloud_composer_environment'

### 0.7.0: 

- Added Datastore Handler for GCP for easy interaction with Google Cloud Datastore

***
Tobias Hoke - Josef Goppold - 25.06.2019
