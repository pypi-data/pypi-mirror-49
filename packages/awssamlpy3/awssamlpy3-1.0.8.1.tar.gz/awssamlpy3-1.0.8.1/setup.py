from setuptools import setup

def readme():
    with open('README.txt') as f:
        return f.read()
		
setup(
    name = 'awssamlpy3',
    version = '1.0.8.1',
    description = 'SAML federated API access for AWS',
    author='Neeharika',
    author_email='neeharika.mm@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
    ],
	long_description=readme(),
	install_requires=['beautifulsoup4','requests','html5lib','boto','configparser'],
	scripts=['aws-saml','aws-saml.bat']
)
