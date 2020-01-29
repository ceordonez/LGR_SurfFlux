# LGR surface Fluxes

## Instalation

Install python3

Libraries used:
- Pandas
- xlswriter
- Matplotlib

## Using pipenv and virtual environment (recommended)
Install pipenv

    pip3 install pipenv --user

find the user directory used by pip3
    
    python -m site --user-base

Add the user directory in the PATH envirment variable

Clone the repository and execute inside the directory of the repository

    git clone 

    pipenv shell

You can change the version of python3 in your PC change the Pipfile

Then install the libraries requires

    pipenv install

## Quick manual

### Using pipenv
Before run the program execute in the folder of the program
    pipenv shell

### All users
Configurate the config\_file.py document

Execute python main.py in the terminal or click (only windows users) in the main.py file to run the program.

Select the starting and end point for each flux.

The program it will create a folder results inside of your path\_out.

Results consis in:
- Excel with a tab per LGR data selected and one tab with the results.
- One figure per flux and one plot with all data and points selected.
