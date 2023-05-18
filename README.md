# Chemical Equation Balancer
Balances a chemical equation, if possible. Originally written in my package [UniSci](https://www.github.com/vivaansinghvi07/unisci) and moved to this repo.

## Usage

To use, simply install the requirements and run the main program. You will be prompted with the following:

```code
Enter chemical equation in the format "A + B -> C + D":
```

Enter your reaction in the correct format and it will solve it for you!

You will then be prompted to select a return type. 

```
Enter your desired return type: 
    1. Reaction
    2. Coefficients
    3. Dictionary
Please enter a number between 1 and 3: 
```

Then, you will be able to see your reaction balanced.

```
Enter chemical equation in the format "A + B -> C + D": C6H12O6 + O2 -> H2O + CO2

Enter your desired return type: 
    1. Reaction
    2. Coefficients
    3. Dictionary
Please enter a number between 1 and 3: 1

C6H12O6 + 6O2 -> 6H2O + 6CO2
```

You can enter more complicated equations such as: 

```
Enter chemical equation in the format "A + B -> C + D": K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 -> Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3

Enter your desired return type: 
    1. Reaction
    2. Coefficients
    3. Dictionary
Please enter a number between 1 and 3: 1

6K4[Fe(SCN)6] + 97K2Cr2O7 + 355H2SO4 -> 3Fe2(SO4)3 + 97Cr2(SO4)3 + 36CO2 + 355H2O + 91K2SO4 + 36KNO3
```

However, interestingly, it seems to break when given the simplest reactions - `H + O -> H2O` raises an error of which I do not know the cause.