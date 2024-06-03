const express = require('express');
const fs = require('fs');
const csv = require('csv-parser');
const yaml = require('js-yaml');
const xml2js = require('xml2js');
const axios = require('axios');

const app = express();
const port = 3000;

// Utility functions for parsing
const parseText = (filePath) => {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        const lines = data.split('\n');
        const result = {};
        lines.forEach(line => {
            const [key, value] = line.split(': ');
            if (key && value) result[key.toLowerCase()] = value;
        });
        return result;
    } catch (error) {
        return { error: error.message };
    }
};

const parseXml = (filePath) => {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        let result = {};
        xml2js.parseString(data, (err, parsed) => {
            if (err) throw err;
            result = parsed;
        });
        return result;
    } catch (error) {
        return { error: error.message };
    }
};

const parseYaml = (filePath) => {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return yaml.load(data);
    } catch (error) {
        return { error: error.message };
    }
};

const parseJson = (filePath) => {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return { error: error.message };
    }
};

const parseCsv = (filePath) => {
    return new Promise((resolve, reject) => {
        try {
            const results = [];
            fs.createReadStream(filePath)
                .pipe(csv())
                .on('data', (data) => results.push(data))
                .on('end', () => {
                    resolve(results[0]);
                })
                .on('error', (err) => reject({ error: err.message }));
        } catch (error) {
            reject({ error: error.message });
        }
    });
};

// Endpoints
app.get('/info.text', (req, res) => {
    const data = parseText('info/info.txt');
    res.json(data);
});

app.get('/info.xml', (req, res) => {
    const data = parseXml('info/info.xml');
    res.json(data);
});

app.get('/info.yaml', (req, res) => {
    const data = parseYaml('info/info.yaml');
    res.json(data);
});

app.get('/info.json', (req, res) => {
    const data = parseJson('info/info.json');
    res.json(data);
});

app.get('/info.csv', async (req, res) => {
    const data = await parseCsv('info/info.csv');
    res.json(data);
});

// Communication with Server B
app.get('/fetch_from_server_b/:format', async (req, res) => {
    const format = req.params.format;
    try {
        const response = await axios.get(`http://localhost:5000/info.${format}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).send(`Error fetching data from Server B: ${error.message}`);
    }
});

app.listen(port, () => {
    console.log(`Server A is running on http://localhost:${port}`);
});
