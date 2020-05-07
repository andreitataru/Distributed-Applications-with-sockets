Its purpose is to control access to a set of shared resources in a distributed system, 
where different customers may require concurrent access to resources. 

Example of execution of the server:
./lock_server.py 9999 10 2 3 100        ./lock_server.py PORT N K Y T

Example of execution of the client:
./lock_client.py 1 127.0.0.1 9999       ./lock_client.py CLIEND_ID HOST PORT

Commands of the server:
EXIT

Commands of the client:
LOCK (TIME) (RESOURCE_ID) | RELEASE (RESOURCE_ID) | STATUS (RESOURCE_ID) | STATS (RESOURCE_ID) | YSTATS | NSTATS | HELP | EXIT
