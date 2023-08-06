# mbclient
Client software and on the fly visualisation tools for the moessbauer effect.

## The client software
The client software is a command line tool capable of connecting to the Red-Pitaya running the [MBFilter](https://github.com/phylex/MBFilter)
program in server mode, providing the server on the Red-Pitaya with all the neccesary information to configure itself properly and to store the data
received from the Red-Pitaya in a `.csv` file for Analysis by the student and also Visualise the data as a pulse-height spektrum and a 2d spektrum of
pulse height vs. Digital Function Generator Address. The Visualisation is updated continuously and can be exited without interfering with the data
taking procedures.

The client program
