from starlette.responses import RedirectResponse
from starlette import status


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
