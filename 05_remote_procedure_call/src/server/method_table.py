from .functions import floor, nroot, reverse, validAnagram, sort
from typing import List, Dict, Any

FunctionTable = Dict[str, Dict[str, Any]]

method_table: FunctionTable = {
    "floor" : {
        "function" : floor,
        "paramTypes" : [float]
    },
    "nroot" : {
        "function" : nroot,
        "paramTypes" : [int, int]
    },
    "reverse" : {
        "function" : reverse,
        "paramTypes" : [str]
    },
    "validAnagram" : {
        "function" : validAnagram,
        "paramTypes" : [str, str]
    },
    "sort" : {
        "function" : sort,
        "paramTypes" : [List[str]]
    }
}