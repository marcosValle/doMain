import requests
from threading import Event, Thread, Lock

lock = Lock()

class TestStatus(Thread):
    def __init__(self, threadID, name, domainPool, outputFile, ready=None):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.domainPool = domainPool
        self.outputFile = outputFile
        self.cleanFile(outputFile)
        self.ready = ready

    def run(self):
        print ("Starting " + self.name)
        self.testTargets()
        print ("Exiting " + self.name)
        self.ready.set()

    def cleanFile(self, fpath):
        open(fpath, 'w').close()

    def fixSchema(self, domain):
        if 'http' not in domain:
            return 'http://'+domain

    def writeToFile(self, fpath, domain):
        lock.acquire()
        with open(fpath, 'a') as f:
            f.write(domain+'\n')
        lock.release()

    def testTargets(self):
        for domain in self.domainPool:
            domain = self.fixSchema(domain.replace('\n', ''))
            try:
                print("Testing: {}".format(domain))
                r = requests.get(domain)
                print(r.status_code)
                if r.status_code == 200:
                    self.writeToFile(self.outputFile, domain)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print(e)
