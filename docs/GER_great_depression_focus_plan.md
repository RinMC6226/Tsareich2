# ドイツ帝国NF「世界恐慌の余波」実装計画

## 目的

ドイツ帝国の1936年帝国議会選挙に向けて、世界恐慌対策を政治分岐の中心に置く。NFは単なる国家補正ではなく、帝国議会ディシジョンの支持率変動、政党連合形成、イベント選択と連動させる。

この計画では、既存の `GER_parliament_*_support_bps` 変数を利用し、NF完了時に各党支持率を動かす。支持率変更後は必ず `GER_parliament_normalize_support = yes` と `GER_parliament_refresh_thresholds = yes` を呼び、GUIを更新する。

## 全体方針

- 初期NF群は「恐慌への対応方針」を選ばせる経済政治ブランチにする。
- `財政均衡を守れ` と `帝国雇用創出` は択一にする。
- 緊縮路線は安定・通貨・財政を強めるが、雇用や左派支持を弱める。
- 雇用創出路線は労働者支持・建設速度を強めるが、財政規律や保守支持を圧迫する。
- 中盤の合流NFは政治秩序、議会協調、経済調整の3軸にする。
- 終盤3NFは1936年選挙前の政権構想を表す。保守連合、議会多数派、中央党妥協の3択にする。
- 終盤3NFはプレイヤーが直接選択せず、`宰相府協議` 完了時のイベント選択肢で自動取得する。

## NF別計画

| NF | アイコン | 主効果案 | 議会連動案 | イベント案 |
|---|---|---|---|---|
| 世界恐慌の余波 | `GFX_focus_generic_economic_recovery` | `GER_great_depression_aftermath` 国家精神を追加。安定度-5%、消費財+5%、建設速度-5%。 | 議会初期化。全党に小幅な争点化フラグを付ける。 | `tsr_ger_depression.1` 恐慌対策が1936年選挙の争点になる。 |
| 財政均衡を守れ | `GFX_focus_generic_reduce_unneccessary_expenditure` | 政治力+50、安定度+3%、消費財-2%、建設速度-3%。 | NLP +15、FKP +10、DKP +10、Zentrum +5、SPD -10、KPD -5。 | `tsr_ger_depression.2` 帝国銀行と財界が均衡財政を支持。 |
| 帝国雇用創出 | `GFX_focus_generic_full_employment` | 建設速度+5%、安定度+2%、政治力-25。 | SPD +15、Zentrum +10、FVP +10、USPD +5、DKP -10、NLP -5。 | `tsr_ger_depression.3` 公共事業案をめぐる協議。 |
| 植民地予算の見直し | `GFX_focus_JAP_ministry_of_colonial_affairs` | 政治力+35、消費財-1%、植民地関連の将来ディシジョン解禁フラグ。 | NLP +10、FKP +5、DKP +5、DVL P/祖国党 -5、SPD -5。 | `tsr_ger_depression.4` 植民地庁予算の査定。 |
| 帝国節約委員会 | `GFX_focus_generic_commission` | `GER_reichssparkommission` 国家精神。政治力獲得+5%、消費財-3%、安定度-2%。 | NLP +10、DKP +10、FKP +5、SPD -10、USPD -5。 | `tsr_ger_depression.5` 官僚機構と軍事予算への監査。 |
| 東部農業救済 | `GFX_focus_generic_agricultural_subsidies` | `GER_osthilfe_program` 国家精神。安定度+3%、消費財+2%、徴兵可能人口または戦争協力度+少量。 | DKP +15、FKP +10、NLP +5、SPD -5、KPD -5。 | `tsr_ger_depression.6` ユンカー救済と批判。 |
| 失業保険法改正 | `GFX_focus_generic_welfare` | `GER_reformed_unemployment_insurance` 国家精神。安定度+4%、消費財+2%、政治力獲得-3%。 | SPD +15、Zentrum +10、FVP +5、USPD +5、NLP -5、DKP -5。 | `tsr_ger_depression.7` 都市労働者への譲歩。 |
| 帝国秩序法 | `GFX_focus_LIT_restore_order` | 共産主義/急進派対策。安定度+5%、政治力+25、民主/左派支持に小ペナルティ。 | DKP +15、DVL P +10、FKP +10、KPD -15、USPD -10、SPD -5。 | `tsr_ger_depression.8` 治安維持法をめぐる議会対立。 |
| 七月決議の精神 | `GFX_focus_generic_support_the_left_right` | 安定度+5%、政治力+25、議会協調系ディシジョン解禁。 | SPD +10、Zentrum +10、FVP +10、USPD +5、DKP -5、DVL P -5。 | `tsr_ger_depression.9` 1917年平和決議の再評価。 |
| 帝国経済会議 | `GFX_focus_generic_the_council_of_europe` | `GER_reichswirtschaftsrat` 国家精神。建設速度+3%、生産効率成長+3%、政治力獲得+3%。 | Zentrum +15、NLP +5、SPD +5、DKP +5、FVP +5。 | `tsr_ger_depression.10` 財界・農業団体・労組の協議機関。 |
| 宰相府協議 | `GFX_focus_generic_conference` | イベントで3つの政権構想を提示。選択により終盤NFを自動取得する。 | 現在の支持率をもとにイベント文面を変える案。 | `tsr_ger_depression.11` 選挙前の最終政治調整。 |
| 黒白赤協定 | `GFX_focus_GER_monarchy_compromise` | `GER_black_white_red_agreement` 国家精神。安定度+5%、戦争協力度+5%、左派対策ディシジョン強化。 | DKP +20、DVL P +15、FKP +10、NLP +5、Zentrum +5、SPD -15、KPD -10。政府フラグを保守連合に更新する案。 | `tsr_ger_depression.12` 保守諸党の反革命統一戦線。 |
| 帝国議会多数派 | `GFX_focus_ETH_re-convene_the_parliament` | `GER_reichstag_majority_bloc` 国家精神。政治力+75、安定度+3%、改革ディシジョン解禁。 | SPD +15、Zentrum +15、FVP +15、USPD +5、DKP -10、DVL P -10。政府フラグを議会多数派に更新する案。 | `tsr_ger_depression.13` 1917年多数派の復活。 |
| 国民和解 | `GFX_goal_generic_national_unity` | `GER_national_reconciliation` 国家精神。安定度+8%、政治力獲得+5%、極左/極右の伸長を抑える。 | Zentrum +20、SPD +5、NLP +5、FKP +5、KPD -5、DVL P -5。政府フラグを中央党妥協に更新する案。 | `tsr_ger_depression.14` 中央党主導の妥協政治。 |

注: `DVL P` は実装時には既存変数名 `GER_parliament_dvlp_*` を使う。

## 国家精神案

新規ファイル案: `common/ideas/TR_GER_ideas.txt`

- `GER_great_depression_aftermath`: 初期恐慌デバフ。NF進行で段階的に軽減または置換する。
- `GER_reichssparkommission`: 緊縮委員会。消費財を下げるが安定度/建設に小ペナルティ。
- `GER_osthilfe_program`: 東部農業救済。安定度と保守支持に寄与するが消費財が増える。
- `GER_reformed_unemployment_insurance`: 都市労働者救済。安定度と左派支持に寄与するが財政負担あり。
- `GER_reichswirtschaftsrat`: 経済調整機関。中道的な経済回復補正。
- `GER_black_white_red_agreement`: 保守・帝政派ブロック。
- `GER_reichstag_majority_bloc`: 議会改革派ブロック。
- `GER_national_reconciliation`: 中央党妥協ブロック。

## 帝国議会ディシジョン連動案

既存カテゴリ `GER_parliament` に追加する方針。

- `GER_parliament_debate_austerity_budget`: `財政均衡を守れ` 完了後。NLP/FKP/DKP支持を増やし、SPD/USPD支持を下げる。コスト政治力35、30日。
- `GER_parliament_promote_public_works`: `帝国雇用創出` 完了後。SPD/Zentrum/FVP支持を増やす。コスト政治力35、30日。
- `GER_parliament_audit_colonial_budget`: `植民地予算の見直し` 完了後。NLP/FKP支持を増やし、DVL Pをやや下げる。
- `GER_parliament_enforce_reichsordnung`: `帝国秩序法` 完了後。KPD/USPD支持を下げ、DKP/DVL P支持を上げる。安定度小増。
- `GER_parliament_july_resolution_compromise`: `七月決議の精神` 完了後。SPD/Zentrum/FVP支持を上げ、極右支持を抑える。
- `GER_parliament_broker_economic_council`: `帝国経済会議` 完了後。Zentrumと穏健各党を小幅上昇。

表示は既存の「ロビー活動」「反対集会」「議席強化」と別に、「恐慌対策」を展開/格納するフラグを追加する案がよい。既存UIに合わせて `GER_parliament_show_crisis_measures` / `GER_parliament_hide_crisis_measures` を追加する。

## イベント構成案

新規ファイル案: `events/TR_GER_depression_events.txt`

- Namespace: `tsr_ger_depression`
- NF完了イベントは原則 `is_triggered_only = yes`
- 物語イベントは1選択肢、分岐イベントは2-3選択肢にする。

イベントの役割:

- 前半NF: 背景説明と小さな追加効果。
- 中盤NF: 支持政党と反発政党を明示し、ディシジョン解禁を通知。
- `宰相府協議`: 3派閥の政権構想を提示する中核イベント。
- 終盤NF: 選挙前の最終路線確定イベント。政府フラグや国家精神を確定させる。

## NF効果実装の共通パターン

NF完了時は以下の順で実装する。

1. 国家精神の追加/置換。
2. 政治力・安定度・戦争協力度などの即時補正。
3. 議会支持率変数を加減。
4. `GER_parliament_normalize_support = yes`
5. `GER_parliament_refresh_thresholds = yes`
6. `country_event = { id = tsr_ger_depression.X }`

議会初期化は最初のNFで安全に呼ぶ。

```txt
if = {
	limit = { NOT = { has_country_flag = GER_parliament_initialized } }
	GER_parliament_initialize = yes
}
```

## アイコン再選定方針

既に本体 `interface/goals.gfx` で存在確認済みのアイコンを使う。必要に応じて以下へ微調整する。

- 法制: `GFX_focus_LIT_restore_order` または `GFX_focus_AUS_lawmaking_leniency`
- 議会: `GFX_focus_ETH_re-convene_the_parliament` または `GFX_focus_AFG_parliamentary_democracy`
- 植民地: `GFX_focus_JAP_ministry_of_colonial_affairs` または `GFX_focus_POL_colonial_league`
- 財政/通貨: `GFX_focus_generic_reduce_unneccessary_expenditure`, `GFX_focus_generic_currency_reforms`
- 経済回復: `GFX_focus_generic_economic_recovery`, `GFX_focus_generic_full_employment`

## 実装順

1. `TR_GER_ideas.txt` と日本語ローカライズを追加する。
2. NF説明文を今回の解説に基づいて追加する。
3. NF completion_reward に基本効果と議会支持率変更を入れる。
4. `TR_GER_depression_events.txt` とイベントローカライズを追加する。
5. 帝国議会ディシジョンに恐慌対策セクションを追加する。
6. 起動ログで `germany.txt`、ideas、events、localisation のエラーを確認する。

## 確定した分岐仕様

- `財政均衡を守れ` と `帝国雇用創出` は相互排他。
- `黒白赤協定`、`帝国議会多数派`、`国民和解` は相互排他。
- 終盤3NFには `available = { always = no }` を置き、手動取得を禁止する。
- `宰相府協議` 完了時に `tsr_ger_depression.11` を発火させ、選択肢ごとに `complete_national_focus` で終盤NFを自動取得する。

## 保留・確認したい点

- 恐慌デバフをゲーム開始時から付与するか、最初のNF取得時に付与するか。
- 議会支持率の変更幅は大きめにして選挙結果を動かすか、既存ロビー活動と同程度に抑えるか。
