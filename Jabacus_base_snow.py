'''Snow load calculations with jabacus.com'''
import requests
import re
import time
import numpy as np
from prettytable import PrettyTable as pt


''' Concatenate strings together for parameters in jabacus GET request'''
def build_url(data: list)->str:
    url = ""
    for i in data:
        url += i[0] + "=" + str(i[1])
        if i != data[len(data) - 1]:
            url += "&"
    return url


''' Find snow load results in HTML response'''
def parse_html_custom(html: str)->tuple:
    local = re.search(r"(?<=>Location: ).*?(?=, zzz<br>Ss)", html).group()
    s_s = re.search(r"(?<=, zzz<br>Ss = ).*?(?= kPa  / Sr =)", html).group()
    s_r = re.search(r"(?<=Sr = ).*?(?= kPa <br>Importance Factor)", html).group()
    s = re.search(r"(?<=</h5><h4> S = ).*?(?= kPa </h4><h4>S =)", html).group()
    result = (local, s_s, s_r, s)
    print(result)
    return result


''' Retrieve snow load results, with Ss and Sr as input, from jabacus'''
def base_snow(id: int)->dict:
    base_url = "http://jabacus.com/engineering/load2015/snow/snowResults.php?"
    data = [("province", "zzz"),
            ("locationid", id),
            ("Ss", ""),
            ("Sr", ""),
            ("Is", 1.0),
            ("Cw", 1.0),
            ("Ca", 1.0),
            ("L", ""),
            ("w", ""),
            ("pitch", 9),
            ("slippery", "false"),
            ]
    url = base_url + build_url(data)
    html = requests.get(url)
    result = parse_html_custom(str(html.content))
    return result


''' Pretty print the table results and return a pt object'''
def print_pt(rows: list)->pt:
    tab = pt(["Locality", "Ss", "Sr", "S"])
    for i in rows:
        tab.add_row(i)
    print(tab)
    return tab


''' Export pt object to .csv file'''
def export_csv(table: list, filename: str):
    with open(filename, 'w', newline='') as f_output:
        f_output.write(table.get_csv_string())


'''
Jabacus use simple integer to define all of the localities in the NBCC. Below
we run the full range of localities to extract Ss, Sr and the calculated S
values. This will allow us to compare with Skyciv results.
'''
if __name__ == "__main__":
    locality_list= []
    for i in range(101,150):
        locality_list.append(base_snow(i))
        time.sleep(np.random.default_rng().uniform())
    print(locality_list)
    pt = print_pt(locality_list)
    export_csv(pt, "Pitch_9_12+Slippery_False.csv")
