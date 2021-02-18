# emotion-recognition

Flask framework for emotion recognition

Install
-------
## clone the repository
    git clone https://github.com/amoljagadambe/emotion-recognition.git
    cd emotion-recognition
    # checkout the correct version
    git tag  # shows the tagged versions
    git checkout latest-tag-found-above
    
Create a virtualenv in the emotion-recognition directory and activate it::

    python -m venv venv
    venv\Scripts\activate.bat
    
Install Dependencies in Virtual Environment::

    pip install -r requirements.txt


    
 RUN
 ---
 
 On Virtual Environment::
    
   
    $ flask run        #the system variable loaded for this command
    or 
    $ python run.py    #you have to pass variable explictly i.e: --host: 0.0.0.0

    
    
Open http://localhost:3000/swagger-ui.html/ in a browser.