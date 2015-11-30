# PlanIt

Hey team, welcome to the PlanIt API.  If you want to know how to use it, start with Examples.md. Before that, configure
your environment by following the getting started section.
 

## Getting Started

Before you begin do the following.

 + Setup neo4j on your local machine.  Download it from neo4j.com and follow the instructions for your system.
 + Run a neo4j server -- pick the defaults when setting up

To test that neo4j is running go to http://localhost:7474 in your browser.  If it works, your up and running.

Now do the following.

```sh
$ git clone https://github.com/buckmaxwell/planit-api.git
$ cd planit-api
$
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$
$ pip install -r requirements.txt
$
$ export NEO4J_REST_URL=http://app44498834:u0hWRbXtBC7HBxhbd2@app44498834.sb02.stations.graphenedb.com:24789/db/data
$
$ python api.py
```
There ya go.  Hit localhost:10200/v1 in the browser to test it out.







                                                     ___ 
                                                  ,o88888 
                                               ,o8888888' 
                         ,:o:o:oooo.        ,8O88Pd8888" 
                     ,.::.::o:ooooOoOoO. ,oO8O8Pd888'" 
                   ,.:.::o:ooOoOoOO8O8OOo.8OOPd8O8O" 
                  , ..:.::o:ooOoOOOO8OOOOo.FdO8O8" 
                 , ..:.::o:ooOoOO8O888O8O,COCOO" 
                , . ..:.::o:ooOoOOOO8OOOOCOCO" 
                 . ..:.::o:ooOoOoOO8O8OCCCC"o 
                    . ..:.::o:ooooOoCoCCC"o:o 
                    . ..:.::o:o:,cooooCo"oo:o: 
                 `   . . ..:.:cocoooo"'o:o:::' 
                 .`   . ..::ccccoc"'o:o:o:::' 
                :.:.    ,c:cccc"':.:.:.:.:.' 
              ..:.:"'`::::c:"'..:.:.:.:.:.' 
            ...:.'.:.::::"'    . . . . .' 
           .. . ....:."' `   .  . . '' 
         . . . ...."' 
         .. . ."'      
        . 


(c) 2015 PlanIt