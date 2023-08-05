# probator-scheduler-sqs

Please open issues in the [Probator](https://gitlab.com/probator/probator/issues/new?labels=scheduler-sqs) repository

## Description

This scheduler takes care of scheduling the actual SQS messaging and tracks the status of the jobs as workers are executing said jobs.

## Configuration Options

| Option name           | Default Value | Type      | Description                                                                                   |
|-----------------------|---------------|-----------|-----------------------------------------------------------------------------------------------|
| enabled               | True          | bool      | Enable SQS based scheduler                                                                    |
| queue\_region         | us-west-2     | string    | Region of the SQS Queues                                                                      |
| status\_queue\_url    | *None*        | string    | URL of the SQS Queue for worker reports                                                       |
| job\_delay            | 2             | float     | Seconds between scheduled jobs. Can be used to avoid spiky loads during execution of tasks    |

This project is based on the work for [Cloud Inquisitor](https://github.com/RiotGames/cloud-inquisitor) by Riot Games
