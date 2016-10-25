########################################################################################################################
########################################################################################################################
#
#   Written By: Rory Barton-Grimley
#   Written For: CCAR - ARSENL
#
#   Sensl Conversion function written by Bryce Garby
#
#   ##############################################################
#   Creation Date:      2016/10/24
#   Latest Modified:    2016/10/25
#   ##############################################################
#
#   Description: Insert description of FIFO conversion here.
#
########################################################################################################################
########################################################################################################################

from fifo_processing_configure import *
from atmospheric_fifo_functions import *

##########################################################################################################

# Start timer for tracking processing time
start_time = time.time()

# Begin loop to process raw data and save as binned distances for each channel
for ii, fifo_fname in enumerate(fifo_files[start_file:(start_file + integration_time)]):

    # Generate timestamp for raw data file 
    time_stamp, file_start_time, original_file_start = compute_time_stamp(fifo_fname)
    
    # Generating Starting and Saving information from first raw data file
    if ii == 0:
        print 'Starting Data Time Stamp', time_stamp
        print

        # Keeping the timestamp of the first data file
        first_time_stamp = time_stamp
        
        # Generate the names for the saved processed data files
        copol_header = header_info(fifo_fname, 'copol', integration_time, bin_width, save_data_type)
        crosspol_header = header_info(fifo_fname, 'crosspol', integration_time, bin_width,save_data_type)
    
    # Perform the conversion from binary data file to absolute time and channel number
    absolute_time, channel = SENSLconv(fifo_fname) 

    # Perform the conversion from absolute time and channel number to binned copol and crosspol distances
    copol_binned, crosspol_binned = process_times(absolute_time, channel)

    # Append processed data to Pandas Dataframes
    copol_df[original_file_start] = copol_binned
    crosspol_df[original_file_start] = crosspol_binned


    ##########################################################################################################
    
    print ii + 1, ' of ', integration_time, 'Seconds Processed'

    # Generating Ending and Saving information from first raw data file       
    if (ii+1) == integration_time:
        print
        print 'Ending Data Time Stamp', time_stamp
        print

        # Keeping the timestamp of the first data file
        last_file_time = time_stamp

##############################################################################################################

print '###################################################'
print '%s Seconds of Copol & Crosspol Data Binned to %s m'%(integration_time,bin_width)
print
print '###################################################'
print 

##############################################################################################################

# Decision Function for saving Pandas data frame to text or HDF 
save_fifo_data(copol_header, crosspol_header, save_data, save_data_type)

##############################################################################################################

print '###################################################'
print
print("--- %s second run time ---" % (time.time() - start_time))