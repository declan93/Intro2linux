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

The `rm` command will delete a file e.g `rm newfile.txt` to remove all files in a directory 
```
rm -rf newdirectory/ 
```
**Never use the above blindly or with sudo privaleges**

*moving and copying data*

We can copy a file from one location to another i.e making a working copy from a master set.
 ``` 
 cp file1.txt newdirectory/
 or
     cp file1.txt newdirectory/newname_file1.txt # here we have renamed the file
 ```
 Likewise sometimes we may need to move a file from one location to another with a new name. We can drop the new name to keep the original name.
 ```
 mv file1.txt newdirectory/newname_file1.txt
 ```
 
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
Below will extract lines containing the pattern and calculate the average. We can use the pipe operator to string commands together. Most unix tools will read the stdin if you do not provide a file. The pipe operator streams the stdout from one process to stdin of another
```
grep PATTERN newfile.txt | sed 's/^chr//g' | awk '{sum += $8} END {print sum/NR}'
```

*working with zipped data*
Often Genomic data is kept in compressed form linux allows us to peak at and analyse zipped data without the need for uncompressing the data.
```
zcat newfile.gz | head # print top 10 lines from zipped file.
```

*writing data out*
`>` is known as redirection a brief introduction to I/O can be found [here](https://www.brianstorti.com/understanding-shell-script-idiom-redirect/)
```
zcat newfile.gz | grep PATTERN > newfile_PATTERN.txt 
```

*File permisions*
Set the file permissions on a specific file
```
chmod 755 file.txt
```
Set the permisions on every file in a directory (-R -> recursively)
```
chmod -R 755 newdirectory
```

### Bash expansions, globbing and some bash scripting ### 
You should avoid using special characters in filenames. Numbers are ok but avoid starting a filename with a number. 

The Bourne again shell (Bash) allows us to use some expansions to conveniently work with our data. 
*match all files with pattern*
Below will list all files that begin with RNASEQ, the `*` matches every other character 
```
ls -l RNASEQ*
```
we can use `?` to match only one character - below `?` will match the "m" in temp
```
dbennett@lugh:/data/Seoighe_data$ ls -l te?p
-rw-rw---- 1 test test 980022 Dec 31  2019 temp
```

Often we will need to run a command on multiple files sequentially. While this is ok for 1 or 2 files often we will have 1000's. This is where a good foundation in bash and unix commands will allow you to minimise the amount of time you need to interact with a computer. 

Here we will use a `for loop`. This will list all files that end with fastq and pass them to the fastqc programme. In each iteration the file to be analysed is stored in a bash variable which we have called `i`. To tell bash we want to use this variable we prefix the variable with `$`

```
for i in *fastq; do
  fastqc $i;
done
```
we can also generate a list of numbers while we can use this command `for i in `seq 1 10`; do echo $i; done` Its more convenient to use a bash expansion 

```
for i in {1..10}; do 
echo $i
done
```

### Making life easier in the terminal ###
#### Bashrc & Alias' ####
