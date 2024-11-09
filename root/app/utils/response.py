from flask import jsonify

def create_response(success, result=None, status=None, message=None):
    """
    Creates a standardized JSON response for API endpoints.

    Args:
        success (bool): Whether the request was successful.
        result (list/dict, optional): The data to return in the response. Defaults to None.
        status (int): The HTTP status code.
        message (str, optional): An optional message to include in the response. Defaults to None.

    Returns:
        tuple: A tuple containing the JSON response and the status code.
    """
    response = {
        "success": success,
        "result": result if result is not None else [],
        "status": status
    }
    if message:
        response["message"] = message
    return jsonify(response), status