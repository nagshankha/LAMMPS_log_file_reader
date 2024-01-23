# LAMMPS log file reader

class LogFileReader defines methods to read a LAMMPS log file and extract the thermo data of all MD runs and
store them as metadata and in Pandas DataFrame inside an instance of class MDRunData

There is an example script read_example_logfile.py which reads and processes MD run data from md_heat_n_anneal.log logfile. 

