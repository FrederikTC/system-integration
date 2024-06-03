const fs = require('fs');
const csv = require('csv-parser');
const yaml = require('js-yaml');
const xml2js = require('xml2js');

// Define file paths
const infoFiles = {
    text: 'info/info.txt',
    xml: 'info/info.xml',
    yaml: 'info/info.yaml',
    json: 'info/info.json',
    csv: 'info/info.csv'
};

const productFiles = {
    text: 'products/product.txt',
    xml: 'products/product.xml',
    yaml: 'products/product.yaml',
    json: 'products/product.json',
    csv: 'products/product.csv'
};

// Reading and parsing the text file
function parseText(filePath) {
    const data = fs.readFileSync(filePath, 'utf8');
    const lines = data.split('\n');
    const result = {};
    lines.forEach(line => {
        const [key, value] = line.split(': ');
        if (key && value) result[key.toLowerCase().replace(' ', '_')] = value;
    });
    return result;
}

// Reading and parsing the XML file
function parseXml(filePath) {
    const data = fs.readFileSync(filePath, 'utf8');
    let result = {};
    xml2js.parseString(data, { explicitArray: false }, (err, parsed) => {
        if (err) throw err;
        result = parsed;
    });
    return result;
}

// Reading and parsing the YAML file
function parseYaml(filePath) {
    const data = fs.readFileSync(filePath, 'utf8');
    return yaml.load(data);
}

// Reading and parsing the JSON file
function parseJson(filePath) {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
}

// Reading and parsing the CSV file
function parseCsv(filePath) {
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
}

// Parsing files
async function parseFiles(files) {
    const parsedData = {};
    parsedData.text = parseText(files.text);
    parsedData.xml = parseXml(files.xml);
    parsedData.yaml = parseYaml(files.yaml);
    parsedData.json = parseJson(files.json);
    parsedData.csv = await parseCsv(files.csv);
    return parsedData;
}

async function parseAll() {
    const contactInfo = await parseFiles(infoFiles);
    const productInventory = await parseFiles(productFiles);
    console.log("Contact Info:", contactInfo);
    console.log("Product Inventory:", productInventory);
}

parseAll();
