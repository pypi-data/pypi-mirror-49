#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import argparse
import configparser
import json
import logging
from functools import wraps
import numpy as np
import subprocess
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS

from tensorflow_inference_service import TensorFlowInferenceService
from gen_client import gen_client
from mxnet_inference_service import MxnetInferenceService
from onnx_inference_service import OnnxInferenceService
from pytorch_onnx_inference_service import PytorchOnnxInferenceService
from h2o_inference_service import H2oInferenceService
from scikitlearn_inference_service import ScikitlearnInferenceService
from xgboost_inference_service import XgboostInferenceService
from pmml_inference_service import PmmlInferenceService
from spark_inference_service import SparkInferenceService
from service_utils import request_util
import python_predict_client
import base64_util

logger = logging.getLogger("simple_tensorflow_serving")

# Define parameters
parser = argparse.ArgumentParser()

parser.add_argument(
    "--host",
    default=os.environ.get("STFS_HOST", "0.0.0.0"),
    help="The host of the server(eg. 0.0.0.0)")
parser.add_argument(
    "--port",
    default=int(os.environ.get("STFS_PORT", "8500")),
    help="The port of the server(eg. 8500)",
    type=int)
parser.add_argument(
    "--enable_ssl",
    default=bool(os.environ.get("STFS_ENABLE_SSL", "")),
    help="If enable RESTfull API over https")
parser.add_argument(
    "--secret_pem",
    default=os.environ.get("STFS_SECRET_PEM", "secret.pem"),
    help="SSL pem file")
parser.add_argument(
    "--secret_key",
    default=os.environ.get("STFS_SECRET_KEY", "secret.key"),
    help="SSL key file")
parser.add_argument(
    "--model_name",
    default=os.environ.get("STFS_MODEL_NAME", "default"),
    help="The name of the model(eg. default)")
parser.add_argument(
    "--model_base_path",
    default=os.environ.get("STFS_MODEL_BASE_PATH", "./model"),
    help="The file path of the model(eg. 8500)")
parser.add_argument(
    "--model_platform",
    default=os.environ.get("STFS_MODEL_PLATFORM", "tensorflow"),
    help="The platform of model(eg. tensorflow)")
parser.add_argument(
    "--model_config_file",
    default=os.environ.get("STFS_MODEL_CONFIG_FILE", ""),
    help="The file of the model config(eg. '')")
# TODO: type=bool not works, make it true by default if fixing exit bug
parser.add_argument(
    "--reload_models",
    default=os.environ.get("STFS_RELOAD_MODELS", ""),
    help="Reload models or not(eg. True)")
parser.add_argument(
    "--custom_op_paths",
    default=os.environ.get("STFS_CUSTOM_OP_PATHS", ""),
    help="The path of custom op so files(eg. ./)")
parser.add_argument(
    "--session_config",
    default=os.environ.get("STFS_SESSION_CONFIG", "{}"),
    help="The json of session config")
parser.add_argument(
    "--debug",
    default=os.environ.get("STFS_DEBUG", ""),
    help="Enable debug for flask or not(eg. False)",
    type=bool)
parser.add_argument(
    "--log_level",
    default=os.environ.get("STFS_LOG_LEVEL", "info"),
    help="The log level(eg. info)")
parser.add_argument(
    "--enable_auth",
    default=os.environ.get("STFS_ENABLE_AUTH", ""),
    help="Enable basic auth or not(eg. False)",
    type=bool)
parser.add_argument(
    "--auth_username",
    default=os.environ.get("STFS_AUTH_USERNAME", "admin"),
    help="The username of basic auth(eg. admin)")
parser.add_argument(
    "--auth_password",
    default=os.environ.get("STFS_AUTH_PASSWORD", "admin"),
    help="The password of basic auth(eg. admin)")
parser.add_argument(
    "--enable_colored_log",
    default=os.environ.get("STFS_ENABLE_COLORED_LOG", ""),
    help="Enable colored log(eg. False)",
    type=bool)
parser.add_argument(
    "--enable_cors",
    default=os.environ.get("STFS_ENABLE_CORS", "True"),
    help="Enable cors(eg. True)",
    type=bool)
parser.add_argument(
    "--enable_b64_autoconvert",
    default=os.environ.get("STFS_B64_AUTOCONVERT", ""),
    help="Enable auto convert b64 string(eg. False)",
    type=bool)
parser.add_argument(
    "--download_inference_images",
    default=os.environ.get("STFS_DOWNLOAD_INFERENCE_IMAGES", "True"),
    help="Download inference images(eg. True)",
    type=bool)
parser.add_argument(
    "--server_backend",
    default=os.environ.get("STFS_SERVER_BACKEND", "uwsgi"),
    help="The web server backend(eg. uwsgi)")

# TODO: Support auto-complete
#argcomplete.autocomplete(parser)

args = parser.parse_args(sys.argv[1:])

for arg in vars(args):
  logger.info("{}: {}".format(arg, getattr(args, arg)))

if args.enable_colored_log:
  import coloredlogs
  coloredlogs.install()

if args.log_level == "info" or args.log_level == "INFO":
  logger.setLevel(logging.INFO)
elif args.log_level == "debug" or args.log_level == "DEBUG":
  logger.setLevel(logging.DEBUG)
elif args.log_level == "error" or args.log_level == "ERROR":
  logger.setLevel(logging.ERROR)
elif args.log_level == "warning" or args.log_level == "WARNING":
  logger.setLevel(logging.WARNING)
elif args.log_level == "critical" or args.log_level == "CRITICAL":
  logger.setLevel(logging.CRITICAL)

if args.debug == True:
  logger.setLevel(logging.DEBUG)


def verify_authentication(username, password):
  """
  Verify if this user should be authenticated or not.

  Args:
    username: The user name.
    password: The password.

  Return:
    True if it passes and False if it does not pass.
  """
  if args.enable_auth:
    if username == args.auth_username and password == args.auth_password:
      return True
    else:
      return False
  else:
    return True


def requires_auth(f):
  """
  The decorator to enable basic auth.
  """

  @wraps(f)
  def decorated(*decorator_args, **decorator_kwargs):

    auth = request.authorization

    if args.enable_auth:
      if not auth or not verify_authentication(auth.username, auth.password):
        response = Response(
            "Need basic auth to request the resources", 401,
            {"WWW-Authenticate": '"Basic realm="Login Required"'})
        return response

    return f(*decorator_args, **decorator_kwargs)

  return decorated


# Initialize flask application
application = Flask(__name__, template_folder='templates')

if args.enable_cors:
  CORS(application)

UPLOAD_FOLDER = os.path.basename('static')
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if (os.path.isdir(UPLOAD_FOLDER)):
  pass
else:
  logging.warn("Create path to host static files: {}".format(UPLOAD_FOLDER))
  os.mkdir(UPLOAD_FOLDER)

# Example: {"default": TensorFlowInferenceService}
model_name_service_map = {}


def init_inference_service():

  if args.model_config_file != "":
    # Read from configuration file
    with open(args.model_config_file) as data_file:
      model_config_file_dict = json.load(data_file)
      # Example: [{u'platform': u'tensorflow', u'name': u'tensorflow_template_application', u'base_path': u'/Users/tobe/code/simple_tensorflow_serving/models/tensorflow_template_application_model/'}, {u'platform': u'tensorflow', u'name': u'deep_image_model', u'base_path': u'/Users/tobe/code/simple_tensorflow_serving/models/deep_image_model/'}]
      model_config_list = model_config_file_dict["model_config_list"]

      for model_config in model_config_list:
        # Example: {"name": "tensorflow_template_application", "base_path": "/", "platform": "tensorflow"}
        model_name = model_config["name"]
        model_base_path = model_config["base_path"]
        model_platform = model_config.get("platform", "tensorflow")
        custom_op_paths = model_config.get("custom_op_paths", "")
        session_config = model_config.get("session_config", {})

        if model_platform == "tensorflow":
          inference_service = TensorFlowInferenceService(
              model_name, model_base_path, custom_op_paths, session_config)
        elif model_platform == "mxnet":
          inference_service = MxnetInferenceService(model_name,
                                                    model_base_path)
        elif model_platform == "onnx":
          inference_service = OnnxInferenceService(model_name, model_base_path)
        elif model_platform == "pytorch_onnx":
          inference_service = PytorchOnnxInferenceService(
              model_name, model_base_path)
        elif model_platform == "h2o":
          inference_service = H2oInferenceService(model_name, model_base_path)
        elif model_platform == "scikitlearn":
          inference_service = ScikitlearnInferenceService(
              model_name, model_base_path)
        elif model_platform == "xgboost":
          inference_service = XgboostInferenceService(model_name,
                                                      model_base_path)
        elif model_platform == "pmml":
          inference_service = PmmlInferenceService(model_name, model_base_path)
        elif model_platform == "spark":
          inference_service = SparkInferenceService(model_name,
                                                    model_base_path)

        model_name_service_map[model_name] = inference_service
  else:
    # Read from command-line parameter
    if args.model_platform == "tensorflow":
      session_config = json.loads(args.session_config)
      inference_service = TensorFlowInferenceService(
          args.model_name, args.model_base_path, args.custom_op_paths,
          session_config)
    elif args.model_platform == "mxnet":
      inference_service = MxnetInferenceService(args.model_name,
                                                args.model_base_path)
    elif args.model_platform == "h2o":
      inference_service = H2oInferenceService(args.model_name,
                                              args.model_base_path)
    elif args.model_platform == "onnx":
      inference_service = OnnxInferenceService(args.model_name,
                                               args.model_base_path)
    elif args.model_platform == "pytorch_onnx":
      inference_service = PytorchOnnxInferenceService(args.model_name,
                                                      args.model_base_path)
    elif args.model_platform == "scikitlearn":
      inference_service = ScikitlearnInferenceService(args.model_name,
                                                      args.model_base_path)
    elif args.model_platform == "xgboost":
      inference_service = XgboostInferenceService(args.model_name,
                                                  args.model_base_path)
    elif args.model_platform == "pmml":
      inference_service = PmmlInferenceService(args.model_name,
                                               args.model_base_path)
    elif args.model_platform == "spark":
      inference_service = SparkInferenceService(args.model_name,
                                                args.model_base_path)

    model_name_service_map[args.model_name] = inference_service

  # Start thread to periodically reload models or not
  if args.reload_models == "True" or args.reload_models == "true":
    for model_name, inference_service in model_name_service_map.items():
      if inference_service.platform == "tensorflow":
        inference_service.dynamically_reload_models()


# The API to render the dashboard page
@application.route("/", methods=["GET"])
@requires_auth
def index():
  return render_template(
      "index.html", model_name_service_map=model_name_service_map)


# The API to process inference request
@application.route("/", methods=["POST"])
@requires_auth
def inference():
  json_result, status_code = do_inference()

  # Do not use encoder for json for performance
  #response = jsonify(json.loads(json.dumps(json_result, cls=NumpyEncoder)))
  response = jsonify(json_result)
  response.status_code = status_code
  return response


def do_inference(save_file_dir=None):
  """
  Args:
    save_file_dir: Path to save data.

  Return:
    json_data: The inference result or error message.
    status code: The HTTP response code.
  """

  if request.content_type.startswith("application/json"):
    # Process requests with json data
    try:
      # Get the json for Python 3 instead of get the data
      json_data = request.json

      if not isinstance(json_data, dict):
        result = {"error": "Invalid json data: {}".format(request.data)}
        return result, 400
    except Exception as e:
      result = {"error": "Invalid json data: {}".format(request.data)}
      return result, 400
  elif request.content_type.startswith("multipart/form-data"):
    # Process requests with raw image
    try:
      json_data = request_util.create_json_from_formdata_request(
          request, args.download_inference_images, save_file_dir=save_file_dir)
    except Exception as e:
      result = {"error": "Invalid form-data: {}".format(e)}
      return result, 400
  else:
    logger.error("Unsupported content type: {}".format(request.content_type))
    return {"error": "Error, unsupported content type"}, 400

  if "model_name" in json_data:
    model_name = json_data.get("model_name")
  else:
    model_name = "default"

  if model_name not in model_name_service_map:
    return {
        "error":
        "Invalid model name: {}, available models: {}".format(
            model_name, model_name_service_map.keys())
    }, 400

  inferenceService = model_name_service_map[model_name]

  if args.enable_b64_autoconvert:
    try:
      # Decode base64 string and modify request json data
      base64_util.replace_b64_in_dict(json_data)
    except Exception as e:
      result = {"error": e.message}
      return result, 400

  try:
    result = inferenceService.inference(json_data)
    return result, 200
  except Exception as e:
    logging.warn("Inference error: {}".format(e.message))
    result = {"error": e.message}
    return result, 400


@application.route('/health', methods=["GET"])
def health():
  return Response("healthy")


@application.route('/image_inference', methods=["GET"])
def image_inference():
  return render_template('image_inference.html')


@application.route('/run_image_inference', methods=['POST'])
def run_image_inference():
  predict_result = do_inference(
      save_file_dir=application.config['UPLOAD_FOLDER'])
  json_result = json.dumps(predict_result)

  file = request.files['image']
  image_file_path = os.path.join(application.config['UPLOAD_FOLDER'],
                                 file.filename)

  return render_template(
      'image_inference.html',
      image_file_path=image_file_path,
      predict_result=json_result)


@application.route('/json_inference', methods=["GET"])
def json_inference():
  return render_template('json_inference.html')


@application.route('/run_json_inference', methods=['POST'])
def run_json_inference():
  # TODO: Fail to parse u'{\r\n  "inputs": [\'\\n\\x1f\\n\\x0e\\n\\x01a\\x12\\t\\n\\x07\\n\\x05hello\\n\\r\\n\\x01b\\x12\\x08\\x12\\x06\\n\\x04\\x00\\x00\\x00?\']\r\n}\r\n          '
  # {
  # "inputs": ['\n\x1f\n\x0e\n\x01a\x12\t\n\x07\n\x05hello\n\r\n\x01b\x12\x08\x12\x06\n\x04\x00\x00\x00?']
  #}
  json_data_string = request.form["json_data"]
  json_data = json.loads(json_data_string)
  model_name = request.form["model_name"]
  model_version = request.form["model_version"]
  signature_name = request.form["signature_name"]

  request_json_data = {
      "model_name": model_name,
      "model_version": model_version,
      "signature_name": signature_name,
      "data": json_data
  }

  predict_result = python_predict_client.predict_json(
      request_json_data, port=args.port)

  return render_template('json_inference.html', predict_result=predict_result)


# The API to get all models
@application.route("/v1/models", methods=["GET"])
@requires_auth
def get_models():
  result = [
      inference_service.get_detail()
      for inference_service in model_name_service_map.values()
  ]
  return json.dumps(result)


# The API to get default of the model
@application.route("/v1/models/<model_name>", methods=["GET"])
@requires_auth
def get_model_detail(model_name):

  if model_name not in model_name_service_map:
    return "Model not found: {}".format(model_name)

  inference_service = model_name_service_map[model_name]
  return json.dumps(inference_service.get_detail())

  #return "Model: {}, version: {}".format(model_name, model_version)


# The API to get example json for client
@application.route("/v1/models/<model_name>/gen_json", methods=["GET"])
@requires_auth
def gen_example_json(model_name):
  inference_service = model_name_service_map[model_name]
  data_json_dict = gen_client.gen_tensorflow_client(inference_service, "json",
                                                    model_name)

  return json.dumps(data_json_dict)


# The API to get example json for client
@application.route("/v1/models/<model_name>/gen_client", methods=["GET"])
@requires_auth
def gen_example_client(model_name):
  client_type = request.args.get("language", default="bash", type=str)
  inference_service = model_name_service_map[model_name]
  example_client_string = gen_client.gen_tensorflow_client(
      inference_service, client_type, model_name)

  return example_client_string


@application.route("/generate_clients", methods=["GET"])
def generate_clients():
  return render_template('generate_clients.html')


@application.route("/run_generate_clients", methods=['POST'])
def run_generate_clients():
  model_name = request.form["model_name"]
  signature_name = request.form["signature_name"]
  language = request.form["language"]

  result = python_predict_client.get_gen_json_and_clients(
      model_name, signature_name, language, port=args.port)

  return render_template("generate_clients.html", result=result)


if args.server_backend != "uwsgi":
  # This will be called by main() or new process by uwsgi, only init once for uwsgi
  init_inference_service()


def start_flask_server():

  # Start the HTTP server
  # Support multi-thread for json inference and image inference in same process
  if args.enable_ssl:
    # Can pass ssl_context="adhoc" for auto-sign certification
    application.run(
        host=args.host,
        port=args.port,
        threaded=True,
        debug=args.debug,
        ssl_context=(args.secret_pem, args.secret_key))
  else:
    application.run(
        host=args.host, port=args.port, threaded=True, debug=args.debug)


def start_uwsgi_process():
  pyargv_string = ""
  for arg in vars(args):
    if getattr(args, arg) == False:
      # TODO: Pass the empty string if the param is False
      pyargv_string += "--{}={} ".format(arg, "")
    elif str(arg) == "server_backend":
      pyargv_string += "--{}={} ".format(arg, "flask")
    else:
      pyargv_string += "--{}={} ".format(arg, getattr(args, arg))

  uwsgi_conf_dict = {
      "uwsgi": {
          "module": "simple_tensorflow_serving.server",
          "pyargv": pyargv_string,
          "http": "{}:{}".format(args.host, args.port),
          "socket": "/tmp/uwsgi.sock",
          "close-on-exec": True,
          "enable-threads": True,
          "http-keepalive": 1,
          "http-auto-chunked": 1,
          # TODO: Log format refers to https://uwsgi-docs.readthedocs.io/en/latest/LogFormat.html
          #"log-format": '%(ltime) "%(method) %(uri) %(proto)" %(status) %(size) "%(referer)" "%(uagent)"'
      }
  }

  uwsgi_ini_file = "/tmp/uwsgi.ini"
  with open(uwsgi_ini_file, "w") as f:
    uwsgi_conf = configparser.ConfigParser()
    uwsgi_conf.read_dict(uwsgi_conf_dict)
    uwsgi_conf.write(f)

  uwsgi_command = "uwsgi --ini {}".format(uwsgi_ini_file)
  logging.info("Try to run command: {}".format(uwsgi_command))
  subprocess.call(uwsgi_command, shell=True)


def main():
  if args.server_backend == "flask":
    start_flask_server()
  elif args.server_backend == "uwsgi":
    start_uwsgi_process()
  else:
    logging.error(
        "Unknown server backend: {}, only support uwsgi, flask".format(
            args.server_backend))
    exit(1)


if __name__ == "__main__":
  main()
