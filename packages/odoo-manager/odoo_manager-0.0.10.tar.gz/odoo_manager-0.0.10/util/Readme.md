# Odoo Utilities
Some script and other tools for working with Odoo, in various stages of completion. 

1. **OOP_Training.ipynb** - this demonstrates some object oriented programing using Python. ipython notebooks, also called jupyter notebooks, can be installed on Ubuntu with `apt-get install ipython-notebook`. For other OS's, see [the Jupyter Notebook website](http://jupyter.org/).
2. **resetDBrpc.py** - this will reset the expiration date on an instance of odoo using RPC. To use, there are some variables that have to be written in the file. Some changes I would like make:
    1. set the new date to something like `now + month`
    2. have it load the parameters from a configuration file, then supply that filename in the command line. This would make it easier to run as a cron job or as an action from within odoo.
    3. More testing - so far, only tested against demo.odoods.com.
3. **changeOdooPassword.py** - If a user has been in Odoo long enough to have Odoo encrypt the password, then this can be used to change that password through a direct database connection.
3. **Selenium**
4. **pyGit** - gather.py is a script that scans your home directory and searches for git repo's. It tries to gather any information about the repo and put it into an html file called git_report.html. It has some formatting, but any feedback is welcome. I itried to make it easy to look at the page and see if there were duplicate repos and uncommited changes on my local hard drive. I used this as I started having multiple copies of repositories when creating the Odoo Apps. 
