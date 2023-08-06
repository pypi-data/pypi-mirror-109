# flask-githubcard
A flask's extension to generate a github card for yourself.

[中文文档](https://github.com/weijiang1994/flask-githubcard/blob/main/README-ZH.md)

### Quick Start 
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
Open your browser and visit your web page, github card like bellow here:

![1623293427414.png](https://7.dusays.com/2021/06/10/66d2716789d8d.png)

### Advanced
#### Configure yourself github info
```python
from flask import Flask
from flask_githubcard import GithubCard
app = Flask(__name__)

githubcard = GithubCard(app)
app.config['GITHUB_USERNAME'] = 'weijiang1994'
app.config['GITHUB_REPO'] = 'Blogin'
```

#### Choose theme
```html
<head>
    {{githubcard.init_css(theme='darkly')}}
</head>
<div>
    {{githubcard.generate_card(theme='darkly')}}
</div>
```

Darkly Theme

![1623294104103.png](https://7.dusays.com/2021/06/10/736fed4674429.png)

### Note

- Due to the use of GitHub's API without authorization, the number of unique IP visits is limited to 60 times per hour, if more than 60 times, 403 will be reported. If the frequency of access is too high, please go to the authorized account on GitHub
- In the case where the network state is not good, the access to Github will have timeout, which may cause the web page to not open!