# HOI4 AI Modding ガイド — Kaiserreich に学ぶ AI 制御技術

このドキュメントは、Kaiserreich (KR) リポジトリの `common/ai_*` フォルダ群を精査し、HOI4 Modding における AI 制御テクニックを体系的にまとめたものです。自作 Mod に AI 挙動を実装する際のリファレンスとして使えます。

対応するエージェント用スキルが `.claude/skills/`(Claude Code)と `codex/skills/`(Codex)にあります:

| スキル | 対象フォルダ |
|---|---|
| `hoi4-ai-strategy-searcher` | `ai_strategy` / `ai_areas` / `ai_faction_theaters` の検索・分析 |
| `hoi4-ai-strategy-helper` | AI strategy の作成・移植 |
| `hoi4-ai-strategy-plans-helper` | `ai_strategy_plans` / `ai_focuses` |
| `hoi4-ai-templates-helper` | `ai_templates`(師団テンプレートAI) |
| `hoi4-ai-equipment-helper` | `ai_equipment`(装備バリアント設計AI) |
| `hoi4-ai-navy-helper` | `ai_navy`(海軍編成AI) |
| `hoi4-ai-design-principles` | AI層全体の設計思想・工数配分・規律(個別ファイルではなく計画・レビュー用) |

---

## 0. 全体マップ — 8つのフォルダはどう連携するか

```
common/
├── ai_strategy/          【中枢】外交・戦線・生産・研究・諜報の重み付け
├── ai_areas/             ai_strategy が参照する地理エリア定義
├── ai_faction_theaters/  陣営単位の戦域(theater)定義
├── ai_strategy_plans/    国家方針(NF)の取得順序スクリプト
├── ai_focuses/           研究カテゴリの重みプロファイル
├── ai_templates/         陸軍師団テンプレートの設計・更新AI
├── ai_equipment/         装備バリアント(艦船・戦車・航空機)の設計AI
└── ai_navy/              海軍の任務目標・艦隊・任務部隊の編成AI
```

連携の要点:

- **role(役割)システムが縦串**: `ai_templates` の `role = infantry` や `ai_equipment` の `roles = { naval_submarine }` が定義する役割トークンを、`ai_strategy` の `role_ratio` / `build_army` が参照して「どの役割に工場を割くか」を決める。
- **`ai_areas` は地理の共通語彙**: 一度エリアを定義すれば、`area_priority`・`front_unit_request`・`put_unit_buffers`・`naval_dominance` など多数の strategy から `area = western_europe` の形で再利用できる。
- **NF の取得順は `ai_strategy_plans`、研究の好みは `ai_focuses`、それ以外の経済・軍事行動はほぼすべて `ai_strategy`** が担当する。

KR には一次資料が2つ同梱されている。必読:

- `common/ai_strategy/_documentation.md` — strategy トークン全一覧+使用例(KRチームがメンテ)
- `common/ai_equipment/_documentation_AI_ships_production_KR.info` — 海軍生産AIの実践ノウハウ+ゲーム内デバッグ手順

---

## 1. `ai_strategy` — AI 制御の中枢

### 1.1 基本構造

ファイル内に「バンドル」を並べる。各バンドルはライフサイクル条件と、有効中に適用される `ai_strategy` エントリ群を持つ。

```pdx
my_strategy_bundle = {
	allowed = { original_tag = GER }    # 静的フィルタ。起動時など稀にしか評価されない
	enable = { date > 1938.1.1 }        # 有効化条件(定期評価)
	abort = { has_capitulated = yes }   # 無効化条件
	# abort_when_not_enabled = yes      # 代替: enable が false になったら無効化

	ai_strategy = { type = conquer id = FRA value = 200 }
	ai_strategy = { ... }               # 何個でも
}
```

**KR の house rule**: 全バンドルに `abort` か `abort_when_not_enabled` を必ず付ける。恒久的な strategy には `abort = { always = no }` と明示する。

### 1.2 ファイル構成の慣習

- `00_*.txt` — 全国家共通のデフォルト・システム系(`00_default.txt`, `00_production.txt`, `00_area_priority.txt`, `00_factions.txt`, `00_naval_production.txt`, `00_espionage.txt` など)
- `TAG.txt`(大文字)— 国別(`GER.txt`, `RUS.txt` など約60ファイル)
- 小文字の地域ファイル — 地域グループ(`china.txt`, `america.txt`, `central_asia.txt` など)

### 1.3 ターゲット指定の4形態

```pdx
ai_strategy = {
	type = front_unit_request
	id = GER                   # ① 固定ID(国タグ/ステート/リージョン/トークン)
	area = western_europe      # ② ai_areas のエリア(複数指定可)
	tag = GER  state = 42      # ③ 戦線系トークンの複合ターゲット(複数指定可)
	country_trigger = {        # ④ 動的トリガー(scope=相手国, FROM=自国)
		NOT = { is_neighbor_of = FROM }
	}
	ratio = 0.25               # 戦線の25%以上がターゲットに掛かる場合のみ適用
	value = -50
}
```

### 1.4 `reversed = yes` — 視点反転テクニック

「全世界が GER にどう反応するか」を `GER.txt` に集約するための仕組み。トリガーは*相手国*のスコープで評価され、`id` に書いた国が strategy の適用者になる。

```pdx
GER_hates_socialists = {
	reversed = yes
	enable = {
		has_socialist_government = yes      # ← 各国(=ターゲット候補)側で評価される
		GER = { has_socialist_government = no }
	}
	abort_when_not_enabled = yes
	ai_strategy = { type = antagonize id = GER value = 1000 }
	ai_strategy = { type = diplo_action_acceptance target = market_access_rights id = GER value = -1000 }
}
```

### 1.5 KR 頻出パターン集

**① グローバル負値+ローカル正値**(本土集中。`globally` という全世界エリアを定義しておくのがミソ):

```pdx
ai_strategy = { type = front_unit_request  area = globally        value = -90 }
ai_strategy = { type = front_unit_request  area = western_europe  value = 90 }  # 相殺して本土のみ通常値
```

**② 敵対ロック**(`antagonize` + 外交受諾の遮断をセットで):

```pdx
ai_strategy = { type = antagonize id = RUS value = 1000 }
ai_strategy = { type = diplo_action_acceptance target = market_access_rights id = RUS value = -1000 }
```

**③ 地形対応の機甲配置**(山岳・砂漠国境に戦車を送らない):

```pdx
ai_strategy = { type = front_armor_score id = "SWI" value = -100 }
ai_strategy = { type = front_armor_score id = "LBA" value = -100 }
```

**④ 師団数上限での生産停止**:

```pdx
enable = { has_reached_maximum_divisions = yes }
ai_strategy = { type = build_army id = infantry value = -1000 }
```

**⑤ 敗戦時の戦線縮小**(段階的エスカレーション):

```pdx
# 同盟内で非隣接戦線は -50、敗色濃厚(surrender_progress > 0.3)なら -100
ai_strategy = {
	type = front_unit_request
	country_trigger = { NOT = { is_neighbor_of = FROM } }
	value = -100
}
```

### 1.6 KR での使用頻度トップ(実測)

| トークン | 件数 | 用途 |
|---|---|---|
| `front_unit_request` | 176 | 戦線への部隊割当を増減 |
| `diplo_action_acceptance` | 146 | 特定外交アクションの受諾度 |
| `conquer` | 103 | 開戦ターゲットの優先度 |
| `front_control` | 92 | 戦線の攻勢強制/凍結(`execution_type = rush` 等) |
| `ignore_claim` | 90 | 請求権の無視 |
| `invade` | 87 | 上陸作戦の対象優先度(負値で禁止) |
| `antagonize` | 86 | 敵視 |
| `build_building` | 78 | 建設指示(`id = <建物>`, 任意で `target = <州>`) |
| `role_ratio` | 75 | 役割別の生産比率(templates/equipment と連携) |
| `area_priority` | 45 | 戦域単位の優先度 |
| `research_weight_factor` | 37 | 研究の重み補正(`research_tech` は強制) |

全トークンの一覧と仕様は `common/ai_strategy/_documentation.md` を参照。

### 1.7 落とし穴

- `type` のトークン名を typo してもエラーが出ず、**無言で無視される**。
- `allowed` は稀にしか評価されない。日付や戦争状態の判定を入れてはいけない。
- 空軍の `unit_ratio` は「重み」(未設定=0=作らない)、陸海軍は「100+value の百分率」と挙動が違う。
- `role_ratio = 0` は生産を止めるが**改装(refit)は止まらない**。改装は `ai_equipment` 側の `priority = 0` で止める。

---

## 2. `ai_areas` — 地理エリアの定義

`default.txt` 1ファイルに `areas = { ... }` を定義。エリアは strategic region のリストか大陸名で構成する。

```pdx
areas = {
	globally = {                       # KR独自: 全世界エリア(グローバル負値パターン用)
		continents = { europe north_america south_america australia africa asia middle_east india central_america }
	}
	western_europe = {
		strategic_regions = { 1 2 3 4 5 ... }   # コメントで地域名を必ず併記
	}
	asia = {
		continents = { asia india }
	}
}
```

KR の定義: `globally` / `western_europe` / `eastern_europe` / `scandinavia` / `north_america` / `latin_america` / `inner_south_america` / `africa` / `asia` / `middle_east` / `oceania` / `pacific` / `china`

**盗むべき発想**: エリアは「AI に教える地政学的語彙」。`china` のように Mod の戦略構図に合わせた粒度で切ると、国別ファイルの記述量が激減する。

---

## 3. `ai_faction_theaters` — 陣営戦域

陣営メンバーの NPC 国に「どの戦域で戦うべきか」を教える仕組み。KR は Reichspakt 等の主要陣営について定義している。

```pdx
reichspakt_western_europe = {
	name = reichspakt_theatre_western_europe     # ローカライズキー
	regions = { 5 6 7 19 20 164 18 173 ... }     # strategic regions
	can_skip_first_region = yes
	preferred_countries = { GER BEL WAL FLA HOL SPA ... }   # この戦域を担当すべき国
	cancel = {                                   # 戦域の解散条件。INT = 評価対象国
		OR = {
			NOT = { INT = { capital_scope = { is_on_continent = europe } } }
			NOT = { has_war_with = INT }
		}
	}
	ai_will_do = {
		base = 0
		modifier = { add = 100 original_tag = GER }   # 国ごとの参加意欲
	}
}
```

KR のコメントに「挙動にややバグあり、要実験(`preferred_countries`)」とある点に注意。

---

## 4. `ai_strategy_plans` — 国家方針の取得順序

AI に NF ツリーの「正しい周回ルート」を教えるスクリプト。KR は主要9カ国のみ(GER, FRA, RUS, JAP, TUR, RAJ, HND, SRI, CA)に用意し、他国は `ai_will_do` 任せにしている — **全国に書く必要はない**という割り切りも参考になる。

```pdx
GER_dkp_ai_plan = {
	name = "GER_dkp_ai_plan"
	enable = {
		has_completed_focus = GER_conservative_revolution
		has_country_flag = GER_dkp_ai          # 政治ルートのAIフラグで分岐
	}
	abort = { has_completed_focus = GER_the_reaction }   # リストの最終NF完了で終了

	ai_national_focuses = {                    # この順に取得を試みる
		GER_ruhrkampf
		GER_conservative_revolution
		...
	}

	ideas = {                                  # 任意: アイデア/閣僚選択の重みボーナス
		partial_economic_mobilisation = 10
	}

	weight = { factor = 1.0 }    # 研究需要にも影響するため ~1.0 推奨(リポジトリ内コメント)
}
```

### KR のプラン連鎖テクニック

1国のプレイスルーを小さなプランに分割し、`enable`/`abort` で数珠つなぎにする:

1. **開始プラン** — `date > 1936.x` + ルートフラグで起動、序盤の経済NFのみ
2. **政治プラン** — 分岐NF完了 + ルートフラグで起動、政治ルート全体
3. **軍備プラン** — 政治完了 + `date > 1939.1.1` で起動(軍事NFを早取りさせない)
4. **戦時プラン** — `has_war_with = X` で起動、`weight = 5.0` で他を圧倒

ルーター役は AI 人格フラグ(`GER_schleicher_ai`, `GER_dkp_ai` など)。ゲームルールやイベントでフラグを1つ立て、ルートごとにプラン連鎖を用意する。

---

## 5. `ai_focuses` — 研究の重みプロファイル

ハードコードされた AI フォーカス種別(`defense` / `aggressive` / `war_production` / `military_equipment` / `military_advancements` / `peaceful` / `naval` / `naval_air` / `aviation`)ごとに、研究カテゴリの重みを定義する。

```pdx
# generic.txt — デフォルト
ai_focus_naval = {
	research = {
		naval_doctrine = 100.0
		ss_tech = 8.0
		dd_tech = 8.0
	}
}

# germany.txt — タグをサフィックスにして国別上書き
ai_focus_naval_GER = {
	research = {
		naval_doctrine = 100.0
		bb_tech = 8.0      # ドイツは戦艦・空母を重視
		cv_tech = 5.0
		ss_tech = 10.0
	}
}
```

KR は `britain` / `danubia` / `france` / `germany` / `italy` / `japan` / `USA` の7ファイルで主要国を調整。ドクトリン(`land_doctrine = 100.0` 等)は桁違いに高い重みを付けるのが定石。

---

## 6. `ai_templates` — 師団テンプレート AI

AI がどの師団テンプレートを設計・更新・運用するかを制御する。

```pdx
line_infantry = {                       # テンプレートグループ(役割×国セットで1つ)
	blocked_for = {
		TRP ETS SIK ...                 # line_cavalry を使う国(コメントで理由を明記)
		LBA SAU ...                     # line_camelry を使う国
		FRA                             # カスタムロジックの国
	}
	role = infantry                     # role_ratio / build_army が参照する役割トークン
	upgrade_prio = { base = 5 }

	infantry_default = {
		upgrade_prio = { base = 1 }
		can_upgrade_in_field = { AI_trigger_can_upgrade_in_field = yes }
		target_template = {
			regiments = { infantry = 9  artillery_brigade = 1 }
			support   = { artillery = 1 anti_air = 1 engineer = 1 logistics_company = 1 field_hospital = 1 }
		}
	}

	infantry_motorised = {
		upgrade_prio = {
			base = 1
			modifier = { factor = 0  NOT = { has_tech = motorised_infantry } }   # 技術ゲート
			modifier = { factor = 0  num_of_military_factories < 90 }            # 工業力ゲート
			modifier = { add = 2     num_of_military_factories > 149
			             has_reached_ninety_percent_of_maximum_divisions = yes }
		}
		...
	}
}
```

### 盗むべきテクニック

1. **工業力で段階解禁されるテンプレ進化ラダー** — default → upgraded(軍需45)→ motorised(90)→ mechanised(135)。貧乏国は安いテンプレを維持し、工業国は自動で高級化する。閾値は意図値の約90%に設定(コメント参照)。
2. **`upgrade_prio base = 0` の「認識専用」エントリ** — 非正規兵・民兵テンプレを優先度0で登録し、「これも歩兵ラインの一部」と AI に認識させて将来の更新対象にする。
3. **`blocked_for` による国セット分離** — 1つのデフォルトファイル+特化ライン(騎兵/駱駝騎兵/非正規/砲兵特化)で全世界をカバーし、各国がちょうど1ラインに属するようコメント付きで管理。
4. **野戦更新の共通 scripted trigger** — 全デザインが `AI_trigger_can_upgrade_in_field` を参照し、ポリシーを1箇所で変更可能に。

---

## 7. `ai_equipment` — 装備バリアント設計 AI

AI に艦船・戦車・航空機の「設計図」を与え、バリアント作成・生産・改装・経験値消費を制御する。**KR の `_documentation_AI_ships_production_KR.info` は HOI4 海軍 AI 資料として最高品質**なので必ず読むこと。

### 7.1 3層ヒエラルキー(KR ドキュメントの核心)

| 層 | 場所 | 制御するもの |
|---|---|---|
| ① `role_ratio`(ai_strategy) | `00_naval_production.txt` 等 | どの役割に造船所/工場を割くか。**XP消費・改装は止められない** |
| ② 設計グループ(ai_equipment 最上位) | `KR_submarines.txt` 等 | グループ単位の生産・改装・XP消費。`priority = 0` で全停止 |
| ③ 個別デザイン(named sub-block) | `submarine_1940` 等 | 世代ごとの設計。`priority` で世代交代、`target_variant` でモジュール構成 |

**生産を止める**→ ①で role_ratio を 0 か負値に。**改装を止める**→ ③で `priority = 0`。

### 7.2 構造例(KR 潜水艦)

```pdx
naval_submarine = {
	category = naval                  # naval / land(planes_* も同システム)
	roles = { naval_submarine }
	priority = { base = 10 }

	submarine_1940 = {
		role_icon_index = 6
		priority = { base = 35 }      # KRの世代ラダー: 1922=0, 1936=20, 1940=35, 1944=50
		target_variant = {
			match_value = 3500.0      # 既存装備とのマッチ強度(改装対象の選定に影響)
			type = ship_hull_submarine_3
			modules = {
				fixed_ship_engine_slot = sub_ship_engine    # カテゴリ指定→最新を自動選択
				fixed_ship_torpedo_slot = ship_torpedo_sub
				mid_1_custom_slot = ship_sub_snorkel        # 個別モジュール指定→固定
			}
		}
	}
}
```

### 7.3 モジュールマッチング演算子(最重要・最難関)

- `<slot> = <カテゴリ>` — 研究済み最新モジュールを自動装備。基本形。
- `<slot> = <モジュール>` — 完全固定。アップグレードのないモジュール用。
- `<slot> > <モジュール>` — 指定より上位なら何でも。**カテゴリを持たないモジュール用**(BB装甲、`ship_light_medium_battery` 等)。
- `<slot> = empty` — 常に空。改装時は装着済みモジュールを撤去。
- ネスト形式 + `any_of = { a b c }` — 先頭優先のフォールバック連鎖:

```pdx
fixed_ship_engine_slot = { upgrade = current  any_of = { engine_3 engine_2 engine_1 } }
# 最良を選びつつ、upgrade = current で既存艦の高額な機関換装を禁止
```

- `requirements = { module = ship_mine_layer }` — ハード条件。汎用駆逐艦が機雷敷設デザインにマッチするのを防ぐ。
- **書かなかったスロットは永遠に空のまま**。埋めたいスロットは必ず列挙する。

### 7.4 KR ドキュメント由来の落とし穴

- 新型船体の技術を持つ AI には旧世代デザインを `modifier = { factor = 0 has_tech = <新型> }` で塞ぐこと。さもないと旧式を作り続ける。
- `ship_medium_battery` を裸のカテゴリ指定にすると、**エラーも出ずにその船体を一切作らなくなる**。`>` か `any_of` を使う。
- 1国に役割を与えすぎると海軍編成が崩壊する。role_ratio で国ごとに役割を絞る。
- **ホットリロード可能**: 一時停止→AI の生産ラインを削除→ファイル編集・保存→再開、で再起動なしに反映される。調整ループが超高速。

---

## 8. `ai_navy` — 海軍の編成と任務

3層構造: **goals(何をするか)→ fleet(どんな艦隊で)→ taskforce(どんな艦で)**。

```pdx
# goals/goals_generic.txt — 任務目標と優先度帯
generic_convoy_raiding = {
	objective_type = convoy_raiding    # ハードコードされた目標トークン
	min_priority = 3
	max_priority = 7
}

# fleet/generic_fleet_templates.txt — 艦隊の構成
generic_dominance_fleet_1 = {
	required_taskforces = { StrikeForce_1 = 1  PatrolReconForce_1 = 2 }
	optional_taskforces = { StrikeForce_1 = 1  PatrolDominanceForce_CA_1 = 1  PatrolDominanceForce_BC_1 = 1 }
}

# taskforce/generic_taskforce_templates.txt — 任務部隊の艦構成
StrikeForce_1 = {
	ai_will_do = { factor = 1 }
	mission = { naval_strike }
	min_composition     = { destroyer = { amount = 6 } }
	optimal_composition = {
		carrier = { amount = 2 }  battleship = { amount = 3 }
		heavy_cruiser = { amount = 3 }  light_cruiser = { amount = 3 }
		destroyer = { amount = 18 }
	}
}
```

### 盗むべきテクニック

1. **min は極小、optimal は理想形** — 小国海軍でも艦隊が成立し、大国は理想編成へ自動成長する。
2. **`role = 4` 指定** — `ai_equipment` の設計役割を持つ艦だけを要求(KR は機雷敷設部隊に本物の敷設駆逐艦を強制)。
3. **資本艦タイプ別のパトロール部隊**(CA版/BC版)を用意し、その国が実際に作る艦種を吸収する。
4. **汎用テンプレートは各層1ファイルのみ**。国ごとの個性は role_ratio と ai_equipment の側で出す — 保守コストが激減する設計判断。
5. 「AI が通商破壊しない」ときは goals ではなく、**まず潜水艦を作っているか**(role_ratio / ai_equipment)を疑う。

---

## 9. デバッグ手法(KR ドキュメントより)

1. コンソールで `aiview` を有効化 — AI の意思決定オーバーレイが見える。
2. 艦船デザイン画面で右側をホバー — マッチした設計グループ名とスコアが出る。**赤警告 = どのデザインにもマッチせず、生産も改装もされない**。
3. 海軍 XP バーをホバー — 1行目が赤(upgrade対象なし)なら、defines・デザイン優先度・役割設定のどこかが XP 消費を塞いでいる。
4. **ホットリロード調整ループ**: 一時停止 → AI 生産ライン全削除(Shift+クリック)→ ファイル編集・保存 → 再開。ai_equipment / 生産系は即時反映。
5. 関連 define: `NDefines.NAI.VARIANT_UPGRADE_MIN_XP = 105` — 100超に保つと AI がドクトリン用に XP を温存する。

---

## 10. 自作 Mod への移植チェックリスト

- [ ] `ai_areas` を自 Mod の戦略構図に合わせて定義したか(`globally` エリアも忘れずに)
- [ ] 全 strategy バンドルに `abort` / `abort_when_not_enabled` があるか
- [ ] `role` トークンが `ai_templates` / `ai_equipment` / `role_ratio` の3者で一致しているか
- [ ] テンプレ進化ラダーの工業力閾値が段階的か(KR: 45/90/135)
- [ ] 旧世代デザインに新技術ゲート(`factor = 0 has_tech = ...`)を入れたか
- [ ] NF プランは政治ルートごとの AI フラグで分岐し、戦時プランに高 weight を与えたか
- [ ] KR 固有の ID(タグ・NF・フラグ・州ID)をコピーしていないか — 盗むのはパターン、中身は自作

---

*出典: Kaiserreich for HOI4 リポジトリ(patch 1.6.3 / HOI4 1.18.3 時点)の `common/ai_*` 各フォルダ、`common/ai_strategy/_documentation.md`、`common/ai_equipment/_documentation*.{md,info}` の精査による。*
