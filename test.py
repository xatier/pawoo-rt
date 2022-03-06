import server


# test oembed tweet html process
def test_process_tweet() -> None:
    tweets = [
        (
            """<blockquote class="twitter-tweet"><p lang="zh" dir="ltr">《原子習慣》真的好看<br>開頭就直接被點醒<br><br>以結果來設定目標是最表層的作法<br>而且很容易陷入溜溜球效應<br>目標達成以後就不再持續<br>陷入不斷重來的迴圈<br><br>要從最內層的改變身分認同開始做起<br>去著重每一天的過程<br>才能建立真正持之以恆的習慣<br>與屬於自己的「系統」<a href="https://twitter.com/hashtag/reading?src=hash&amp;ref_src=twsrc%5Etfw">#reading</a> <a href="https://twitter.com/hashtag/%E5%8E%9F%E5%AD%90%E7%BF%92%E6%85%A3?src=hash&amp;ref_src=twsrc%5Etfw">#原子習慣</a><br>$ <a href="https://t.co/IbGqVz9Cub">pic.twitter.com/IbGqVz9Cub</a></p>&mdash; M157q.py (@M157q) <a href="https://twitter.com/M157q/status/1436130693155672067?ref_src=twsrc%5Etfw">September 10, 2021</a></blockquote>""",  # noqa: E501
            """《原子習慣》真的好看\n開頭就直接被點醒\n\n以結果來設定目標是最表層的作法\n而且很容易陷入溜溜球效應\n目標達成以後就不再持續\n陷入不斷重來的迴圈\n\n要從最內層的改變身分認同開始做起\n去著重每一天的過程\n才能建立真正持之以恆的習慣\n與屬於自己的「系統」 #reading   #原子習慣 \n$  https://pic.twitter.com/IbGqVz9Cub """  # noqa: E501
        ),
        (
            """<blockquote class="twitter-tweet"><p lang="en" dir="ltr">when reading text in a non-native language &amp; wondering how it&#39;s pronounced, u can enter this in devtools to have the browser pronounce it:<br><br>u=new SpeechSynthesisUtterance(getSelection().toString());u.lang=&#39;ru-RU&#39;;speechSynthesis.speak(u)<br><br>(replace &#39;ru-RU&#39; with any BCP 47 tag)</p>&mdash; yan (@bcrypt) <a href="https://twitter.com/bcrypt/status/1500348547887079424?ref_src=twsrc%5Etfw">March 6, 2022</a></blockquote>""",  # noqa: E501
            """when reading text in a non-native language & wondering how it's pronounced, u can enter this in devtools to have the browser pronounce it:\n\nu=new SpeechSynthesisUtterance(getSelection().toString());u.lang='ru-RU';speechSynthesis.speak(u)\n\n(replace 'ru-RU' with any BCP 47 tag)"""  # noqa: E501
        ),
        (
            """<blockquote class="twitter-tweet"><p lang="zh" dir="ltr">結果昨天 Cloudflare TPE 爛掉<br>導致中華的使用者都爛掉 因為只有中華會走<a href="https://twitter.com/hashtag/%E6%AD%A3%E7%89%88%E5%8F%97%E5%AE%B3%E8%80%85?src=hash&amp;ref_src=twsrc%5Etfw">#正版受害者</a></p>&mdash; Davy (๑•̀ㅂ•́)و 🌐 (@david50407) <a href="https://twitter.com/david50407/status/1491699012101361665?ref_src=twsrc%5Etfw">February 10, 2022</a></blockquote> """,  # noqa: E501
            """結果昨天 Cloudflare TPE 爛掉\n導致中華的使用者都爛掉 因為只有中華會走 #正版受害者 """  # noqa: E501
        ),
    ]

    for tweet, expected in tweets:
        assert server.process_tweet(tweet) == expected
