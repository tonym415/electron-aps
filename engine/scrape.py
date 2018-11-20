import os, sys, time, json, shutil

config = {
        'src': r"C:\\Users\\thunda\Downloads",
        'dst': r"C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Rocksmith2014\dlc",
        'log': r"C:\\Users\\thunda\\.bin\\CDLC.json",
        'ext': '.psarc',
        'purpose': """
                    The purpose of this script is to move .psarc Rocksmith CDLC files to the appropriate folder to play
                    them in the game.
                 """
    }

def pr(strVar):
        print(strVar)
        sys.stdout.flush()

def getCurrentTime(justtime=False):
        fmt = "%H:%M:%S" if justtime else "%Y-%m-%d %H:%M:%S"
        return time.strftime(fmt)

def collectCDLC():

        # build transaction data object
        TX = {
            'init': getCurrentTime(),
            'src': config['src'],
            'dest': config['dst'],
            'log': config['log'],
            'ext': config['ext'],
            'files': [],
            'mvCount': 0
        }

        # loop through all files with specific extension
        mvCount = TX['mvCount']
        for file in [f for f in os.listdir(TX['src']) if f.endswith(TX['ext'])]:
            mvCount += 1
            TX['files'].append({'file': file, 'exec': getCurrentTime(True), 'epoch': time.time()})
            origName = "%s\%s" % (TX['src'], file)  # fully qualified filename
            destName = "%s\%s" % (TX['dst'], file)
            strMoving = "Moving %s =====>>>> %s" % (file, destName)     # human-readable output
            pr(strMoving)
            shutil.move(origName, destName)

        strSuccess = "\nMoved %s files" % mvCount
        strError = "\nNo new CDLC's found!!!\n"
        strResult = strSuccess if mvCount > 0 else strError
        TX['mvCount'] = mvCount
        pr(strResult)            # human-readable output

args = sys.argv
if len(args) > 0:
        if args[1] == "cfg":
                pr(config)
        else:
                pr(args)