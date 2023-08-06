from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import random
import os

class fbot:
    def __init__(self,name):
        self.name = name
        self.training_data = [{},{}]
    def train(self):
        try:
            while True:
                que = input('Whats the question : ')
                type = input('Whats the type(like greeting or goodbye etc.) of that question : ')
                ans = input('Whats should be the answers of that question : ')
                os.system('clear')
                if type in self.training_data[0]:
                    self.training_data[0][type].append(que)
                else:
                    self.training_data[0][type] = [que]
                if type in self.training_data[1]:
                    self.training_data[1][type].append(ans)
                else:
                    self.training_data[1][type] = [ans]
        except KeyboardInterrupt:
            os.system('clear')
            return self.training_data
    def trained_data(self,trained_data):
        self.patterns = trained_data[0]
        self.answers = trained_data[1]
    def start(self,inp_msg):
        try:
            patterns = self.patterns
            answers  = self.answers
            while True:
                x = []
                ch = []
                c = []
                b = 0
                for i in patterns:
                    ch.append(i)
                msg = input(inp_msg)
                for i in patterns:
                    x2 = []
                    for j in patterns[i]:
                        x2.append(fuzz.partial_ratio(msg,j))
                    x.append(x2)
                for i in x:
                    c.append(max(i))
                for i in range(len(c)):
                    if c[i] > c[b]:
                        b = i
                #print('Your msg type is :- ',ch[b])
                print(f'\n{self.name}',random.choice(answers[ch[b]]),'\n')
        except:
            print('You have to provide the trained data to start the bot.\nYou can provide it at cbot().trained_data(patterns,answers)')
