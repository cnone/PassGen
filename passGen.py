# Date: 08/01/2017
# Author: Ethical-H4CK3R
# Description: Generates possible passwords
#
#

import time
import shutil
import zipfile
import urllib2
import subprocess

# current version
__version__ = 0.32

class Update(object):
 def __init__(self):
  self.dir = '.update'
  self.zip = '.update.zip'
  self.repo = 'https://github.com/Ethical-H4CK3R/PassGen/archive/master.zip'
  self.script = 'https://raw.githubusercontent.com/Ethical-H4CK3R/PassGen/master/passGen.py'
  self.currentVersion = None

 def repoVersion(self):
  try:
   content = urllib2.urlopen(self.script).read()
   content = content.split()
   num = [content[n+2] for n,w in enumerate(content) if '__version__' in w if content[n+1] == '=']
   return eval(''.join(num))
  except:
   self.displayMsg('Check your internet connection & try again',-1)

 def installUpdate(self):
  try:
   # delete existing folder
   if shutil.os.path.exists(self.dir):
    shutil.rmtree(self.dir)
   src = urllib2.urlopen(self.repo).read()
   # download
   with open(self.zip,'w') as _zipfile:
    _zipfile.write(src)
   # unzip
   with zipfile.ZipFile(self.zip,'r') as _zipfile:
    shutil.os.mkdir(self.dir)
    _zipfile.extractall(self.dir)
   # copy files
   for fld in shutil.os.listdir(self.dir): # the zip folder
    for item in shutil.os.listdir('{}/{}'.format(self.dir,fld)): # the repo folder
     _item = '{}/{}/{}'.format(self.dir,fld,item)
     if shutil.os.path.isfile(_item):
      shutil.copyfile(_item,'./{}'.format(item))
     else:
      shutil.copytree(_item,'./{}'.format(item))
   # remove
   shutil.rmtree(self.dir)
   shutil.os.remove(self.zip)
   self.displayMsg('Restart program to install updates',1)
  except:
   self.displayMsg('Failed to update',-1)

 def update(self):
  print 'Searching for an update ...'
  newerVersion = self.repoVersion()
  time.sleep(1.5)
  if newerVersion > self.currentVersion:
   subprocess.call(['clear'])
   print 'New Version: {}'.format(newerVersion)
   print 'Current Version: {}\n'.format(self.currentVersion)
   if raw_input('Do you want to continue? [Y/n]: ')[0].lower() == 'y':
    self.installUpdate()
  else:
   if newerVersion:
    self.displayMsg('No updates found',0)

class Handler(object):
 def __init__(self):
  self.generator = Generator()
  self.vendors = ['TG1','DVW','DG8','U10','TC8']
  self.questions = {
            # target info
            'firstname':None,
            'middlename':None,
            'lastname':None,
            'nickname':None,
            # 'yearOfBirth':None,

            # child info
            'childFN':None,
            'childMN':None,
            'childLN':None,
            # 'childYOB':None,
            'childNN':None,

            # spouse info
            'spouseFN':None,
            'spouseMN':None,
            'spouseLN':None,
            # 'spouseYOB':None,
            'spouseNN':None,

            # pet info
            'petname':None,
            # 'petYOB':None,

            # numbers
            'ssn':None,
            'pin':None,
            'phone':None,

            # wifi info
            'essid':None,
            'bssid':None
           }

 def mklist(self):
  for q in self.questions:
   v = self.questions[q]
   n = q

   if v:
    # are we looking at a pin
    if n=='pin':
     self.generator.nums.append(v)
     self.generator.list.append(v)

    # are we looking at wifi info
    elif n == 'essid' or n == 'bssid':
      if n != 'essid':continue
      essid = v
      bssid = [key for key in self.questions if key == 'bssid']
      bssid = bssid[0] if bssid else bssid
      if not bssid:continue
      bssid = self.questions[bssid]

      # generate default password
      if len(essid)>3:
       if essid[:3] in self.vendors:
        passkey = self.generator.default(essid,bssid)
        if not passkey in self.generator.list:
         self.generator.list.append(passkey)

    # full name
    elif n == 'firstname':
     firstname,lastname = v,self.questions['lastname']
     self.generator.word.append(firstname)

     if lastname:
      self.generator.word.append('{}{}'.format(firstname,lastname.lower()))
      self.generator.word.append('{}{}'.format(firstname,lastname))

    elif n == 'spouseFN' or n == 'childFN':
     # love makes people weak
     self.generator.word.append(v)
     self.generator.word.append('ilove{}'.format(v))
     self.generator.word.append('love{}'.format(v))
     self.generator.word.append('iloveU{}'.format(v))
     self.generator.word.append('mylove{}'.format(v))
     self.generator.word.append('{}143'.format(v))

    # are we looking at basic info
    else:
     if v.isdigit():
      if any([n=='yearOfBirth',n=='spouseYOB',n=='childYOB','petYOB']):
       rev  = ''.join([n for n in reversed([n for n in v])])
       end  = v[-2:]

       # different formats of year
       if not v in self.generator.nums:
        self.generator.nums.append(v)
       if not rev in self.generator.nums:
        self.generator.nums.append(rev)
       if not end in self.generator.nums:
        self.generator.nums.append(end)

      else:
       if not v in self.generator.list:
        self.generator.list.append(v)
     else:
      if not v in self.generator.word:
       self.generator.word.append(v)

  # generate password list & reset
  self.generator.generate()
  self.reset()

 def fresh(self):
  # fresh start ?
  return False if [_  for _ in self.questions if self.questions[_]] else True

 def reset(self,item=None):
  del self.generator.list[:]
  del self.generator.word[:]
  for q in self.questions:
   self.questions[q] = None

class Generator(object):
 def __init__(self):
  self.name  = None
  self.list  = [] # holds numbers, don't mix with numbers or symbols
  self.word  = [] # holds words, mix with numbers and symbols
  self.file  = [] # the passwords to write
  self.nums  = range(10000)

 # def now(self):
 #  return time.strftime('%m-%d-%Y_%I:%M:%S',time.localtime())

 def cases(self,word):
  # firstname, Firstname
  return word.lower(),word.title()

 def numbers(self,word):
  self.file.append(word.lower())
  self.file.append(word.title())
  for num in self.nums:
   for case in self.cases(word):
    self.file.append('{}{}'.format(''.join(case),num))

 def default(self,essid,bssid):
  # default passkey on routers
  return '{}{}{}'.format(essid[:-2],''.join([k for i,k in enumerate(bssid)\
  if any([i==9,i==10,i==12,i==13])]),essid[-2:])

 def writefile(self):
  # self.name = 'wordlist-{}.lst'.format(self.now())
  with open(self.name,'w') as fwrite:
   for item in self.file:
    fwrite.write('{}\n'.format(item))

 def generate(self):
  print 'Generating ...'
  time.sleep(1.5)
  [self.file.append(_) for _ in self.list if _]
  [self.numbers(word) for word in self.word]
  if len(self.file):
   while 1:
    # try:
     subprocess.call(['clear'])
     self.name = raw_input('[-] Enter a name for the wordlist: ')
     # if not self.name.strip():return
     if shutil.os.path.exists(self.name):
      opt = raw_input('\n[!] {} already exists, override it? [Y/n]: '.\
      format(self.name))
      if opt:
       if opt.lower()[0] == 'y':break
     else:break
    # except:return
   self.writefile()

class PassGen(Handler,Update):
 def __init__(self):
  Update.__init__(self)
  Handler.__init__(self)
  self.currentVersion = __version__

  self.y = '\033[33m' # yellow
  self.g = '\033[32m' # green
  self.b = '\033[34m' # blue
  self.n = '\033[0m'  # null --> reset
  self.r = '\033[31m' # red

 def display(self):
  subprocess.call(['clear'])
  for n,q in enumerate(sorted(self.questions,key=len)):
   if not n:
    print '-------------------------------'
    print '||    Name     ||    Value   ||'
    print '-------------------------------'
   n,v = q.ljust(11),self.questions[q]
   v = '{}{}{}'.format(self.r,str(v).rjust(7),self.n) if not v else\
   '{}{}{}'.format(self.b,v.rjust(len(str(v))+3),self.n)
   print '|| {} || {}'.format(n,v)
  passwords = len(self.generator.file)
  if passwords:
   print '\nGenerated: {}\nSize: {}'.format(self.generator.name,passwords)

 def displayMsg(self,msg,level):
  # level = -1: red
  # level = 0: yellow
  # level = 1: green
  symbol = '!' if level == -1 else '-' if not level else '+'
  color = self.r if level == -1 else self.b if not level else self.g
  symbol = '{}{}{}'.format(color,symbol,self.n)
  enter = 'Press {}[{}Enter{}]{} To Continue'.format(self.g,self.n,self.g,self.n)
  art = '{}[{}{}]{}'.format(self.y,symbol,self.y,self.n)
  msg = '{} {}\n\n{}'.format(art,msg,enter)
  subprocess.call(['clear'])
  raw_input(msg)

 def _help(self):
  print 'Usage: {}fieldname {}={} value{}'.format(self.b,self.y,self.g,self.n)
  print '\n{}Do Not Use Any Symbols{}\n'.format(self.r,self.n)
  print 'exit             {}to exit{}'.format(self.b,self.n)
  print 'help             {}display help{}'.format(self.b,self.n)
  print 'reset            {}clear fields{}'.format(self.b,self.n)
  print 'update           {}check for update{}'.format(self.b,self.n)
  print 'generate         {}generate password list{}'.format(self.b,self.n)
  print 'current version  {}{}{}'.format(self.g,__version__,self.n)
  raw_input('\nPress {}[{}Enter{}]{} To Continue'.format(self.g,self.n,self.g,self.n))

 def run(self):
  while 1:
   self.display()
   if not self.generator.file:
    print '\ntype {}help{} for help'.format(self.y,self.n) if self.fresh() else ''
   if self.generator.file:
    del self.generator.file[:]
   cmd = raw_input('\n> {}'.format(self.b))
   subprocess.call(['clear'])
   print self.n

   # check for assignments
   if '=' in cmd:
    try:
     name = cmd.split()[0].lower().strip().replace('\n','')
     value = cmd.split()[2].lower().strip().replace('\n','')
    except:continue
    key = [_ for _ in self.questions if _.lower() == name.lower()]
    if not key:continue
    key = key[0]
    if key != 'bssid' and key != 'essid':
     self.questions[key] = str(value).title()
    else:
     self.questions[key] = str(value).upper()

   else:
    # check for key words, such as help, reset, and generate
    cmd = cmd.lower()
    [self._help() if cmd=='help' else self.reset() if cmd=='reset' else \
     self.mklist() if cmd=='generate' else exit() if cmd=='exit' else\
     self.update() if cmd=='update' else None]

if __name__ == '__main__':
 try:PassGen().run()
 except KeyboardInterrupt:exit('\n')
