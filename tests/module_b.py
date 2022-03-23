import module_c

def function_b():
    print("function_b from module_b was called!")

def function_b_that_calls_c():
    module_c.function_c()