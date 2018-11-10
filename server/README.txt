파일 경로에 한글이 반드시 없어야 함

locally test server code :

- Create an isolated Python environment in a directory external to your project and activate it:
python -m virtualenv env
env\Scripts\activate

- Navigate to your project directory and install dependencies:
cd YOUR_PROJECT
python -m pip install -r requirements.txt

- Run the application:
python main.py

