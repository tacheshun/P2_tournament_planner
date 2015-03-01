# Project 2 - Tournament Planner

Database schema to store the game matches between players. Also, there is a Python module to rank the players and pair them up in matches in a tournament. Is part of Full Stack Web Developer Nanodegree from Udacity. 

# How to run
- Make sure you have git, python, virtualbox and vagrant installed on your system. Also the database ```tournament``` must be created previously. Then:
- Clone this repository: 
```
git clone git@github.com:tacheshun/P2_tournament_planner.git
```
- In command line, go to the directory of the repository and execute ``` vagrant up ```.
- The test cases can be run by entering vagrant machine and executing ```tournament_test.py``` like so:
```
vagrant ssh
cd /vagrant/p2_tournament_planner/tournament
python tournament_test.py
``` 

- In the terminal you should see the result of the tests.
