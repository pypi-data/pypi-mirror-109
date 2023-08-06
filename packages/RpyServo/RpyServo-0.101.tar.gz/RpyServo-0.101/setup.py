from setuptools import setup, find_packages
 
setup(name='RpyServo',
 
      version='0.101',
 
      url='https://github.com/marceloquesada/RpyServo',
 
      author='Marcelo Quesada',
 
      author_email='m.mergulhao@aluno.ufabc.edu.br',
 
      description='An easy way to manage servos in a RPi',
 
      packages=find_packages(include=['RpyServo', 'Rpy.*']),
 
      long_description=open('README.md').read(),
      
      setup_requires=['pytest-runner'],
      
      tests_require=['pytest'],
 
      install_requires=['pigpio'])
