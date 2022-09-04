# Intro2linux
Resource for CRT-GDS cohort4

### Terminal ###
#### How to open the terminal
There are two main methods for launching a terminal on Linux machines. The terminal will default to opening at the top of your home directory.
  1) Search "terminal" in the applications menu
  2) Press ctrl + alt + t 

#### Moving about ####
There are a number of essential commands. `ls` allows us to list the files in the directory. We can pass flags to `ls` to change the structure of the output e.g `ls -lhrt` use either `man ls` or `ls --help` to find out the meaning each flag. For all commands shown below, you should read the man pages for them to be familiar with the flags and conventions. For tools like `awk`, `grep` and `sed` the examples below do not give a full insight to how powerful they can be. 

`ls ..` Will list directories one level up from your current working directory.

`pwd` will print your current location. **Never work in the root directory** On your own machines you should always be under your home directory. When working on HPC servers you should be working on a dedicated storage mount.

`cd` is used to change directory e.g `cd /home/declan/newdirectory`. `cd -` will return you back to the previous directory. 

You may need to create specific directories. We can create a new directory with `mkdir` e.g `mkdir newdirectory`

#### Working with files ####
##### create files ######
we can open a file with programmes suh as vi, nano, pico, or gedit (which will launch the desktop/GUI text editor)
There is a short learning curve to working with vi but it has some powerful features and is lightweight. 

`vi newfile.txt` 

vi has a number of modes - it will open in normal mode and we will most of the time want to be in `insert mode` by typing either `a` or `i` we can save the changes and close the editor by hitting the escape key to return to normal mode and typing `:wq` we can discard the changes made and exit by using `:q!`.

We can print the whole file using `cat` alternatively some times we are only interested in the first n lines or the last n lines. We can use `head file.txt` and `tail file.txt` to print the first and last ten lines in a file.

*less is more*
To view a file one page at a time we can use a programme called `less` e.g `less file.txt`, type `q` to exit.

The `rm` command will delete a file e.g `rm newfile.txt` to remove all files in a directory we can pass the `-rf` flag
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
grep PATTERN newfile.txt | sed 's/^chr//g' | awk '{sum += $3} END {print sum/NR}'
```
We can sort the data and find unique lines (cat is not required below)

```
cat file.txt | sort | uniq 

```

Or count occurences of entries in a file 

```
sort file.txt | uniq -c
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

*looping over files*


Often we will need to run a command on multiple files sequentially. While this is ok for 1 or 2 files often we will have 1000's. This is where a good foundation in bash and unix commands will allow you to minimise the amount of time you need to interact with a computer. 

Here we will use a `for loop`. This will list all files that end with fastq and pass them to the fastqc programme. In each iteration the file to be analysed is stored in a bash variable which we have called `i`. To tell bash we want to use this variable we prefix the variable with `$`

```
for i in *fastq; do
  echo "fastqc $i"; echo evaluates the variable within a string and prints it to the screen; remove echo and the " and the fastwc program will run if installed
done
```
we can also generate a list of numbers while we can use this command `for i in `seq 1 10`; do echo $i; done` Its more convenient to use a bash expansion 

```
for i in {1..10}; do 
echo $i; # echo evaluates the variable and prints it to the screen
done
```
The `>>` operator can be used in conjunction with a for loop to extract information and append it to one file. What would happen if `>` was used instead?
```
for i in *fastq; do
  cat $i >> file_with_looped_info.txt;
done
```
### bash scripts ###
Often we may need to run many commands together. we can use a bash script to do this. Generally bash scripts end with the suffix `.sh` . The first line is called a shebang this tells the system what programme to run the script with. 


```
#!/bin/bash
# example shell script called bash_script1.sh

# extract information from every fastq file
rm file_with_looped_info.txt # remove previously made file
for i in *fastq; do
  cat $i >> file_with_looped_info.txt;
done

# zip it
bgzip file_with_looped_info.txt

# perform analysis using python
python dosomething.py file_with_looped_info.txt.gz

```
We then have two separate ways to run this file. We can set the permissions bit to make it executable. We can then call the script by typing its name e.g `./shell_script_name.sh`. We can alternatively type `bash shell_script_name.sh`

Its often bad practice to write a script to do one specific action with hardcoded inputs and outputs. We can pass arguments to a script the example below, called `mpileup.sh`, will take an argument i.e bash mpileup.sh SAMPLE.bam

```
#!/bin/bash

samtools mpileup $1 > ${1/.bam/.mpup}

```
The `$1` is evaluated as the filename, SAMPLE.bam. We can use some bash wizzardry to remove the .bam suffix and replace it with a different suffix, using the structure `${VAR/FIND/REPLACE}`. You will come across many ways to do this e.g, `NEWNAME=$(basename sample.bam .bam).mpup` . You can pass more arguments by using $2, $3 etc... 

If we provide a full path to the raw data we can also strip the full path using shell variables
```
NEWNAME="/path/to/somewhere/fizzbuzz.txt" # new name can be an argument variable too
echo ${NEWNAME##*/}
fizzbuzz.txt
```

### Making life easier in the terminal ###

#### Paths and environments ####
What happens if you move directory and call the above script exactly as above? The system will not be able to find the shell script. How does Linux know where the cd command or ls commands are located? With linux we can specify the path to our software - this is an environment variable that contains the paths to the software we have specified. When we call a command the system will check each location. We have seen paths in action above with `ls ..`

`..` idicates up one level on the current path `.` indicates current working directory, i.e, `ls` == `ls ./`

When we open a shell/terminal a set of environment variables gets read and stored. If a command is in our path `whereis` will print its location.

```
whereis cd
```
We can add software to our path via the bashrc. The .bashrc is a hidden file in your home directory. We can access it via `vi/nano/gedit` and add the path to our script or software. Below will add the directory bin in my home directory to my path so any executable file located there can be called from any location.

```
export PATH="/home/declan/bin:$PATH"
```
Often we need to build software locally - It can be critical the paths to the underlying source libraries, such as LD_LIBRARY are specified

We can also use the bashrc to create specific color schemes for our terminal 

#### Alias' ####

As Genomic data scientists, linux is often the most important tool we have at our disposal. We can make our lives much easier by evoking bash alias.
For example `ls -lhtr` can be added to the bashrc as an alias 

```
alias l='ls -lhrt'
```
We can now type `l` to run the above command. You can check what the command is by typing `type l`

As you find commands or bash functions that you use a lot you can these to make working efficient - . 

### Some more useful commands ###

`ps (aux)`							              list your running processes

`kill processID`				        stop a process (use ps to find processID)

`top`						              	more detailed view of running processes

`Ctrl-c`				            		terminate current job

`w / who` 			              	show information on logged in users	

`tar -czf file.tar.gz files`		created a gzipped archive from files

`tar -xzf file.tar.gz`			    extract files from a gzipped archive

`wget http://address/file`		  download a file from the specified address

`exit`							            log out of the current shell


### Connecting to remote servers ###

Often we will need to make use of high performance computing /supercomputing/ cloud computing. We can connect to most of these services via a command line tool called ssh (secure shell). 
```
ssh USERNAME@ip/hostname
```
This will open a shell on the remote server. As with the bashrc. We can create something called an ssh/config file e.g `vi ~/.ssh/config` 

```

Host * # all hosts
ServerAliveInterval 180 # This keeps the connection open longer, if you have an internet connection that is intermittent

Host HPC1
        HostName mybigHPC.somewhere.ie # can be the external IP address also.
        User Username
        ForwardX11 yes # This allows an x11 window to be opened, e.g if we are making plots in R and don't want to write to a file just yet. 
        
```
We can the connect by typing `ssh HPC1`

To move data on/off a remote service we can use `scp`

```
scp data.txt HPC:/data_storage/ # from local to remote
scp HPC:/data_storage/data.txt ./ # from remote to local
```
