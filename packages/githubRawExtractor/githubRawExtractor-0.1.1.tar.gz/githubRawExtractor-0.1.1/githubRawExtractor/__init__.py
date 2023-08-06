import requests


class Extractor:
    def __init__(self, githubrawlink):
        self.githubrawlink = githubrawlink
        self.content = requests.get(self.githubrawlink).text

    def extract(self):
        return self.content

    def save(self, filelocation):
        f = open(filelocation, "w")
        f.write(self.content)

    def execute(self):
        exec(self.content)