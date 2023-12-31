@echo off
echo Preparing lambda Langchain layer...
echo purging cache
pip cache purge
echo Removing old directory...
rmdir python /s /q
echo Installing packages...
pip install --platform manylinux2014_x86_64 --target=.\python\lib\python3.10\site-packages --implementation cp --python 3.10 --only-binary=:all: -r requirements.txt
