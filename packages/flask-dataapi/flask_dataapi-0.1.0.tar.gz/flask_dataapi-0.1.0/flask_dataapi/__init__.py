"""
Copyright (C) 2019 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask import jsonify, render_template


class DataApi:
    def __init__(self, app):
        self.app = app

    def render_json(self, template, **kwargs):
        return jsonify(**kwargs)

    def proxy(self, f, mode):
        if mode == 'ui':
            name = f.__name__
            render_func = render_template
        elif mode == 'api':
            name = f.__name__ + '_api'
            render_func = self.render_json
        else:
            raise ValueError('Unknown mode: %s' % mode)

        def func(*args, **kwargs):
            print(args)
            print(kwargs)
            return f(render_func, *args, **kwargs)

        func.__name__ = name
        return func

    def route(self, path, *args, **kwargs):
        def decorate(f):
            # Register the original path
            self.app.route(path, *args, **kwargs)(self.proxy(f, 'ui'))
            if path.endswith('/'):
                api_path = path + 'api.json'
            else:
                api_path = path + '.json'
            self.app.route(api_path, *args, **kwargs)(self.proxy(f, 'api'))

        return decorate
