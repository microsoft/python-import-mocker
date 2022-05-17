import module_b
import module_c

def function_a():
    print("function_a from module_a was called!")

def function_a_that_calls_b():
    module_b.function_b()

def function_a_that_calls_c():
    module_c.function_c()

def function_a_that_imports_and_calls_d():
    import module_d
    module_d.function_d()

def function_a_that_imports_and_calls_e_(x,y,z):
    import module_e
    module_e.function_e(x+y+z)