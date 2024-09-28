from flask import jsonify

class ApiResponse:

    @staticmethod
    def ok(data=None, total=None):
        """
        200 OK - General successful GET response.
        """
        response_data = {
            "data": {
                "total": total if total is not None else len(data) if data else 0,
                "items": data if data else []
            }
        }
        return jsonify(response_data), 200

    @staticmethod
    def created(data=None):
        """
        201 CREATED - Response for resource creation.
        """
        response_data = {
            "message": "Resource created successfully.",
            "data": {
                "items": data if data else []
            }
        }
        return jsonify(response_data), 201

    @staticmethod
    def updated(data=None, updated_fields=None):
        """
        200 OK - Response for resource update.
        """
        response_data = {
            "message": "Resource updated successfully.",
            "data": {
                "items": data if data else [],
                "updated_fields": updated_fields if updated_fields else []
            }
        }
        return jsonify(response_data), 200

    @staticmethod
    def deleted(deleted_id):
        """
        200 OK - Response for resource deletion.
        """
        response_data = {
            "message": "Resource deleted successfully.",
            "data": {
                "items": [
                    {
                        "deleted_id": deleted_id
                    }
                ]
            }
        }
        return jsonify(response_data), 200

    @staticmethod
    def bad_request(missing_field=None, message=None):
        """
        400 BAD REQUEST - Response for invalid request.
        """
        response_data = {
            "message": "Invalid request parameters.",
            "details": {
                "missing_field": missing_field,
                "message": message
            }
        }
        return jsonify(response_data), 400

    @staticmethod
    def not_found(resource, resource_id=None):
        """
        404 NOT FOUND - Response for missing resource.
        """
        if resource_id is None:
            # Mensaje general cuando no hay ID proporcionado
            response_data = {
                "message": f"No {resource} found.",
                "details": {
                    "resource": resource,
                    "message": f"No {resource} available or no results match the criteria."
                }
            }
        else:
            # Mensaje específico cuando se busca un recurso con ID
            response_data = {
                "message": "Resource not found.",
                "details": {
                    "resource": resource,
                    "id": resource_id,
                    "message": f"{resource} with id {resource_id} does not exist."
                }
            }
        
        return jsonify(response_data), 404

    @staticmethod
    def conflict(field=None, value=None, message=None):
        """
        409 CONFLICT - Response for conflict in the request.
        """
        response_data = {
            "message": f"Conflict: {message}",
            "details": {
                "field": field,
                "value": value,
                "message": message
            }
        }
        return jsonify(response_data), 409

    @staticmethod
    def internal_server_error():
        """
        500 INTERNAL SERVER ERROR - Response for unexpected server errors.
        """
        response_data = {
            "message": "An internal server error occurred. Please try again later."
        }
        return jsonify(response_data), 500
