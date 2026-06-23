# ドイツ帝国NF設計方針

本文書はドイツ帝国の国家方針ツリー（政治・恐慌対策部分）の設計原則と現状をまとめたものである。実装者（人間・AI問わず）はこの文書を読んでからNFの追加・改修を行うこと。

関連ファイル:
- `common/national_focus/germany.txt` — NFツリー本体
- `events/TR_GER_depression_events.txt` — 恐慌政治イベント
- `common/scripted_effects/GER_depression_effects.txt` — 議会支持率変動エフェクト
- `common/scripted_effects/GER_parliament_effects.txt` — 議会システム本体
- `common/ideas/TR_GER_ideas.txt` — 国民精神
- `common/decisions/GER_parliament_decisions.txt` — 議会ディシジョン
- `docs/GER_great_depression_focus_plan.md` — NF別の詳細実装計画（効果値・イベント案）
- `docs/GER_great_depression_if_scenario.md` — 物語・世界観の背景文書
- `docs/prehistory/nations/GER.md` — ドイツ前史（canon: draft）

---

## 1. 1936年初期状態

ドイツ帝国は第一次世界大戦の戦勝国であり、ロシア・ベルギー・イタリアと帝国同盟（imperial_alliance）を形成している。しかし1927年からの世界恐慌で深刻な経済打撃を受けており、1936年帝国議会選挙を控えている。

### 初期国民精神

| 国民精神 | 主な効果 | 備考 |
|---|---|---|
| GER_victor_of_the_great_war | 安定度+5%, 戦争協力度+5%, PP獲得+5%, 中核州攻防+10% | 戦勝国の恩恵 |
| GER_october_constitution | PP獲得+10%, 安定度+5%, イデオロギー防衛+20% | 1918年十月憲法 |
| GER_great_depression | **安定度-25%, 消費財+30%, 建設速度-15%, 工場出力-10%** | 恐慌デバフ（非常に重い） |
| GER_austrian_question | 安定度-10%, PP獲得-10%, 民需工場占有3 | オーストリア問題 |
| GER_bloated_army | 指揮統制+5%, 士気回復-10%, 訓練時間+20%, 補給消費+15% | 肥大化した軍 |
| GER_veterans_association | 戦争協力度+10%, 徴兵+5%, 動員法コスト-25% | 在郷軍人会 |

### 初期政治

- 与党: right（保守ブロック: NLP+FKP+DKP）、支持率32%
- 選挙周期: 60ヶ月、最終選挙1931.9.13 → 次回選挙1936年後半
- 議会: 482議席、9政党。与党連合は139議席の少数与党

### 要点

GER_great_depression は開始時から付与されており、ゲーム開始直後からドイツに重い経済ペナルティを課している。これが政治ツリーの中心的な動機となる。

---

## 2. 設計原則

### 2.1 選挙前フェーズ（y=0~y=5）

政治ツリー y=0~y=5 は「1936年帝国議会選挙前の政策論争・政権構想決定」フェーズである。開発チームとの協議で確定した方針。

- **与党側NF（左ルート: 財政均衡）**: 現政権が実行する施策であり、実際のゲームプレイ効果を持つ。ただし緊縮政策なので痛みも伴う。
- **野党側NF（右ルート: 雇用創出）**: 野党の公約・要求の段階であり、原則として経済効果を持たない。議会支持率変動とPP・安定度の変化のみ。選挙勝利後に公約が実行される。

#### 根拠

十月憲法下のドイツ帝国では、宰相は皇帝が任命し、与党が政府を運営している。野党は議会で多数派を形成しても、それだけで法律を通せるかは制度的に曖昧である。したがって選挙前の段階では、与党だけが政策を実行できるという非対称性がゲームメカニクスに反映される。

### 2.2 恐慌は選挙前に解決しない

GER_great_depression の本格的な解決（除去・大幅軽減）はy=5以降の後続ツリー（選挙後フェーズ）で行う。y=0~y=5では与党ルートによる部分緩和のみを行い、プレイヤーに「選挙後の政権がどう恐慌を処理するか」を期待させる。

### 2.3 NF日数

全NFはcost = 5（35日）で統一されている。y=0からy=5までの最短経路は6NF = 210日（約7ヶ月）。1936年1月開始なので、最速でも7~8月に政権構想が確定する。選挙時期（1936年後半想定）と整合する。

---

## 3. ツリー構造

```
y=0:         [世界恐慌の余波]           ← ルートNF
              /              \
y=1:  [財政均衡を守れ]    [帝国雇用創出]   ← 相互排他。与党vs野党
         /     \            /      \
y=2: [植民地予算] [節約委員会] [東部農業] [失業保険]
         \     /      \       /     \    /
y=3: [帝国秩序法]  [帝国経済会議]  [七月決議の精神]
              \         |         /
y=4:         [宰相府協議]            ← イベントで3分岐決定
           /       |       \
y=5: [黒白赤協定] [議会多数派] [国民和解]  ← 相互排他・手動取得不可
```

### prerequisite構造の注意点

- y=2→y=3の接続はOR prerequisiteを使っている。例えば GER_reichsordnungsgesetz は `prerequisite = { focus = GER_ueberpruefung_des_kolonialetats focus = GER_reichssparkommission }` であり、どちらか一方を完了していれば取得可能。
- GER_reichswirtschaftsrat は3つのNFからのOR prerequisiteを持ち、左右どちらのルートからもアクセス可能な合流点である。
- GER_kanzleramtsbesprechungen は2つの独立したprerequisiteブロックを持つ。左右いずれかのy=3 NF **かつ** GER_reichswirtschaftsrat が必要。

### y=5の自動取得メカニズム

y=5の3NF（黒白赤協定、帝国議会多数派、国民和解）は `available = { always = no }` で手動取得を禁止している。GER_kanzleramtsbesprechungen完了時にイベント `tsr_ger_depression.11` が発火し、プレイヤーの選択に応じて `complete_national_focus` で自動取得される。

イベントの選択肢と条件:

| 選択肢 | 取得NF | 条件 |
|---|---|---|
| 黒白赤協定を成立させる | GER_schwarz_weiss_rot_abkommen | GER_reichsordnungsgesetz 完了済み |
| 帝国議会多数派を形成する | GER_reichstagsmehrheit | 無条件 |
| 国民和解を掲げる | GER_nationale_versoehnung | GER_der_geist_der_juliresolution 完了済み |

黒白赤協定と国民和解は追加のprerequisite（それぞれ帝国秩序法、七月決議の精神）を持つため、対応するy=3 NFを完了していないと選択できない。帝国議会多数派は無条件で選択可能。

---

## 4. 効果設計方針

### 4.1 現状の問題

現時点のNF効果は以下の点で不十分:

1. **効果が薄い**: ほぼ全てのNFがPP・安定度の加減のみ。GER_great_depression（消費財+30%、建設速度-15%）に対する具体的な経済対策が存在しない。
2. **与党/野党の差がない**: 設計原則では与党ルートに実効果、野党ルートに支持率変動のみとするが、現状は両ルートとも同程度の薄い効果しかない。
3. **恐慌の段階緩和がない**: GER_great_depression は一切変更されないまま全NFが完了する。
4. **イベントが少ない**: tsr_ger_depression.11（宰相府協議）のみ。各NFに物語イベントがない。
5. **ai_chance がない**: tsr_ger_depression.11 の全選択肢に ai_chance が設定されていない。

### 4.2 方向性

#### 与党ルート（財政均衡: y=1左）

実際の経済政策としてゲームプレイ効果を与える。緊縮路線なので安定度を少し犠牲にしながら財政を改善する方向。

- GER_great_depression の段階的軽減（modifier値の一部を改善するサブ国民精神の追加、またはswap_ideas による段階置換）
- 消費財削減、建設速度の部分回復など具体的な経済効果
- ただし緊縮の痛み（安定度低下、左派支持低下）も伴う

#### 野党ルート（雇用創出: y=1右）

選挙前の公約段階なので経済効果なし。議会支持率を動かすことが主な効果。

- PP・安定度の変化（政治的なインパクト）
- 議会支持率シフト（GER_depression_shift_support_* エフェクト）
- 将来の政策実行を予告するフラグ設定（選挙後のツリーで参照）
- GER_reichsarbeitsbeschaffung にある工場建設（random_owned_controlled_state）は再検討が必要。公約段階で建設が始まるのは設計原則と矛盾する可能性がある。

#### y=5 政権構想

y=5の3NFは選挙前の最終路線確定であり、後続ツリーへの接続点となる。ここでは:

- country_flag の設定（後続ツリーの分岐条件）
- 路線に応じた国民精神の追加
- 議会支持率の大幅シフト

### 4.3 恐慌緩和メカニズム案

与党ルートのNF完了時にGER_great_depression のペナルティを段階的に軽減する案:

**案A: サブ国民精神の追加**
恐慌本体は変更せず、GER_reichssparkommission 等のサブ国民精神で一部ペナルティを相殺する。

- 利点: 既存のGER_great_depression を変更しないのでシンプル
- 欠点: 国民精神が増えてUIが煩雑になる

**案B: swap_ideas による段階置換**
与党ルートのNFを完了するたびに恐慌国民精神を軽減版に置き換える（例: GER_great_depression → GER_great_depression_1 → GER_great_depression_2）。

- 利点: UIがすっきりする。恐慌が「改善している」ことが視覚的にわかる
- 欠点: 国民精神の定義が増える。置換順序の管理が必要

**未決定。** どちらの案を採用するかは実装開始時に決定する。

---

## 5. 接続システム

### 5.1 議会システム

議会システム（`GER_parliament_effects.txt`）は9政党×議席数の変数管理と選挙メカニクスを提供する。NFはこのシステムと以下のように連動する:

- 各NFの `completion_reward` で `GER_depression_shift_support_*` を呼び出し、政党支持率（`_bps` 変数）を変動させる
- 変動後は `GER_parliament_normalize_support` → `GER_parliament_refresh_thresholds` で正規化・GUI更新
- 初回NF完了時に `GER_depression_initialize_parliament_if_needed` で議会を安全に初期化

### 5.2 議会ディシジョン

`GER_parliament_decisions.txt` にはロビー活動・反対集会・影響工作のディシジョンがある。NF完了に連動して恐慌対策専用のディシジョンを追加する計画がある（`docs/GER_great_depression_focus_plan.md` 参照）が、未実装。

### 5.3 イベント

現状は `tsr_ger_depression.11`（宰相府協議3分岐）のみ。計画では各NF完了時の物語イベント（tsr_ger_depression.1~.14）を追加予定。

---

## 6. 軍事ツリーとの関係

軍事ツリー（x=34, GER_kriegsministerum → GER_the_sixty_sixth_act）は政治ツリーとは独立した別ブランチで開発されている。prerequisiteの接続はなく、並行して進められる。本文書の範囲外。

---

## 7. 実装状況

### 完了

- [x] NFツリー構造（13政治NF + 2軍事NF）の配置と prerequisite/mutually_exclusive
- [x] 全政治NFに GER_ プレフィックス付与
- [x] 議会支持率変動エフェクト（GER_depression_effects.txt: 12エフェクト）
- [x] tsr_ger_depression.11 イベント（宰相府協議3分岐）
- [x] 日本語・英語ローカライゼーション（タイトル・説明文）
- [x] y=5の自動取得メカニズム（available = always no + complete_national_focus）
- [x] country_flag 設定（y=5の3NF）
- [x] AGENTS.md の命名規則・コメント規則

### 未実装

- [ ] 与党ルートNFへの実経済効果の追加（恐慌段階緩和）
- [ ] 野党ルートNFの効果整理（公約段階として適切な効果に調整）
- [ ] 各NF完了時の物語イベント（tsr_ger_depression.1~.10, .12~.14）
- [ ] tsr_ger_depression.11 の ai_chance 設定
- [ ] 恐慌対策ディシジョンの追加
- [ ] germany.txt へのセクションヘッダコメント・NFごとの意図コメント追加
- [ ] y=5以降の後続ツリー設計（選挙後フェーズ）
- [ ] GER_reichsarbeitsbeschaffung の工場建設効果の再検討

---

## 8. 未決定事項

1. **恐慌緩和方式**: サブ国民精神追加 vs swap_ideas 段階置換（§4.3参照）
2. **野党ルートの工場建設**: GER_reichsarbeitsbeschaffung にある `random_owned_controlled_state` の工場建設は公約段階の設計原則と矛盾する可能性がある。削除して支持率変動のみにするか、「小規模な実験的事業」として残すか
3. **議会支持率変動幅**: 現在のbps値がロビー活動ディシジョンと比べて適切なバランスかの検証
4. **ai_chance の設計**: AIドイツがどのルートを好むか。保守ブロックが与党なので、AI的には財政均衡ルート→黒白赤協定が自然だが、ゲームバリエーションのために一定確率で他ルートも選ぶべきか
5. **選挙後ツリー**: y=5の後にどう接続するか。選挙イベントの設計、政権交代メカニクス、恐慌の本格解決ツリーの全体像はまだ未設計
