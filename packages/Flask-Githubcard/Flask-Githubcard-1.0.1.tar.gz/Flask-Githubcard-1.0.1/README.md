# flask-githubcard
A flask's extension to generate a github card for yourself.

###Quick Start 
```shell
pip install flask-githubcard
```
 Step 1: Initial the extension
 ```python
from flask import Flask
from flask_githubcard import GithubCard
app = Flask(__name__)
githubcard = GithubCard(app)
```
Step 2: In your `<head>` section of your base template add the following code:
```html
<head>
    {{githubcard.init_css()}}
    {{githubcard.init_js()}}
</head>
```
Step 3: Render the github card in your template.
```html
<div>
    {{githubcard.generate_card()}}
</div>
```

### Advanced
#### Configure yourself github info
```python
from flask import Flask
from flask_githubcard import GithubCard
app = Flask(__name__)

githubcard = GithubCard(app)
```
