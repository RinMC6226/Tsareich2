---
id: todo
title: 前史アーカイブ 中央課題一覧
type: faction
canon: draft
related: []
---

# 前史アーカイブ 中央課題一覧 (TODO)

前史ファイル群から抽出した **不足・矛盾・実装待ち・構成課題** を集約する。
各ファイル内にも `<!-- TODO -->` と frontmatter `to_do:` があるが、横断的に追うための一覧。
解消したら該当ファイルの `to_do` とこの一覧の両方を更新すること。

---

## 1. 矛盾・要整合（最優先）

- ~~**日露戦争の講和が食い違う。**~~ **解決済み**: 講和条約名は**ポーツマス条約**に確定。ロシア勝利・日本は事実上の敗戦。全ファイル統一完了。
  - ~~付随：開戦の最後通牒の発布主体~~ **解決済み**: 史実どおり日本側が国交断絶を通告。全ファイル統一完了。
- ~~**第一次大戦の勝敗・参戦陣営の突合。**~~ **解決済み**: 全15ファイル（event 12件 + nation 4件）を突合し、陣営（独露伊 対 英仏墺土、JAP限定参戦）・勝敗（独露同盟の勝利、1917–1918）・年号に食い違いなし。各ファイルの「矛盾」注記は史実WWIとの逆転に関する自己注記であり、ドキュメント間の矛盾ではない。
- ~~**確定度表記の不統一。**~~ **解決済み**: TIMELINE.md の確定度列を各 event ファイルの frontmatter `canon` フィールドに合わせて統一。方針: 年月日が未確定でも内容（陣営・勝敗・経緯）が確定していれば `canon` とする。日付の不確定は `to_do` で別途追跡。`1905_state-duma-opening` のみ原文欠落のため `draft` 維持。

## 2. 不足・未確定（前史テキスト側）

- **`02_russia.txt` 末尾が文の途中で欠落。** 「国家院の開設」節が「民衆に浸透するにつれ」で切れている → 続きの原文が必要（[events/1905_state-duma-opening.md](events/1905_state-duma-opening.md) は `draft`、[nations/RUS.md](nations/RUS.md) も `draft`）。
- **月日不明が多数（`YYYY.0.0` 表記）。** 原文に月日が無い年が多い（1895, 1898, 1900, 1903, 1904, 1911, 1913, 1914, 1917, 1918 全件, 1920, 1921, 1928, 1929, 1933, 1934, 1936 等）。判明し次第、各 event と TIMELINE を更新。
- **加藤高明内閣（1924–）のイベント未作成。** [nations/JAP.md](nations/JAP.md) に「1924年以降に独露関係を再構築」とあるが対応 event 無し。新規作成か既存（1921/1934）への統合かを決める。
- **国民精神「対馬条約」「日英同盟」の内容が原文に無い。** 締結年・相手・効果が未定義（[nations/JAP.md](nations/JAP.md)）。idea 化に追加情報が必要。
- **1930年代三陣営の確定年が曖昧。** 原文「1930年代後半」のみ（[events/1930s_three-bloc-order.md](events/1930s_three-bloc-order.md)）。
- **POD の起点年。** 原文上の分岐は「1890年ビスマルク失脚回避」だが、年表化された最古事件は1895年（[README.md](README.md) POD節・[TIMELINE.md](TIMELINE.md)）。1890年起点の独立 event を設けるか要判断。

## 3. 実装待ち（ゲーム側）

- **全 character token 未確定。** `history/characters/` に該当が無く、[ENTITIES.md](ENTITIES.md) の人物表は token 未記入。実在18名（ビスマルク〜ノックス）の token 整備が必要。
- **日本の初期政党支持率。** 7党の支持率（極左〜極右）を `history/countries/JAP - Japan.txt` の politics に実装（[nations/JAP.md](nations/JAP.md)）。Tsareich2 のイデオロギー区分への各党マッピングを確定。
- **日本の国民精神8件。** 対馬条約／日英同盟／憲政の常道／大正デモクラシー／昭和天皇／軍部の弱体化／財閥経済／世界恐慌 を `common/ideas`（JAP）に実装。modifier・アイコン・localisation 未定義。
- **三陣営の faction 実装。** 独露（伊）大陸同盟／インターナショナル（仏西）／英米海洋陣営 の faction 定義・初期加盟・外交関係・AI戦略（[events/1930s_three-bloc-order.md](events/1930s_three-bloc-order.md), [ENTITIES.md](ENTITIES.md)）。
- **米大統領選のゲーム内再現。** 史実の大統領選は1936年11月で、ゲーム開始日 1936.1.1 より後。前史の既成事実ではなくイベント/focus で発生させるべきか、開始時点でノックス政権済みかを確定（[events/1936_us-presidential-election.md](events/1936_us-presidential-election.md)）。
- **各ファイルの `implements:` が空。** 実装オブジェクト（focus/idea/event/state）確定後に各前史ファイルへ紐付ける。

## 4. 構成上の課題

- **専用 nations ファイルの要否。** ITA・SPR・ENG・USA は前史頻出だが nations/*.md 未作成（FRA は作成済み）（[ENTITIES.md](ENTITIES.md)）。
- **解体国の後継の扱い。** オーストリア＝ハンガリー（AUS）・オスマン（TUR）は1918年解体。1936時点の後継国家・継承境界が未定義。
- **派閥専用ファイルの要否。** 現状 factions/ は空。三陣営を factions/*.md に切り出すか、events + ENTITIES の表で足りるか判断。
