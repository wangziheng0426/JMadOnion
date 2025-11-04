from __future__ import absolute_import
import base64
import json
import ssl
import traceback

try:
    # python3
    from urllib.request import urlopen, Request  # type: ignore
    from urllib.error import HTTPError  # type: ignore
except ImportError:
    # python2
    from urllib2 import urlopen, Request, HTTPError  # type: ignore

ssl.match_hostname = lambda cert, hostname: True  # type: ignore


def send(address, message, requestType, body=None, useAuth=False, username="", password="", useTls=True, caCert=None,
         insecure=False):
    """
        Used for sending requests that require a message body, like PUT and POST.
        Params: address of the webservice (string).
                message to the webservice (string).
                request type for the message (string, PUT or POST).
                message body for the request (string, JSON object).
    """
    try:
        httpString = "https://" if useTls else "http://"
        if not address.startswith(httpString):
            address = httpString + address
        url = address + message

        if body is not None:
            request = Request(url, data=body.encode('utf-8'))
            request.add_header('Content-Type', 'application/json; charset=utf-8')
        else:
            request = Request(url)

        request.get_method = lambda: requestType

        if useAuth:
            userPassword = '%s:%s' % (username, password)
            userPasswordEncoded = base64.b64encode(userPassword.encode('utf-8')).decode()
            request.add_header('Authorization', 'Basic %s' % userPasswordEncoded)

        context = None
        if useTls:
            context = ssl.create_default_context(cafile=caCert)
            context.check_hostname = not insecure
            context.verify_mode = ssl.CERT_NONE if insecure else ssl.CERT_REQUIRED

        response = urlopen(request, context=context)

        data = response.read().decode()
        data = data.replace('\n', ' ')

        try:
            data = json.loads(data)
        except:
            pass
        return data

    except HTTPError as e:
        if e.code == 401:
            return "Error: HTTP Status Code 401. Authentication with the Web Service failed. Please ensure that the authentication credentials are set, are correct, and that authentication mode is enabled."
        else:
            return traceback.print_exc()
    except Exception as e:
        return traceback.print_exc()
