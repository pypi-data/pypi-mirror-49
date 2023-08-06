# aws-cost-report      
  
usage: cost-report \[-h\] \[-j\] \[-v\]  
  
command line tool which will return total cost for the current month's AWS usage.  
oraganizations with multiple accounts will see a list of accounts.  
  
usage:   
> $ cost-report  
> $ cost-report -j # optionally output json/dictionary  
  
expected output:  
> AWS Costs - 8378\_ACCT\_ID (July): $2.18    
  
optional arguments:  
> -h, \-\-help     show this help message and exit  
> -j, \-\-json     output json object  
> -v, \-\-version  show program's version number and exit  

### install  
  
pip install aws-cost-report
