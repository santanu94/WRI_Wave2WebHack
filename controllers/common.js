const express = require('express');
const router = express.Router();
const fs = require('fs');
const csv = require('csv-parser');
const regionModel = require('../models/regionModel');
const locModel = require('../models/locModel');
var regionNameList = ['KRS', 'KAB', 'HEM', 'HAR'];
var maxStorageRegionWise = [49.45, 50, 50, 50];
var weatherRegionNameList = ['Kodagu', 'Mysuru', 'Hassan'];

var latsArray = [12.3375, 12.2958, 13.0033];
var longsArray = [75.8069, 76.6394, 76.1004];

var jsonFolderPath = './python_scripts/predictions';
var datasetPath = './python_scripts/dataset/Weather';

router.get('/regionList', (req, res) => {
    console.log('regionList');
    var regionModelList = [];
    for (let i=0; i<regionNameList.length; i++) {
        regionModelList.push(new regionModel(regionNameList[i], 'primary', maxStorageRegionWise[i]));
    }
    res.status(200);
    res.json({ 'regionList': regionModelList });
});

router.get('/weatherRegionList', (req, res) => {
    console.log('weatherRegionList');
    res.status(200);
    res.json({ 'regionList': weatherRegionNameList });
});

router.get('/getYearlist', (req, res) => {
    console.log('getYearlist');
    var yearlist = [];
    for (let i = 2011; i <= 2020; i++) {
        yearlist.push(i + ' - ' + (i + 1));
    }
    res.status(200);
    res.json({ 'yearlist': yearlist });
});

router.get('/coordinatesList', (req, res) => {
    console.log('coordinatesList');
    var coordinatesList = [];
    for (let i=0; i<weatherRegionNameList.length; i++) {
        coordinatesList.push(new locModel(latsArray[i], longsArray[i], weatherRegionNameList[i]));
    }
    res.status(200);
    res.json({ 'coordinatesList': coordinatesList });
});

router.get('/getDailynSeasonalData', (req, res) => {
    console.log('getDailynSeasonalData');
    var dailyDataObject = {};
    var objectName = ['AMCS STORAGE', 'ACTUAL INFLOW', 'AMCS OUTFLOW', 'DURATION'];
    var returnArrayName = ['storageArray', 'inflowArray', 'outflowArray', 'durationArray'];
    var year = req.query.years.split(' - ');
    var jsonStatspath = jsonFolderPath + '/' + req.query.region + '/stats' + '_' + year[0] + '_' + year[1] + '.json';
    var jsonPredpath = jsonFolderPath + '/' + req.query.region + '/predictions' + '_' + year[0] + '_' + year[1] + '.json';
    if (checkIfFileExists(jsonStatspath) && checkIfFileExists(jsonPredpath)) {
        var statsData = JSON.parse(fs.readFileSync(jsonStatspath, {encoding:'utf8', flag:'r'}));
        var predictionData = JSON.parse(fs.readFileSync(jsonPredpath, {encoding:'utf8', flag:'r'}));
        if (!statsData['INFLOW CHANGE']) {
            dailyDataObject['cumulativeInflowDiff'] = [];
        } else {
            dailyDataObject['cumulativeInflowDiff'] = Object.values(statsData['INFLOW CHANGE']);
        }
        for (let i = 0; i < objectName.length; i++) {
            dailyDataObject[returnArrayName[i]] = Object.values(predictionData[objectName[i]]);
        }
        var dates_arr = [];
        Object.keys(predictionData['ACTUAL INFLOW']).forEach(element => {
            if (element.split('-')[0].length === 4) {
                const date = new Date(element);
                dates_arr.push(date.getDate() + '-' + (date.getMonth() + 1) + '-' + date.getFullYear());
            } else {
                dates_arr.push(element);
            }
        });
        dailyDataObject['datesArray'] = dates_arr;
        dailyDataObject['yearsPredictedvsActualData'] = statsData['CURRENT CYCLE TOTAL SEASONAL OUTFLOW PREDICTED VS ACTUAL'];
        dailyDataObject['yearsPredictedvsNormalData'] = statsData['CURRENT CYCLE TOTAL SEASONAL OUTFLOW PREDICTED VS NORMAL'];
        res.status(200);
    } else {
        for (let i = 0; i < objectName.length; i++) {
            dailyDataObject[returnArrayName[i]] = [];
        }
        dailyDataObject['cumulativeInflowDiff'] = [];
        dailyDataObject['datesArray'] = [];
        dailyDataObject['yearsPredictedvsActualData'] = {};
        dailyDataObject['yearsPredictedvsNormalData'] = {};
        res.status(500);
    }
    res.json(dailyDataObject);
});

router.get('/getWeatherData', (req, res) => {
    console.log('/getWeatherData');
    var weatherdatapath = datasetPath + '/' + 'opwnweathermap_historic.csv';
    var returnObject = {};
    var headersNotNeeded = ['dt', 'timezone', 'temp_min', 'temp_max', 'snow_1h', 'snow_3h', 'weather_id', 'weather_icon'];
    const results = [];
    if (checkIfFileExists(weatherdatapath)) {
        fs.createReadStream(weatherdatapath)
        .pipe(csv({
            mapHeaders: ({ header, index }) => {
                if (headersNotNeeded.indexOf(header) > -1) {
                    return null;
                } else {
                    return header;
                }
            }
        }))
        .on('data', (x) => {
            if (x.city_name === req.query.region && x.dt_iso.indexOf(req.query.date) > -1) {
                results.push(x);
            }
        })
        .on('end', () => {
            returnObject['weather'] = results;
            res.status(200);
            res.json(returnObject); 
        });
    } else {
        returnObject['weather'] = [];
        res.status(500);
        res.json(returnObject); 
    }
});

function checkIfFileExists(jsonpath) {
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

module.exports = router;