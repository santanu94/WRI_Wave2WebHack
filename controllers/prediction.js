const express = require('express');
const fs = require('fs');
const router = express.Router();
var spawn = require("child_process").spawn;
var scriptPath = './python_scripts/predictions_json.py';
var jsonFolderPath = './python_scripts/predictions';

var types = ['INFLOW', 'ACTUAL OUTFLOW', 'ACTUAL INFLOW', 'AMCS OUTFLOW'];
var predictionReturnObject = {};

router.get('/getInflowOutflowArrayData', (req, res) => {
    console.log('inflowCurrentCycle');
    var year = req.query.years.split(' - ');
    var jsonpath = jsonFolderPath + '/' + req.query.region + '/predictions' + '_' + year[0] + '_' + year[1] + '.json';
    if (checkIfJsonExists(jsonpath)) {
        readJsonData(jsonpath, res);
    } else {
        var process = spawn('python', [scriptPath, req.query.region, year[0]]);
        process.stderr.on('data', (data) => {
            console.log(data.toString());
        });
        process.on('exit', (code) => {
            console.log('Process exited with '+ code);
            if (code === 0) {
                if (checkIfJsonExists(jsonpath)) {
                    readJsonData(jsonpath, req, res);
                }
            } else {
                res.status(500);
                res.json(predictionReturnObject);
            }
        });
    }
});

router.get('/getExpandedData', (req, res) => {
    console.log('expanded');
    var year = req.query.years.split(' - ');
    var jsonpath = jsonFolderPath + '/' + req.query.region + '/predictions' + '_' + year[0] + '_' + year[1] + '.json';
    readJsonDataExpanded(jsonpath, req.query.typeOfData, res);
});

router.get('/getForecastData', (req, res) => {
    console.log('forecast');
    var year = req.query.years.split(' - ');
    var jsonpath = jsonFolderPath + '/' + req.query.region + '/predictions' + '_' + year[0] + '_' + year[1] + '.json';
    readForecastData(jsonpath, req.query.forecastDate, req.query.typeOfData, res);
});

function readForecastData(jsonpath, forecastDate, typeofdata, res) {
    fs.readFile(jsonpath, {encoding:'utf8', flag:'r'}, (err, data) => {
        var forcastData = {};
        if (err) {
            console.log(err);
            forcastData.datesArray = [];
            forcastData.dataArray = [];
            res.status(500);
        } else {
            var totaljsondata = JSON.parse(data);
            var dateValues = forecastDate.split('-');
            const date = new Date(+dateValues[2], +dateValues[1] - 1, +dateValues[0]);
            var foreDate = date.getFullYear()
                + '-' + 
                (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1)
                + '-' +
                (date.getDate() < 10 ? '0' + date.getDate() : date.getDate());
            console.log(foreDate);
            var forecastObject = totaljsondata['FORECAST'][foreDate][typeofdata];
            forcastData.datesArray = Object.keys(forecastObject).slice(0, 14);
            forcastData.dataArray = Object.values(forecastObject).slice(0, 14);
            res.status(200);
        }
        res.json(forcastData);
    });
}

router.get('/getInflowTrends', (req, res) => {
    console.log('trendsData');
    var inflowTrendsReturnObject = {};
    var yearlist = [];
    for (let i = 2011; i <= 2020; i++) {
        yearlist.push((i + ' - ' + (i + 1)).toString());
    }
    if (yearlist.indexOf(req.query.year) === 1) {
        var yearArray = yearlist[0].split(' - ');
        var jsonpath = jsonFolderPath + '/' + req.query.region + '/stats' + '_' + yearArray[0] + '_' + yearArray[1] + '.json';
        if (checkIfJsonExists(jsonpath)) {
            var statsData = JSON.parse(fs.readFileSync(jsonpath, {encoding:'utf8', flag:'r'}))['DAILY CUMULATIVE INFLOW'];
            var keysArray = Object.keys(statsData);
            inflowTrendsReturnObject.noOfValues = 1;
            inflowTrendsReturnObject.trendsValue = parseFloat(statsData[keysArray[keysArray.length - 1]].toFixed(2));
            res.status(200);
        }
    } else {
        inflowTrendsReturnObject.trendsLabel = yearlist.slice(0, yearlist.indexOf(req.query.year));
        inflowTrendsReturnObject.trendsArray = [];
        for (let i = 0; i <= yearlist.indexOf(req.query.year) - 1; i++) {
            var yearArray = yearlist[i].split(' - ');
            var jsonpath = jsonFolderPath + '/' + req.query.region + '/stats' + '_' + yearArray[0] + '_' + yearArray[1] + '.json';
            if (checkIfJsonExists(jsonpath)) {
                var statsYearData = JSON.parse(fs.readFileSync(jsonpath, {encoding:'utf8', flag:'r'}))['DAILY CUMULATIVE INFLOW'];
                var keysArray = Object.keys(statsYearData);
                inflowTrendsReturnObject.trendsArray.push(parseFloat(statsYearData[keysArray[keysArray.length - 1]].toFixed(2)));
            }
        }
        inflowTrendsReturnObject.noOfValues = inflowTrendsReturnObject.trendsArray.length;
        res.status(200);
    }
    res.json(inflowTrendsReturnObject);
});

function checkIfJsonExists(jsonpath) {
    console.log('pathcheck');
    try {
        if (fs.existsSync(jsonpath)) {
          return true;
        }
    } catch(err) {
        console.error(err);
    }
    return false;
}

function readJsonData(jsonpath, res) {
    fs.readFile(jsonpath, {encoding:'utf8', flag:'r'}, (err, data) => {
        if (err) {
            console.log(err);
            predictionReturnObject.inflowCurrentCycleArray = [];
            predictionReturnObject.outflowArray = [];
            predictionReturnObject.actualInflowArray = [];
            predictionReturnObject.amcsOutflowArray = [];
            res.status(500);
        } else {
            var totaljsondata = JSON.parse(data);
            types.forEach(element => {
                let jsondata = totaljsondata[element];
                var transArray = initializeResultArray();
                Object.keys(jsondata).forEach(key => {
                    transArray[parseInt(key.split('-')[1])-1] += jsondata[key];
                });
                var elementName = '';
                if (element === 'INFLOW') {
                    elementName = 'inflowCurrentCycleArray';
                } else if (element === 'ACTUAL OUTFLOW') {
                    elementName = 'outflowArray';
                } else if (element === 'ACTUAL INFLOW') {
                    elementName = 'actualInflowArray';
                } else if (element === 'AMCS OUTFLOW') {
                    elementName = 'amcsOutflowArray';
                } 
                predictionReturnObject[elementName] = transArray.slice(5, 12).concat(transArray.slice(0, 5));
            });
            res.status(200);
        }
        res.json(predictionReturnObject);
    });
}

function readJsonDataExpanded(jsonpath, typeofdata, res) {
    var typesOfData = [];
    if (typeofdata === 'INFLOW') {
        typesOfData = [
            typeofdata,
            'ACTUAL INFLOW'
        ];
    } else {
        typesOfData = [
            typeofdata,
            'OUTFLOW',
            'AMCS OUTFLOW'
        ];
    }
    fs.readFile(jsonpath, {encoding:'utf8', flag:'r'}, (err, data) => {
        var expandedData = {};
        if (err) {
            console.log(err);
            expandedData.predictedfullYearData = [];
            expandedData.actual_amcsfullYearData = [];
            res.status(500);
        } else {
            var totaljsondata = JSON.parse(data);
            typesOfData.forEach(dataType => {
                var listFirstHalf = [];
                var listSecondHalf = [];
                var partjsondata = totaljsondata[dataType];
                Object.keys(partjsondata).forEach(
                    key => {
                        if (parseInt(key.split('-')[1]) < 6) {
                            listSecondHalf.push(partjsondata[key]);
                        } else {
                            listFirstHalf.push(partjsondata[key]);
                        }
                    }
                );
                if (dataType === 'OUTFLOW') {
                    expandedData.outflowfullYearData = listFirstHalf.concat(listSecondHalf);
                }
                if (dataType === 'INFLOW' || dataType === 'ACTUAL OUTFLOW') {
                    expandedData.predictedfullYearData = listFirstHalf.concat(listSecondHalf);
                } else {
                    expandedData.actual_amcsfullYearData = listFirstHalf.concat(listSecondHalf);
                }
            });
            res.status(200);
        }
        res.json(expandedData);
    });
}

function initializeResultArray() {
    let resultList = [];
    for (let i = 1; i <= 12; i++) {
        resultList.push(0);
    }
    return resultList;
}

module.exports = router;
