import module_b
import module_c

def function_a():
    print("function_a from module_a was called!")

def function_a_that_calls_b():
    module_b.function_b()

def function_a_that_calls_c():
    module_c.function_c()

def function_a_that_imports_and_calls_d(x,y,z):
    import module_d
    module_d.function_d(x+y+z)