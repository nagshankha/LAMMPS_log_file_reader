from LAMMPS_log_file_reader import LogFileReader

l = LogFileReader('md_heat_n_anneal.log')
l.open_file()
l.extract_thermo_outputs_in_MD_run()
