''' Controller for the KeysightN7744A '''
# Matthew van Niekerk & Karl McNulty, RIT Integrated Photonics.
# 2019


import visa
rm = visa.ResourceManager() # define resource manager

# Keysight N7744A controller class; provides quick and simplifiesd functions to control the keysight power
# meter.
#
# Parameters:
# keysight_address              - string address to a resource (neds to be address to Keysight for class to
#                                 function)
# chan_no                       - channel number that the Keysight is using (options: 1, 2, 3, 4)
# show_output                   - prints the outputs of each function if True, otherwise outputs are suppressed
#
# Functions:
# output()                      - unique print statement which only prints if: show_output = True
# is_connected()                - returns the state of the keysight's connection (True - keysight is connecetd)
# release()                     - releases keysight from connection; no further commands can be called
#                                 thereafter
# set_channel()                 - set the current channel being used on the keysight (options: 1, 2, 3, 4)
# get_channel()                 - returns current channel number being used
# current units()               - returns the current units being used (0 - dBm, 1 - Watts)
# set_units_dbm()               - sets the units to be in dBm
# set_units_watts()             - sets the units to be in Watts
# current_measurement_mode()    - returns the current measurement mode (0 - absolute, 1 - relative)
# set_mmode_abs()               - sets the measurement mode to absolute
# set_mmode_rel()               - sets the measurement mode to relative
# current_ranging_mode()        - returns the current ranging mode (0 - manual, 1 - auto)
# set_rmode_auto()              - sets the ranging mode to auto
# set_rmode_manual()            - sets the ranging mode to manual
# current_sensing_time()        - returns the sensing time over which a measurement is made
# set_sensing_time()            - sets the sensing time
# measure_power()               - takes an optical power measurement and returns the value
#
class KeysightN7744A_Controller:

    # Initialization of the keysight controller
    def __init__(self, keysight_address = 'USB0::0x0957::0x3718::SG48101084::0::INSTR', verbose = False, chan_no = 1, show_output = True):
        # try to open the keysight resource
        try:
            self.power_meter = rm.open_resource(keysight_address)
            self.address = keysight_address
            if verbose:
                print('RESOURCE CONNECTED')
        except:
            print('RESOURCE NOT CONNECTED')

        # try to get the keysight device info
        try:
            self.connection = True
            self.device_info = self.power_meter.query('*IDN?')
            if verbose:
                print('CONNECTED TO: ' + self.device_info)
        except:
            self.connection = False
            self.device_info = None
            print('INCORRECT DEVICE CONNECTED')
            del self
        
        self.channel = str(chan_no)
        self.verbose = show_output

############### BEGIN: GENERAL CLASS FUNCTIONS ###############################################################
    # Allows for option of printing outputs or not
    def output(self, str):
        if self.verbose:
            print(str)
            return
        else:
            return

    # Return connection status of the Keysight
    def is_connected(self):
        return self.connection

    # Release the Keysight from connection
    def release(self):
        self.connection = False # indicate connection is done
        self.power_meter.close() # release connection to Keysight
        return
    
    # Reset the channel number (otherwise it is set to the inittialization value)
    def set_channel(self, new_chan_no):
        self.channel = str(new_chan_no)
        return
    
    # Get the current channel number
    def get_channel(self):
        return self.channel
############### END: GENERAL CLASS FUNCTIONS #################################################################

############### BEGIN: KEYSIGHT SPECIFIC FUNCTIONS ###########################################################
    # Return the current units identifier (1 or 0) and prints the curretn units being used
    def current_units(self):
        units = self.power_meter.query('SENS' + self.channel + ':POW:UNIT?') # 0 - dBm, 1 - Watts
        
        if '0' in units: # print out appropriate unit name based on identifier
            self.output('Current Units: dBm')
        elif '1' in units:
            self.output('Current Units: Watts')
        else:
            self.output('Units Set to Default (Watts)')
        
        return units

    # Set the units to be in dBm
    def set_units_dbm(self):
        try:
            for i in range(1,5):
                self.power_meter.write('SENS' + str(i) + ':POW:UNIT 0')
                #   self.output('Units Set To dBm')
        except:
            self.output('Could Not Set Units To dBm')
        return

    # Set the units to be in Watts
    def set_units_watts(self):
        try:
            for i in range(1,5):
                self.power_meter.write('SENS' + str(i) + ':POW:UNIT 1')
                #   self.output('Units Set To dBm')
        except:
            self.output('Could Not Set Units To dBm')
        return
    
    # Returns the measurement mode identifier (0 or 1) an prints the current measurement mode
    def current_measurement_mode(self):
        mode = self.power_meter.query('SENS' + self.channel + ':POW:REF:STAT?') # 0 - absolute, 1 - relative

        if '0' in mode: # print out appropriate measurement mode based on identifier
            self.output('Current Measurement Mode: Absolute')
        elif '1' in mode:
            self.output('Current Measurement Mode: Relative')
        else:
            self.output('Current Measurement Mode Could Not Be Found')

        return mode

    # Set the measurement mode to be Absolute
    def set_mmode_abs(self):
        try:
            self.power_meter.write('SENS' + self.channel + ':POW:REF:STAT 0')
            self.output('Measurment Mode Set to Absolute')
        except:
            self.output('Could Not Set Measurement Mode to Absolute')
        return

    # Set the measurement mode to be Relative
    def set_mmode_rel(self):
        try:
            self.power_meter.write('SENS' + self.channel + ':POW:REF:STAT 1')
            self.output('Measurment Mode Set to Relative')
        except:
            self.output('Could Not Set Measurement Mode to Relative')
        return

    # Returns the ranging mode identifier (0 or 1) an prints the current ranging mode
    def current_ranging_mode(self):
        mode = self.power_meter.query('SENS' + self.channel + ':POW:RANG:AUTO?') # 0 - manual mode, 1 - auto mode

        if '0' in mode: # print out appropriate ranging mode based on identifier
            self.output('Current Ranging Mode: Manual')
        elif '1' in mode:
            self.output('Current Ranging Mode: Auto')
        else:
            self.output('Current Ranging Mode Could Not Be Found')
        
        return mode

    # Set the ranging mode to be Auto
    def set_rmode_auto(self):
        try:
            self.power_meter.write('SENS' + self.channel + ':POW:RANG:AUTO 1')
            self.output('Ranging Mode Set to Auto')
        except:
            self.output('Could Not Set Ranging Mode to Auto')
        return

    # Set the ranging mode to be Manual
    def set_rmode_manual(self):
        try:
            self.power_meter.write('SENS' + self.channel + ':POW:RANG:AUTO 0')
            self.output('Ranging Mode Set to Manual')
        except:
            self.output('Could Not Set Ranging Mode to Manual')
        return

    # Returns the current amount of time the power meter will take whilemaking a measurement
    def current_sensing_time(self):
        sensing_time = self.power_meter.query('SENS' + self.channel + ':POW:ATIM?') # check sensing time
        return sensing_time

    # Set the sensing time for a measurement
    def set_sensing_time(self, time_sec):
        time = str(time_sec)
        try:
            self.power_meter.write('SENS' + self.channel + ':POW:ATIM ' + time) # set the sensing time
            self.output('Sensing Time Set To ' + time)
        except:
            self.output('Could Not Change Sensng Time')
        return

    # Take a measurement
    def measure_power(self):
        meas = self.power_meter.query('READ' + self.channel + ':POW?')
        return meas
    
    def measure_all(self):
        self.set_channel(1)
        meas1 = float(self.measure_power())
        self.set_channel(2)
        meas2 = float(self.measure_power())
        self.set_channel(3)
        meas3 = float(self.measure_power())
        self.set_channel(4)
        meas4 = float(self.measure_power())
        return meas1,meas2,meas3,meas4
############### END: KEYSIGHT SPECIFIC FUNCTIONS #############################################################