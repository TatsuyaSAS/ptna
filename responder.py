import random
import re
from analyzer import *
from markov import *
from itertools import chain

class Responder:
    """ 応答クラスのスーパークラス
    """
    def __init__(self, name, dictionary):
        """ Responderオブジェクトの名前をnameに格納

             @param name Responderオブジェクトの名前
             @param dictionary Dictionaryオブジェクト
        """
        self.name = name
        self.dictionary = dictionary

    def response(self, input, mood, parts):
        """ オーバーライドを前提としたresponse()メソッド

             @param input 入力された文字列
             @param mood 機嫌値
             @ param parts 形態素解析結果のリスト
             戻り値　空の文字列
        """
        return ""

    def get_name(self):
        """ 応答オブジェクトの名前を返す
        """
        return self.name

class RepeatResponder(Responder):
    """ オウム返しのためのサブクラス
    """
    def response(self, input, mood, parts):
        """ 応答文字列を作って返す

             @param imput 入力された文字列
             @param mood 機嫌値
        """
        return "{}ってなに？".format(input)

class RandomResponder(Responder):
    """ ランダムな応答のためのサブクラス
    """
    def response(self, input, mood, parts):
        """ 応答文字列を作って返す

             @param input 入力された文字列
             @param mood 機嫌値
             戻り値　リストからランダムに抽出した文字列
        """
        return random.choice(self.dictionary.random)

class PatternResponder(Responder):
    """ パターンに反応するためのサブクラス
    """
    def response(self, input, mood, parts):
        """ パターンにマッチした場合に応答文字列を作って返す

             @param input 入力された文字列
             @param mood 機嫌値
        """
        self.resp = None
        # pattern["pattern"]と["phrases"]に対して反復処理
        for ptn_item in self.dictionary.pattern:
            # match()でインプット文字列にパターンマッチを行う
            m = ptn_item.match(input)
            # マッチした場合は機嫌値moodを引数にしてchoice()を実行
            # 戻り値の応答文字列。またはNoneを取得
            if (m):
                self.resp = ptn_item.choice(mood)
            # choice()の戻り値がNoneでない場合は
            # 応答例の中の%match%をインプットされた文字列内の
            # マッチした文字列に置き換える
            if self.resp != None:
                return re.sub("%match%", m.group(), self.resp)
        # パターンマッチしない場合はランダム辞書から返す
        return random.choice(self.dictionary.random)

class TemplateResponder(Responder):
    """ テンプレートに反応するためのサブクラス
    """
    def response(self, input, mood, parts):
        """ テンプレートを使用して応答フレーズを生成する

        @param input インプット文字列
        @param parts インプット文字列の形態素解析結果
        @param mood アップデート後の機嫌値
        """
        # インプット文字列の名詞の部分のみを格納するリスト
        keywords = []
        # テンプレート本体を格納する変数
        template = ""
        # 解析結果partsの「文字列」➡word、「品詞情報」➡partに順次格納
        for word, part in parts:
            # 名詞であるかをチェックしてkeywordsリストに格納
            if (keyword_check(part)):
                keywords.append(word)
        # keywordsリストに格納された名詞の数を取得
        count = len(keywords)
        # keywordsリストに1つ以上の名詞が存在し、
        # 名詞の数に対応するテンプレートが存在するかをチェック
        if (count > 0) and (str(count) in self.dictionary.template):
            # テンプレートリストから名詞の数に対応するテンプレートを
            # ランダムに抽出
            template = random.choice(self.dictionary.template[str(count)])
            # テンプレートリストから名詞の数に対応するテンプレートを
            # keywordsに格納されている名詞を埋め込む
            for word in keywords:
                template = template.replace("%noun%", word, 1)
            return template
        return random.choice(self.dictionary.random)

class MarcovResponder(Responder):
    """ マルコフ連鎖を利用して応答を生成するためのサブクラス

    """
    def response(self, input, mood, parts):
        m = [] #
        # 解析結果の形態素と品詞に対して反復処理
        for word, part in parts:
            # インプット文字列に名詞があればそれを含むマルコフ連鎖文を検索
            if keyword_check(part):
                # マルコフ文字列で生成した文章を1つずつ処理
                for sentence in self.dictionary.sentences:
                    # 形態素の文字列がマルコフ連鎖の文章に含まれているかを検索する
                    # 最後を".*?"にすると検索文字列だけにもマッチするので
                    # + ".*"として検索文字列だけにマッチしないようにする
                    find = ".*" + word + ".*"
                    # マルコフ連鎖文にマッチさせる
                    tmp = re.findall(find, sentence)
                    if tmp:
                        # マッチする文章があればリストmに追加
                        m.append(tmp)
        # findall()はリストを返してくるので多重リストをフラットにする
        m = list(chain.from_iterable(m))

        # 集合に変換して重複した文章を取り除く
        check = set(m)
        # 再度、リストに戻す
        m = list(check)

        if m:
            # インプット文字列の名詞にマッチしたマルコフ連鎖文からランダムに選択
            return(random.choice(m))

        # マッチするマルコフ連鎖文がない場合
        return random.choice(self.dictionary.random)
