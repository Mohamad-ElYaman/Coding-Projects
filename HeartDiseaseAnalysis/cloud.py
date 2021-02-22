from google.api_core.client_options import ClientOptions
import googleapiclient.discovery

def hello_world(request):
    request_json = request.get_json()
    if request.args and 'instances' in request.args:
        return predict(request.args.get('instances'))
    elif request_json and 'instances' in request_json:
        return predict(request_json['instances'])
    else:
        return f'data not found'

def predict(instances):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        region (str): regional endpoint to use; set to None for ml.googleapis.com
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS="key.json"
    project ='heartdisease-297903'
    region = 'us-east1'
    model = 'Heart_Disease_New'
    version = None
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': [instances]}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])
    
    return response