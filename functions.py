import re
import time
import math
import sys

from multiprocessing import Process
from psycopg2._psycopg import OperationalError, ProgrammingError, InternalError

import roman


def jump_lines(f, num_of_lines):
    line = f.readline()
    while num_of_lines > 1 and line != '':
        line = f.readline()
        num_of_lines -= 1


def jump_to_line_with_string(f, string):
    line = f.readline()
    while line.find(string) < 0 and line != '':
        line = f.readline()


movieRegEx = '((\s+\(([0-9\/IVXC\?]*)\)){0,1}(\s+\((TV|V)\))*(\s+\{([^\{\}]+)\})*(\s+\{\{([^\{\}]+)\}\})*(\s+\(([^\(\)]+)\)){0,1}(\s+\(([^\(\)]+)\)){0,1}(\s+\[([^\[\]]+)\])*(\s+\<([^\<\>]+)\>)*)$'


def wrap_regex(l, r):
    return '\s+' + l + '([^' + r + l + ']*)' + r + '$'


def get_from_end(l, r, string):
    # print wrapRegEx(l, r)
    ret = re.search(wrap_regex(l, r), string)
    return None if ret is None else ret.groups()[0]


def remove_from_end(l, r, string):
    return re.sub(wrap_regex(l, r), '', string)


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


def get_movie(string):
    debug = False
    if debug:
        print("Starting String: " + string)
    movie = {}
    reg = re.search(movieRegEx, string)
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
    movie.update(get_movie_split(string).items())
    return movie


def get_movie_split(string, p=False):
    # print(str)
    string = string.split()
    movieName = [string[0]]
    k = 1
    while k < len(string) and re.match('\(([0-9]{4}|[\?]{4})+(\/[IVXC]*)*\)', string[k]) is None:
        movieName.append(string[k])
        k += 1
    ret = {'name': ' '.join(movieName).replace('"', ''), 'year_id': None,
           'year': None}
    try:
        year_id = string[k].replace('(', '').replace(')', '')
    except IndexError:
        year_id = None
        print('String:', string, 'k', k)
    if year_id == '????':
        year_id = None
    if year_id is not None:
        yearSplit = year_id.split('/')
        ret['year'] = yearSplit[0]
        if ret['year'] is None or not ret['year'].isdigit():
            ret['year'] = None
        if p:
            print(yearSplit)
        if len(yearSplit) > 1:
            if yearSplit[-1] == '????':
                ret['year_id'] = None
            elif yearSplit[-1].isdigit():
                ret['year_id'] = yearSplit[-1]
            else:
                ret['year_id'] = roman.fromRoman(yearSplit[-1])
    return ret


actorRegEx = '([^,]*),?\s?([^\(]*).?\(?([^\(\)]*)'


def get_actor(actor):
    tmpactor = actor
    name_id = re.search('\([IVXC]*\)', actor)
    if name_id is not None and len(name_id.group()):
        name_id = name_id.group()
    else:
        name_id = None
    if name_id is not None:
        actor = actor.replace(name_id, '')
    actor = actor.strip().split(', ')

    # reg = re.search(actorRegEx, actor)
    # groups = reg.groups()
    # print groups
    ret = {}
    ret['lname'] = actor[0]
    ret['fname'] = actor[1] if len(actor) > 1 else None
    ret['name_id'] = name_id
    if ret['name_id'] is not None:
        ret['name_id'] = roman.fromRoman(ret['name_id'].strip('()').upper())
    # print(tmpactor)
    # print(ret)
    return ret


timers = {}


def start_timer(name):
    timers[name] = time.time()
    print('---Starting "' + name + '"')


def check_timer(name):
    print('---Checking "' + name + '" :' + readable_time(time.time() - timers[name]))


def analyzed_time(time):
    t = {}
    t['hours'] = int(math.floor(time / 3600))
    time %= 3600
    t['minutes'] = int(math.floor(time / 60))
    time %= 60
    t['seconds'] = int(math.floor(time))
    time = time - t['seconds']
    t['milliseconds'] = int(time * 1000)
    return t


def readable_time(r_time):
    t = analyzed_time(r_time)
    ret = str(t['hours']) + ' Hours, '
    ret += str(t['minutes']) + ' Minutes, '
    ret += str(t['seconds']) + ' Seconds and '
    ret += str(t['milliseconds']) + ' Milliseconds '
    return ret


def reset_table(cur, table):
    cur.execute("TRUNCATE " + table + " CASCADE;")
    cur.execute("ALTER SEQUENCE " + table + "_id_seq RESTART WITH 1;")


def beep(num=1):
    for i in range(0, num):
        print("\a")


''' Used to read Actors from File that was created for SQL use '''


def get_top100_actors():
    actorsFile = open('../assets/TOP1000Actors.txt')
    actors = actorsFile.readline().decode("utf-8-sig").encode("utf-8").strip('()').split('),(')
    return [actor.strip("'") for actor in actors]


def read_file_line(f):
    try:
        return f.readline()  # .decode('ISO 8859-1').encode('utf8')
    except:
        print(print(sys.exc_info()))
        print("NTI ZNTO MPOUTZO")
        return []


def executeScriptsFromFile(filename, cur):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cur.execute(command)
        except OperationalError as e:
            print("Command skipped: ", str(e), command)
        except ProgrammingError as e:
            if command and command.replace('\n', '') != '':
                print("Command skipped: ", str(e), command)
        # except InternalError as e:
        #     print("Command skipped: ", str(e))


def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()
