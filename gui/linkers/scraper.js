const fs = require('fs-extra');
const mongojs = require('mongojs')
const path = require('path');
const db = mongojs('CDLC_log', ['records']);
db.on('error', function(err) {
    console.log('db error', err)
})
db.on('connect', function(err) {
    console.log('db connected', err)
})

function setVals() {
    defaults = {
        s: 'C:\\Users\\thunda\\Downloads',
        d: 'C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Rocksmith2014\\dlc',
        l: 'C:\\Users\\thunda\\.bin\\CDLC.json',
        x: '.psarc'
    }
    useDefaults = document.getElementById('useDefaults').checked;
    if (!useDefaults) defaults = {}
    document.getElementById('source-view').value = defaults.s || "";
    document.getElementById('destination-view').value = defaults.d || "";
    document.getElementById('log-view').value = defaults.l || "";
    document.getElementById('extension').value = defaults.x || ""
    if (useDefaults) swal('Defaults', 'Default values loaded...', 'success');
}

function toggle(elID) {
    document.getElementById(elID).classList.toggle('show');
}

function appendResults(str) {
    resultArea = document.getElementById('results')
    let currentValue = resultArea.value;
    resultArea.value = currentValue + str;
}

function updateResults(str) {
    resultArea = document.getElementById('results')
    resultArea.value = "";
    resultArea.value = str;
}

function showFolder(e) {
    el = document.getElementById(e.id);
    dispEl = document.getElementById(e.id + '-view');
    fullpath = el.files[0].path;
    dispEl.value = fullpath;
}

function transferFiles(result_element) {
    var options = {
        db: db,
        SRC: document.getElementById('source-view').value,
        DST: document.getElementById('destination-view').value,
        EXT: document.getElementById('extension').value,
        LOG: document.getElementById('log-view').value
    };

    opts = JSON.stringify(options, null, 4);
    alertOpts = {
        title: 'Scraping',
        text: opts,
        type: 'success',
        icon: '../images/RS2014.png'
    }

    swal(alertOpts);

    let status = new FileMover(options).run();
    toggle(result_element);
    updateResults(status);

    alertOpts.text = status;
    alertOpts.title = "Results";
    swal(alertOpts);
}

function showLog() {
    db.records.find(function(err, users) {
        if (err || !records) console.log("No records users found");
        else users.forEach(function(record) {
            appendResults(record);
        });
    });
    let result = db.records.find().sort({
        $natural: 1
    }).limit(10).toArray;
    updateResults(result);
}



/// ///////////////////////////////////////////////////////////////////////////
//  FileMover class

class FileMover {
    constructor(config) {
        // build transaction data object
        this.db = (config.db !== undefined ? config.db : {})
        this._TRANSACTION = {
            init: new Date().toLocaleString(),
            SRC: config.SRC,
            DST: config.DST,
            LOG: config.LOG,
            EXT: config.EXT,
            tx_status: [],
            files: [],
            mvCount: 0,
            errors: {
                errCount: 0,
                err: []
            }
        };

        this.statusUpdate = obj => {
            let ret = '';
            if (typeof obj === 'object') {
                ret = JSON.stringify(obj, null, 4);
            } else if (typeof obj === 'string') {
                ret = obj;
            }
            this._TRANSACTION.tx_status.push(ret);
        };

        this.log = () => {
            this.db.records.insert(this._TRANSACTION);
            this.statusUpdate(`Log Save added files: \n\n${this._TRANSACTION.files.join('\n')}`);
        };
        this.listFiles = path => {
            const list = [];
            return fs.readdirSync(path, function(err, items) {
                return undefined !== items ? items : list;
            });
        };
        this.processFiles = (src, dst, list) => {
            this.statusUpdate(`Moving ${list.length} files from ${src} to ${dst}`);
            this._TRANSACTION.files.concat(list);
            // move each file in the list to destination
            for (var i = 0; i < list.length; i++) {
                // get root filename
                let file = list[i];
                this._TRANSACTION.files.push(file);

                let srcPath = src + '\\' + file;
                let dstPath = dst + '\\' + file;

                fs.moveSync(srcPath, dstPath);
                this._TRANSACTION.mvCount = this._TRANSACTION.mvCount + 1;
            }
        };

        this.run = () => {
            // aquire list of all files with proper extension
            let fileList = this.listFiles(this._TRANSACTION.SRC).filter(item => {
                return this._TRANSACTION.EXT == path.extname(item);
            });

            // status strings
            let NOTFOUND = `[${config.SRC}] No files found with '${config.EXT}' extension!`;
            let FOUND = `Processing ${fileList.length} files with '${config.EXT}' extension!`;
            if (fileList.length > 0) {
                this.statusUpdate(FOUND);
                // process files
                this.processFiles(config.SRC, config.DST, fileList);
                if (this._TRANSACTION.mvCount > 0) this.log();
                this.statusUpdate('Done!!!');
            } else {
                this.statusUpdate(NOTFOUND);
            }
            return this._TRANSACTION.tx_status.join('\n');
        };
    }
}