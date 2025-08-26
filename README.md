## Overview

This script automates labelling confluence pages. Script requires two input:
-  **label** 
- **pathname** to a file (see more below)

These inputs are passed as command line arguments with the following usage

`
./main.py [label] [pathname]
`

The users creates a file which contains folder and page urls, each url should be in a seperate line.

For each url, the script marks each children of folder/page being referenced by the url with the label

## Running the script

Running the script requires three environment variables
The script supports .env file which can structured as follows:
```
CONFLUENCE_API_KEY=<YOU_API_KEY>
CONFLUENCE_USERNAME=tanishqchoudharysprinklr@gmail.com
CONFLUENCE_URL=https://tanishqchoudharysprinklr.atlassian.net/wiki
```

To run the file use the following commands
```
pip install -r requirements.txt
chmod a+x main.py
./main.py review urls.txt
```