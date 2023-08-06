# cryptochecker
A python pip library for checking Bitcoin and Ethereum transactions

Install with:
`pip install cryptochecker`

Example:

```
from cryptochecker import transaction
response = transaction.check('btc','f12e3081945ff47cfa1099ca4563f2526772a460e08057239e4f7a8c9fbbe04c',False)
print(response)
```

This will return a dictionary with the following keys:

`status, addresses_to, addresses_from, fee_amount, t_output, t_input`

Function `check` takes 3 parameters:

1. btc/eth, 
2. tx_hash, 
3. True/False (for True the script will return a class object, from where you can print response.status)
