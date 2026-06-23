---
id: entities
title: 前史 エンティティ・レジストリ
type: faction
canon: draft
related: []
to_do:
  - "FRA の人物は character token 確定済み（common/characters/FRA.txt に5名）。GER・RUS・JAP・USA の人物 token はなお未確定。"
  - "ITA・SPR・ENG・USA は前史に頻出するが nations/*.md が未作成。FRA は作成済み。"
  - "AUS（オーストリア＝ハンガリー）・TUR（オスマン）は1918年に解体。1936時点の後継国家の扱いが未確定。"
  - "三陣営（独露伊大陸同盟・インターナショナル・英米海洋陣営）の faction 実装（faction名・初期加盟・外交関係）が未着手。"
---

# エンティティ・レジストリ (ENTITIES)

前史に登場する **国家・人物・派閥** の名称を、**ゲーム内ID** に対応づける表。
AIが「この国/人物は実装上どのTAG・どのオブジェクトか」を一意に解決できるようにする。

新しい主体が前史に登場したら、まずここに登録する。TAGはゲームと一致させる（ロシア帝国=**RUS**、ソ連=SOV とは別）。

---

## 国家 (Nations)

### 前史ファイルあり

| lore名 | TAG | 1936時点の政体 | 前史ファイル | 主要実装の所在 |
|---|---|---|---|---|
| ドイツ帝国 | GER | 半議会制立憲君主国 | [nations/GER.md](nations/GER.md) | common/national_focus/GER_*, 帝国議会システム（docs/plan/done/parliament_system_v2.md） |
| ロシア帝国 | RUS | 立憲君主制（帝政＋国家院） | [nations/RUS.md](nations/RUS.md) | <!-- TODO: RUS の focus/ideas 実装所在が未確定 --> |
| 大日本帝国 | JAP | 立憲君主制（議会主導） | [nations/JAP.md](nations/JAP.md) | history/countries/JAP - Japan.txt, common/ideas（国民精神, 未実装） |
| フランス・コミューン | FRA | 復讐主義的革命政権 | [nations/FRA.md](nations/FRA.md) | history/countries/FRA - France.txt, common/characters/FRA.txt |

### 前史に登場（専用ファイル未作成）

| lore名 | TAG | 1936時点の立場 | 備考 |
|---|---|---|---|
| イタリア王国 | ITA | 反革命的国家主義王国 | 独露伊大陸同盟側。<!-- TODO: nations/ITA.md 要否 --> |
| スペイン共和国 | SPR | 第二共和政 | インターナショナル。<!-- TODO: nations/SPR.md 要否 --> |
| イギリス | ENG | 海洋帝国 | 英米海洋陣営。<!-- TODO: nations/ENG.md 要否 --> |
| アメリカ合衆国 | USA | 共和党ノックス政権 | 英米海洋陣営。選挙のゲーム内再現は要検討。 |
| オーストリア＝ハンガリー | AUS | （1918年解体） | <!-- TODO: 1936時点の後継国家の扱い未確定 --> |
| オスマン帝国 | TUR | （1918年解体） | 海峡・アルメニア・メソポタミア・シリアを独露が影響下に。<!-- TODO: 後継未確定 --> |

---

## 人物 (Characters)

`history/characters/` の token と対応づける。**現状すべて token 未確定（to_do）**。

| lore名 | 所属TAG | 役割 | character token | 前史ファイル |
|---|---|---|---|---|
| オットー・フォン・ビスマルク | GER | 宰相（失脚回避・対露協調） | <!-- TODO --> | [events/1905_first-moroccan-crisis-tangier.md](events/1905_first-moroccan-crisis-tangier.md) ほか |
| ヴィルヘルム2世 | GER | 皇帝 | <!-- TODO --> | [events/1908_kaiser-diplomacy-retreat.md](events/1908_kaiser-diplomacy-retreat.md) |
| アルフレート・フォン・キーデルレン＝ヴェヒター | GER | 外務長官 | <!-- TODO --> | [events/1911_second-moroccan-crisis.md](events/1911_second-moroccan-crisis.md) |
| ティルピッツ | GER | 海軍（海軍拡張論） | <!-- TODO --> | [events/1911_second-moroccan-crisis.md](events/1911_second-moroccan-crisis.md) |
| ローザ・ルクセンブルク | GER | SPD左派 | <!-- TODO --> | [events/1912_reichstag-spd-largest-party.md](events/1912_reichstag-spd-largest-party.md) |
| カール・リープクネヒト | GER | SPD左派 | <!-- TODO --> | [events/1912_reichstag-spd-largest-party.md](events/1912_reichstag-spd-largest-party.md) |
| アレクサンドル・ベゾブラーゾフ | RUS | 陸軍関係者（対日開戦派） | <!-- TODO --> | [events/1903_russo-japanese-war-eve.md](events/1903_russo-japanese-war-eve.md) |
| 昭和天皇 | JAP | 君主（国家元首） | <!-- TODO --> | [nations/JAP.md](nations/JAP.md) |
| 桂太郎 | JAP | 首相（日露戦争期、総辞職） | <!-- TODO --> | [nations/JAP.md](nations/JAP.md) |
| 伊藤博文 | JAP | 元老（政権再編を主導） | <!-- TODO --> | [nations/JAP.md](nations/JAP.md) |
| 西園寺公望 | JAP | 首相（1906.1 成立） | <!-- TODO --> | [nations/JAP.md](nations/JAP.md) |
| 原敬 | JAP | 首相（政党内閣確立、1918退陣） | <!-- TODO --> | [events/1918_hara-cabinet-fall.md](events/1918_hara-cabinet-fall.md) |
| 高橋是清 | JAP | 蔵相／首相（財政再建・積極財政） | <!-- TODO --> | [events/1921_takahashi-financial-reconstruction.md](events/1921_takahashi-financial-reconstruction.md) |
| 加藤高明 | JAP | 首相（1924～、独露関係再構築） | <!-- TODO --> | [nations/JAP.md](nations/JAP.md)（イベント未作成） |
| 浜口雄幸 | JAP | 首相（1928～、緊縮） | <!-- TODO --> | [events/1928_showa-depression.md](events/1928_showa-depression.md) |
| 若槻禮次郎 | JAP | 首相（1931～） | <!-- TODO --> | [events/1928_showa-depression.md](events/1928_showa-depression.md) |
| 幣原喜重郎 | JAP | 首相（1934～、協調外交） | <!-- TODO --> | [events/1934_shidehara-cooperative-diplomacy.md](events/1934_shidehara-cooperative-diplomacy.md) |
| フランク・ノックス | USA | 大統領（共和党、1936～） | <!-- TODO --> | [events/1936_us-presidential-election.md](events/1936_us-presidential-election.md) |
| マルセル・デア | FRA | 国家元首（コミューン最高指導者、1934～） | <!-- TODO: 新規作成要 --> | [nations/FRA.md](nations/FRA.md) |
| ジャック・ドリオ | FRA | 赤色民兵指導者（デアの右腕） | <!-- TODO: 新規作成要 --> | [nations/FRA.md](nations/FRA.md) |
| ジャン・ジョレス | FRA | SFIO指導者→臨時革命委員会議長（1919年粛清） | <!-- TODO --> | [nations/FRA.md](nations/FRA.md) |
| ジョルジュ・ヴァロワ | FRA | 国民サンディカリスムの理論家 | <!-- TODO --> | [nations/FRA.md](nations/FRA.md) |
| モーリス・トレーズ | FRA | 内政の重鎮（労組の国家組織化） | <!-- TODO --> | [nations/FRA.md](nations/FRA.md) |
| ジャック・デュクロ | FRA | 秘密警察（革命保安局）長官 | <!-- TODO --> | [nations/FRA.md](nations/FRA.md) |
| シャルル・ド・ゴール | FRA | 陸軍・機甲将軍 | <!-- TODO: 新規作成要 --> | [nations/FRA.md](nations/FRA.md) |
| フランソワ・ダルラン | FRA | 海軍・赤色艦隊総司令官 | <!-- TODO: 新規作成要 --> | [nations/FRA.md](nations/FRA.md) |
| エドゥアール・ダラディエ | FRA | country_leader（social_democracy、差し替え予定） | FRA_edouard_daladier | [nations/FRA.md](nations/FRA.md) |
| ルネ・ニコ | FRA | country_leader（orthodox_marxism） | FRA_rene_nicod | [nations/FRA.md](nations/FRA.md) |
| アルフレッド・ロスメル | FRA | country_leader（syndicalism） | FRA_alfred_rosmer | [nations/FRA.md](nations/FRA.md) |
| マルセル・ビュカール | FRA | 革命的愛国者（将軍・顧問候補） | FRA_marcel_bucard | [nations/FRA.md](nations/FRA.md) |
| シャルル・モーラス | FRA | 王党派（亡命、体制転覆ルート） | FRA_charles_maurras | [nations/FRA.md](nations/FRA.md) |

---

## 派閥・ブロック (Factions / Blocs)

1936年初期の世界は三陣営。詳細は [events/1930s_three-bloc-order.md](events/1930s_three-bloc-order.md)。

| lore名 | 中心TAG | 構成 | 前史ファイル | ゲーム上の表現 |
|---|---|---|---|---|
| 独露（伊）大陸同盟 | GER | GER, RUS, ITA | [events/1930s_three-bloc-order.md](events/1930s_three-bloc-order.md) | <!-- TODO: faction定義・初期加盟。独露再保障条約→独露同盟(1910s)→大陸同盟(1930s)の発展形 --> |
| インターナショナル | FRA | FRA, SPR | [events/1920_spanish-second-republic.md](events/1920_spanish-second-republic.md) | <!-- TODO: faction定義。革命輸出陣営 --> |
| 英米海洋陣営 | ENG | ENG, USA | [events/1936_us-presidential-election.md](events/1936_us-presidential-election.md) | <!-- TODO: faction定義。海洋通商秩序再建 --> |
| （歴史）協商陣営 | ENG | ENG, FRA, AUS, TUR | [events/1914_great-war-outbreak.md](events/1914_great-war-outbreak.md) | 大戦中の対独露陣営。1918年講和で解体（記録用） |
