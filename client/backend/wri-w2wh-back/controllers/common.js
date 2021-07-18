const express = require('express');
const router = express.Router();
const regionModel = require('../models/regionModel');
var regionNameList = ['KRS', 'KAB', 'HEM', 'HAR'];

router.get('/storagePercent', (req, res) => {
    console.log('storagePercent');
    var storage = 35;
    res.status(200);
    res.json({ 'storagePercent': storage });
});

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

router.get('/getCumulativeInflowDiff', (req, res) => {
    console.log('getCumulativeInflowDiff');
    var cumulativeInflowDiff = 19.33;
    res.status(200);
    res.json({ 'cumulativeInflowDiff': cumulativeInflowDiff }); 
});

module.exports = router;