import os
import subprocess
import sys

if __name__ == '__main__':
    kwargs = dict(x.split('=', 1) for x in sys.argv[1:])
    # prepare_db_tracker(kwargs['--host'])
    testrunner = subprocess.Popen(f"pytest {os.environ.get('TEST_HOME')}/src/portal/tests --host {kwargs['--host']} -sv "
                     f"--junitxml={os.environ.get('TEST_HOME')}/src/portal/tests/reports/full_run_xunit_report.xml "
                     f"--html {os.environ.get('TEST_HOME')}/src/portal/tests/reports/full_run.html", shell=True)
    testrunner.wait()
