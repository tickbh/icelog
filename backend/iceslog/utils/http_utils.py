from fastapi import Request


def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    
    return request.client.host

browsers = ["Firefox", "Chrome"]
def get_browser(request: Request):
    useragent = request.headers.get('User-Agent')
    if not useragent:
        return"unknow"
    
    for b in browsers:
        if b in useragent:
            return b
    return"unknow"