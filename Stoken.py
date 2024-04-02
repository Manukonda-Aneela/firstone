from itsdangerous import URLSafeTimedSerializer
from keys import secret_key,salt1,salt2
def token (data,salt):
    anee=URLSafeTimedSerializer('aneela@ is tester in the mnc company')
    return anee.dumps(data,salt1)