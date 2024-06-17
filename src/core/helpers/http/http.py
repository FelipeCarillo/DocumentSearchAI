import json
from typing import Any, Dict, Optional


class HTTPRequest:
    def __init__(self, event: Dict[str, Any]):
        self.method: str = event.get("httpMethod", "")
        self.headers: Dict[str, Any] = event.get("headers", {})
        self.parameters: Dict[str, Any] = self._extract_parameters(event)
        self.body: Dict[str, Any] = self._extract_body(event)

    def _extract_parameters(self, event: Dict[str, Any]) -> Dict[str, Any]:
        parameters = {}
        # Merging queryStringParameters and pathParameters into parameters
        if event.get("queryStringParameters"):
            parameters.update(event.get("queryStringParameters"))
        if event.get("pathParameters"):
            parameters.update(event.get("pathParameters"))
        return parameters

    def _extract_body(self, event: Dict[str, Any]) -> Dict[str, Any]:
        body = event.get("body")
        if body and event.get("isBase64Encoded", False):
            import base64

            body = base64.b64decode(body).decode("utf-8")
        if body and isinstance(body, str):
            body = json.loads(body)
        return body


class HTTPResponse:
    def __init__(self, message: str, statusCode: int, data: Dict[str, Any] = None):
        self.message = message
        self.statusCode = statusCode
        self.data = data if data else {}

    def to_dict(self) -> Dict[str, Any]:
        response = {
            "statusCode": self.statusCode,
            "body": json.dumps({"message": self.message, "data": self.data}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }
        return response


class OK(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 200, data)


class Created(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 201, data)


class NoContent(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 204, data)


class BadRequest(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 400, data)


class Unauthorized(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 401, data)


class Forbidden(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 403, data)


class NotFound(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 404, data)


class UnprocessableEntity(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 422, data)


class InternalServerError(HTTPResponse):
    def __init__(self, message: str, data: Dict[str, Any] = None):
        super().__init__(message, 500, data)
