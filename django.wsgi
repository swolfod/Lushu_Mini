import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/lushu_demo/demo_env/lib/python3.4/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/lushu_demo/Lushu_Mini')
sys.path.append('/var/www/lushu_demo/Lushu_Mini/Lushu_Mini')

os.environ['DJANGO_SETTINGS_MODULE'] = 'Lushu_Mini.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/var/www/lushu_demo/demo_env/bin/activate_this.py")
exec(open(activate_env).read())
# execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
