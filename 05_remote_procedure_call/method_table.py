from functions import floor, nroot, reverse, validAnagram, sort

method_table = {
    "floor": {
        "function": floor,
        "param_types": [ float ],
        "result_type": [ "int" ]
    }, 
    "nroot": {
        "function": nroot,
        "param_types": [ int, int ],
        "result_type": [ "int" ]
    },
    "reverse": {
        "function": reverse,
        "param_types": [ str ],
        "result_type": [ "str" ]
    },
    "validAnagram": {
        "function": validAnagram,
        "param_types": [ str, str ],
        "result_type": [ "bool" ]
    },
    "sort": {
        "function": sort,
        "param_types": [ list[str] ],  
        "result_type": [ "list[str]" ]
    }
}