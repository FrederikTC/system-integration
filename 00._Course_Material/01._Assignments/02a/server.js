const express = require('express');
const fs = require('fs');
const csv = require('csv-parser');
const yaml = require('js-yaml');
const xml2js = require('xml2js');

const app = express();
const port = 3000;

// Utility functions for parsing
const parseText = (filePath) => {
    const data = fs.readFileSync(filePath, 'utf8');
    const lines = data.split('\n');
    const result = {};
    lines.forEach(line => {
        const [key, value] = line.split(': ');
        if (key && value) result[key.toLowerCase()] = value;
    });
    return result;
};

const parseXml = (filePath) => {
    const data = fs.readFileSync(filePath, 'utf8');
    let result = {};
    xml2js.parseString(data, (err, parsed) => {
        if (err) throw err;
        result = parsed.contact || parsed.product;
    });
    return result;
};

const parseYaml = (filePath) => {
    const data = fs.readFileSync(filePath, 'utf8');
    return yaml.load(data);
};

const parseJson = (filePath) => {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
};

const parseCsv = (filePath) => {
    return new Promise((resolve, reject) => {
        const results = [];
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (data) => results.push(data))
            .on('end', () => {
                resolve(results[0]);
            })
            .on('error', (err) => reject(err));
    });
};

// Endpoints
app.get('/parse/text', (req, res) => {
    const data = parseText('info/info.txt');
    res.json(data);
});

app.get('/parse/xml', (req, res) => {
    const data = parseXml('info/info.xml');
    res.json(data);
});

app.get('/parse/yaml', (req, res) => {
    const data = parseYaml('info/info.yaml');
    res.json(data);
});

app.get('/parse/json', (req, res) => {
    const data = parseJson('info/info.json');
    res.json(data);
});

app.get('/parse/csv', async (req, res) => {
    const data = await parseCsv('info/info.csv');
    res.json(data);
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
