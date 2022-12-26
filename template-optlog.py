
import optparse
import logging
import pandas
import json
import yaml
from os.path import isfile, isdir, exists

# -----------------------
# sample csv file
# -----------------------
# Sensor,Value,Unit
# temperature,0,deg
# humidity,100,percent
# pressure,1000,mmHg
# windspeed,5,Beaufort



#----------------------------------------------------------------------------
# main 
#----------------------------------------------------------------------------
def main():
   
    # Specify default values for optional arguments
    p = optparse.OptionParser()

    # Logging: Log file and directory
    p.add_option('--logDir', '-L', default='./log')
    p.add_option('--logFile', '-l', default='template.log')
    
    # Configuration: Settings will be provided in a file in yaml format
    p.add_option('--confDir', '-C', default='./config')
    p.add_option('--confFile', '-c', default='default.yaml')

    # Data files and directories
    p.add_option('--dataDir', '-D', default='./data')    
    p.add_option('--inputDir', '-I', default='input')
    p.add_option('--inputFile', '-i', default='in.csv')
    p.add_option('--outputDir', '-O', default='output')
    p.add_option('--outputFile', '-o', default='out.csv')
    p.add_option('--forceOverwrite', '-f', action="store_true", default=False)

    # Retrieve parameters
    options, arguments = p.parse_args() 

    # Assign option to variable 
    forceOverwrite = options.forceOverwrite

    # ----------------------------------------------------------------------------------------------
    # Configure logging: Remove any loggers for a clean start
    # ----------------------------------------------------------------------------------------------
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    # write to file and console
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(funcName)s _%(lineno)d_ %(message)s', 
                        datefmt='%Y-%m-%dT%H:%M:%S',
                        handlers=[
                                logging.FileHandler(options.logDir + '/' + options.logFile),
                                logging.StreamHandler()])
                                
    logging.info('Executing template-optlog.py ------------------------------------------- ')



    # ----------------------------------------------------------------------------------------------
    # procedure body
    # ----------------------------------------------------------------------------------------------
    inFile = options.dataDir + '/' + options.inputDir + '/' + options.inputFile

    if not exists(inFile):
        logging.error("inFile does not exist. You must provide a csv file in " + inFile)
        return()

    logging.info('Reading CSV file ' + inFile)
    di = pandas.read_csv(inFile, sep=',', header=0)

    # gather some info on dataframe
    logging.info('Shape: ' + str(di.shape))
    logging.info('Types: \n' + str(di.dtypes))
    logging.info('' + 
                    '\n -------------------------------------------------------------------------' + 
                    '\n Summary of inFile: ' +
                    '\n -------------------------------------------------------------------------' + 
                    '\n' + di.describe().to_string() +
                    '\n -------------------------------------------------------------------------') 


    # do some processing
    do = di

    # write results
    outDir = options.dataDir + '/' + options.outputDir
    if not isdir(outDir):
        logging.error("outDir does not exist. You must create directory " + outDir)
        return()

    outFile = outDir + '/' + options.outputFile
    if (not exists(outFile)) | forceOverwrite:
        logging.info('Writing CSV file ' + outFile)
        do.to_csv(outFile, index=False)
    else:
        logging.warning('File exists but forceOverwrite not specified. Not writing  ' + outFile)

    # ----------------------------------------------------------------------------------------------

    logging.info('Finished template-optlog.py ------------------------------------------- ')



#----------------------------------------------------------------------------
# invocation 
#----------------------------------------------------------------------------  
if __name__ == "__main__":
    main()