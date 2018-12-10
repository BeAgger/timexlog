"""
Main application
"""
import os
from timexlog import create_app

config_name = os.getenv('TIMEX_CONFIG')
app = create_app(config_name)
# app = create_app()

if __name__ == '__main__':
    app.run()
