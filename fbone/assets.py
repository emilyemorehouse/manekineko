# -*- coding: utf-8 -*-
"""
    fbone.assets
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    fbone asset "pipeline"
"""

from flask_assets import Environment, Bundle


#: application css bundle
css_fbone = Bundle("less/style.less",
                       filters="less", output="css/style.css",
                       debug=False)

#: consolidated css bundle
css_all = Bundle("vendor/bootstrap/css/bootstrap-theme.css",
                 "vendor/bootstrap/css/bootstrap.css",
                 css_fbone, filters="cssmin", output="css/fbone.min.css")

#: vendor js bundle
js_vendor = Bundle("vendor/bootstrap/js/bootstrap.min.js",
                   filters="jsmin", output="js/vendor.min.js")


def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    webassets.register('js_vendor', js_vendor)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
