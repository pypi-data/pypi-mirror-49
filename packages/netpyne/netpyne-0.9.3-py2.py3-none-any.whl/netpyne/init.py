"""
init.py

A modularized framework to develop and run large-scale network simulations. 
Built solely in Python with MPI support. 

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi main.py

Contributors: salvadordura@gmail.com
"""

import framework as f

def createAndSimulate(netParams, simConfig):
    ''' Sequence of commands to run full model '''
    f.sim.initialize(netParams, simConfig)  # create network object and set cfg and net params
    f.net.createPops()                  # instantiate network populations
    f.net.createCells()                 # instantiate network cells based on defined populations
    f.net.connectCells()                # create connections between cells based on params
    f.net.addStims()                    # add external stimulation to cells (IClamps etc)
    f.sim.setupRecording()              # setup variables to record for each cell (spikes, V traces, etc)
    f.sim.runSim()                      # run parallel Neuron simulation  
    f.sim.gatherData()                  # gather spiking data and cell info from each node
    f.sim.saveData()                    # save params, cell info and sim output to file (pickle,mat,txt,etc)
    f.analysis.plotData()               # plot spike raster
    

# Main call example
# createAndSimulate(                                      # execute sequence of commands to run full model
#    simConfig = M1yfrac.simConfig,     # pass simulation config options and network params as arguments
#    netParams = M1yfrac.netParams)      



def createAndExport(netParams, simConfig, reference, connections=True,stimulations=True):
    ''' Sequence of commands to run full model '''
    f.sim.initialize(netParams, simConfig)  # create network object and set cfg and net params
    f.net.createPops()                  # instantiate network populations
    f.net.createCells()                 # instantiate network cells based on defined populations
    f.net.connectCells()                # create connections between cells based on params
    f.net.addStims()                    # add external stimulation to cells (IClamps etc) 
    f.sim.setupRecording()              # setup variables to record for each cell (spikes, V traces, etc)
    f.sim.exportNeuroML2(reference,connections,stimulations)     # export cells and connectivity to NeuroML 2 format

    