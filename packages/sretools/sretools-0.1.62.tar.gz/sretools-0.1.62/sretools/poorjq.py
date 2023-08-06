import sys
import argparse
import os
import json
import yaml
import xmltodict
import re
import traceback
from types import FunctionType


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--infile", dest="infile", help="input file")
    parser.add_argument("-t", "--srctype", dest="srctype", default="JSON", help="JSON,YAML or XML")
    parser.add_argument("-c", "--code", dest="code", help="code to compile. may be a file.")
    parser.add_argument("-i", "--indent", dest="indent", default=4, help="how many spaces for indent. default 4.")
    parser.add_argument("-m", "--module", dest="module", help="import modules.")
    parser.add_argument("-F", "--functionize", dest="func", action="store_true", default=False, help="indicate code only use but doesn't define function(doc) ",)
    parser.add_argument("-X", "--debug", dest="debug", action="store_true", default=False, help="debug mode",)
    args = parser.parse_args()

    if not args.code :
        print("# must specify code by -c.")
        sys.exit(-1)

    if args.infile:
        if not os.path.isfile(args.infile):
            print("# {} not exists.".format(args.infile))
        with open(args.infile, "r") as f:
            INPUT = f.read()
    else:
        INPUT = sys.stdin.read()

    try :
       if args.srctype.upper() == "JSON" :
            __JS = json.loads(INPUT)
       elif args.srctype.upper() == "YAML" :
            __JS = yaml.safe_load(INPUT)
       elif args.srctype.upper() == "XML" :
            __JS = xmltodict.parse(INPUT)
       else :
        print("# unsupported file type.")
        return -1
    except :
        print("# invalid JSON/YAML/XML.")
        traceback.print_exc()
        return -1

    if os.path.isfile(args.code) :
        code = open(args.code,"r").read()
    else :
        code = args.code

    if args.func :
        import random
        import string
        fname = "".join([random.choice(string.ascii_letters) for _ in range(20)])
        newcode = ""
        if args.module :
            for m in args.module.split(",")  :
                if m :
                    m.strip()
                    if m.startswith("from ") :
                        newcode += m + "\n"
                    else :
                        newcode += "import " + m + "\n"
        newcode += "def {}(__JS) :\n".format(fname)
        for ln in code.splitlines() :
            newcode += " "*(int(args.indent)) + ln.rstrip()
        code = newcode
    else :
        if not re.search(r"def \w+\(\_\_JS\)\s*:*",code,re.DOTALL) :
            print("# cannot find function definition.")
            sys.exit(-1)

    if args.debug :
        print("# code to compile :")
        print(code)

    xcode = compile(code,"<string>","exec")
    cobj = None
    for c in xcode.co_consts :
        if c and type(c) not in [str,int,tuple] :
            cobj = c
            break
    if not cobj :
        print("# no code object found.")
        sys.exit(-1)

    xfunc = FunctionType(cobj, globals())
    print(xfunc(__JS))



if __name__ == "__main__" :
    main()
