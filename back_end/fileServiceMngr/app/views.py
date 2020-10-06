from flask import Flask, request, jsonify, make_response
import json
import service
import os
from config import config
import logging
import consumer
import threading



#
# logging.basicConfig(filename=config["logging"]["file_paths"], filemode="a+", format='%(asctime)s %(levelname)s-%(message)s',
#                      datefmt='%Y-%m-%d %H:%M:%S')
app = Flask(__name__)
#
# logging.info("Check")
serv = service.service()


@app.route('/client/history/<client_id>', methods=['GET'])
def getClientHistory(client_id) -> str:
    logging.info('ClientHistory API')
    try:
        clientHstry = serv.mongo_client.find(client_id)
        logging.info("MongoDb - Got client History")
        return jsonify(clientHstry)
    except Exception as e:
        logging.error("MongoDb - Got error on fetching data from MongoDb")
        return
    return jsonify(serv.mongoClient.find(client_id))


@app.route('/file/upload', methods=['GET', 'POST'])
def fileUpload():
    if request.method == 'POST':
        if request.files:
            #logging.info('fileUpload API')
            file = request.files["file"]
            req = request.form.to_dict(flat=False)
            # upload_file_bucket = 'weightsbucket'
            upload_file_key = 'weights/' + str(file.filename)
            try:
                serv.aws_client.upload_fileobj(file, config["aws"]["upload_file_bucket"], str(
                    config["aws"]["upload_file_key"]+"/"+str(file.filename)))
                logging.info("AWS S3 - Upload successful")
            except Exception as e:
                logging.error("AWS S3- Upload fail")
            url = '%s/%s/%s' % (serv.aws_client.meta.endpoint_url,
                                config["aws"]["upload_file_bucket"], str(upload_file_key))
            inserted_id = serv.mongo_client.create(req, file.filename, url)
            # TODO
            '''
           Update Mysql Database.
           #succ = update_client_history(request.form,id,file.filename)
           '''
            return json.dumps({"filename": file.filename, "mongo_db_id": str(inserted_id)})
    return make_response(jsonify(success=False))


@app.errorhandler(500)
def internal_error(exception):
    logging.error(exception)
    return False, 500


class ThreadedTask(threading.Thread):
    def __init__(self, ):
        threading.Thread.__init__(self)

    def run(self):
        queue_manager = consumer.RabbitMQManager()
        queue_manager.chan.basic_qos(prefetch_count=1)
        # define the queue consumption
        queue_manager.chan.basic_consume(queue=queue_manager.queue_name,
                                         on_message_callback=queue_manager.receive_msg)
        # start consuming
        queue_manager.chan.start_consuming()


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", False)

    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)

    task = ThreadedTask()

    task.start()

    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT,
            debug=ENVIRONMENT_DEBUG, use_reloader=False)
