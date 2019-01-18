# check-hibp
Query a local copy of the HIBP database.

## Setup
Download and extract hashed passwords from https://haveibeenpwned.com:  
https://downloads.pwnedpasswords.com/passwords/pwned-passwords-sha1-ordered-by-hash-v4.7z  
Download size is ~10G, size after extraction is ~23G.

## Usage
```
usage: check-hibp.py [-h] -f FILE [-i] [-q]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File containing hashes that will be used for
                        searching. This can be retrieved from
                        https://haveibeenpwned.com.
  -i, --interactive     Interactive mode. You will be prompted to enter a
                        password.
  -q, --quiet           Quiet mode. Print only found passwords and summary.
```

## Examples
Interactive (tool will ask you to enter a password):  
`python3 check-hibp.py -f /path/to/extracted-passwords-file -i`

Non-Interactive (supply passwords via stdin):  
`python3 check-hibp.py -f /path/to/extracted-passwords-file < mysecretpasswords`  
Note that keeping plaintext passwords in unencrypted files is dangerous.  

For (at least halfway) secure batch mode, consider decrypting and piping from an encrypted file, like this:  
`gpg -d mysecretpasswords.txt.gpg | python3 check-hibp.py -f /path/to/extracted-passwords-file`  

Note that matched passwords (i.e., insecure ones that were part of a leak)
will be printed in plaintext to facilitate locating and changing them.  
If you don't like that (maybe because you have people looking over your shoulder),
change [line 33](https://github.com/xai/check-hibp/blob/master/check-hibp.py#L33).  

To avoid printing the sha1 hash of each queried password, use `-q` to enable quiet mode.  
Only matches plus a summary will be printed.
