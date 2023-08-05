#!/usr/bin/python
import ast
import os

class PREFS(object):
    """docstring for PREFS"""
    def __init__(self, prefs, filename = "prefs", separator = "=", ender = "\n", interpret = False, dictionary = False):
        super(PREFS, self).__init__()
        self.prefs = prefs
        self.filename = filename
        self.separator = separator
        self.ender = ender
        self.interpret = interpret
        self.dictionary = dictionary

        self.ReadPrefs()
        
    def ReadPrefs(self):
        try:
            prefsTXT = open(f"{self.filename}.txt", "r")
            
            content = {}
            lines = prefsTXT.readlines()
            lines1 = []


            if not self.dictionary:
                if len(lines) > 1:
                    e = 0
                    for line in lines:
                        lines1.append(line.replace(self.ender, ""))

                        if not self.interpret:
                            content[lines1[e].split(self.separator, 1)[0]] = lines1[e].split(self.separator, 1)[1]
                        elif self.interpret:
                            content[ lines1[e].split(self.separator, 1)[0] ] = ast.literal_eval( lines1[e].split(self.separator, 1)[1] )

                        e += 1

                elif len(lines) == 1:
                    content = self.ReadOneLine(lines)


            elif self.dictionary:
                content = ast.literal_eval(lines[0])

            prefsTXT.close()
            return content

        except FileNotFoundError:
            try:
                self.CreatePrefs(self.prefs())
            except TypeError:
                self.CreatePrefs(self.prefs)

    def ReadOneLine(self, lines):
        result = {}        

        line = lines[0].split(self.ender)
        line.pop()
        for i in line:
            if not self.interpret:
                result[i.split(self.separator, 1)[0]] = i.split(self.separator, 1)[1]
            elif self.interpret:
                result[i.split(self.separator, 1)[0]] = ast.literal_eval(i.split(self.separator, 1)[1])        

        return result

    def CreatePrefs(self, prefs):
        try:
            prefsTXT = open(f"{self.filename}.txt","w+")
        except FileNotFoundError:
            os.mkdir(self.filename.split("/")[0])
            prefsTXT = open(f"{self.filename}.txt","w+")

        if not self.dictionary:
            for i in prefs.items():

                if isinstance(i[1], str) and self.interpret: prefsTXT.write(f"{i[0]}=\"{i[1]}\"{self.ender}")
                else: prefsTXT.write(f"{i[0]}={i[1]}{self.ender}")

        elif self.dictionary:
            prefsTXT.write(str(prefs))

        prefsTXT.close()

        self.ReadPrefs()

    def WritePrefs(self, pref, value):
        content = self.ReadPrefs()
        content[pref] = value

        if not self.dictionary:
            text = ""
            for item in content.items():
                text += f"{item[0]}{self.separator}{item[1]}{self.ender}"

        elif self.dictionary:
            text = str(content)

        prefsTXT = open(f"{self.filename}.txt","w+")
        prefsTXT.write(text)
        prefsTXT.close()

        self.ReadPrefs()

    def ReWritePrefs(self, prefs = None):
        if os.path.exists(f"{self.filename}.txt"):
            os.remove(f"{self.filename}.txt")
            if not self.dictionary:
                try:
                    self.CreatePrefs(prefs)
                except AttributeError:
                    self.CreatePrefs(self.prefs)
            
            elif self.dictionary:
                if not isinstance(prefs, dict):
                    self.CreatePrefs(self.prefs)
                if isinstance(prefs, dict):
                    self.CreatePrefs(prefs)

        self.ReadPrefs()
            
    def ChangeFilename(self, filename):
        self.filename = filename

        self.ReadPrefs()

    def DeleteFile(self):
        if os.path.exists(f"{self.filename}.txt"):
            os.remove(f"{self.filename}.txt")