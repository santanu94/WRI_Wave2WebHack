const express = require('express');
const router = express.Router();
var spawn = require("child_process").spawn;
var scriptPath = 'D:/Personal_project/WRI_Wave2WebHack/client/backend/wri-w2wh-back/test_scripts/test_data_script.py';

router.get('/inflowCurrentCycle', (req, res) => {
    console.log('inflowCurrentCycle');
    var inflowCurrentCycleArray = [];
    var process = spawn('python', [scriptPath, req.query.region, 'inflowcc']);
    process.stdout.on('data', (data) => {
        var dataArrayString = data.toString();
        dataArrayString.substr(1, dataArrayString.indexOf(']')-1).split(',').forEach((element) => {
            inflowCurrentCycleArray.push(Number(element));
        });
    });
    process.stderr.on('data', (data) => {
        console.log(data.toString());
    });
    process.on('exit', (code) => {
        console.log('Process exited with '+ code);
        if (code === 0) {
            res.status(200);
        } else {
            res.status(500);
        }
        res.json({ 'inflowCurrentCycleArray': inflowCurrentCycleArray });
    });
});

router.get('/outflow', (req, res) => {
    console.log('outflow');
    var outcomeArray = [];
    var process = spawn('python', [scriptPath, req.query.region, 'outflow']);
    process.stdout.on('data', (data) => {
        var dataArrayString = data.toString();
        dataArrayString.substr(1, dataArrayString.indexOf(']')-1).split(',').forEach((element) => {
            outcomeArray.push(Number(element));
        });
    });
    process.stderr.on('data', (data) => {
        console.log(data.toString());
    });
    process.on('exit', (code) => {
        console.log('Process exited with '+ code);
        if (code === 0) {
            res.status(200);
        } else {
            res.status(500);
        }
        res.json({ 'outflowArray': outcomeArray });
    });
});

router.get('/inflowTrends', (req, res) => {
    console.log('inflowTrends');
    var inflowTrendsArray = [];
    var process = spawn('python', [scriptPath, req.query.region, 'inflowtrends']);
    process.stdout.on('data', (data) => {
        var dataArrayString = data.toString();
        dataArrayString.substr(1, dataArrayString.indexOf(']')-1).split(',').forEach((element) => {
            inflowTrendsArray.push(Number(element));
        });
    });
    process.stderr.on('data', (data) => {
        console.log(data.toString());
    });
    process.on('exit', (code) => {
        console.log('Process exited with '+ code);
        if (code === 0) {
            res.status(200);
        } else {
            res.status(500);
        }
        res.json({ 'inflowTrendsArray': inflowTrendsArray });
    });
});

module.exports = router;
