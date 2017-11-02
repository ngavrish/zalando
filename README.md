Enironment:
Install Python 3.6
Put latest chromedriver in PATH
Install python modules from requirements.txt by running pip install -r requirements.txt
Install xvfb

Running the tests:
From the folder /qa-automation/src/zalando/portal/tests run pytest wishlist.py -sv --host www.zalando.de
To run it with HTML report, run pytest wishlist.py -sv --host www.zalando.de --html report.html