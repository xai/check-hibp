# check-hibp
Query a local copy of the HIBP database.

## Setup
Download and extract hashed passwords from https://haveibeenpwned.com:  
https://downloads.pwnedpasswords.com/passwords/pwned-passwords-sha1-ordered-by-hash-v4.7z  
Download size is ~10G, size after extraction is ~23G.  

Now have a look at the code of check-hibp.py.  
Don't worry, it's a lot shorter than this README ;)  

Really, don't feed any random tool your passwords.
Check that it's safe.  
Or trust it. But then again, don't trust random people on github.

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

## Some ideas for batch checking passwords
First of all, I know that there is a ton of extensions, addons, and services that can do all that.  
My point is to not use them and do everything as transparent as possible instead.  

### A Warning
I might be repeating myself, but it is not a good idea to have an unencrypted file with all your plaintext passwords lying around.  

So the first thoughts should be spend on how to secure the file that contains your passwords.  
I would recommend gpg for that, as it is secure (well, if your passphrase is at least) and fits well into the commandline-centric approach we're taking here.  
You can use it with private/public keys or with symmetric encryption.  

After we have a plan on how to secure the passwords, we can focus on obtaining them.  
The basic idea is to extract them from wherever they are stored now into some kind of csv file, which we can filter and pipe into check-hibp to locate weak passwords.  

The remainder will focus on how to extract that data from different tools/services.  
This is work in progress, please let me know if you have working instructions for a specific tool/service.  

### Password managers
If you already use a password manager, it will most likely be easy to extract all credentials as csv.  
Use something like `cut` or `awk` to extract the correct column into a file that you encrypt with gpg.  
Then see Examples on how to proceed.  
Also, if you don't already use a password manager, this is an excellent opportunity to start doing so.  
E.g., an offline tool that works on many platforms is available at https://keepassxc.org.

### Chrome
In case you have them stored in chrome, it's also pretty straightforward to extract them into csv files:  
Open `chrome://flags/` within chrome, search for 'Export passwords' and activate the feature.  
After a restart of chrome, open 'Managed passwords' in settings and you will find a new menu right next to 'Saved passwords', that lets you export all entries.  
Finally, use something like `cut -d, -f4` to select the correct column.

### Firefox
Surprisingly, firefox of all tools makes it rather a pain in the ass to extract saved credentials.  
Running an external tool or extension is out of the question for me (even if open source, because then I would have to audit it first),
so I found [this solution](https://support.mozilla.org/en-US/questions/1077630#answer-834769) using the browser console of firefox and a chunk of javascript.  
Its not exactly pretty, but it gets us some json with the desired data.  
Remember to encrypt the json file with gpg.  
All that's left is extracting the respective password fields, which you can accomplish with, e.g., [jq](https://stedolan.github.io/jq/) (also in many distro repositories) like this:  
`gpg -qd firefox.json.gpg | jq '.[] | .password'`
