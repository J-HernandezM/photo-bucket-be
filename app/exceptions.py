from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Not Found", **kwargs):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, **kwargs)


class PhotoNotFound(NotFoundError):
    def __init__(self, **kwargs):
        super().__init__(detail="Photo Not Found", **kwargs)


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Access Denied", **kwargs):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, **kwargs)
