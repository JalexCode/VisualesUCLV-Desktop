from contextlib import closing
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from util.const import *
from util.util import *

def asd():
    with closing(requests.get(VISUALES_UCLV_URL, verify=False, timeout=TIMEOUT)) as response:
        if response.status_code == 200:
            # parse data
            bs = BeautifulSoup(response.text, features="lxml")
            children = bs.find_all("td")[4:]
            for i in range(0, len(children), 5):
                filename = children[i + 2].get_text().strip()
                print(filename)
                if filename == "listado.html":
                    # get files metadata
                    size = children[i + 4].get_text().strip()
                    size = get_bytes(size)
                    modificated_date = children[i + 3].get_text().strip()
                    modificated_date = datetime.fromisoformat(modificated_date)
                    return size, modificated_date
print(asd())          