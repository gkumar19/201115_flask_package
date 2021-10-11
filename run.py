# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 23:06:32 2020

@author: Gaurav
"""
from flaskblog import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=80)