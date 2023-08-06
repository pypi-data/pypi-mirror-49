이게 뭔가요?
------------

한글 폰트를 `fonttools <https://github.com/fonttools/fonttools>`__\ 를 이용해 
`Google Fonts + 한국어 <https://googlefonts.github.io/korean/>`__\ 처럼 분할해주는 툴입니다.

개발환경 설정
-------------

.. code:: bash

   git clone https://github.com/laziu/krwftgen.git
   cd krwftgen
   python -m venv .venv            # >= 3.4
   source .venv/bin/activate       # PS: '.\.venv\Scripts\Activate.ps1'
   python -m pip install -r dev-requirements.txt
   python -m pip install -r requirements.txt
   python -m pip install --editable .
   # krwftgen -h
