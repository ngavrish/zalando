import subprocess
import os
import sys
from time import sleep

import psycopg2


prefix = f"{os.environ.get('TEST_HOME')}/src/portal/tests/"

test_sets = [f"{prefix}smoke_test.py::test_login_logout {prefix}smoke_test.py::test_reset_backstage",
             f"{prefix}smoke_test.py::test_add_order2driver {prefix}smoke_test.py::test_remove_order_from_driver "
             f"{prefix}dispatching_test.py::test_basic_dispatching",
             f"{prefix}ota_test.py",
             f"{prefix}driver_test.py --vehicleTitle \"Charge Truck P1\""]

long_sets = [f"{prefix}smoke_test.py::test_login_logout {prefix}smoke_test.py::test_reset_backstage",
             f"{prefix}smoke_test.py::test_add_order2driver {prefix}smoke_test.py::test_remove_order_from_driver "
             f"{prefix}wishlist.py::test_basic_dispatching {prefix}wishlist.py::test_dispatch_max",
             f"{prefix}ota_test.py",
             f"{prefix}driver_test.py --vehicleTitle \"Charge Truck P1\""]



def get_db_connection(dbname='tracker', user='appuser', host='ngavrish-coreos.charge.tech'):
    cntr = 0
    while cntr < 10:
        try:
            conn = psycopg2.connect(f"dbname='{dbname}' user='{user}' host='{host.strip()}'")
            conn.autocommit = True
        except Exception as e:
            print(e)
            sleep(1)
            cntr+=1
        else:
            break
    return conn


def prepare_db_tracker(host):
    conn = get_db_connection(host=host)
    cur = conn.cursor()
    cur.execute('TRUNCATE appuser.orders CASCADE; COMMIT;')

if __name__ == '__main__':
    kwargs = dict(x.split('=', 1) for x in sys.argv[1:])
    test_num = 0
    test_runners = []
    # prepare_db_tracker(kwargs['--host'])
    sets = test_sets
    if kwargs.get('--long'):
        sets = long_sets
    for test_name in sets:
        test_num += 1
        runner = subprocess.Popen(f"pytest {test_name} --host {kwargs['--host']} -sv "
                         f"--junitxml={prefix}/reports/thread{str(test_num)}_xunit_report.xml "
                         f"--html {prefix}/reports/thread{str(test_num)}.html", shell=True)
        test_runners.append(runner)

    exit_codes = [runner.wait() for runner in test_runners]
    print("TESTS HAVE FINISHED WITH EXIT CODES " + str(exit_codes))
