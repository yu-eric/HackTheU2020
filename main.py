import os

from google.cloud import automl
from flask import Flask, request, render_template

model_id = os.environ['MODEL_ID']

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/', methods=['GET', 'POST'])
def home_page():
    # from flask import request
    if request.method == 'GET':
        context = {
            "done": False
        }
        return render_template('site.html', **context)
    else:
        # get image content from POST request inputs
        file = request.files["myFile"]
        image_content = b''
        for data in file.stream: # read image as a stream
            image_content += data

        # google api variables
        project_id = "alpine-infinity-290102"

        prediction_client = automl.PredictionServiceClient()

        # Get the full path of the model.
        model_full_id = automl.AutoMlClient.model_path(
            project_id, "us-central1", model_id
        )

        image = automl.Image(image_bytes=image_content)
        payload = automl.ExamplePayload(image=image)

        req = automl.PredictRequest(
            name=model_full_id,
            payload=payload,
        )
        response = prediction_client.predict(request=req)
        class_ = response.payload[0].display_name
        measure = response.payload[0].classification.score

        context = {
            "done": True,
            "guess_mal": class_ == "COVID_19",
            "class_": class_,
            "measure": '{:.2%}'.format(measure)
        }
        return render_template('site.html', **context)


@app.route('/about')
def about_page():
    return"<h1>about page</h1>"