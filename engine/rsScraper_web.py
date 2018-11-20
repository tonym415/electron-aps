##!C:\\Program Files\\Python36\\python.exe
# The purpose of this script is to move .psarc Rocksmith CDLC files to the appropriate folder to play them in the game
#
# Author: Silent Thunda
# 27 Nov 16

import argparse
import os
import sys
import time
import json
import shutil
import yaml
import pprint
import fire


class CDLCScraper(object):
    config = {
        'src': r"C:\\Users\\thunda\\Downloads",
        'dst': r"C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Rocksmith2014\\dlc",
        'log': r"C:\\Users\\thunda\\.bin\\CDLC.json",
        'ext': '.psarc',
        'purpose': """
                    The purpose of this script is to move .psarc Rocksmith CDLC files to the appropriate folder to play
                    them in the game.
                 """
    }


    def __init__(self, src=CDLCScraper.config['src'], ):
        super(CDLCScraper, self).__init__()
        """  self.parser = argparse.ArgumentParser(description=CDLCScraper.config["purpose"])
        self.parser.add_argument('--src', '-s', help='Source folder for files', default=CDLCScraper.config['src'])
        self.parser.add_argument('--dst', '-d', help='Destination folder for files', default=CDLCScraper.config['dst'])
        self.parser.add_argument('--ext', '-x', help='File extension to search for', default=CDLCScraper.config['ext'])
        self.parser.add_argument('--cfg', '-c', help='specify config file (Yaml)')
        self.parser.add_argument('--log', '-l', help='Log file for script', default=CDLCScraper.config['log'])
        self.parser.add_argument('--run', '-r', help='Run Scaper', default=CDLCScraper().run()) """
        args = self.parser.parse_args()

        if args.cfg:
            ext = os.path.splitext( args.cfg )[1][1:]
            if ext == 'yml':
                ctype = 'Yaml'
            elif ext == 'json':
                ctype = 'JSON'
            else:
                ctype = None
            print("Using Config file('{}') -- lang: {}".format(args.cfg, ctype))
            with open(args.cfg, 'r') as cfgfile:
                # load configuration file
                cfg = yaml.load(cfgfile)

                # sync config contents with required args not including purpose
                setup = (key for key in type(self).config.keys() if key != 'purpose')
                for key in setup :
                    try:
                        if key == 'src': self.SRCFLD = cfg['setup'][key]
                        if key == 'dst': self.DESFLD = cfg['setup'][key]
                        if key == 'log': self.LOG = cfg['setup'][key]
                        if key == 'ext': self.EXT = cfg['setup'][key]
                    except KeyError:
                        continue
                        # print("{}: {}".format(key, cfg['setup'][key]))
        else:
            # if no arguments are sent, assign default files
            self.SRCFLD = args.src if args.src else type(self).config.get('src')
            self.DESFLD = args.dst if args.dst else type(self).config.get('dst')
            self.EXT = args.ext if args.ext else type(self).config.get('ext')
            self.LOG = args.log if args.log else type(self).config.get('log')
            self.TX = {}        # scraper instance transaction data dictionary



    def die(self):
        exit(-1)



    def viewConfig(self):
        print(self.info())
        sys.stdout.flush()

    def info(self):
        info = """
        Using the following files for processing:
        Source file:\n\t{SRCFLD}
        Destination file:\n\t{DESFLD}
        Log file:\n\t{LOG}
        File Ext:\n\t{EXT}
        """.format(**self.__dict__)
        return info

    def getCurrentTime(self, justtime=False):
        fmt = "%H:%M:%S" if justtime else "%Y-%m-%d %H:%M:%S"
        return time.strftime(fmt)

   

        # build transaction data object
        TX = {
            'init': now.toLocaleString(),
            'src': SRC,
            'dest': DST,
            'log': LOG,
            'files': [],
            'mvCount': 0
        };

        # loop through all files with specific extension
        mvCount = self.TX['mvCount']
        for file in [f for f in os.listdir(self.SRCFLD) if f.endswith(self.EXT)]:
            mvCount += 1
            self.TX['files'].append({'file': file, 'exec': self.getCurrentTime(True), 'epoch': time.time()})
            origName = "%s\%s" % (self.SRCFLD, file)  # fully qualified filename
            destName = "%s\%s" % (self.DESFLD, file)
            strMoving = "Moving %s =====>>>> %s" % (file, destName)     # human-readable output
            print(strMoving)
            sys.stdout.flush()
            
            shutil.move(origName, destName)

        strSuccess = "\nMoved %s files" % mvCount
        strError = "\nNo new CDLC's found!!!\n"
        strResult = strSuccess if mvCount > 0 else strError
        self.TX['mvCount'] = mvCount
        print(strResult)            # human-readable output
        sys.stdout.flush()

    def viewLog(self):
        print(self.LOG)
        sys.stdout.flush()

    def listFiles(self):
        import json
        with open(self.LOG, encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
        print(data)
        sys.stdout.flush()

    def run(self):
        self.collectCDLC()
        self.TX['term'] = self.getCurrentTime()

        # get current log (array of json object)
        logdata = None
        with open(self.LOG) as log:
            logdata = json.load(log)

            # add latest transaction to log data
            logdata.append(self.TX)
            log.close()

        # write data back to file
        with open(self.LOG, 'w') as log:
            json.dump(logdata, log, sort_keys=False, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    scraper = CDLCScraper()
    fire.Fire(scaper)    
    opt = """
        What would you like to do?
    
        r = run scaper
        l = view log
        q = quit
    
        Enter a letter, please:
    """
    print(opt)
    answer = None
    while True:
        if answer is None: pass
        elif answer in ['q', 'Q']: break
        elif answer in ['r', 'R']:
            print('\nProcessing New DLC\'s....\n{}'.format(CDLCScraper().getCurrentTime()))
            CDLCScraper().run()
        elif answer in ['l', 'L']:
            CDLCScraper().viewLog()
            answer = None
            pass
        else:
            print("{0}: {1} \r***** WARNING: ('{1}') Invalid Input *****""".format(type(answer), answer))
            pass
        answer = input(opt)
    
    print("\n\nThank you for using RS CDLC Scraper!!!\n")
    print("To Exit this window: Type 'exit' and press enter")
    exit(0)
else:
    CDLCScraper()
    #exit(1)
