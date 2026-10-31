import re


def process_defstr(variablesdict:dict,proc_param:str):
    # name of variable must start with "var-"
    # example proc_param: myvar,my value"
    # example proc_param: myvar,"my value "
    # example proc_param: myvar,"my value, good"
    # quotes in values are not allowed

    varname, sep, varvalue = proc_param.partition(",")
    if not varname.startswith("var-"):
        print ("varname does not start with 'var-'")
    if varvalue.startswith('"') and varvalue.endswith('"'):
        varvalue = varvalue[1:-1]
    variablesdict[varname] = varvalue
    return

def extract_placeholders(text: str) -> list[str]:
    return re.findall(r'%([^%]+)%', text)
