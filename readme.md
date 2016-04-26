# Stage 5 Back-End Final Project: Tournament
## Written by Sagar Doshi on April 26, 2016

#### Introduction to Programming Nanodegree | Udacity


#### Legal
This is an open-source project that I've created for the purpose of self-
education. As a result, I'm applying the open-ended MIT License as below:

Copyright (c) [2016] [Sagar Doshi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


#### Requirements
* This program was built using Python 2.7.10.
* This program manipulates relational databases using PostgreSQL.
* This program requires a virtual environment to run. I've used Vagrant. If
you're unfamiliar with Vagrant, here's a [Getting Started Guide]
(https://www.vagrantup.com/docs/getting-started/).
* This program was kicked off by using the initial stub built by the Udacity
staff. That's accessible at [Udacity's Github page for the
fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).
* In order to obtain the full program as I've written it, you can get that at
[the swisstournament section of my own Github page]
(https://github.com/koopsykoopsy/swisstournament).


### Files and Libraries
Apart from this README file, there are three critical files used here:
* **tournament.sql:** sets up the database schema
* **tournament.py:** does the heavy work of manipulating the database to set up
a Swiss-style tournament
* **tournament_test.py:** tests tournament.py to make sure it's working as
expected

As mentioned above, these files generally just use Python 2.7.10 to work. There
are a few libraries that I've imported to make things work more smoothly:
* **psycopg2:** allows for PostgreSQL to work properly
* **contextlib:** helps dramatically simplify the tournament.py structure by
abstracting the connection to the database
* **random:** helps generate random numbers


### Running the Program

**FIRST**
As explained above, we'll be using Vagrant. Assuming you've installed Vagrant
through the instructions above, here's how you set up the virtual machine
you'll need for all the fun stuff to come.

Open a command-line interface: you'll probably use Terminal on Mac OS or
Command Prompt on Windows. New to the command-line interface? There are many
resources online. One nice refresher is at [Lifehacker]
(http://lifehacker.com/5633909/who-needs-a-mouse-learn-to-use-the-command-line-for-almost-anything).

**SECOND**
In your command-line interface, navigate to the folder where you have installed
the Vagrantfile (most likely, you've taken this from the Udacity Github page
referenced above).

**THIRD**
Type `vagrant up` and hit return. This will create a virtual machine using
Vagrant. Please note that this may take a little while, and a number of actions
might occur. Just sit back and relax.

**FOURTH**
Once Vagrant is ready to go, you'll know because it will offer you an
opportunity to type something fresh in front a line that looks something like
`Your_Machine:vagrant your_username$` (with your computer's name and your
username replaced accordingly). At this point, type `vagrant ssh` and hit
return in order to actually access the virtual machine we've created and open
it up for manipulation.

**FIFTH**
Once you see something like `vagrant@vagrant-ubuntu-trusty-32:~$`, you're ready
to start. Only one thing left: we just have to get to the right folder. Typing
`cd ../../vagrant/tournament` will take us there.

**SIXTH**
Now the real stuff begins. We first create our database using PostgreSQL, or
psql for short. The following command tells your machine to execute the file
named tournament.sql with psql: `psql -f tournament.sql`.

**SEVENTH**
At this point, you've created the relevant database schema. Now we run the test
to see whether everything works. Type `python tournament_test.py` and hit
return now. If you see a series of 10 printouts, followed by a `Success! All
tests pass!` then all is as it should be.
