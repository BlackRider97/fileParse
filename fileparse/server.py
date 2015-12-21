#!/usr/bin/env pythone

"""

Author: Rajneesh Mitharwal: Created at 21 December 2014

"""
from flask import (Flask, request,redirect, abort,jsonify,make_response)

from utils.config import Config

import logging
import time
import datetime
import json
import os

app = Flask(__name__)

config_obj = Config()
app.fileparse_config = Config().dataMap
app.preloaded_file_paths = {}

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request', 'pass': "false"} ), 400)


def get_all_directores_log_file_cache(_dir):
    if app.preloaded_file_paths.get(_dir, None):
        return app.preloaded_file_paths[_dir] 
    result = get_all_directores_log_file(_dir)
    app.preloaded_file_paths[_dir] = result
    return app.preloaded_file_paths[_dir]

def get_all_directores_log_file(_dir):
    if not _dir:
        []
    result = [] 
    dir_iteams = []
    try:
        dir_iteams = os.listdir(_dir)
    except:
        pass
    for _files in dir_iteams:
        abs_dirpath = str(os.path.join(_dir, _files))
        if _files and _files.endswith(".log"):
            if "analytics" not in abs_dirpath:
                continue 
            result.append(abs_dirpath)
            continue
        result.extend(get_all_directores_log_file(abs_dirpath))
    return result

@app.route('/get_logs/<int:time_stamp>/<tag>/<msisdn>', methods = ['GET'])
def get_analytics_logs(time_stamp, tag, msisdn):  
    if not time_stamp or not msisdn or not tag:
        abort(400)    
    directories = app.fileparse_config['directories']
    data = []
    for _dir in directories:
        all_log_files = get_all_directores_log_file_cache(_dir)
        for _file in all_log_files:
                for line in open(_file, "r"):
                    data_split = line.split("|")
                    if len(data_split) < 3:
                        continue
                    time_string = data_split[0].strip("UTC")
                    log_tag = data_split[1]
                    log_packet = ''.join(data_split[2:])
                    if tag != log_tag:
                        continue 
                    log_timestamp = int(time.mktime(datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M").timetuple()))
                    if log_timestamp < time_stamp:
                        continue
                    if not msisdn in log_packet:
                        continue
                    data.append(json.loads(log_packet))                                  
    return jsonify( { 'data': data, 'status': "ok" } ), 201

if __name__ == '__main__':
    logging.error("Starting file parse server.....")
    app.run(debug = True)     