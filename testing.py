'''This program is to created to find the peak of a signal.
It is also uesd as a practice exercise for learning the Python.'''
#print
"""print substrings
ex: print('Hello'[0:3]), outputs, Hel
print number
ex: print(2), outputs: 2
\n a new line
print out the raw text, just like what you actual see in the quote
ex; print(r'quote\n'), outputs: quote\n
"""
#variables & data types
"""semi colon ; is not needed.
List: it is like a one dimension array.
ex: myList=[1,2,3,'Hello']
Dictionary: it is like a multi dimension array.
ex; myDict={'a':1, 'b':2, 'c':3}
use type() can define the type of the data in ()
ex; print(type(myStr), myStr), outputs: <class 'str'> Hello
print(myList[3]), outputs: Hello
print(myDict['a'], outputs:1
add string
ex: print(myStr, 'World') or greeting = myStr + 'World', print(greeting)
outputs: Hello World
"""
#conditional
"""if condition:
    statement
    elsif condition:
    statement
    else
    statement
if there is multiple conditions, then add add or.
"""
#loops
"""people = ['j','2','3']
for person in people:
    print('Current Person: ', person)
outputs: current person: j
         current person: 2
         current person: 3
seq index
for i in range(len(people)):
    print('Current Person: ', people[i])
output: same
for i in range(0,10):
    print(i)
outputs: 0-9

while condition:
    statement
    if condition:
    break    
"""
#function
"""def voidfunction(arguments):
    statement
def intfunction(arguments):
    statement
    return parameter

!!!important:
num=5 (outside of the funtion, it is immutable)
addOnetoNum(num)
print('value outside the function', num)
outputs:inside function: 6  !!!only the variable inside fo the nction will change
        outside function: 5 !!!only the variable outside of the function will maintain the same
LIST and Dictionary will change still
myList.append(4): append will add 4 to the list.
"""
#string function
"""string.capitalize(): it capitalize the first letter of the first word, other chars change to lowercase
    string.swapcase(), will change the cap to low, low to the cap.
    len(string): returns a integer which indicates the length of the string
    string.replace("string1',"string2)): replace the string 1 with string 2
    string.count(variable)): count the number from 1 in the
    string.startswith(string): if this string is inside of string, then true
    string.endswith(string): end with
    string.split(): will split the string of the list
    string.find(char): if it found char in the string, it will return back its number, count from 1
    string index(char) is same as find, but if it can't find it, it will return error
    string.isalnum(): true if all alphanum
    string.isalpha(): true if all alphabeetic
    string.isnumeric():true if all num
"""
#access separate files
"""import nameofmodule (files= module in python)
    nameofmodule.specificElement(arguement)
direct access to specificElement(argument)
from nameofmodule import NameofspecificElement
specificlement(argument)
"""
#I/O
"""open a file
objectname=open(nameoffile,mode)
get some info
objectname=open(nameoffile.'w'): to write the open file
objectname.name: returns the name of the open file
objectname.closed: returns true if open file is closed
objectname.close(): close the open file
objectname.mode: return mode
objectname.write(string):write the string to the open file
open to append
objectname=open(nameoffile,'a') add stuff to the open file
read from file
objectnae=open(nameoffile, 'r+')
objectname.read():retrieve the data from open file
create file: 'w+'
objectanme.write(string): this creates a file and name it.
"""
#create class & object
"""class nameofclass:
        __attribute1='' :__indicates it is a private variable
        __attribute2=''
        def set_attribute1(self,attribute1):
            self.__attribute1=attribute1
        def get_attribute1(attribute1):
            return self.attribute1
        def __init__(self, attributes)
            set all attributes
        def toString(self):
        return'{} can be contacted at {}'.format(self.attributes)
classobject=nameofclass()
classobject.set_attribute1
class inheritName(nameofclass):
    __specificAttribute=
    def __init__(self,attributes):
        self.__attributes=
        self.__specificAttribute=
        supper(c
"""