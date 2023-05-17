from sympy import symbols, Eq, solve
from pynterface import Color, clear_window, numbered_menu, Text
import math
import re

# certainly not elements
PAREN_OPEN = "X"    
PAREN_CLOSE = "J"    

def balance_equation(reaction: str) -> dict:

    # splits reaction into two parts
    split_reaction = reaction.split('->')
    reactants = list(split_reaction[0].split("+"))   # remove the duplicates
    products = list(split_reaction[1].split("+"))

    # remove whitespace
    for i in range(len(reactants)):
        reactants[i] = reactants[i].strip()
    for i in range(len(products)):
        products[i] = products[i].strip()

    # gets atom counts in each reactant, stored as a dict mapping a molecule name to a dict of atom counts
    reactant_atoms = {}
    product_atoms = {}
    for reactant in reactants:
        reactant_atoms[reactant] = get_atoms(reactant)
    for product in products:
        product_atoms[product] = get_atoms(product)

    # gets the unique atoms in the reaction
    unique_atoms = set()
    for atom_dict in reactant_atoms.values():
        for atom in atom_dict:
            unique_atoms.add(atom)

    # checks it against products - they should be equal
    product_unique_atoms = set()
    for atom_dict in product_atoms.values():
        for atom in atom_dict:
            product_unique_atoms.add(atom)
    if unique_atoms != product_unique_atoms:
        raise Exception("Equation could not be balanced.")

    # generates systems of equations
    equations = []
    for atom in unique_atoms:
        reactants_expression = 0
        products_expression = 0

        # determine where the atom is in the dictionary, get its coefficient and molecule
        for reactant, atom_dict in reactant_atoms.items():
            if atom in atom_dict:
                reactants_expression += atom_dict[atom] * symbols(__hide_parens(reactant))
        for product, atom_dict in product_atoms.items():
            if atom in atom_dict:
                products_expression += atom_dict[atom] * symbols(__hide_parens(product))
        
        # add to system
        equations.append(Eq(reactants_expression, products_expression))

    # solves the equation
    symbs = set([__hide_parens(reactant) for reactant in reactants] 
                  + [__hide_parens(product) for product in products])
    base_symbol = symbs.pop()

    try:
        solution = solve(equations, symbs, dict=True)[0]
    except:
        raise Exception("Equation could not be balanced.")

    # format coefficients to be whole numbers
    multiplication_factor = 1
    for expression in solution.values():
        div_by = expression.as_numer_denom()[1]
        multiplication_factor = math.lcm(multiplication_factor, div_by)

    # return output
    output = { __show_parens(str(base_symbol)) : multiplication_factor }
    for symbol, expression in solution.items():
        output[__show_parens(str(symbol))] = round(float(expression.coeff(base_symbol, 1)) * multiplication_factor)
    return output

# in charge of performing splits by parentheses to be interpreted
def __split_parentheses(molecule: str) -> dict:

    molecule += " "     # for indexing another time

    # empty vars for returning
    parens = []
    paren_numbers = []
    non_paren = ""

    # temp values
    temp_inside_paren = ""
    temp_paren_num = ""
    paren_level = 0
    find_num = False
    i = 0

    # go through the molecule
    while i < len(molecule):

        # gets the character
        c = molecule[i]

        # open parentheses
        if c in ['(', '[']:            
            paren_level += 1
            if paren_level > 1:
                temp_inside_paren += c

        # closed parentheses
        elif c in [')', ']']:          

            # if its base parentheses, seperate it
            if paren_level == 1:
                find_num = True                     # say that we need to find a number if possible
                parens.append(temp_inside_paren)    # add to the things inside parentheses
                temp_inside_paren = ""              # reset variable

            # otherwise include it
            else:
                temp_inside_paren += c           

            # decrease parentheses level no matter what
            paren_level -= 1

        # get the number after the parentheses
        elif find_num:       

            # keep adding to the number   
            if c.isnumeric():
                temp_paren_num += c

            # if not part of the number go back a character and add number to the paren numbers
            else:
                if temp_paren_num == "":
                    temp_paren_num = "1"
                paren_numbers.append(int(temp_paren_num))   # adds integer version to mulitply by thing
                temp_paren_num = ""                         # resets variables
                find_num = False
                i -= 1                                      # moves incrementor back

        # adds to molecules inside the parentheses
        elif paren_level > 0:
            temp_inside_paren += c

        # adds to outside parentheses
        else:
            non_paren += c

        # increments character address
        i += 1
    
    # adds in case there is a number at the end
    if temp_paren_num != '':
        paren_numbers.append(int(temp_paren_num))

    return {
        "parens": parens,
        "paren_numbers": paren_numbers,
        "non_paren": non_paren
    }

# Gets a dictionary of atoms and their counts from a generated string.
def get_atoms(molecule: str) -> dict:

    elements_str = __get_atoms_str_loop(molecule)
    counts = {}

    for ele in re.findall("[A-Z][^A-Z]*", elements_str):

        # get number
        num_str = re.search('[0-9]+', ele)
        num = int(num_str.group()) if num_str != None else 1

        # get element
        symb = re.search('[A-Z|a-z]+', ele).group()

        if symb in counts:
            counts[symb] += num
        else:
            counts[symb] = num

    return counts

# recursively creates a string containing all the elements listed one by one
def __get_atoms_str_loop(molecule: str) -> str:

    split_molecule = __split_parentheses(molecule)
    elements_str = split_molecule["non_paren"]
    parens = split_molecule["parens"]
    paren_numbers = split_molecule["paren_numbers"]

    for factor, thing in zip(paren_numbers, parens):
        elements_str += __get_atoms_str_loop(thing) * factor

    return elements_str

def __hide_parens(molecule: str) -> str:
    """
    Replaces parentheses with an arbitrary symbol 
    """
    
    # performs substitutions
    molecule = re.sub('[(\[]', PAREN_OPEN, molecule)
    molecule = re.sub('[)\]]', PAREN_CLOSE, molecule)

    return molecule

def __show_parens(molecule: str) -> str:
    """
    Puts parentheses back from __hide_parens() function.
    """
    return molecule.replace(PAREN_OPEN, "(").replace(PAREN_CLOSE, ")")

if __name__ == "__main__":

    # get the answer
    clear_window()
    equation = input("Enter chemical equation in the format \"A + B -> C + D\": ")
    result = balance_equation(equation)

    option = numbered_menu(options=["Reaction", "Coefficients", "Dictionary"], 
                           beginning_prompt="\nEnter your desired return type: ")
    
    print(Text.BOLD)

    if option == "Reaction":

        # formats to string
        equation = equation.split("->")
        reactants = " + ".join([Color.BLUE + (s if (s:=str(result[(r:=reactant.strip())])) != '1' else '') + Color.RESET_COLOR + r 
                                for reactant in equation[0].split("+")])
        products = " + ".join([Color.BLUE + (s if (s:=str(result[(p:=product.strip())])) != '1' else '') + Color.RESET_COLOR + p 
                            for product in equation[1].split("+")])
        output = list(" " + reactants + " -> " + products)
        for match in reversed([*re.finditer(r"\+|->", "".join(output))]):
            output[m[0]:m[1]] = [Color.RED] + output[(m:=match.span())[0]:m[1]] + [Color.RESET_COLOR]
        
        print("".join(output).strip())

    elif option == "Coefficients":

        print(str(result)[1:-1].replace('\'', ''))    # format dict

    elif option == "Dictionary": 

        print(result)

    print()     # for newline