from md_run_data import MDRunData

class LogFileReader:
   
   def __init__(self, logfilepath):
      
      # Initiates an instance with the path to the log file 
      # stored in a member variable
      self.logfilepath = logfilepath
    
   #####################################################   
      
   def open_file(self):
      
      # Read the log file in a file object
      self.f = open(self.logfilepath, 'rt')
      
   #####################################################
      
   def close_file(self):
      
      # Close the file object
      self.f.close()
      
   #####################################################
   
   def extract_thermo_outputs_in_MD_run(self):
      
      run_records = [] # stores the tabular thermo outputs from each run 
                       # command as separate instance of class MDRunData
      start = False # toggle flag which turns on, on encountering a run command

      for i, line in enumerate(self.f):
         
         sline = line.split()
         if len(sline) == 0: # if it is an empty line continue with the loop
            continue
         
         if sline != ['run', '0'] and sline[0] == 'run':
            
            # Looking for "run N ..." where N!=0; stores N in Nsteps (# of run steps)
            if not sline[1].isdigit():
               continue
            else:
               Nsteps = int(sline[1])
            
            # Only reads MD runs specified with commands "run N" or "run N upto"   
            if len(sline) == 2:
               run_upto = False
            elif len(sline) == 3:
               if sline[-1] == 'upto':
                  run_upto = True
               else:
                  continue
            else:
               continue        
            
            self.f.readline() #Skip a line
            start = True
            run_records.append(MDRunData()) 
            headline = True # Indicates that the next line that will be 
                            # read has the thermo keywords
            continue # reloops to read the next line (with thermo keywords)
         
         if start:
            if headline:
               headline = False
               run_records[-1].rundata_init(sline) # Stores the thermo keywords in the MDRunData instance
            elif sline[0] == 'Loop': # End of run where run metadata (like loop time etc. are updated)
               start = False
               run_records[-1].metadata_update(loop_time_in_secs = float(sline[3]), 
                          nprocs = int(sline[5]), Nsteps = int(sline[8]), 
                          natoms = int(sline[11]))
               if 'Step' in run_records[-1].thermo_output.columns:
                  if run_records[-1].Nsteps != ( run_records[-1].thermo_output['Step'].iloc[-1]
                                               - run_records[-1].thermo_output['Step'].iloc[0] ):
                     raise RuntimeError('Number of run steps is not same as the '+
                                        'number of steps printed in the diagnostics')
                  if run_upto:
                     if run_records[-1].thermo_output['Step'].iloc[-1] != Nsteps:
                        raise RuntimeError('The last run step does not correspond to '+
                                           'the N in "run N upto" command')
                  else:
                     if run_records[-1].Nsteps != Nsteps:
                        raise RuntimeError('Number of run steps does not correspond to '+
                                           'the N in "run N" command')
            else:
               run_records[-1].rundata_update(conv_str2num(sline)) # Storing thermo data
      
      if len(run_records) == 1:         
         self.run_records = run_records[0]
      else:
         self.run_records = run_records
               
   #####################################################            
                  
def conv_str2num(list_of_str):
   
   # Function which converts the list of numerical strings of thermo data
   # into integers and floats  

   if not isinstance(list_of_str, list):
      raise ValueError('The input must be a list of strings')
   
   if not all([isinstance(x, str) for x in list_of_str]):
      raise ValueError('The input must be a list of strings')      
      
   l = []
   
   for s in list_of_str:
      flag=0
      sl = s.split('.')
      
      if len(sl) > 2 or len(sl) == 0:
         raise RuntimeError(s+' cannot be converted to integer or float')
         
      if sl[0].isdigit() or sl[0][1:].isdigit():
         if not (sl[0][0].isdigit() or (sl[0][0] in ['+', '-'])):
            raise RuntimeError(s+' cannot be converted to integer or float')
         
         if len(sl) == 1:
            l.extend([int(s)])
            continue
         else:
            flag=1
      else:
         raise RuntimeError(s+' cannot be converted to integer or float')
      
      if flag == 1:
         if sl[1].isdigit():
            l.extend([float(s)])
         elif 'e+' in sl[1]:
            sle = sl[1].split('e+')
            if len(sle) != 2:
               raise RuntimeError(s+' cannot be converted to integer or float')
            elif not all([x.isdigit() for x in sle]):
               raise RuntimeError(s+' cannot be converted to integer or float')
            else:
               l.extend([float(s)])
         elif 'e-' in sl[1]:
            sle = sl[1].split('e-')
            if len(sle) != 2:
               raise RuntimeError(s+' cannot be converted to integer or float')
            elif not all([x.isdigit() for x in sle]):
               raise RuntimeError(s+' cannot be converted to integer or float')
            else:
               l.extend([float(s)])
      else:
         raise RuntimeError(s+' cannot be converted to integer or float')
         
   return l

         
   ##################################################### 
      
         
