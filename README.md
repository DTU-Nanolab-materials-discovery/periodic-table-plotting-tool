# periodic-plotting-tool

The options to create a plot in the shape of a periodic table: 
Option 1: check_input_periodic_table(data_array,label_list, Units_str)
Option 2: plot_as_periodic_table(data_array,label_list, Units_str)
Option 3: plot_as_reduced_periodic_table(data_array,label_list, Units_str)
Option 4: plot_as_reduced_periodic_table_log (data_array,label_list, Units_str)


Necessary inputs:
-data_array
  -2D array (118,x) or (86,x)
  -Floats
  -Rows for elements 
  -Row number = Z -1
  -Columns for properties /stoichiometries
  -For grouped properties (Option 4) insert Nan columns in the right places

-label_list
  -String list
  -Same length as columns in data_array
  -Will be displayed as it is as a label in the legend

-units_str
  -One string
  -Will be displayed exactly like this under the colorbar

Special for the respective options

Option 1:
-Checks input compatibility
-Needs the definition of a plot_ …additionally
-Interacts with the user in form of error outputs and questions to the terminal

Option 2 and 3:
-Differ in the length of this loop
-To change/adjust something follow the comments

Option 4:
-Adjust the data = (…) list
  -The numbers give the size difference between the fields and the blanks in-between
  -Add empty rows into the data_array in the same positions as the indicated blanks

-Includes grouped properties and a logarithmic scale
  -Should be able to modify Option 2 or 3 with either grouped properties or logarithmic scales




