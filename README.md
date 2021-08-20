# FlushActivity
- get_all_tweets.py：自分の全てのツイートを取得
- get_all_likes.py：likeした全てのツイートを取得
- delete_my_tweets.py：指定した日付までのツイートを削除
- delete_my_likes.py：指定した日付までのツイートをunlike

# config.iniの参考設定
[oauth]  
api_key = XXX  
api_secret = XXX  
access_token = XXX  
access_secret = XXX  

[twitter]  
date_format = %%a %%b %%d %%H:%%M:%%S %%z %%Y  

[period]  
year = 2021  
month = 3  
day = 1  

# 参考
- requests-oauthlib(https://github.com/requests/requests-oauthlib)
- 【初心者】10分でVSCodeセットアップ〜前編〜(https://torusblog.org/visualstudiocode-setpu-10-minuits/)
- 【初心者でも解る】VSCodeでライブラリ簡単インストール〜後編〜(https://torusblog.org/vscode-library-install-after/)
- Python - M1 MacにVisual Studio codeをインストールしてpythonを実行する(https://degitalization.hatenablog.jp/entry/2021/01/03/201258#Step4---PythonのExtensionを入れておく  )
