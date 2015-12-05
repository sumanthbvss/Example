import os
import re
from html.parser import HTMLParser

i=0
class MyHTMLParser(HTMLParser):
    def __init__(self):
       HTMLParser.__init__(self)
       self.recording = 0
       self.isp = 0
       self.israting = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.recording = 1
        if tag == 'a':
            for key, value in attrs:
                if key == 'class':
                    if value == 'movie-link' or value == 'movie-body-text-bold':
                        self.isp = 1
        if tag == 'span':
            for key, value in attrs:
                if key == 'class':
                    if value == 'movie-body-text':
                        self.israting = 1
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.recording -= 1
        if tag == 'a':
            self.isp = 0;
        if tag == 'span':
            self.israting = 0
    def handle_data(self, data):
        if self.recording:
            file = open("newfile%s.csv" %i, "a", encoding='utf-8')
            result = re.sub(",", ";", str(data))
            file.write(result+',')
            file.close()
        if self.isp:
            if not str(data).startswith('Average') and not "FRESH" in str(data) and not "ROTTEN" in str(data) and not "Number of Reviews" in str(data) and not "Click to read the article" in str(data) and not "review]" in str(data):
                file = open("newfile%s.csv" %i, "a", encoding='utf-8')
                file.write(str(data)+',')
                file.close()
        if self.israting:
            #if str(data).startswith('Average'):
            result = re.sub("<.*?>", "", str(data))
            result = re.sub("\n\t\r", "", str(data))
            result = result.strip()
            print (result)
            #if not result.startswith('Reviews') and not result.startswith('Fresh') and not result.startswith('Rotten'):
            if "/10" in result:
                file = open("newfile%s.csv" %i, "a", encoding='utf-8')
                file.write(result+',')
                file.close()
            
        #with open("newfile%s.txt" %i, 'rb+') as filehandle:
         #   filehandle.seek(-1, os.SEEK_END)
          #  filehandle.truncate()

            
        #if self.isp:
         #   file = open("newfile%s.txt" %i, "a")
          #  input = str(data)
           # client = Algorithmia.client('sim0Msfwf+ITgS1ZUBm6dB5X5dw1')
            #algo = client.algo('nlp/SentimentAnalysis/0.1.1')
            #file.write(str(algo.pipe(input))+'\n')
            #file.close()
            
#os.path.dirname(os.path.realpath(__file__))
for files in os.listdir(os.getcwd()):
    if files.endswith(".html"):
        file = open("html_list.txt", "a")
        file.write("%s\n" % files)
        file.close()
f = open('html_list.txt')
for line in iter(f):
    print(line)
    line = line.strip('\n')
    f1=open(line,"r")
    s=f1.read()
    parser = MyHTMLParser()
    parser.feed(s)
    i+=1
f.close()
