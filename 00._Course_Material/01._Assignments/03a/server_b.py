from flask import Flask, jsonify
import requests
import csv
import json
import yaml
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Utility functions for parsing
def parse_text(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        data = {}
        for line in lines:
            key, value = line.strip().split(': ', 1)
            data[key.lower()] = value
        return data
    except Exception as e:
        return {"error": str(e)}

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = {child.tag: child.text for child in root}
        return data
    except Exception as e:
        return {"error": str(e)}

def parse_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        return {"error": str(e)}

def parse_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return {"error": str(e)}

def parse_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = next(reader)
        return data
    except Exception as e:
        return {"error": str(e)}

# Endpoints
@app.route('/info.text', methods=['GET'])
def get_text():
    data = parse_text('info/info.txt')
    return jsonify(data)

@app.route('/info.xml', methods=['GET'])
def get_xml():
    data = parse_xml('info/info.xml')
    return jsonify(data)

@app.route('/info.yaml', methods=['GET'])
def get_yaml():
    data = parse_yaml('info/info.yaml')
    return jsonify(data)

@app.route('/info.json', methods=['GET'])
def get_json():
    data = parse_json('info/info.json')
    return jsonify(data)

@app.route('/info.csv', methods=['GET'])
def get_csv():
    data = parse_csv('info/info.csv')
    return jsonify(data)

# Communication with Server A
@app.route('/fetch_from_server_a/<format>', methods=['GET'])
def fetch_from_server_a(format):
    try:
        response = requests.get(f'http://localhost:3000/info.{format}')
        response.raise_for_status()  # Raise HTTPError for bad responses
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
