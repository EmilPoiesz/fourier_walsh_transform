import numpy as np
import itertools

#########################################################################
#                                                                       #
#                  FOURIER-WALSH-TRANSFORM                              #
#                                                                       #
#   Any boolean function can be calculated as a polynomial              #
#   with rational coefficients using the Fourier-Walsh transform.       #
#   This program has the majority boolean function as default.          #
#                                                                       #
#   https://en.wikipedia.org/wiki/Walsh_function                        #
#                                                                       #
#   This project was meant for my own exploration. It is not an         #
#   efficient way to calculate boolean functions                        #
#                                                       -Emil Poiesz    #
#########################################################################

# Boolean functions
def majority(x):
    assert len(x) % 2 == 1
    return 1 if sum(x) > 0 else -1

def minority(x):
    assert len(x) % 2 == 1
    return 1 if sum(x) < 0 else -1

#Fourier-Walsh transform
def fourer_walsh_transform(input_list, boolean_function):
    n=len(input_list)
    inputs = list(itertools.product([1,-1], repeat=n))
    bool_func_values = [boolean_function(list(input_values)) for input_values in inputs]
    coefficients = fourier_coefficients(n, inputs, bool_func_values)
    
    return calculate_fourier_welsh(coefficients, input_list)

def fourier_coefficients(n, inputs, bool_func_values):
    coefficients = {}
    for subset in itertools.product([0,1], repeat=n):
        subset = np.array(subset)
        subset_products = np.prod(np.power(inputs, subset), axis=1)
        coefficient = np.mean(subset_products * bool_func_values)
        coefficients[tuple(subset)] = coefficient
    return coefficients

def calculate_fourier_welsh(coefficients, input):
    value = 0
    value_str = 'f(X) = '
    for subset, coefficient in coefficients.items():
        #is the subset product 1 or -1? 
        subset_prod = np.prod([input[i] if subset[i] == 1 else 1 for i in range(len(input))])
        value += subset_prod * coefficient
        if coefficient == 0.0: continue
        if subset_prod == -1.0:
            value_str += f'({subset_prod})*{coefficient} + '
        else:
            value_str += f'{subset_prod}*{coefficient} + '
    value_str = value_str[:-3]
    value_str += f' = {value}'
    return value, value_str

#Conversions
def to_bool(inputs, elements):
    return [1 if x == elements[0] else -1 for x in inputs]

def to_outputs(value, elements):
    return elements[0] if value == 1.0 else elements[1]

#Program output
boolean_function_dict ={
    'majority': majority,
    'minority': minority
}

print()
print('This python program comutes the output of any boolean function using a Fourier-Walsh transform.')
print('Read more here: https://en.wikipedia.org/wiki/Walsh_function\n \n')
print('You can choose between the following boolean functions:')
print('majority => majority([T,F,T]) = T') 
print('minority => minority([T,F,T]) = F \n') 

print('Please type the boolean function you wish to use. (Default is "majority")')

user_input = input('To exit type "0" \n')
while user_input != "0":

    if user_input == '': boolean_function = 'majority'
    elif user_input not in boolean_function_dict: 
        print('That is not a valid boolean function.')
        print('Please type the boolean function you wish to use. (Default is "majority")')
        user_input = input('To exit type "0" \n')
        continue
    else: boolean_function = user_input

    print('Please enter a comma-seperated list containing only two distinct elements.')
    user_input = input('Example: x,y,x,x,y \n')
    user_input = list(user_input.split(','))
    elements = list(dict.fromkeys(user_input))
    if len(elements) > 2: print('The list must not contain more than two distinct elements.'); continue

    boolean_inputs = to_bool(user_input, elements)
    output, _ = fourer_walsh_transform(boolean_inputs, boolean_function_dict[boolean_function])
    print(f'The majority element is {to_outputs(output, elements)}')

    user_input = input('\nTo exit, type "0", or try a new list: \n')
