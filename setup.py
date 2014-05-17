from setuptools import setup

setup(
    name='thebot-webhooks',
    version='0.1.0',
    description='A generic purpose webhooks for TheBot.',
    keywords='thebot plugin',
    license = 'New BSD License',
    author="Alexander Artemenko",
    author_email='svetlyak.40wt@gmail.com',
    url='http://github.com/svetlyak40wt/thebot-webhooks/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    py_modules=['thebot_webhooks'],
    install_requires=[
        'thebot>=0.3.0',
        'times',
        'anyjson',
        'pytils',
    ],
)
