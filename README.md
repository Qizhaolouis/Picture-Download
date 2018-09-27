# Picture-Download
download pictures from shopping websites

## Requirement
- Python3
- packages
    - requests
    - os
    - bs4
    - time

## Initialization
- path
    - Where you would like to save the pictures. Should end with '/'
- sleep_time
    - How long to wait after request the url
- max_page
    - How many pages you would like to request, default is 7.

## Usage
- If run in Jupyter notebook. 
    - Copy the class object to a cell, change the `path` to `''`. 
    - run the cell:
    ```Python
    tools = ['apple','hammer', 'handdle'] ## put your search terms as a list
    homedepot_search = Homedepot_search()
    homedepot_search.max_page = 10 ## the default is 7, change it bigger if you want to have more pictures.
    for tool in tools:
        homedepot_search.download_from_homedepot(tool)
    ```
- Run using command line:
    - Change the `'if __name__ == '__main__'` part to the code above
    - run ```python \path\to\file\HomeDepot.py```
