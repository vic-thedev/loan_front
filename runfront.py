import os
import streamlit.web.bootstrap as bootstrap
from streamlit import config as _config

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'the_front.py')

_config.set_option("server.headless", True)
args = []

#streamlit.cli.main_run(filename, args)
bootstrap.run(filename, '', args, flag_options={})