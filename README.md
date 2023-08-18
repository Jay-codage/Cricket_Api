
# Project Title

Cricket-API


## Project Descriptions
I've created a dynamic REST API using Python and Django that offers real-time cricket updates through web scraping. This API automatically fetches and updates live data, providing users with instant access to match scores, player stats, and game details
## Initial Setup
Create a virtual environment for the repository by executing.
*     virtualenv -p python3.8 ~/.virtualenv/VENV_NAME
For virtualenv **https://www.youtube.com/watch?v=GZbeL5AcTgw**
## Running Tests

Manual Setup For Backend Development
1) Activate the virtual environment by executing:
    `source ~/.virtualenv/VENV_NAME/bin/activate`
2) Install any new or updated dependencies by executing:
    `pip3 install -r requirements.txt` 
3) Run any new or updated database migrations by executing:
    `pycharm : python manage.py migrate`
    **`others: ./manage migrate`**
4) Add database after migrate:
`    pycharm : python manage.py makemigrations`
     `others: ./manage makemigrations`
5) Create a superuser if necessary by executing:
    `pycharm : python manage.py createsuperuser`
    **`others: ./manage createsuperuser`**
6) Run the development server by executing:
    **`pycharm : python manage.py runserver`**
    **`others: ./manage runserver`**

## To fetch live data, follow these steps in your terminal

1) Navigate to the **`cricket_api/scrapping`** directory.
2) Run the following Python files one by one: **`match.py`**, **`match_link_transfer.py`**, and **`test_match_scorecard.py`**.
    
    #### Here's a condensed version of the instructions:
   * cd cricket_api/scrapping
   * python match.py
   * python match_link_transfer.py
   * python test_match_scorecard.py
   
Make sure you have Python installed and the necessary dependencies are satisfied before running the commands.