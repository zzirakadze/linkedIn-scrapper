## LinkedIn Scrapper
### Please run below commands in your command line to use the scripts
### 1. Install Python3
```shell
brew install python
```
##### 2. Create a virtual env inside the project
```shell
virtualenv venv -p /usr/bin/python3
```
##### 3. Activate the virtual env
```shell
source venv/bin/activate
```
##### 4. Install packages from [requirements.txt](requirements.txt)
```shell
python3 -m pip install -r requirements.txt
```

#### To make scripts executable from terminal run for each .py file e.g:
```shell
chmod +x ./main.py
```
___

#### To allow chromedriver to start on MAC in project folder run:
```shell
spctl --add --label 'Approved' chromedriver 
```
___
#### To Run the application
```shell
python3 ./main.py
```
____

