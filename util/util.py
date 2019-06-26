import traceback
import sys
def get_stack_trace():
    stack = __system_trace_stack__()
    return stack

def __system_trace_stack__():
    exc_type,exc_value,exc_trace_back = sys.exc_info()[0:3]
    if exc_trace_back == None:
        return ""
    return __format_trace_entry__(exc_type, exc_value, exc_trace_back)

def __format_trace_entry__(exc_type, exc_value, exc_trace_back, filter = False):
    if type(exc_type) == type(''):
        exc_type_name = exc_type
    else:
        exc_type_name = exc_type.__name__
    trace_back = []
    while exc_trace_back:
        filename = exc_trace_back.tb_frame.f_code.co_filename
        lineno = exc_trace_back.tb_lineno
        printable = True
        if printable:
            trace_back.append('%s:%d'%(filename, lineno))
        exc_trace_back = exc_trace_back.tb_next
    trace_info = exc_type_name + ":" + str(exc_value) + "\n" + "".join(trace_back) + "\n"
    return trace_info

if __name__ == "__main__":
    def fun():
        print("------------")
        try:
            f = open("wufei.txt","r")
            f.close()
        except:
            print(get_stack_trace())
    fun()
    print("---------222222---------")