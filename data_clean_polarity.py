import os
import re
import Algorithmia
from html.parser import HTMLParser
from os.path import expanduser, join

i=0
script_dir = os.path.dirname(os.path.abspath(__file__))
path_pos = os.path.join(script_dir, 'pos')
path_neg = os.path.join(script_dir, 'neg')
path_neu = os.path.join(script_dir, 'neu')

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
                    if value == 'movie-link':
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
            completeName = os.path.join(path_pos,"newfile%s.txt" %i)
            file = open(completeName, "a")
            result = re.sub(",", ";", str(data))
            file.write(result+'\n')
            file.close()
            completeName1 = os.path.join(path_neg,"newfile%s.txt" %i)
            file1 = open(completeName1, "a")
            result1 = re.sub(",", ";", str(data))
            file1.write(result1+'\n')
            file1.close()
            completeName2 = os.path.join(path_neu,"newfile%s.txt" %i)
            file2 = open(completeName2, "a")
            result2 = re.sub(",", ";", str(data))
            file2.write(result2+'\n')
            file2.close()
        if self.isp:
            if not str(data).startswith('Average') and not "Number of Reviews" in str(data):
                input = str(data)
                re.sub(r'[^\x00-\x7F]+','', input)
                if input != None and type(input) == type(u"") and input.find(u'\u2019') >= 0 : input = input.replace(u'\u2019', '\'')
                if input != None and type(input) == type(u"") and input.find(u'\u201c') >= 0 : input = input.replace(u'\u201c', '\"')
                if input != None and type(input) == type(u"") and input.find(u'\u2026') >= 0 : input = input.replace(u'\u2026', '\...')
                if input != None and type(input) == type(u"") and input.find(u'\u2013') >= 0 : input = input.replace(u'\u2013', '\-')
                if input != None and type(input) == type(u"") and input.find(u'\u2018') >= 0 : input = input.replace(u'\u2018', '\'')
                if input != None and type(input) == type(u"") and input.find(u'\u2011') >= 0 : input = input.replace(u'\u2011', '\-')
                if input != None and type(input) == type(u"") and input.find(u'\u2014') >= 0 : input = input.replace(u'\u2014', '\-')
                if input != None and type(input) == type(u"") and input.find(u'\u201d') >= 0 : input = input.replace(u'\u201d', '\"')
                client = Algorithmia.client('sim0Msfwf+ITgS1ZUBm6dB5X5dw1')
                algo = client.algo('nlp/SentimentAnalysis/0.1.1')
                polarity = str(algo.pipe(input))
                if polarity == '1':
                    completeName = os.path.join(path_neg,"newfile%s.txt" %i)
                    file = open(completeName, "a")
                    file.write(input + '\n')
                    file.close()
                if polarity == '2':
                    completeName = os.path.join(path_neu,"newfile%s.txt" %i)
                    file = open(completeName, "a")
                    file.write(input + '\n')
                    file.close()
                if polarity == '3':
                    completeName = os.path.join(path_pos,"newfile%s.txt" %i)
                    file = open(completeName, "a")
                    file.write(input + '\n')
                    file.close()
        if self.israting:
            #if str(data).startswith('Average'):
            result = re.sub("<.*?>", "", str(data))
            result = re.sub("\n\t\r", "", str(data))
            result = result.strip()
            print (result)
            #if not result.startswith('Reviews') and not result.startswith('Fresh') and not result.startswith('Rotten'):
            if "/10" in result:
                completeName = os.path.join(path_pos,"newfile%s.txt" %i)
                file = open(completeName, "a")
                file.write(result+',')
                file.close()
                completeName1 = os.path.join(path_neg,"newfile%s.txt" %i)
                file1 = open(completeName1, "a")
                file1.write(result+',')
                file1.close()
                completeName2 = os.path.join(path_neu,"newfile%s.txt" %i)
                file2 = open(completeName2, "a")
                file2.write(result+',')
                file2.close()
            
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
