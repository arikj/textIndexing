import sys
import collections
import string
import binarysearchtree
import math
from preprocessing_2 import *
numDoc = 500
cache = {}


class CharNode(binarysearchtree.Node):
    def __init__(self, character, frequency, left_child=None, right_child=None):
        self.character = character
        self.frequency = frequency
        self.left_child = left_child
        self.right_child = right_child
 
    @property
    def _cmp_key(self):
        return self.frequency


def pad(bits):
    for x in xrange(len(bits),8):
        bits += '0'
    return bits
def convertToChar(bits):
    result = ''
    x = int(len(bits))/8
    for j in range(0,x):
        ascii = 0
        for i in range(0,8):
            ascii += ((int)(bits[i+j*8])*(2**(7-i)))
        result += str(chr(ascii))
    #print "ascii = " + str(ascii)
    return result
def trim(bits):
    x = len(bits)/8
    return bits[8*x:]
def convertToBinary(ascii):
    bitstring = ''
    bitstring = '{0:08b}'.format(ascii)
    #print bitstring
    return bitstring
def read(x):
    filer = "write/set1/write"+str(x)+".bin"
    filew = "check/read"+str(x)+".txt"
    fpw = open(filer,"w")
    fpw.write("")
    fpw.close()
    fpw = open(filew,"a")
    fpr = open(filer,"rb")
    buff = fpr.read(1)
    bitstring = ''
    while buff!='':
        ascii = ord(buff)
        bitstring += convertToBinary(ascii)
        buff = fpr.read(1)
    fpr.close()
    fpw.write(bitstring)
    return bitstring
    fpw.close()
    #print "string for file " + str(x) + "= "+bitstring
def writeToBin(huffman_tree):
    preProcess = preprocessing()
    for x in range(0,numDoc):
        filer = "documents/set1/doc"+str(x)+".txt"
        filew = "write/set1/write"+str(x)+".bin"
        print "writing to "+ filew
        #fdbug = "write/set1/write"+str(x)+".txt"
        #fpd = open(fdbug,'w')
        #fpd.write("")
        #fpd.close()
        fpw = open(filew,'w')
        fpw.write("")
        fpw.close()
        fpw = open(filew,'a')
        #fpd = open(fdbug,'a')
        fpr=open(filer,'r')
        content = fpr.read()
        content = preProcess.processText(content)
        code = ""
        for character in content:
            if character in cache:
                #fpw.write(cache[character])
                code += cache[character]
                #fpd.write(cache[character])
                if(len(code) >= 8):
                    #print "in len code"
                    c = convertToChar(code)
                    #print c
                    code = trim(code)
                    fpw.write(c)
                continue
            node = huffman_tree
            bitstring = ''
            while node.character != character:
                #print "i m in"
                if node.left_child:
                    if character in node.left_child.character:
                        node = node.left_child
                        bitstring += '0'
                        continue
                if node.right_child:
                    node = node.right_child
                    bitstring += '1'
                if not (node.left_child) and not (node.right_child):
                    break
            code += bitstring
            #fpd.write(bitstring)
            cache[character] = bitstring
            if(len(code) >= 8):
                #print "in len code 1"
                c = convertToChar(code)
                #print c
                fpw.write(c)
                code = trim(code)
        if(len(code) > 0):
            #print code
            code = pad(code)
            #print code
            c = convertToChar(code)
            fpw.write(c)
        fpw.close()
        #fpd.close()
        fpr.close()
def encodeString(content,table):
    bitstring = ''
    c =''
    debug =''
    for character in content:
        if(character in table):
            bitstring += table[character]
            debug += table[character]
            # print bitstring
            if(len(bitstring) >= 8):
                # print "inside"
                c +=  convertToChar(bitstring)
                bitstring = trim(bitstring)
                # print bitstring
    padding = 0
    if(len(bitstring) > 0):
            padding = 8-len(bitstring)
            bitstring = pad(bitstring)
            #print code
            c += convertToChar(bitstring)
    # print content
    # print table
    # print debug
    return c,padding


def encodes(filer):
    l = 0
    preProcess = preprocessing()
    nodes = {}
    print "reading from " + filer
    fp=open(filer,'r')
    content = fp.read()
    print "preprocessing called"
    content1 = preProcess.processText(content)
    print "preprocessing ended"
    l += len(content1)
    #print l
    for character in content1:
        if not character in nodes:
            #print "character " + character + "added"
            nodes[character] = CharNode(character, 0)
        nodes[character].frequency += 1.0
    fp.close()
    for character in nodes:
        nodes[character].frequency /= l
 
    frequency_map = []
    for character, node in nodes.items():
        frequency_map.append((node.frequency, node))
 
    sorted_nodes = sorted(frequency_map, key=lambda item: item[1].frequency, reverse=True)
    while len(sorted_nodes) > 1:
        x_frequency, x = sorted_nodes.pop()
        y_frequency, y = sorted_nodes.pop()
 
        merged_frequency = x_frequency + y_frequency
        merged_node = CharNode(x.character + y.character, merged_frequency)
        #print 'New Node "{0}" with frequency {1}'.format(repr(merged_node.character), merged_node.frequency)
        if x.frequency > y.frequency:
            merged_node.right_child = x
            merged_node.left_child = y
        else:
            merged_node.right_child = y
            merged_node.left_child = x
 
        sorted_nodes.append((merged_frequency, merged_node))
        sorted_nodes = sorted(sorted_nodes, key=lambda item: item[0], reverse=True)
 
    huffman_tree = sorted_nodes.pop()[1]
    table = {}
    for character in content1:
        if character in table:
            continue
        node = huffman_tree
        bitstring = ''
        while node.character != character:
            if character in node.left_child.character:
                node = node.left_child
                bitstring += '0'
                continue
            node = node.right_child
            bitstring += '1'
        table[character] = bitstring
    return table

def write(huffman_tree):
    for x in range(0, numDoc):
        filer = "documents/set1/doc"+str(x)+".txt"
        filew = "write/set1/write"+str(x)+".txt"
        fpr=open(filer,'r')
        fpw = open(filew,'a')
        content = fpr.read()
        for character in content:
            if character in cache:
                fpw.write(cache[character])
                continue
            node = huffman_tree
            bitstring = ''
            while node.character != character:
                if character in node.left_child.character:
                    node = node.left_child
                    bitstring += '0'
                    continue
                node = node.right_child
                bitstring += '1'
            fpw.write(bitstring)
            cache[character] = bitstring



class createTree():
    def __init__(self):
        self.character = ""
        self.left_child = None
        self.right_child = None

    def insert(self, lists, key):
        if len(lists) == 0:
            self.character = key
            return

        if lists[0] == '0':
            if self.left_child == None:
                self.left_child = createTree()
            
            self.left_child.insert(lists[1:], key)

        else:
            if self.right_child == None:
                self.right_child = createTree()
            self.right_child.insert(lists[1:], key)

    def recreateTree(self, hufftable):
        for key in hufftable:
            lists  = list(hufftable[key])
            self.insert(lists, key)


    def decodeHuff(self, encodedString , padding, hufftable):
        resultBits = ""
        for k in range(0, len(encodedString)):
            resultBits += convertToBinary(ord(encodedString[k]))

        if padding != 0:
            resultBits = list(resultBits[:-1*padding])
        else:
            resultBits = list(resultBits)
            
        resultString = ""

        node = self
        for k in resultBits:
            if k == '0':
                node = node.left_child
            else:
                node = node.right_child

            if node.left_child == None and node.right_child == None:
                resultString += node.character
                node = self

        return resultString


def main():
    l = 0
    nodes = {}
    preProcess = preprocessing()
    for x in range(0, numDoc):
        fileread = "documents/set1/doc"+str(x)+".txt"
        print "reading from " + fileread
        fp=open(fileread,'r')
        content = fp.read()
        print "preprocessing called"
        content1 = preProcess.processText(content)
        print "preprocessing ended"
        #print content1 
        l += len(content1)
        #print l
        for character in content1:
            if not character in nodes:
                #print "character " + character + "added"
                nodes[character] = CharNode(character, 0)
            nodes[character].frequency += 1.0
        fp.close()
    for character in nodes:
        nodes[character].frequency /= l
 
    frequency_map = []
    for character, node in nodes.items():
        frequency_map.append((node.frequency, node))
 
    sorted_nodes = sorted(frequency_map, key=lambda item: item[1].frequency, reverse=True)
    while len(sorted_nodes) > 1:
        x_frequency, x = sorted_nodes.pop()
        y_frequency, y = sorted_nodes.pop()
 
        merged_frequency = x_frequency + y_frequency
        merged_node = CharNode(x.character + y.character, merged_frequency)
        #print 'New Node "{0}" with frequency {1}'.format(repr(merged_node.character), merged_node.frequency)
        if x.frequency > y.frequency:
            merged_node.right_child = x
            merged_node.left_child = y
        else:
            merged_node.right_child = y
            merged_node.left_child = x
 
        sorted_nodes.append((merged_frequency, merged_node))
        sorted_nodes = sorted(sorted_nodes, key=lambda item: item[0], reverse=True)
 
    huffman_tree = sorted_nodes.pop()[1]
 
    # Don't write actual bits for now, but rather whole bytes (0 and 1).
    # I'm aware that this defeats the purpose in a way -- but this is just a
    # test.
    writeToBin(huffman_tree)
    #write(huffman_tree)
    print 'Table', cache
    tablefile = open("table.txt","w")
    for character in cache:
        tablefile.write("\n" + character.encode("utf-8") + "\t" + cache[character])
    tablefile.close()
    #read()
 
if __name__ == '__main__':
    main()