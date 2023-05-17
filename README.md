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
Enter chemical equation in the format "A + B -> C + D": C6H12O6 + O2 -> CO2 + H2O

Enter your desired return type: 
    1. Reaction
    2. Coefficients
    3. Dictionary
Please enter a number between 1 and 3: 1

1C6H12O6 + 6O2 -> 6CO2 + 6H2O
```