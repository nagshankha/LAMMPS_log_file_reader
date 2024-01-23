from LAMMPS_log_file_reader import LogFileReader
import matplotlib; matplotlib.use('tkagg')
import matplotlib.pyplot as plt

l = LogFileReader('md_heat_n_anneal.log')
l.open_file()
l.extract_thermo_outputs_in_MD_run()

print('List of MDRunData instances')
print(l.run_records)
print('\n')
print('Metadata for the 1st run')
print(f'Loop time = {l.run_records[0].loop_time_in_secs} s')
print(f'Number of processors used = {l.run_records[0].nprocs}')
print(f'Number of run steps = {l.run_records[0].Nsteps}')
print(f'Number of atoms in the system = {l.run_records[0].natoms}')

### Plotting temperature versus timestep for each run

fig = plt.figure(figsize=(16.,8.))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

ax1.plot(l.run_records[0].thermo_output['Step'], 
         l.run_records[0].thermo_output['Temp'], label='Run 1')
ax2.plot(l.run_records[1].thermo_output['Step'], 
         l.run_records[1].thermo_output['Temp'], label='Run 2')
ax3.plot(l.run_records[2].thermo_output['Step'], 
         l.run_records[2].thermo_output['Temp'], label='Run 3')

ax1.legend(); ax2.legend(); ax3.legend()
ax1.set_xlabel('Step'); ax2.set_xlabel('Step'); ax3.set_xlabel('Step')
ax1.set_ylabel('Temperature (K)')

# Combining all run data from all three instances of MDRunData

l.run_records[0].append(l.run_records[1:])

# Plotting temperature versus timestep from all MD runs combined
fig2 = plt.figure()
ax = fig2.add_subplot(111)
ax.plot(l.run_records[0].thermo_output['Step'], 
        l.run_records[0].thermo_output['Temp'], label='Data from all runs')
ax.set_xlabel('Step'); ax.set_ylabel('Temperature (K)')

plt.show()

