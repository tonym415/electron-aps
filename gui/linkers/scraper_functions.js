const fs = require('fs-extra');
const path = require('path');

// let EXT = '.psarc';
// let LOG = 'C:\\Users\\thunda\\.bin\\CDLC.json';
// let DST =
//     'C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Rocksmith2014\\dlc';
// let SRC = 'C:\\Users\\thunda\\Downloads';

// // test directory on used for testing
// let _SRC = 'C:\\Users\\thunda\\Desktop\\Tests';

export class FileMover {
    constructor(config) {

        // build transaction data object
        this._TRANSACTION = {
            init: new Date().toLocaleString(),
            src: this.config.SRC,
            dest: this.config.DST,
            log: this.config.LOG,
            files: [],
            mvCount: 0,
            errors: {
                errCount: 0,
                err: []
            }
        };

        this.log = () => {
            // read old log
            const prev = fs.readJsonSync(this.config.LOG, {
                throws: false
            });
            console.dir(prev);

            // append transaction
            prev.push(_TRANSACTION);
            console.dir(prev);

            // write log to file
            fs.outputJsonSync(LOG, prev);
            return {
                status: "success",
                message: `Log Appended [ ${this._TRANSACTION.log}]`
            }
        };
        this.listFiles = (path) => {
            list = [];
            return fs.readdirSync(path, function(err, items) {
                return undefined !== items ? items : list;
            });
        }
        this.processFiles = (src, dst, list) => {
            console.log(`Moving ${list.length} files from ${src} to ${dst}`);
            this._TRANSACTION.props.files.concat(list);
            // move each file in the list to destination
            for (var i = 0; i < fileList.length; i++) {
                // get root filename
                let file = fileList[i];
                this._TRANSACTION.props.files.push(file);

                let srcPath = src + '\\' + file;
                let dstPath = dst + '\\' + file;

                fs.moveSync(srcPath, dstPath);
                this._TRANSACTION.props.mvCount = this._TRANSACTION.props.mvCount + 1;
            }
        }

        this.run = () => {
            // aquire list of all files with proper extension
            var fileList = this.ListFiles(SRC).filter(item => {
                return EXT == path.extname(item);
            });

            // status strings
            let NOTFOUND = `[${SRC}] No files found with '${EXT}' extension!`;
            let FOUND = `Processing ${fileList.length} files with '${EXT}' extension!`;
            if (fileList.length > 0) {
                console.log(FOUND);
                // process files
                this.processFiles(SRC, DST, fileList);
                if (this._TRANSACTION.mvCount > 0) this._TRANSACTION.log();
                console.log('Done!!!');
            } else {
                console.log(NOTFOUND);
            }
        }

    };
}