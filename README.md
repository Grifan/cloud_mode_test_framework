
## Set python virtual environment
>__NOTE__ Make sure you are using  Python 3.11.1 or higher, pip package manager was installed (version pip 22.3.1 or higher)


1. Copy existing `example.env` file and name it as `.env`
2. Install virtualenv: `pip install virtualenv`
3. Create new virtual environment:
    * Windows: `virtualenv venv`
    * Unix-based: `virtualenv -p $(which python3) venv`
    or `python3 -m virtualenv venv`
    >__NOTE__ Also it's possible to create virtual environment via Pycharm main menu                                                
     Open File -> Settings -> Project:__dmb-hw-automation__ -> Project Interpreter. Find and click by cogwheel and select __Add...__ option

4. Activate script:
    * Windows: go to the _venv/Scripts_ directory: `activate`
    * Unix-based: `source venv/bin/activate`
5. Navigate to project source dir (`cd ../..`) and install python packages to virtualenv:
    * Windows: `pip install -r requirements.txt`
    * Unix-based: `sudo pip install -r requiremennamets.txt`
6. Test framework uses allure report. 
To be able to execute tests and generate report, you need install `allure-commandline` version `2.20.1`. Stick instruction from [Get Started](https://docs.qameta.io/allure/#_get_started) accordingly with your OS 
   >__NOTE__ To run commandline application, Java Runtime Environment must be installed.
7. Self check cmd commands with cmd outputs (versions could be greater):
    * python version `python --version` Cmd output `Python 3.11.1`
    * pip version `pip --version` Cmd output `pip 22.3.1`
    * pytest version `tytest --version` Cmd output `pytest 7.2.1`
    * allure version `allure --version` Cmd output `2.20.1`


## Run tests cmd commands
1. Execute all tests (_-s_ argument means: print test logs into console):
   * `pytest -s tests/`
2. Execute all api tests:
   * `pytest -s tests/api/`
3. Execute all ui tests:
   * `pytest -s tests/ui/` 
4. Execute test with specific name (e.g. we need execute only negative API tests):
   * `pytest tests/api -s -k 'negative'`
5. Execute tests with allure. Just add next parameter (with required directory path) to pytest run command:`--alluredir=./<YOUR_TEST_RESULTS_DIR_PATH>`
   * `pytest -s --alluredir=./allure_results tests/api`

### Allure report generation
Execute allure cmd with directory path used while tests executing 
   * `allure serve ./allure_results`

### Delivery tests
Lint verification: `flake8 .`
