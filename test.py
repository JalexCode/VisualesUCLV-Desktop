# import threading
# from contextlib import closing
# from datetime import datetime
# from queue import Queue
#
# from bs4 import BeautifulSoup
# import requests
#
# from util.const import *
# from util.util import *
#
#
# def asd(i):
#     with closing(requests.get("https://ecured.cu", verify=False, timeout=TIMEOUT)) as response:
#         if response.status_code == 200:
#             return f"{i}: OK"
#
# max_workers = 5
# q = Queue(max_workers)
#
# def worker():
#     while True:
#         item = q.get()
#         print(item)
#         q.task_done()
#
#
# threading.Thread(target=worker, daemon=True).start()
#
# for item in range(max_workers):
#     q.put(asd(item))
#
# q.join()
# print("OK ALL")
# import requests
#
# url1 = "http://ftp.uo.edu.cu/Windows/Diccionarios/El%20Manual%20de%20Estilo%20Editorial%2C%20el%20Original%20para%20Edicion%20%28199/El%20Manual%20de%20Estilo%20Editorial%2C%20el%20Original%20para%20Edicion%20%281999%29.pdf"
# r = requests.get(url1, verify=False)
# print(r.headers)

a = """application/vnd.oasis.opendocument.text
application/vnd.oasis.opendocument.spreadsheet
application/vnd.oasis.opendocument.presentation
application/vnd.oasis.opendocument.graphics
application/vnd.ms-excel
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
application/vnd.ms-powerpoint
application/vnd.openxmlformats-officedocument.presentationml.presentation
application/msword
application/vnd.openxmlformats-officedocument.wordprocessingml.document
application/vnd.mozilla.xul+xml"""
print("\"" + "\", \"".join(a.split("\n")) + "\"")