import os, sys
ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/.."
SRC_DIR = ROOT_DIR + "/src"
LIB_DIR = SRC_DIR + "/lib"
DATA_DIR = ROOT_DIR + "/data"
sys.path.append(SRC_DIR)
sys.path.append(LIB_DIR)
