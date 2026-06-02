---
id: timeline
title: 前史 背骨年表
type: faction
date_start: 1895.0.0
date_end: 1936.1.1
canon: draft
related: []
to_do:
  - "POD（分岐点）の正確な年月日が未確定。1890年のビスマルク失脚回避が起点だが、年表先頭の最古事件は1895年のため date_start を 1895.0.0 とした。1890年起点の事件ファイルが必要かを確認すること。"
  - "月日不明の年が多数（.0.0 表記）。原文に月日が無いため年のみとした。判明し次第、各行と events/*.md を更新すること。対象: 1895, 1898, 1900, 1903, 1904, 1905(国家院), 1906(1月のみ), 1908(10月のみ), 1911, 1913, 1914, 1917, 1918(全件), 1920, 1921, 1928, 1929, 1933, 1934, 1936。"
  - "1906_party-politics-establishment は 1906.1.0（月のみ判明・日不明）。1908の2件は 1908.10.0（月のみ判明・日不明）。"
  - "三陣営再編（1930s_three-bloc-order）の date を 1936.0.0 とした events データに合わせたが、原文では「1930年代後半」とあり年が曖昧。確定年を確認すること。"
---

# 前史 背骨年表 (TIMELINE)

POD（分岐点）から開始日 **1936.1.1** までの主要事件を時系列で並べる。
ここは **背骨（概要）** であり、詳細は各 `events/*.md` に書いてリンクする。

各行は1事件。`詳細` 列から該当ファイルへ飛べるようにする。

<!-- TODO: POD（分岐点）の確定。原文では1890年の社会主義者鎮圧法延長によるビスマルク失脚回避が起点だが、年表化された最古事件は1895年。1890年起点の独立した event ファイルを設けるか要確認。 -->

---

## 独露同盟の成立

独露再保障条約の延長を起点に、保守帝国同士の協商が経済協力・バルカン調整・反革命協力へ発展し、1910年代に正式な独露同盟へと結実していく時期。

| 年月日 | 出来事 | 関与TAG | 確定度 | 詳細 |
|---|---|---|---|---|
| 1895.0.0 <!-- TODO: 月日不明 --> | 独露干渉と日本海危機（遼東半島還付） | RUS, GER, JAP, ENG, FRA | draft | [独露干渉と日本海危機](events/1895_dual-intervention-liaodong.md) |
| 1898.0.0 <!-- TODO: 月日不明 --> | 満州権益をめぐる独露日の角逐 | RUS, GER, JAP | draft | [満州権益](events/1898_manchuria-concessions.md) |
| 1900.0.0 <!-- TODO: 月日不明 --> | 義和団の乱 | RUS, GER, JAP, ENG | draft | [義和団の乱](events/1900_boxer-rebellion.md) |
| 1903.0.0 <!-- TODO: 月日不明 --> | 日露戦争開戦前夜 | RUS, GER, JAP | draft | [日露戦争開戦前夜](events/1903_russo-japanese-war-eve.md) |
| 1904.0.0 <!-- TODO: 月日不明 --> | 日露戦争 | RUS, JAP | draft | [日露戦争](events/1904_russo-japanese-war.md) |
| 1905.0.0 <!-- TODO: 月日不明 --> | 国家院（国会）の開設 | RUS | draft | [国家院の開設](events/1905_state-duma-opening.md) |
| 1905.3.31 | 独露協調の固定化（第一次モロッコ事件） | GER, RUS, FRA, ENG | draft | [独露協調の固定化（第一次モロッコ事件）](events/1905_first-moroccan-crisis-tangier.md) |
| 1906.1.0 <!-- TODO: 日不明（1月のみ判明） --> | 政党政治の定着と軍部影響力の後退 | JAP | draft | [政党政治の定着と軍部影響力の後退](events/1906_party-politics-establishment.md) |
| 1908.10.0 <!-- TODO: 日不明（10月のみ判明） --> | オーストリア＝ハンガリーの離反（ボスニア危機） | GER, RUS, AUS | draft | [オーストリア＝ハンガリーの離反（ボスニア危機）](events/1908_austria-hungary-defection.md) |
| 1908.10.0 <!-- TODO: 日不明（10月のみ判明） --> | 皇帝外交の後退（デイリー・テレグラフ事件） | GER, ENG, RUS | draft | [皇帝外交の後退（デイリー・テレグラフ事件）](events/1908_kaiser-diplomacy-retreat.md) |
| 1911.0.0 <!-- TODO: 月日不明 --> | 海軍競争と第二次モロッコ事件 | GER, FRA, RUS, ENG | draft | [海軍競争と第二次モロッコ事件](events/1911_second-moroccan-crisis.md) |
| 1912.1.12 | 帝国議会と国内対立（1912年選挙でSPDが第一党） | GER, RUS | draft | [帝国議会と国内対立（1912年選挙）](events/1912_reichstag-spd-largest-party.md) |
| 1913.0.0 <!-- TODO: 月日不明 --> | ツァーベルン事件 | GER | draft | [ツァーベルン事件](events/1913_zabern-affair.md) |

## 世界大戦の勃発

独露協調の強化が墺洪・オスマンの協商接近を招き、複数の対立が重なって世界大戦が勃発する時期。

| 年月日 | 出来事 | 関与TAG | 確定度 | 詳細 |
|---|---|---|---|---|
| 1914.0.0 <!-- TODO: 月日不明 --> | 世界大戦の勃発 | GER, RUS, AUS, TUR, ITA, ENG, FRA, JAP | draft | [世界大戦の勃発](events/1914_great-war-outbreak.md) |

## フランス革命と講和

フランス第三共和政の崩壊とコミューン成立、そして独露同盟の決定的勝利に至る講和の時期。

| 年月日 | 出来事 | 関与TAG | 確定度 | 詳細 |
|---|---|---|---|---|
| 1917.0.0 <!-- TODO: 月日不明 --> | フランス革命とコミューン成立 | FRA | draft | [フランス革命とコミューン成立](events/1917_french-revolution.md) |
| 1918.0.0 <!-- TODO: 月日不明 --> | 1918年講和と独露同盟の勝利 | FRA, GER, RUS, ENG | draft | [1918年講和と独露同盟の勝利](events/1918_peace-settlement.md) |

## 戦後秩序

ドイツの半議会制立憲君主国への移行、墺洪・オスマンの解体、各国の戦後処理が進む時期。

| 年月日 | 出来事 | 関与TAG | 確定度 | 詳細 |
|---|---|---|---|---|
| 1918.0.0 <!-- TODO: 月日不明 --> | ドイツ帝国の憲法改革（半議会制立憲君主国へ） | GER | draft | [ドイツ帝国の憲法改革（半議会制立憲君主国へ）](events/1918_german-constitutional-reform.md) |
| 1918.0.0 <!-- TODO: 月日不明 --> | 戦後秩序（墺洪・オスマンの解体） | AUS, TUR, GER, RUS | draft | [戦後秩序（墺洪・オスマンの解体）](events/1918_post-war-order.md) |
| 1918.0.0 <!-- TODO: 月日不明 --> | 戦争責任問題と原政権の退陣 | JAP | draft | [戦争責任問題と原政権の退陣](events/1918_hara-cabinet-fall.md) |

## イタリアと西欧革命圏

イタリアの反革命的な国家主義王国化と、スペイン第二共和政の前倒し成立によるインターナショナル形成の時期。

| 年月日 | 出来事 | 関与TAG | 確定度 | 詳細 |
|---|---|---|---|---|
| 1918.0.0 <!-- TODO: 月日不明 --> | イタリアの戦後処理と国家主義王国化 | ITA | draft | [イタリアの戦後処理と国家主義王国化](events/1918_italy-postwar-nationalist-turn.md) |
| 1920.0.0 <!-- TODO: 月日不明 --> | スペイン第二共和政の前倒し成立とインターナショナル形成 | SPR, FRA | draft | [スペイン第二共和政の前倒し成立とインターナショナル形成](events/1920_spanish-second-republic.md) |

## 英米と世界恐慌

イギリスの海洋帝国再建、世界恐慌の発生、日本の財政運営と協調外交、米ノックス政権の成立に至る時期。

| 年月日 | 出来事 | 関与TAG | 確定度 | 詳細 |
|---|---|---|---|---|
| 1921.0.0 <!-- TODO: 月日不明 --> | 高橋是清の財政再建と協調外交路線の確立 | JAP, GER, RUS | draft | [高橋是清の財政再建と協調外交路線の確立](events/1921_takahashi-financial-reconstruction.md) |
| 1928.0.0 <!-- TODO: 月日不明 --> | 緊縮政策と昭和恐慌 | JAP | draft | [緊縮政策と昭和恐慌](events/1928_showa-depression.md) |
| 1929.0.0 <!-- TODO: 月日不明 --> | 世界恐慌の発生 | USA, GER, ENG | draft | [世界恐慌の発生](events/1929_great-depression.md) |
| 1933.0.0 <!-- TODO: 月日不明 --> | 高橋是清の積極財政と経済回復 | JAP | draft | [高橋是清の積極財政と経済回復](events/1933_takahashi-reflation.md) |
| 1934.0.0 <!-- TODO: 月日不明 --> | 幣原喜重郎内閣と協調外交による安定 | JAP, GER, RUS, ENG | draft | [幣原喜重郎内閣と協調外交による安定](events/1934_shidehara-cooperative-diplomacy.md) |
| 1936.0.0 <!-- TODO: 月日不明 --> | 1936年米大統領選とノックス政権 | USA, ENG | draft | [1936年米大統領選とノックス政権](events/1936_us-presidential-election.md) |

## 1930年代の国際構造

世界が独露大陸同盟・インターナショナル・英米海洋陣営の三陣営に再編され、次なる大戦へ向かう時期。

| 年月日 | 出来事 | 関与TAG | 確定度 | 詳細 |
|---|---|---|---|---|
| 1936.0.0 <!-- TODO: 「1930年代後半」とあり確定年が曖昧 --> | 1930年代の三陣営への再編 | GER, RUS, ITA, FRA, SPR, ENG, USA | draft | [1930年代の三陣営への再編](events/1930s_three-bloc-order.md) |
