#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2009 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

import os, sys, shutil, fnmatch, re, time, getopt

#
# NOTE: This scripts generates .gitignore files in directories
# containing Makefile files with targets. The content of the
# .gitignore file is generated by parsing the output of make -n
# clean. 
#
# In other words, the .gitignore file contains ignore rules for files
# produced by the Makefile and supposed to be cleaned by make clean.
#

progname = os.path.basename(sys.argv[0])
preamble = "// Generated by " + progname
preamble = preamble + """

// IMPORTANT: Do not edit this file -- any edits made here will be lost!
"""

#
# Find files matching a pattern.
#
def find(path, patt):
    result = [ ]
    files = os.listdir(path)
    for x in files:
        fullpath = os.path.join(path, x);
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            result.extend(find(fullpath, patt))
        elif fnmatch.fnmatch(x, patt):
            result.append(fullpath)
    return result


def createGitIgnore(filename, gitIgnoreFiles):
    file = open(filename, "r")
    lines = file.readlines()
    cwd = os.getcwd()

    newLines = [ ]
    ignore = ["*.o", "*.bak", "core"]

    for x in lines:
        x = x.strip()
        if x.startswith("rm -f"):
            x = x.replace("rm -f", "", 1)
        elif x.startswith("rm -rf"):
            x = x.replace("rm -rf", "", 1)
        else:
            continue

        if len(x) == 0:
            continue

        files = x.split()
        for f in files:
            if f in ignore:
                continue

            if f.startswith(".."):
                k = os.path.join(cwd, os.path.dirname(f), ".gitignore")
                v = os.path.basename(f) + "\n"
            else:
                k = os.path.join(cwd, ".gitignore")
                v = f + "\n"

            k = os.path.normpath(k)
            if not gitIgnoreFiles.has_key(k):
                gitIgnoreFiles[k] = [ ]
            gitIgnoreFiles[k].append(v)

    file.close()

def usage():
    print "Usage: " + sys.argv[0] + " [options]"
    print
    print "Options:"
    print "-e    Run for Ice-E."
    print "-h    Show this message."
    print

icee = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "he")
except getopt.GetoptError:
    usage()
    sys.exit(1)
for o, a in opts:
    if o == "-h":
        usage()
        sys.exit(0)
    elif o == "-e":
        icee = True
if len(args) != 0:
    usage()
    sys.exit(1)


#
# Find where the root of the tree is.
#
for toplevel in [".", "..", "../..", "../../..", "../../../.."]:
    toplevel = os.path.abspath(toplevel)
    if os.path.exists(os.path.join(toplevel, "cpp", "config", "makegitignore.py")):
        break
else:
    print("cannot find top-level directory")
    sys.exit(1)

if icee:
    makefiles = find(os.path.join(toplevel, "cppe"), "Makefile")
else:
    makefiles = find(os.path.join(toplevel, "cpp"), "Makefile")
cwd = os.getcwd()
gitIgnoreFiles = { }
for i in makefiles:
    os.chdir(os.path.dirname(i))
    if not os.system('grep -q TARGETS Makefile'):
        try:
            os.system("make -n clean > .tmp-gitignore")
            createGitIgnore(".tmp-gitignore", gitIgnoreFiles)
            os.remove(".tmp-gitignore")
        except:
            os.remove(".tmp-gitignore")
            raise
    os.chdir(cwd)
    
os.chdir(cwd)

excludePath = [ os.path.join(toplevel, "cpp", "bin"), os.path.join(toplevel, "cpp", "lib"), \
                os.path.join(toplevel, "cppe", "bin"), os.path.join(toplevel, "cppe", "lib") ]
for (path, files) in gitIgnoreFiles.iteritems():
    if os.path.dirname(path) in excludePath:
        continue
    
    gitIgnore = open(path, "w")
    gitIgnore.write(preamble);
    gitIgnore.writelines(files)
    gitIgnore.close()

