# resume_importer

## usage
```sh
resumeImporter [-h] --paths [PATHS [PATHS ...]] [-r]
                          [--source_id SOURCE_ID] [--api_key API_KEY]
                          [--timestamp_reception TIMESTAMP_RECEPTION]
                          [--verbose] [--silent] [--n-worker N_WORKER]
                          [--logfile LOGFILE]
```

## description
  resume_importer uploads resume to Riminder's platform. The resumes are selected using the paths argument and can be a directory or just a file. In case a profile does not get sent, a folder named `failed-resumes` will be created in the current directory with a copy of the failed files.

## options
* --paths path/to/target/file/or/directory1 path/to/target/file/or/directory2 ... path/to/target/file/or/directoryn
  * Directory where document will be takken
  * **Required**
* -h
  * print help message and exit
* --source_id source_id
  * Source id of the source where files will be upload.
  * Will be asked if absent.
* --api_key api_secret_key
  * Your api secret, available on your riminder platform.
  * Will be asked if absent.
* --verbose
  * Enable verbose mode
* --silent
  * Enable silent mode
* --n-worker n
  * Select the number of worker (thread) you want to use.
  * **Default**: 3
* --logfile path/to/file
  * Select a file where export logs will be logged
* --timestamp_reception timestamp
  * Timestamp of the reception of these file
  * **Default**: Time when file get to the server.
