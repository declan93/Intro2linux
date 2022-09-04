# Intro2linux
Resource for CRT-GDS cohort4

### Terminal ###
#### How to open the terminal
There are two main methods for launching a terminal on Linux machines. The terminal will default to opening at the top of your home directory.
  1) Search "terminal" in the applications menu
  2) Press ctrl + alt + t 

#### Moving about ####
There are a number of essential commands. `ls` allows us to list the files in the directory. We can pass flags to `ls` to change th structure of the output e.g `ls -lhrt` use either `man ls` or `ls --help` to find out the meaning each flag.

`pwd` will print you current location. **Never work in the root directory** On your own machines you should always be under your home directory. When working on HPC servers you should be working on a dedicated storage mount.

`cd` is used to change directory e.g `cd /home/declan/newdirectory`. `cd -` will return you to the previous directory. 

You may need to create specific directories. We can create a new directory with `mkdir` e.g `mkdir newdirectory`

#### Working with files ####
##### create files ######
we can open a file with programmes suh as vi, nano, pico, or gedit (which will launch the desktop/GUI text editor)
There is a short learning curve to working with vi but it has some powerful features and is lightweight. 

`vi newfile.txt` 

vi has a number of modes - it will open in normal mode and we will most of the time want to be in `insert mode` by typing either `a` or `i` we can save the changes and close the editor by hitting the escape key to return to normal mode and type `:wq` we can discard the changes made by dropping the `w`.

The `rm` command will delete a file e.g `rm newfile.txt` 

##### Advanced file manipulation #####

Often we will only want to eyeball some data or else perform some basic statistics like counting the number of entries. Unix provides us with a plethora of command line tools. Below are some examples of commands I use frequently and are by no means exhaustive. 

*Counting*
```
wc -l newfile.txt # count number of lines in a file
grep "PATTERN" newfile.txt | wc -l # note the use of the "pipe" symbol - we can string commands together
```

*Finding and Replacing*
 ```
 sed 's/chr//g' newfile.txt # replace all occurences of chr with nothing - be very careful - 99% of the time we will only want to remove chr from chromosomes names - we need to make sure chr doesn't occur elsewhere
 
 sed 's/^chr//g' newfile.txt # we can use a special character, ^, to only replace chrs which occur at the start of the line. 
 ```
 
 *extracting columns* from a file.
 ```
 awk '{print $1,$2}' newfile.txt # cut can also be used.
```

*calculate the average value of a column of data*
```
awk '{sum += $8} END {print sum/NR}' newfile.txt # calculate mean of column 8
```

*string commands together*
Below will extract lines containing the pattern and calculate the average.
```
grep PATTERN newfile.txt | sed 's/^chr//g' | awk '{sum += $8} END {print sum/NR}'
```

*working with zipped data*


### Making life easier in the terminal ###
#### Bashrc & Alias' ####
