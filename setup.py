from distutils.core import setup

setup(name='DukeThinClient',
    version='1.0.0',
    description='A thin client for interacting with dockerized duke primitive',
    packages=['DukeThinClient'],
    install_requires=["numpy","pandas","requests","typing","gensim"],
    entry_points = {
        'd3m.primitives': [
            'distil.duke = DukeThinClient:duke'
        ],
    },
)
