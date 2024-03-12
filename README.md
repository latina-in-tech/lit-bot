# LatinaInTech Bot (a.k.a. LiT Bot)

## Index
- [Introduction](#introduction)
- [Current features](#current-features)
- [Used technologies](#used-technologies)
- [Setup](#setup)
- [How to use](#how-to-use)

## Introduction
The LatinaInTech (aka LiT) bot is the official bot of the Telegram group of the community of the same name.<br>
The idea of having a bot to offer group users a series of additional features to the UX is an idea that espouses the philosophy of the community, that of being a point of reference for enthusiasts of the tech world of the province (and not).

[Go to index ↑](#index)

## Current features
At the moment, the features implemented in the bot are:
- [view community events](#view-community-events)
- [creation of a new job offer](#creation-of-a-new-job-offer)
- [view job offers registered by community users](#view-job-offers-registered-by-community-users)
- download slides templates for lightining talks
- view community contacts
- view bot commands
- view community FAQ
- view community rules

[Go to index ↑](#index)

## Used technologies
The technologies used by the application are:
- Python (3.12.1)
- SQLite (3.44.2)

The libraries used by Python are:
- python-dotenv
- python-telegram-bot
- SQLAlchemy
- SQLAlchemy-Utils

## Setup

### Prerequisites
To use the bot, you need to have a Telegram API token, which can be obtained by following the [official guide](https://core.telegram.org/bots/tutorial#introduction).

Then, you can choose to install the application in two ways:
- on your PC
- using Docker containers

If you want to install the application on your PC, then keep following this guide;<br>
otherwise, jump directly to the setup guide [using Docker containers.](#setup-using-docker-containers)

In both cases, you still need to setup your .env file in order to get the application working correctly.

### Setup on your PC

Once this point has been established, we can move on to the phase of creating the Python virtual environment, within which all the dependencies necessary for the correct functioning of the application will be installed.

To proceed with completing this step, you must have the `virtualenv` module installed.<br>
If this is not installed, run the command:

```console
python -m pip install virtualenv
```

Once the `virtualenv` module is installed, you can proceed with cloning this repository.<br>
To proceed with completing this step, use the command:

```console
git clone https://github.com/latina-in-tech/lit-bot.git
```

Once the repository has been cloned, you can proceed with the creation of the application's virtual environment.<br>
To proceed with completing this step, use the command:

```console
python -m virtualenv .\venv
```

Once the creation of the virtual environment of the application (hereinafter _venv_) has been completed, you can proceed with its activation, using the command:

```console
.\venv\Scripts\activate
```

Once venv is activated, you can proceed with installing the application dependencies (requirements.txt), using the command:

```console
pip install -r requirements.txt
```

Once the application dependencies are installed, you can proceed with the creation of the `.env` file in the root folder, within which it is necessary to specify a series of environment variables for the correct functioning of the application.<br>
The variables are:


```console
BOT_TOKEN=<api_token>

SA_DB_DIALECT=sqlite
SA_DB_DRIVER=pysqlite
SA_DB_FILEPATH=db.sqlite
``` 

Once the .env file has been created, and the variables have been correctly valued, the application is ready to be used, running the command:

```console
python .
```

[Go to index ↑](#index)

### Setup using Docker containers

In order to use Docker containers to setup the application, you need to have Docker Desktop installed in your operating system.

Once this point has been estabilished, you can proceed with building the Docker image with the command:

```console
docker image build . --tag "lit-bot-image"
```

Once the Docker image has been built, you can proceed with creating and running the container with the command:

```console
docker container run --interactive --detach --name lit-bot-container lit-bot-image
```

You can also use Docker Compose to build and run the application stack, using the command:
```console
docker compose up --detach
```

Once the Docker container is created and is running, the application is ready to be used.

[Go to index ↑](#index)

## How to use

To use the LatinaInTech bot, you need to search for it on Telegram by typing `@latinaintechbot` in the general search bar.<br>
Once you have found the bot, you can proceed with launching it, making sure you receive the welcome message as shown below:

![start command](/docs/images/commands/start.png)

[Go to index ↑](#index)

By typing the command `/cmds`, the list of commands that can be used by the user will be shown.<br>
For guidance on how to use individual commands, you can type the command you want to use, followed by the help switch:

```console
/jobs help
```

[Go to index ↑](#index)

### View community events
To see upcoming community events, you need to type the `/events` command, which will display a list like the one below:

**TODO - Example**

[Go to index ↑](#index)

### Creation of a new job offer
To create a new job offer, you need to type the command `/create_job`, which will start a conversation with the user, asking for the various fields required to correctly register the job offer.<br>
You can see the whole process through the following images.
<details>
    <summary>Click here to expand</summary><br>
    
![create_job - start](/docs/images/conversation/create_job/create_job_start.png)

![create_job - contract type](/docs/images/conversation/create_job/create_job_contract_type.png)

![create_job - job category](/docs/images/conversation/create_job/create_job_job_categry.png)

![create_job - job position](/docs/images/conversation/create_job/creat_job_position.png)

![create_job - job description](/docs/images/conversation/create_job/create_job_description.png)

![create_job - job link](/docs/images/conversation/create_job/create_job_link.png)

![create_job - job ral](/docs/images/conversation/create_job/create_job_ral.png)

![create_job - job created](/docs/images/conversation/create_job/create_job_job_created.png)

</details>
<br>

[Go to index ↑](#index)

### View job offers registered by community users
To view the list of job offers registered within the community, you need to type the `/jobs` command, which will show a list like the one below:

![jobs - jobs start](/docs/images/conversation/jobs/jobs_start.png)

![jobs - jobs category](/docs/images/conversation/jobs/jobs_job_category.png)

![jobs - jobs category selected](/docs/images/conversation/jobs/jobs_job_category_selected.png)

[Go to index ↑](#index)
