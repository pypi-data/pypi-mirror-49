from setuptools import setup, find_packages

setup(
        name='Flask-pyoidc',
        version='2.1.0',
        packages=['flask_pyoidc'],
        package_dir={'': 'src'},
        url='https://github.com/zamzterz/flask-pyoidc',
        license='Apache 2.0',
        author='Samuel Gulliksson',
        author_email='samuel.gulliksson@gmail.com',
        description='Flask extension for OpenID Connect authentication.',
        install_requires=[
            'oic==0.12',
            'Flask',
            'requests'
        ],
        package_data={'flask_pyoidc': ['files/parse_fragment.html']},
)
