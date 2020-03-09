## HTML Table to markdown table converter  
  
This program takes an html file as input, validates it and then searches for all tables within it to convert them to a single md file as output containing a list of tables  
  
#### Required Packages:  
  
* beautifulsoup4 - 4.8.1   
* lxml - 4.4.2    
  
> Tested on python version - 3.7.5  
  
## How to use  
  
Help and available options can be listed by the following cmd  
  
```  
 python3 html_to_markdown.py -h  
```

```
usage: html_to_markdown.py [-h] -i INPUT_HTML_FILE [-o OUTPUT_MD_FILE]
                           [-a {1,2,3}]

Program to find and convert HTML Tables into markdown. HTML file is read from
inputs/ folder and output md file is written in outputs/ folder

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_HTML_FILE, --input_html_file INPUT_HTML_FILE
                        Input html file path
  -o OUTPUT_MD_FILE, --output_md_file OUTPUT_MD_FILE
                        Enter name of output md file to be stored in outputs/
                        folder
  -a {1,2,3}, --alignment {1,2,3}
                        Choose alignment for text in markdown tables 1: left,
                        2: right, 3: center

```
<br>  
In the terminal enter following cmd to run the program:  
  
```  
python3 html_to_markdown.py -i inputs/input3.html -o output3.md -a 1  
```  
  
<br>  
Example output stored in `outputs/` folder as a md file:  

  
## Found 1 table  
  
  
### Table 1:  
  
  
Firstname | Lastname  
--- | ---  
Jill | Smith  
Eve | Jackson  
  
  
<br><br>  
***  
## Run Tests  
  
From ```project``` root dir:  
  
```shell  
python3 tests.py  
```  
  
  
## Contact  
  
Feel free to contact me at my email indoria@usc.edu
