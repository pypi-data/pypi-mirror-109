__all__=['write', 'printerr', 'service']
import sys

terminal_codes={'':'\033[0m', 'red':'\033[31m', 'green':'\033[32m',
                'black':'\033[30m', 'yellow':'\033[33m', 'blue':'\033[34m',
                'magenta':'\033[35m', 'cyan':'\033[36m', 'white':'\033[37m',
                'bright':'\033[1m', 'dim':'\033[2m', 'underscore':'\033[4m',
                'blink':'\033[5m', 'reverse':'\033[7m', 'hidden':'\033[8m'}
logfile=None
colored_keywords={}
printed_rchar=0
no_colors=False


def write(text, end='\n', how='', keywords={}, is_service=False, is_stderror=False): 
    global printed_rchar
  
    if not keywords and colored_keywords:
        keywords=colored_keywords
    msg=str(text)
    if end:
        msg=msg+end

    if not is_service and not logfile is None:
        no_color_msg=msg
        
    # colors
    if (how or keywords) and sys.stdout.isatty() and not no_colors:
        if how:
            for c in how.split(','): 
                if not c in terminal_codes:
                    raise Exception(f"ERROR option 'how' for write was not recognized: {c} ; possible values are: {','.join([i for i in terminal_codes if i])}")
                msg=terminal_codes[c]+msg+terminal_codes['']
        for word in keywords:
            code=''
            for c in keywords[word].split(','):
                code+=terminal_codes[c]
            msg=msg.replace(word, code+word+terminal_codes[''])

    # flushing rchars
    if printed_rchar:
        sys.stderr.write('\r'+printed_rchar*' '+'\r' )
        printed_rchar=0
        
    if is_stderror or is_service:
        sys.stderr.write(msg)
    else: 
        sys.stdout.write(msg)
        
    if not is_service and not logfile is None:
        print(str(no_color_msg), end='', file=logfile)

        
def service(text, **kwargs):
    global printed_rchar
    write("\r"+text, end='', is_service=True, **kwargs)
    printed_rchar=len(text)

def printerr(text, *args, **kwargs):
    write(text, *args, **kwargs, is_stderror=True)
