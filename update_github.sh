# step 1 确认版本号
# A. 确认config.py内的私有源是否已打码
# B. git pull
# C. 看看最新的标签
# D. 在本地给代码打上新标签
# E. 修改 __init__.py、setup.py 和 meta.yaml 中的版本号

# step 2 本地打包
rm -r dist/ build/ *.egg-info/
python setup.py bdist_wheel
python setup.py sdist

# step 3 上传 https://pypi.org/project/aitool/
# A. 在官网设置api token
# B. 登录时 username: __token__  password: <hidden>
python3 -m twine upload dist/*

# step 4 本地安装然后试用
pip install aitool --upgrade
rm -r dist/ build/ *.egg-info/
