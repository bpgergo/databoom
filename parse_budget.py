import csv
import re
import datetime
from models import Budget
import logging

pattern1 = re.compile("^(\d+) .*$")
s1 = "011130 Önkormányzatok és önkormányzati hivatalok jogalkotó és általános igazgatási tevékenysége"
s2 = "13 Foglalkoztatottak egyéb személyi juttatásai 14 K1113 "


def get_value(s, p):
    m = re.search(p, s)
    if m:
        return m.group(1)
    else:
        return None

def test():
    print("func:", get_value(s1, pattern1))
    print("econ:", get_value(s2, pattern1))


def process_row(org_id, dt, row, econ_ids, econ_ids_row):
    func_id = get_value(row[0], pattern1)
    for i, field in enumerate(row):
        econ_id = econ_ids_row[i]
        if econ_id in econ_ids:
            budget = Budget(func_id=func_id, econ_id=econ_id, amount=field, org_id=org_id,
                    date_start=dt, comm=None, tags=None)
            yield budget


def generate_rows(org_id, dt, fname, econ_ids):

    econ_ids_row = None
    with open(fname, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        cnt = 0
        for row in reader:
            logging.info("processing row:%s" % row)

            if cnt == 1:
                econ_ids_row = [get_value(s, pattern1) for s in row]
            elif cnt > 1:
                for budget in process_row(org_id, dt, row, econ_ids, econ_ids_row):
                    yield budget
            cnt += 1


if __name__ == '__main__':
    test()
    #print(list(generate_rows("databoom-budget.csv")))
