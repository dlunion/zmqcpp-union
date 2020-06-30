

import os
import sys
import re

def load_file(file):

	with open(file, "r") as f:
		return f.read()


def ignore_include_syntax(code):

	return re.sub(r'#include[. ]+".*?"', lambda x: "// ans ignore: " + x.group(), code, count=0, flags=re.S | re.M)


def find_all_include_syntax(code):

	local = re.findall(r'#include."(.*?)"', code, re.S | re.M)
	remote = re.findall(r'#include.<(.*?)>', code, re.S | re.M)
	local = list(map(lambda x: "L:" + x, local))
	remote = list(map(lambda x: "R:" + x, remote))
	return local + remote


def encode_include_syntax(name):
	if name[:2] == "L:":
		return '#include "{}"'.format(name[2:])
	else:
		return '#include <{}>'.format(name[2:])


def enum_ordered_include(file, lean_map, pmap, ordered_files):

	if file in pmap:
		return

	pmap.add(file)
	lean = lean_map[file][0] if file in lean_map else []

	for f in lean:
		enum_ordered_include(f, lean_map, pmap, ordered_files)

	ordered_files.append(file)



# main

directory = "src.zmq4.3.2"
fs = os.listdir(directory)

lean_map = {}
for file in fs:

	path = f"{directory}/{file}"
	code = load_file(path)
	incs = find_all_include_syntax(code)

	lean_map["L:" + file] = [incs, ignore_include_syntax(code)]


ordered_files = []
pmap = set()

for file in fs:
	enum_ordered_include("L:" + file, lean_map, pmap, ordered_files)


h = list(filter(lambda x: x[-4:]==".hpp" or x[-2:]==".h", ordered_files))
cpp = list(filter(lambda x: x[-4:]==".cpp" or x[-2:]==".c", ordered_files))
LS = list(filter(lambda x: x[:2] == "L:", h))
RS = list(filter(lambda x: x[:2] == "R:", h))

# save zmq_u.hpp
with open(r"zmq_u.hpp", "w") as f:


	f.write(
		'''#pragma once
#ifndef __UNION_EMQ_HPP
#define __UNION_EMQ_HPP
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#define ZMQ_STATIC
'''
	)
	#[f.write("{}\n".format(encode(item))) for item in RS]
	#[f.write("{}\n".format(encode(item))) for item in LS]

	[f.write("\n//========= begin of {} ============\n\n{}\n\n//========= end of {} ============\n\n".format(encode_include_syntax(item), lean_map[item][1], encode_include_syntax(item))) 
		for item in LS if item in lean_map]


	f.write("\n#endif  // __UNION_EMQ_HPP\n\n")



# save zmq_u.cpp
with open(r"zmq_u.cpp", "w") as f:

	f.write(
		'''#include "zmq_u.hpp"

#ifdef _WIN32
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "iphlpapi.lib")
#endif
		''')
	[f.write("\n//========= begin of {} ============\n\n{}\n\n//========= end of {} ============\n\n\n\n\n\n".format(item[2:], lean_map[item][1], item[2:])) 
		for item in cpp if item in lean_map]