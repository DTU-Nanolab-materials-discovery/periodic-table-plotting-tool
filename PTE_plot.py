#%% full and reduced PTE plot Version 1: linear colorbar, same spacing 
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from mendeleev import element
from mpl_toolkits.axes_grid1 import make_axes_locatable

def check_input_periodic_table(data_array, label_list, Units_str):    #checks input and offers the possibility of plotting the periodic table if everything is fine
    #define variables
    dataset=data_array                                              # transfer input to variable used throughout the function
    label=label_list                                                # transfer input to variable used throughout the function
    Units=Units_str                                                 # transfer input to variable used throughout the function
   
    if len(dataset )!= 118:                                         # check for an entry per element
        print('dataset has to have exactly one entry for each element(2D array (118,x))')
    elif len(dataset[0]) != len(label):                             # check that the amount of property labels is equal to the amount of properties plotted
        print('a title for each plotted property is needer in a list')
    elif all(isinstance(item, str) for item in label) == False:     # check that all property labels are strings
        print('the entries in the property label list have to be strings')
    elif type(Units) != str:                                        # check the units are given as a string
        print('the units have to be inserted as one string')
    else:                                                           # if everything passed you arrive here
        answer = 'o'
        while answer != 'y' and answer != 'n':                      # asks for user input 'y' or 'n' otherwise asks again, want a plot or not
            answer = str(input('Your input is ok. do you want a PSE plot?(y/n)'))
        
        if answer == 'y':                                           # check answer and plot or not
            plot_as_periodic_table(dataset, label, Units)            # call the plot function
        else:
            print('ok no periodic table plot')                                 


# data_array: Nan values will be plotted in whiten and therefore not visible, one column per property/slices, one row per element
# label_list: has to be a list of strings, will be used to label the legend 
# the Units string will be used as the title of the colorbar and should describe the property represented in the data_array
def plot_as_periodic_table(data_array, label_list, Units_str): #will plot an undefined number of slices of equal size from the data in a periodic table up to Oganesson(118) but crashes for wrong inputs!!!
    #define variables
    dataset=data_array                                              # transfer input to variable used throughout the function
    label=label_list                                                # transfer input to variable used throughout the function
    Units=Units_str                                                 # transfer input to variable used throughout the function
    i = 0                                                           # for counting
    j = 0                                                           # for counting
    elementX = 0                                                    # to temporarily store the x position of the respective element in the PTE
    elementY = 0                                                    # to temporarily store the y position of the respective element in the PTE
    LaAccounterX = 0                                                # to count through the Lanthanides and Actinides
    numberOfProperties = len(dataset[0])                            # get number of properties from number of columns in input
    maxValue = np.nanmax(dataset)                                   # gets the maximum value in the input that is not NaN
    radius = 1.2                                                    # adjust the size of the pie charts (1.2 ends in them touching each other in this format)
    font = 'Times New Roman'                                        # used to adjust the font type throughout the plot

    #create equal pieces and spacing in the pie chart
    data = [1]*numberOfProperties                                   # for the equal size of the slices, substitute with an array if different sizes are wanted
    explode =[0.05]*numberOfProperties                              # moves the slices away from the middle, done equal for all pieces, substitute with an array if wanted otherwise 
    colors = [None]*numberOfProperties                              # creates a working array for the colors in one individual pie chart, do not change

    # resizing of color-scheme
    individualColor=mpl.colormaps['brg'].resampled(50000)           # change the string if you want to use another colormap, do not change the number

    #initialise plot
    fig = plt.figure(figsize=(18,11))                               # creates a figure with these dimensions or x/y ratios, when changes all other sizing parameters like the radius, font-size etc. have to be readjusted

    # Adjust the spacing between subplots to make them closer together
    plt.subplots_adjust(wspace=0, hspace=0)                         # Adjust these values as needed


    #iterate through the elements
    while i<118:
        #define the current element
        elem = element(i+1)
   
        #check if there is a value for the group_id as the Lanthanoids and Actinoids do not have a value 
        if type(elem.group_id) == int :                             # for "normal element" where the group_id and period are accessible and can be used to locate the subplot 
            elementX = int(elem.group_id)                           # retrieve  group_id from mendeleev as X position
            elementY = int(elem.period)                             # retrieve  period from mendeleev as Y position
        elif LaAccounterX < 14:                                     # if there is no value in group_id you reached the 14 Lanthanoids, count through them to locate them
            elementY=9                                              # set y position to set value to position in the PTE
            elementX=LaAccounterX+3                                 # set x position to the LaAccounterX number plus an offset to fit the PTE
            LaAccounterX=LaAccounterX+1 
        else:                                                       # if there is no value in group_id and the counter is > 14  you reached the Actinoids
            elementY=10                                             # set y position to set value to position in the PTE
            elementX=LaAccounterX-11                                # set x position to the LaAccounterX number plus an offset minus the 14 Lanthanoids  to fit the PTE
            LaAccounterX=LaAccounterX+1
    
        #turn data from dataset-input into colors
        j=0
        while j < numberOfProperties:                               # iterate through the number of slices to plot; for different setting like 0= white adjust this paragraph to your liking
            if np.isnan(dataset[i][j]) == True:                     # for missing values the color is set to white 
                colors[j] = 'white'
            #elif dataset[i][j] ==  0                               # an example for an individual adjustment
            #    colors[j] = 'black'
            else:                                                   # if none of the previous criteria is true a color from the colormap according to the value is assigned
                PropertyJ= dataset[i][j]/(maxValue-0.00001)         # the use of maxValue makes sure the scalebar and color choice scale with the data in the dataset
                colors[j] = individualColor(PropertyJ)
            j=j+1
    
        #plot the individual subplot donut chart
        ax1 = plt.subplot2grid((11,18), (elementY-1, elementX-1))   # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position)
        plt.pie(data, radius=radius, colors=colors, explode=explode, startangle=90)               # create the subplot pie chart, data determines the splitting into slices, color sets the color of the slices and explode pushes all the pieces slightly out of the center to create the white space in-between, startangle = 90 sets the start to the top of the cycle 0 would result in the start being on the right side
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')        # define the circle in the center to turn the pie chart into a donut chart, (0,0) sets the center of the circle to the middle, 0.70 set the radius(can be adjusted to get a thicker or thinner donut), whit sets the color
        fig = plt.gcf()                                             # check you are in the current figure
        fig.gca().add_artist(centre_circle)                         # add circle in the middle of the pie chart
        plt.rcParams['axes.titley'] = 0.5                           # horizontal positioning of the title/ Element symbol, y is in axes-relative coordinates.
        plt.rcParams['axes.titlepad'] = -6                          # vertical positioning of the title/ Element symbol, in points 
        plt.rcParams['axes.titlesize'] = 18                         # change font-size of the title/ Element symbol
        plt.title(str(elem.symbol), fontsize=24, fontname = font)                    # set elemental symbol as title in the middle

        i=i+1   

 
    # Add Legend
    j=0
    while j < numberOfProperties:                                   # create a grey (#858481) color list for the legend
        colors[j] = '#858481'                                       # adjust color to your liking by changing the string
        j=j+1
    ax1 = plt.subplot2grid((11,18), (0,8), rowspan=2, colspan=2)    # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position), rowspan and colspan increase the size of this subplot
    plt.pie(data, radius=radius, colors=colors, startangle=90, labels=label, labeldistance=1.3,textprops={'fontsize': 24, 'fontweight': 'bold', 'fontname': font}, explode=explode)# create the subplot pie chart, data determines the splitting into slices, color sets the color of the piece and explode pushes all the pieces slightly out of the center to create the white space in-between, startangle = 90 sets the start to the top of the cycle 0 would result in the start being on the right side, labels uses your input to label the individual slices, label distance adjusts the position of the labels relative to the donut chart, textprops influences the fontsize of the labels and font type and so on
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')            # define the circle in the center to turn the pie chart into a donut chart, (0,0) sets the center of the circle to the middle, 0.70 set the radius(can be adjusted to get a thicker or thinner donut), whit sets the color          
    fig = plt.gcf()                                                 # check you are in the current figure
    fig.gca().add_artist(centre_circle)                             # add circle in the middle of the pie chart


    #Add color-bar
    ax1 = plt.subplot2grid((11,18), (10,1), rowspan=1, colspan=18)  # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position), rowspan and colspan increase the size of this subplot
    cax= plt.axes(ax1)                                              # needed to introduce an axis in this subplot to label the color-bar
    norm = mpl.colors.Normalize(vmin=0, vmax=maxValue)              # needed parameter for the color-bar function, adjust min Value and max Value according to dataset (define minValue)
    cmap = mpl.cm.brg                                               # needed parameter for the color-bar function, accesses the colormap
    divider = make_axes_locatable(ax1)                              # somehow necessary ???
    cax = divider.append_axes("bottom", size="180%", pad=0.2)       # Adjust size/height of the color-bar and pad/ positioning as needed
    cbar = plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation='horizontal') # creates the color-bar
    cbar.set_label(label=Units, fontsize = 24, fontname = font)                            # modifies the fontsize and font type of the label/unit
    # Adjust the font type of color-bar tick labels  and fontsize
    for label in cbar.ax.get_xticklabels():
        label.set_fontname(font)
        label.set_fontsize(24)
    # Set the axis spines (introduced before to adjust height of the color-bar) to transparent
    for spine in ax1.spines.values():
        spine.set_color('none')
    # Remove ticks and axis labels
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlabel('')
    ax1.set_ylabel('')

    # Display PTE
    plt.show()



# data_array: Nan values will be plotted in whiten and therefore not visible, one column per property/slices, one row per element
# label_list: hast to be a list of strings, will be used to label the legend 
# the Units string will be used as the title of the colorbar and should describe the property represented in the data_array
def plot_as_reduced_periodic_table(data_array, label_list,  Units_str): # will plot an undefined number of slices of equal size from the data in a periodic table up to Radon(86) but crashes for wrong inputs!!!
    #define variables
    dataset=data_array                                              # transfer input to variable used throughout the function
    label=label_list                                                # transfer input to variable used throughout the function
    Units=Units_str                                                 # transfer input to variable used throughout the function
    i = 0                                                           # for counting
    j = 0                                                           # for counting
    elementX = 0                                                    # to temporarily store the x position of the respective element in the PTE
    elementY = 0                                                    # to temporarily store the y position of the respective element in the PTE
    LaAccounterX = 0                                                # to count through the Lanthanides and Actinides
    numberOfProperties = len(dataset[0])                            # get number of properties from number of columns in input
    maxValue = np.nanmax(dataset)                                   # gets the maximum value in the input that is not NaN
    radius = 1.4                                                    # adjust the size of the pie charts 1.4 ends in them touching each other in this plot might have to be readjusted to your liking
    font = 'Times New Roman'                                        # used to adjust the font type throughout the plot

    #create equal pieces and spacing in the pie chart
    data = [1]*numberOfProperties                                   # for the equal size of the slices, substitute with an array if different sizes are wanted
    explode =[0.05]*numberOfProperties                              # moves the slices away from the middle, done equal for all pieces, substitute with an array if wanted otherwise 
    colors = [None]*numberOfProperties                              # creates a working array for the colours in one individual pie chart, do not change


    # resizing of color-scheme
    individualColor=mpl.colormaps['brg'].resampled(50000)           # change the string if you want to use another colormap, do not change the number

    #initialise plot
    fig = plt.figure(figsize=(18,9))                               # creates a figure with these dimensions or x/y ratios, when changes all other sizing parameters like the radius, fontsize etc. have to be readjusted



    #iterate through the elements
    while i<86:
        #define the current element
        elem = element(i+1)
        
        #check if there is a value for the group_id as the Lanthanoids and Actinoids do not have a value 
        if type(elem.group_id) == int :                             # for "normal element" where the group_id and period are accessible and can be used to locate the subplot 
            elementX = int(elem.group_id)                           # retrieve  group_id from mendeleev as X position
            elementY = int(elem.period)                             # retrieve  period from mendeleev as Y position
        elif LaAccounterX < 14:                                     # if there is no value in group_id you reached the 14 Lanthanoids, count through them to locate them
            elementY=8                                              # set y position to set value to position in the PTE
            elementX=LaAccounterX+3                                 # set x position to the LaAccounterX number plus an offset to fit the PTE
            LaAccounterX=LaAccounterX+1 

        #turn data from dataset-input into colors
        j=0
        while j < numberOfProperties:                               # iterate through the number of slices to plot; for different setting like 0= white adjust this paragraph to your liking
            if np.isnan(dataset[i][j]) == True:                     # for missing values the color is set to white 
                colors[j] = 'white'
            #elif dataset[i][j] ==  0                               # an example for an individual adjustment
            #    colors[j] = 'black'
            else:                                                   # if non of the previous criteria is true a color from the colormap according to the value is assigned
                PropertyJ= dataset[i][j]/(maxValue-0.00001)         # the use of maxValue makes sure the scalebar and color choice scale with the data in the dataset
                colors[j] = individualColor(PropertyJ)
            j=j+1

        #plot the individual subplot donut chart
        ax1 = plt.subplot2grid((9,18), (elementY-1, elementX-1))   # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position)
        plt.pie(data, radius=radius, colors=colors, explode=explode, startangle=90)               # create the subplot pie chart, data determines the splitting into slices, color sets the color of the slices and explode pushes all the pieces slightly out of the center to create the white space in-between, startangle = 90 sets the start to the top of the cycle 0 would result in the start being on the right side
        centre_circle = plt.Circle((0, 0), 0.85, fc='white')        # define the circle in the center to turn the pie chart into a donut chart, (0,0) sets the center of the circle to the middle, 0.70 set the radius(can be adjusted to get a thicker or thinner donut), whit sets the color
        fig = plt.gcf()                                             # check you are in the current figure
        fig.gca().add_artist(centre_circle)                         # add circle in the middle of the pie chart
        plt.rcParams['axes.titley'] = 0.5                           # horizontal positioning of the title/ Element symbol, y is in axes-relative coordinates.
        plt.rcParams['axes.titlepad'] = -6                          # vertical positioning of the title/ Element symbol, in points 
        plt.rcParams['axes.titlesize'] = 18                         # change fontsize of the title/ Element symbol
        plt.title(str(elem.symbol), fontsize=24, fontname = font)                    # set elemental symbol as title in the middle

        i=i+1   


    # Add Legend
    j=0
    while j < numberOfProperties:                                   # create a grey (#858481) color list for the legend
        colors[j] = '#858481'                                       # adjust color to your liking by changing the string
        j=j+1
    ax1 = plt.subplot2grid((9,18), (0,8), rowspan=2, colspan=2)    # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position), rowspan and colspan increase the size of this subplot
    plt.pie(data, radius=radius, colors=colors, startangle=90, labels=label, labeldistance=1.3,textprops={'fontsize': 24, 'fontweight': 'bold', 'fontname': font}, explode=explode)# create the subplot pie chart, data determines the splitting into slices, color sets the color of the piece and explode pushes all the pieces slightly out of the center to create the white space in-between, startangle = 90 sets the start to the top of the cycle 0 would result in the start being on the right side, labels uses your input to label the individual slices, label distance adjusts the position of the labels relative to the donut chart, textprops influences the font-size of the labels and font type and so on
    centre_circle = plt.Circle((0, 0), 0.85, fc='white')            # define the circle in the center to turn the pie chart into a donut chart, (0,0) sets the center of the circle to the middle, 0.70 set the radius(can be adjusted to get a thicker or thinner donut), whit sets the color          
    fig = plt.gcf()                                                 # check you are in the current figure
    fig.gca().add_artist(centre_circle)                             # add circle in the middle of the pie chart

    #Add color-bar
    ax1 = plt.subplot2grid((9,18), (8,1), rowspan=1, colspan=18)  # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position), rowspan and colspan increase the size of this subplot
    cax= plt.axes(ax1)                                              # needed to introduce an axis in this subplot to label the color-bar
    norm = mpl.colors.Normalize(vmin=0, vmax=maxValue)              # needed parameter for the color-bar function, adjust min Value and max Value according to dataset (define minValue)
    cmap = mpl.cm.brg                                               # needed parameter for the color-bar function, accesses the colormap
    divider = make_axes_locatable(ax1)                              # somehow necessary ???
    cax = divider.append_axes("bottom", size="180%", pad=0.2)       # Adjust size/height of the color-bar and pad/ positioning as needed
    cbar = plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation='horizontal') # creates the color-bar
    cbar.set_label(label=Units, fontsize = 24, fontname = font)                            # modifies the fontsize and font type of the label/unit
    # Adjust the font type of color-bar tick labels  and fontsize
    for label in cbar.ax.get_xticklabels():
        label.set_fontname(font)
        label.set_fontsize(24)
    # Set the axis spines (introduced before to adjust height of the color-bar) to transparent
    for spine in ax1.spines.values():
        spine.set_color('none')
    # Remove ticks and axis labels
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlabel('')
    ax1.set_ylabel('')

    # Display PSE
    plt.show()


#%% reduced PTE plot Version 2: logarithmic colorbar, different spacing
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from mendeleev import element
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker



# data_array: Nan values will be plotted in whiten and therefore not visible, one column per property/slices, one row per element; special case here: introduce Nan rows between your groups and adjust the data array in the beginning!!!
# label_list: hast to be a list of strings, will be used to label the legend 
# the Units string will be used as the title of the colorbar and should describe the property represented in the data_array
def plot_as_reduced_periodic_table(data_array, label_list, Units_str): # will plot an defined number of slices (6 in groups of 2) of equal size, separated by a smaller one from the data in a periodic table up to Radon(86) but crashes for wrong inputs!!!
    dataset=data_array                                              # transfer input to variable used throughout the function
    label=label_list                                                # transfer input to variable used throughout the function
    Units=Units_str                                                 # transfer input to variable used throughout the function
    i = 0                                                           # for counting
    j = 0                                                           # for counting
    elementX = 0                                                    # to temporarily store the x position of the respective element in the PTE
    elementY = 0                                                    # to temporarily store the y position of the respective element in the PTE
    LaAccounterX = 0                                                # to count through the Lanthanides and Actinides
    numberOfProperties = len(dataset[0])                            # get number of properties from number of columns in input
    radius = 1.25                                                   # adjust the size of the pie charts 1.25 ends in them touching each other in this setting
    font = 'Times New Roman'                                        # used to adjust the font type throughout the plot
    minValue = 0.1                                                  # set to your liking
    maxValue =10                                                    # set to your liking

    #creates two equal and one smaller slice and spacing in the pie chart
    data = (1,1,0.2,1,1,0.2,1,1,0.2)                                # for the equal size of the slices, substitute with an array if different sizes are wanted
    explode =[0.05]*numberOfProperties                              # moves the slices away from the middle, done equal for all pieces, substitute with an array if wanted otherwise 
    colors = [None]*numberOfProperties                              # creates a working array for the colors in one individual pie chart, do not change


    # create the colormap for this plot
    cmap = mpl.colormaps['brg'].resampled(50000)                    # change the string if you want to use another colormap, do not change the number
    newColormap = mpl.colors.SymLogNorm(0.1, vmin=minValue, vmax=maxValue)     # create the logarithmic color-scale  

    #initialise plot
    fig = plt.figure(figsize=(18,9))                                # creates a figure with these dimensions or x/y ratios, when changes all other sizing parameters like the radius, fontsize etc. have to be readjusted

    # Adjust the spacing between subplots to make them closer together
    plt.subplots_adjust(wspace=0, hspace=0)                         # Adjust these values as needed


    #iterate through the elements
    while i<86:
        #define the current element
        elem = element(i+1)
   
        #check if there is a value for the group_id as the Lanthanides and Actinides do not have a value 
        if type(elem.group_id) == int :                             # for "normal element" where the group_id and period are accessible and can be used to locate the subplot 
            elementX = int(elem.group_id)                           # retrieve  group_id from mendeleev as X position
            elementY = int(elem.period)                             # retrieve  period from mendeleev as Y position
        elif LaAccounterX < 14:                                     # if there is no value in group_id you reached the 14 Lanthanoids, count through them to locate them
            elementY=8                                              # set y position to set value to position in the PTE
            elementX=LaAccounterX+3                                 # set x position to the LaAccounterX number plus an offset to fit the PTE
            LaAccounterX=LaAccounterX+1 
        

        #turn data from dataset-input into colors
        j=0
        while j < numberOfProperties:                               # iterate through the number of slices to plot; for different setting like 0= white adjust this paragraph to your liking
            if dataset[i][j] <= minValue:                           # for smaller values than the chosen minValue the color is set to white
                colors[j] = 'white'
            #elif dataset[i][j] >=  maxValue:                       # an example for an individual adjustment
            #    colors[j] = 'black'
            else:                                                   # if none of the previous criteria is true a color from the colormap according to the value is assigned
                PropertyJ= dataset[i][j]
                colors[j] = cmap(newColormap(PropertyJ))            # otherwise store the color value determined by the logarithmic/ new Colormap and the data point 
            j=j+1
    
        #plot the individual subplot donut chart
        ax1 = plt.subplot2grid((9,18), (elementY-1, elementX-1))   # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position)
        plt.pie(data, radius=radius, colors=colors, explode=explode, startangle=95)               # create the subplot pie chart, data determines the splitting into slices, color sets the color of the slices and explode pushes all the pieces slightly out of the center to create the white space in-between, startangle = 90 sets the start to the top of the cycle 0 would result in the start being on the right side
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')        # define the circle in the center to turn the pie chart into a donut chart, (0,0) sets the center of the circle to the middle, 0.70 set the radius(can be adjusted to get a thicker or thinner donut), whit sets the color
        fig = plt.gcf()                                             # check you are in the current figure
        fig.gca().add_artist(centre_circle)                         # add circle in the middle of the pie chart
        plt.rcParams['axes.titley'] = 0.5                           # horizontal positioning of the title/ Element symbol, y is in axes-relative coordinates.
        plt.rcParams['axes.titlepad'] = -6                          # vertical positioning of the title/ Element symbol, in points 
        plt.rcParams['axes.titlesize'] = 18                         # change fontsize of the title/ Element symbol
        plt.title(str(elem.symbol), fontsize=24, fontname = font)                                 # set elemental symbol as title in the middle

        i=i+1     

 
    # Add Legend
    j=0
    while j < numberOfProperties:                                   # create a 2 x grey (#858481) and 1 x white color list for the legend
        colors[j] = '#858481'                                       # adjust color to your liking by changing the string
        colors[j+1] = '#858481'                                     # adjust color to your liking by changing the string
        colors[j+2] = 'white'                                       # adjust color to your liking by changing the string
        j=j+3
    ax1 = plt.subplot2grid((9,18), (0,7), rowspan=2, colspan=2)    # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position), rowspan and colspan increase the size of this subplot
    plt.pie(data, radius=radius, colors=colors, startangle=95, labels=label, labeldistance=1.2,textprops={'fontsize': 24, 'fontweight': 'bold', 'fontname': font}, explode=explode)# create the subplot pie chart, data determines the splitting into slices, color sets the color of the piece and explode pushes all the pieces slightly out of the center to create the white space in-between, startangle = 90 sets the start to the top of the cycle 0 would result in the start being on the right side, labels uses your input to label the individual slices, label distance adjusts the position of the labels relative to the donut chart, textprops influences the fontsize of the labels and font type and so on
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')            # define the circle in the center to turn the pie chart into a donut chart, (0,0) sets the center of the circle to the middle, 0.70 set the radius(can be adjusted to get a thicker or thinner donut), whit sets the color          
    fig = plt.gcf()                                                 # check you are in the current figure
    fig.gca().add_artist(centre_circle)                             # add circle in the middle of the pie chart


    #Add color-bar
    ax1 = plt.subplot2grid((9,18), (8,0), rowspan=1, colspan=18)    # create a subplotgrid (11 rows, 18 columns) and go to the position specified in the second brackets (Y position, X position), rowspan and colspan increase the size of this subplot
    cax= plt.axes(ax1)                                              # needed to introduce an axis in this subplot to label the color-bar
    divider = make_axes_locatable(ax1)                              # somehow necessary ???
    cax = divider.append_axes("bottom", size="100%", pad=0.2)       # Adjust size/height of the color-bar and pad/ positioning as needed
    cbar = plt.colorbar(mpl.cm.ScalarMappable(norm=newColormap, cmap=cmap), cax=cax, orientation='horizontal')# creates the color-bar
    
    # Define a custom tick formatter function to display the labels as integers and not as 10^x
    def custom_formatter(x, pos):
        if x >= 1:
            return f"{int(x)}"
        else:
            return f"{x:.2f}"
    # Use the custom formatter for the color-bar ticks
    cbar.ax.xaxis.set_major_formatter(ticker.FuncFormatter(custom_formatter))

    # set and adjust labels
    cbar.set_label(label=Units, fontsize = 24, fontname = font)                      # modifies the fontsize of the label/unit
    # Adjust the font type of color-bar tick labels  and fontsize
    for label in cbar.ax.get_xticklabels():
        label.set_fontname(font)
        label.set_fontsize(24)
    # Set the axis spines (introduced before to adjust height of the color-bar) to transparent
    for spine in ax1.spines.values():
        spine.set_color('none')
    # Remove ticks and axis labels
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlabel('')
    ax1.set_ylabel('')


    # Display PSE
    plt.show()


# %% test the function with dummy input
import numpy as np

a = np.empty( (118, 3))
i=0

while i<118:
    a[i][0]= i+1
    a[i][1]= int(i/2)
    a[i][2]= None
    i=i+1

#dummy data
b = ['Property1', 'Property2', 'Property3']
c ='Dummy title for dummy data'
d ='test unit'

#insert dummy data into function
check_input_periodic_table(a, b, c, d)
#plot_as_periodic_table(a, b, c, d) 
