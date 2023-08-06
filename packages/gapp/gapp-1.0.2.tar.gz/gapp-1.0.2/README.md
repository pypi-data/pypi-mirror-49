# gapp
![travis-badge](https://travis-ci.org/Madoshakalaka/gapp.svg?branch=master)

Buttons and other graphics elements to control code.

## How to Use

`pip install gapp`

```python
from gapp import StartEndApp

my_app = StartEndApp(lambda: print('Yo, app started'), lambda : print('Yo, app ended'), 'My App')
my_app.start_app()
```

![start_end_app](https://raw.githubusercontent.com/Madoshakalaka/gapp/master/readme_assets/start_end_app.PNG)

<!--You picture won't show on pypi if you use relative path.-->
<!--If you want to add any image, please add the image to readme_assets folder and add the filename as below-->
<!--![some show case picture](https://raw.githubusercontent.com/Madoshakalaka/gapp/master/readme_assets/showcasePicture.png)-->
