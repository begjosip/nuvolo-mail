<p align="center">
    <img src="templates/images/nuvolo.png" alt="logo" />
</p>


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<div align="center">

![Python: Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![RabbitMQ: RabbitMQ](https://img.shields.io/badge/-rabbitmq-%23FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Flask: Flask](https://img.shields.io/badge/-flask-%23000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML: HTML](https://img.shields.io/badge/html-%23f06529?style=for-the-badge&logo=html5&logoColor=white)
![Jinja: Jinja](https://img.shields.io/badge/jinja-%23FF0000?style=for-the-badge&logo=jinja&logoColor=white)

</div>

---
### Description

Repository for sending email to users from queue messages over SMTP server. Developed using Python 3.10, Flask, RabbitMQ
and Jinja2 with HTML for email templates.

---

### Instructions

Position correctly to project root directory and run command:
```shell
pip install -r requeriments.txt
``` 

Given command will install all needed packages to your Python environment.
Before running application check `.env` file and setup requeired properties.
```
PORT=
SMTP_SERVER=
SMTP_PORT=
SMTP_APP_MAIL=
SMTP_PASSWORD=
```
After setting these properies and valid RabbitMQ docker container you can run 
```shell
python app.py
```
on desired port to listen and consume messages from queues.



