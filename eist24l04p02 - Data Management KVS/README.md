# Key-Value Storage Main Exercise

In the basic exercise of our KVS we implemented a local file folder to manage our files. In this exercise, we want to make the folder _online_ by implementing a client-server model.

## Exercise Structure

The exercise includes 2 main components:

#### Server

Allocated in the `server` folder

- `ff.py`: Implementation of the file folder
- `api.py`: Implemenetation of the API endpoint handlers
- `app.py`: Implementation of the server

#### Client

Allocated in the `client` folder

- `client.py`: Implementation of the client

## Setup & Installation

In order to work with this exercise, you need to install Python on your machine. More information how to install and setup Python can be found [here](https://www.python.org/)

Once Python is installed on your machine, install the requirements for the exercise by running the following command in the exercise directory `pip install -r requirements.txt`

**Optional**: If you want to have separated working environment, you can setup the virtual environment (more [details](https://docs.python.org/3/library/venv.html))

## Run Instructions

In order to run the project, you need to both server and client. In the current working directory, run

- Server: `python server/app.py`
- Client: `python client/client.py`

**Note:** By default, the client uses command-prompt to interact with the server. If you just want to quickly check your implementation by an simple run, then comment out the call of `client_prompt()` and uncomment `example_use()`
