const express = require('express');
const router = express.Router();
const fs = require('fs');
const regionModel = require('../models/regionModel');
var regionNameList = ['KRS', 'KAB', 'HEM', 'HAR'];

var jsonFolderPath = './python_scripts/predictions';

router.get('/regionList', (req, res) => {
    console.log('regionList');
    var regionModelList = [];
    regionNameList.forEach(value => {
        regionModelList.push(new regionModel(value, 'primary'));
    });
    res.status(200);
    res.json({ 'regionList': regionModelList });
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

router.get('/getDailynSeasonalData', (req, res) => {
    console.log('getDailynSeasonalData');
    var dailyDataObject = {};
    var objectName = ['AMCS STORAGE', 'ACTUAL INFLOW', 'AMCS OUTFLOW', 'DURATION'];
    var returnArrayName = ['storageArray', 'inflowArray', 'outflowArray', 'durationArray'];
    var year = req.query.years.split(' - ');
    var jsonStatspath = jsonFolderPath + '/' + req.query.region + '/stats' + '_' + year[0] + '_' + year[1] + '.json';
    var jsonPredpath = jsonFolderPath + '/' + req.query.region + '/predictions' + '_' + year[0] + '_' + year[1] + '.json';
    if (checkIfJsonExists(jsonStatspath) && checkIfJsonExists(jsonPredpath)) {
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
        dailyDataObject['datesArray'] = Object.keys(predictionData['ACTUAL INFLOW']);
        dailyDataObject['seasonalOutflowAmcsArray'] = Object.values(statsData['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']);
        dailyDataObject['seasonalOutflowNoAmcsArray'] = Object.values(statsData['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']);
        dailyDataObject['seasonalLabelsArray'] = ['Annual cumulative total seasonal outflow AMCS', 'Annual cumulative total seasonal outflow no AMCS'];
        res.status(200);
    } else {
        for (let i = 0; i < objectName.length; i++) {
            dailyDataObject[returnArrayName[i]] = [];
        }
        dailyDataObject['cumulativeInflowDiff'] = [];
        dailyDataObject['datesArray'] = [];
        dailyDataObject['seasonalOutflowAmcsArray'] = [];
        dailyDataObject['seasonalOutflowNoAmcsArray'] = [];
        dailyDataObject['seasonalLabelsArray'] = [];
        res.status(500);
    }
    res.json(dailyDataObject); 
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

module.exports = router;