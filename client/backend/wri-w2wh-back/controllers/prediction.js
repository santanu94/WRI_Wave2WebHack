const express = require('express');
const router = express.Router();
var regionNameList = ['KRS', 'KAB', 'HEM', 'HAR'];

router.get('/inflowCurrentCycle', (req, res) => {
    console.log('inflowCurrentCycle');
    var inflowCurrentCycleArray = [];
    switch(req.query.region) {
        case regionNameList[0]:
            inflowCurrentCycleArray = [85, 72, 78, 75, 77, 75, 55, 55.3, 22.3, 59, 61, 84];
            break;
        case regionNameList[1]:
            inflowCurrentCycleArray = [11, 15, 59, 61, 84, 66, 55, 2, 33, 31, 111, 21, 17];
            break;
        case regionNameList[2]:
            inflowCurrentCycleArray = [11, 15, 59, 61, 77, 75, 88, 85, 97, 87, 59, 61, 84];
            break;
        case regionNameList[3]:
            inflowCurrentCycleArray = [7, 62, 15, 41, 66, 22, 11, 16.3, 22.3, 59, 61, 22];
            break;
    }
    res.status(200);
    res.json({ 'inflowCurrentCycleArray': inflowCurrentCycleArray });
});

router.get('/outflow', (req, res) => {
    console.log('outflow');
    var outcomeArray = [];
    switch(req.query.region) {
        case regionNameList[0]:
            outcomeArray = [85, 72, 78, 75, 77, 75, 55, 55.3, 22.3, 59, 61, 84];
            break;
        case regionNameList[1]:
            outcomeArray = [11, 15, 59, 61, 84, 66, 55, 2, 33, 31, 111, 21, 17];
            break;
        case regionNameList[2]:
            outcomeArray = [11, 15, 59, 61, 77, 75, 88, 85, 97, 87, 59, 61, 84];
            break;
        case regionNameList[3]:
            outcomeArray = [7, 62, 15, 41, 66, 22, 11, 16.3, 22.3, 59, 61, 22];
            break;
    }
    res.status(200);
    res.json({ 'outflowArray': outcomeArray });
});

router.get('/inflowTrends', (req, res) => {
    console.log('inflowTrends');
    var inflowTrendsArray = [];
    switch(req.query.region) {
        case regionNameList[0]:
            inflowTrendsArray = [85, 72, 78, 75, 77, 75, 55, 55.3, 22.3, 59, 61, 84];
            break;
        case regionNameList[1]:
            inflowTrendsArray = [11, 15, 59, 61, 84, 66, 55, 2, 33, 31, 111, 21, 17];
            break;
        case regionNameList[2]:
            inflowTrendsArray = [11, 15, 59, 61, 77, 75, 88, 85, 97, 87, 59, 61, 84];
            break;
        case regionNameList[3]:
            inflowTrendsArray = [7, 62, 15, 41, 66, 22, 11, 16.3, 22.3, 59, 61, 22];
            break;
    }
    res.status(200);
    res.json({ 'inflowTrendsArray': inflowTrendsArray });
});

module.exports = router;
