import re
import time
import math
import roman


def jumpLines(f, numOfLines):
    line = f.readline()
    while (numOfLines > 1 and line != ''):
        line = f.readline()
        numOfLines -= 1


def jumpToLineWithString(f, str):
    line = f.readline()
    while line.find(str) < 0 and line != '':
        line = f.readline()


movieRegEx = '((\s+\(([0-9\/IVXC\?]*)\)){0,1}(\s+\((TV|V)\))*(\s+\{([^\{\}]+)\})*(\s+\{\{([^\{\}]+)\}\})*(\s+\(([^\(\)]+)\)){0,1}(\s+\(([^\(\)]+)\)){0,1}(\s+\[([^\[\]]+)\])*(\s+\<([^\<\>]+)\>)*)$'


def wrapRegEx(l, r):
    return '\s+' + l + '([^' + r + l + ']*)' + r + '$'


def getFromEnd(l, r, str):
    # print wrapRegEx(l, r)
    ret = re.search(wrapRegEx(l, r), str)
    return None if ret == None else ret.groups()[0]


def removeFromEnd(l, r, str):
    return re.sub(wrapRegEx(l, r), '', str)


"""
def getMovie(str):
    debug = False
    if debug: print("Starting String: " + str)
    movie = {}

    movie['billingPosition'] = getFromEnd('\<', '\>', str)
    str = removeFromEnd('\<', '\>', str)
    if debug: print('remove <: ' + str)

    movie['roles'] = getFromEnd('\[', '\]', str)
    str = removeFromEnd('\[', '\]', str)
    if debug: print('remove [: ' + str + '?')

    movie['creditsName'] = getFromEnd('\(as', '\)', str)
    str = removeFromEnd('\(as', '\)', str)
    if debug: print('remove (as: ' + str + '?')

    movie['episodeName'] = getFromEnd('\{', '\}', str)
    str = removeFromEnd('\{', '\}', str)
    if debug: print('remove {: ' + str + '?')

    str = re.sub('\s+\{[^\}]*\}\}$', '', str)
    if debug: print('remove {{: ' + str + '?')

    str = re.sub('\s+\(([TV]*)\)$', '', str)
    if debug: print('remove {{: ' + str + '?')
    return dict(movie.items() + getMovieSplit(str).items())
"""


def getMovie(str):
    debug = False
    if debug: print("Starting String: " + str)
    movie = {}
    reg = re.search(movieRegEx, str)
    groups = (reg.groups())
    # print groups[2],groups[4],groups[6],groups[8],groups[10],groups[12]

    movie['billingPosition'] = groups[16]
    movie['roles'] = groups[14]
    movie['creditsName'] = groups[12]
    movie['comments'] = groups[10]
    movie['suspended'] = groups[8]
    movie['episodeName'] = groups[6]
    movie['tv'] = groups[4]

    # print(movie)
    # str = re.sub(movieRegEx, '', str)

    return dict(movie.items() + getMovieSplit(str).items())


def getMovieSplit(str, p=False):
    # print(str)
    str = str.split()
    movieName = []
    movieName.append(str[0])
    k = 1
    while k < len(str) and re.match('\(([0-9]{4}|[\?]{4})+(\/[IVXC]*)*\)', str[k]) == None:
        movieName.append(str[k])
        k += 1
    ret = {'name': ' '.join(movieName).replace('"', ''), 'year_id': None,
           'year': None}
    year_id = str[k].replace('(', '').replace(')', '')
    if year_id == '????':
        year_id = None
    if year_id is not None:
        yearSplit = year_id.split('/')
        ret['year'] = yearSplit[0]
        if ret['year'] is None or not ret['year'].isdigit():
            ret['year'] = None
        if p: print  yearSplit;
        if len(yearSplit) > 1:
            if yearSplit[-1] == '????':
                ret['year_id'] = None
            elif yearSplit[-1].isdigit():
                ret['year_id'] = yearSplit[-1]
            else:
                ret['year_id'] = roman.fromRoman(yearSplit[-1])
    return ret


actorRegEx = '([^,]*),?\s?([^\(]*).?\(?([^\(\)]*)'


def getActor(actor):
    tmpactor = actor
    name_id = re.search('\([IVXC]*\)', actor)
    if name_id is not None and len(name_id.group()):
        name_id = name_id.group()
    else:
        name_id = None
    if name_id is not None:
        actor = actor.replace(name_id,'')
    actor= actor.strip().split(', ')

    # reg = re.search(actorRegEx, actor)
    # groups = reg.groups()
    # print groups
    ret = {}
    ret['lname'] = actor[0]
    ret['fname'] = actor[1] if len(actor)>1 else None
    ret['name_id'] = name_id
    if (ret['name_id'] is not None):
        ret['name_id'] = roman.fromRoman(ret['name_id'].strip('()').upper())
    # print(tmpactor)
    # print(ret)
    return ret


timers = {}


def startTimer(name):
    timers[name] = time.time()
    print '---Starting "' + name + '"'


def checkTimer(name):
    print '---Checking "' + name + '" :' + readableTime(time.time() - timers[name])


def analyzedTime(time):
    t = {}
    t['hours'] = int(math.floor(time / 3600))
    time %= 3600
    t['minutes'] = int(math.floor(time / 60))
    time %= 60
    t['seconds'] = int(math.floor(time))
    time = time - t['seconds']
    t['milliseconds'] = int(time * 1000)
    return t


def readableTime(rTime):
    t = analyzedTime(rTime)
    ret = str(t['hours']) + ' Hours, '
    ret += str(t['minutes']) + ' Minutes, '
    ret += str(t['seconds']) + ' Seconds and '
    ret += str(t['milliseconds']) + ' Milliseconds '
    return ret


def resetTable(cur, table):
    cur.execute("TRUNCATE " + table + " CASCADE;")
    cur.execute("ALTER SEQUENCE " + table + "_id_seq RESTART WITH 1;")


def beep(num=1):
    for i in range(0, num):
        print "\a"


''' Used to read Actors from File that was created for SQL use '''
def getTop100Actors():
    actorsFile = open('../assets/TOP1000Actors.txt')
    actors = actorsFile.readline().decode("utf-8-sig").encode("utf-8").strip('()').split('),(')
    return [actor.strip("'") for actor in actors]

def readFileLine(f):
    return f.readline().decode('iso-8859-1').encode('utf8')