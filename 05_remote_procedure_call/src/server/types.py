from typing import Dict, Any, List
from functions import floor, nroot, reverse, validAnagram, sort

type_mapping: Dict[str, Any] = {
    "int": int, 
    "double": float,
    "string": str,
    "string[]": List[str]
}

FUNCTION_MAP = {
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
    "validAnagram": validAnagram,
    "sort": sort
}