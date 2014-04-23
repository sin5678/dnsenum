__author__ = 'sincoder@vip.qq.com'

import sys
import threading
import socket
import itertools

threadList = []
lock = threading.Lock()


class CheckThread(threading.Thread):
    __host = ''

    def __init__(self, host):
        threading.Thread.__init__(self)
        self.__host = host

    def run(self):
        global lock
        try:
            lock.acquire()
            sys.stdout.write('%-30.30s\r' % self.__host)
            lock.release()
            ip = self.__host + ' ' + socket.gethostbyname(self.__host)
            lock.acquire()
            sys.stdout.write('\r')
            sys.stdout.write('%-30s\n' % ip)
            lock.release()
        except socket.error:
            pass


def main():
    global threadList
    wordfile = None
    if len(sys.argv) < 3:
        print 'Usage: dnsenum [domain name] [thread count] <word file>'
        exit()
    domain = sys.argv[1]
    MaxThraed = int(sys.argv[2])
    if len(sys.argv) == 4:
        wordfile = sys.argv[3]
    threadList = [0] * MaxThraed
    wordlist = ['']
    if wordfile is not None:
        try:
            wordlist = file_get_contents(wordfile).replace('\r', '').split('\n');
        except IOError:
            print 'error open file'
            exit()
        wordlist = filter(None, wordlist) #remove emptry string
        wordlist = list(set(wordlist)) #remove dup string
        for w in wordlist:
            t = CheckThread(w + '.' + domain)
            t.start()
            while not put_into_thread_list(t):
                continue
    else:
        #brute force
        word_len = 1
        while word_len <= 4:
            for i in itertools.permutations('abcdefghijklmnopqrstuvwxyz', word_len):
                name = ''.join(i)
                name = name + '.' + domain
                t = CheckThread(name)
                t.start()
                while not put_into_thread_list(t):
                    continue
            word_len += 1

    for x in threadList:
        if x != 0:
            x.join()
    sys.stdout.write('\r')
    print 'Check Over                           '


def put_into_thread_list(t):
    global threadList
    for n, x in enumerate(threadList):
        if x == 0:
            threadList[n] = t
            return True
    for n, x in enumerate(threadList):
        if not x.isAlive():
            x.join()
            threadList[n] = 0
    return False


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


if __name__ == '__main__':
    main()
else:
    print 'am i a module ?'