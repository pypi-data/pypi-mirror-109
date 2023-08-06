from distutils.core import setup

with open("pederas.md", "r") as f:
  pederas = f.read()

setup(
  name = 'apex_stats',        
  packages = ['apex_stats'],  
  version = '0.2.31',     
  license='MIT', 
  description = 'API wrapper for https://apex.tracker.gg',   
  author_email = 'yamozha16@protonmail.ch',  
  url = 'https://github.com/yamozha/apex_stats',  
  long_description=pederas,
  long_description_content_type='text/markdown'

)
