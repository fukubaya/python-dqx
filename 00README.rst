======================================================================
dqx モジュール
======================================================================

Atout
======================================================================
ドラゴンクエストXプレイヤー専用サイト「目覚めし冒険者の広場」
http://hiroba.dqx.jp/sc/ のキャラページからステータス情報を取得する

Example
======================================================================
 >>> from dqx import dqx
 >>> dqx_user = dqx.User('499148186426')
 # http://hiroba.dqx.jp/sc/character/XXXXXXXXXXXX の XXXXXXXXX を文字列で指定
 
 >>> print dqx_user.name
 None
 # オブジェクト作成直後は情報なし
 
 >>> dqx_user.retrieve_and_update()
 # サイトから情報を取得しオブジェクトを更新．
 
 >>> print dqx_user.uid
 499148186426
 # サイトでのID
 
 >>> print dqx_user.title
 初心者
 # かたがき
 
 >>> print dqx_user.name
 ふくばや
 # なまえ
 
 >>> print dqx_user.cid
 XH349-176
 # キャラID
 
 >>> print dqx_user.race
 ドワーフ
 # 種族
 
 >>> print dqx_user.sex
 男
 # 性別
 
 >>> print dqx_user.job
 僧侶
 # 職業
 
 >>> print dqx_user.level
 17
 # レベル
 
 >>> print dqx_user.imglastupdate
 2012-08-12 06:11:00
 # 画像の最終更新日
 
 >>> print dqx_user.welcomefriend
 ヤリ装備で攻撃力＋１０です。おはらい可。
 # サポート仲間とうろく状況のメッセージ．とうろくしていない場合はNone
 
 >>> print dqx_user.message
 みせってい
 # メッセージ
 
 
 >>> print dqx_user.equipment
 みぎて:せいどうのやり, ひだりて:(せいどうのやり), アタマ:せいどうのかぶと, からだ上:うろこのよろい上＋１, からだ下:うろこのよろい下, ウデ:せいどうのこて, 足:うろこのブーツ, 顔アクセ:そうびなし, 首アクセ:そうびなし, 指アクセ:そうびなし, 他アクセ:そうびなし, しょくにん:銅の錬金ランプ☆☆☆
 # そうび
 
 >>> print dqx_user.equipment.rhand
 せいどうのやり
 # そうびのみぎて
 
 >>> print dqx_user.equipment.lhand
 (せいどうのやり)
 # そうびにひだりて
 # 他は head, ubody, lbody, arm, foot, faceacc, neckacc, fingacc, othacc, art
 
 >>> print dqx_user.location
 サーバー:サーバー１６, フィールド:岳都ガタラ
 # いる場所
 
 >>> print dqx_user.location.server
 サーバー１６
 # いる場所のサーバー
 
 >>> print dqx_user.location.field
 岳都ガタラ
 # いる場所のフィールド
 
 >>> print dqx_user.parameter
 さいだいHP:66, さいだいMP:38, こうげき力:57, しゅび力:59, こうげき魔力:5, かいふく魔力:48, ちから:36, すばやさ:43, みのまもり:37, きようさ:34, みりょく:23, おしゃれさ:31, おもさ:133
 # パラメータ
 
 >>> print dqx_user.parameter.maxhp
 66
 # さいだいHP
 # 他は maxmp, attack, defend, mattack, mhealing, power, speed, guard, dext, charm, appearance, weight 
 
 >>> print dqx_user.skillpoint
 {u'\u30e4\u30ea': 3, u'\u30b9\u30c6\u30a3\u30c3\u30af': 3, u'\u68cd': 3, u'\u3057\u3093\u3053\u3046\u5fc3': 12, u'\u76fe': 0}
 # スキルポイント．辞書形式．
 
 >>> print dqx_user.skillpoint[u'ヤリ']
 3
 
 >>> print dqx_user.skills[u'しんこう心']
 [u'\u304a\u306f\u3089\u3044']
 # とくぎ．辞書形式で中身はリスト．
 
 >>> print dqx_user.skills[u'しんこう心'][0]
 おはらい
 
 >>> print dqx_user.skilleffects
 {u'\u30e4\u30ea': [u'\u3053\u3046\u3052\u304d\u529b+10']}
 # スキル効果．辞書形式で中身はリスト．
 
 >>> print dqx_user.skilleffects[u'ヤリ'][0]
 こうげき力+10
 
 >>> print dqx_user.spells
 [u'\u30db\u30a4\u30df', u'\u30ad\u30a2\u30ea\u30fc', u'\u30ea\u30db\u30a4\u30df', u'\u30b6\u30e1\u30cf', u'\u30b6\u30aa', u'\u30de\u30db\u30ea\u30fc', u'\u30ba\u30c3\u30b7\u30fc\u30c9']
 # じゅもん．リスト形式．
 
 >>> print dqx_user.spells[0]
 ホイミ


sample.py
======================================================================
 % python sample.py 499148186426
 uid:499148186426
 かたがき:初心者
 なまえ:ふくばや
 キャラID:XH349-176
 種族:ドワーフ
 性別:男
 職業:僧侶
 レベル:17
 サポート仲間とうろく状況:とうろく中 (ヤリ装備で攻撃力＋１０です。おはらい可。)
 画像の最終更新日時:2012-08-12 06:11:00
 メッセージ:みせってい
 いる場所:{サーバー:サーバー１６, フィールド:岳都ガタラ}
 そうび:{みぎて:せいどうのやり, ひだりて:(せいどうのやり), アタマ:せいどうのかぶと, からだ上:うろこのよろい上＋１, からだ下:うろこのよろい下, ウデ:せいどうのこて, 足:うろこのブーツ, 顔アクセ:そうびなし, 首アクセ:そうびなし, 指アクセ:そうびなし, 他アクセ:そうびなし, しょくにん:銅の錬金ランプ☆☆☆}
 パラメータ:{さいだいHP:66, さいだいMP:38, こうげき力:57, しゅび力:59, こうげき魔力:5, かいふく魔力:48, ちから:36, すばやさ:43, みのまもり:37, きようさ:34, みりょく:23, おしゃれさ:31, おもさ:133}
 スキルポイント:{ヤリ:3, スティック:3, 棍:3, しんこう心:12, 盾:0}
 とくぎ:{しんこう心:おはらい}
 スキル効果:{ヤリ:こうげき力+10}
 じゅもん:[ホイミ,キアリー,リホイミ,ザメハ,ザオ,マホリー,ズッシード]
 % 

