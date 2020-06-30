## datamart_scripts
repo for various datamart helper scripts to register datasets

### Verifier Description: 
The verifier.py script reads in your `.csv` file and verifies that it complies with the datamart schema. For a description of the schema, <a href="https://docs.google.com/presentation/d/1n91lkhDc5XYGuYPQDLiodj4vYlR-pZ6d6_dgvnw-400/edit?usp=sharing">Click Here</a>

### Test out the verifier.py script:
  1. Download `verifier.py`, `bad.csv`, and `good.csv` to a new folder on your local machine
  2. Open a Terminal window
  3. Change your working directory to your new folder: `cd /path/to/your_new_folder`
  4. Run the following CLI: 
  
        `python3 verifier.py file.csv` 
  
        where `file.csv` is your csv file. There are two examples included: `bad.csv` and `good.csv`. You can use these examples to test the functionality or test your own `.csv` file.
  
  5. The verification results are printed out to the terminal window. If you'd like to write them to a file, run: 
  
        `python3 verifier.py file.csv >> results.txt`
