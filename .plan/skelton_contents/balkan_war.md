# バルカン戦争コンテンツ設計（確定仕様）

## 概要

1936年末〜1937年にかけてバルカン半島で勃発する架空の地域戦争。
表面的にはハンガリー＝ユーゴスラビア間の民族紛争だが、
実態はドイツとロシアのバルカン半島における権益争いから生まれた代理戦争である。

ルーマニアの日和見的参戦、ハンガリー内部の少数民族蜂起を経て、
ハンガリーは領土の大半を失い「残存国家」となる。
一方、勝者のユーゴスラビアもロシアへの戦時債務という代償を負う。

---

## 背景設定

### 世界情勢

- ドイツとロシアは表向き同盟関係にあるが、バルカン半島での影響圏をめぐり水面下で対立
- ハンガリーはドイツの影響下にある中欧の中堅国で、旧ハプスブルク領の広大な領土を保持
- ユーゴスラビアはロシアの友好国であり、ハンガリー支配下の南スラヴ人の「解放」を掲げている

### ハンガリーの多民族領土

| 地域 | State | 民族 | 備考 |
|------|-------|------|------|
| ヴォイヴォディナ | 45 | セルビア人 | YUG/SERコア |
| プレクムリェ | 1049 | スロヴェニア人 | YUGコア |
| バナト | 82 | ルーマニア人・セルビア人 | 戦後BNT独立→ROM編入 |
| 西バナト | 764 | セルビア人 | 戦後BNT独立→YUG編入 |
| スロヴァキア | 70, 71, 664 | スロヴァキア人 | SLOコア |
| カルパト・ルテニア | 73 | ルテニア人 | SLO/UKRコア |
| セーケイ地方 | 1054 | ハンガリー人 | HUNコア、戦後ROM移譲 |
| クリシャナ | 83 | ルーマニア人 | 戦後ROM移譲 |

### 各国の思惑

| 国 | 立場 | 目的 |
|----|------|------|
| ユーゴスラビア (YUG) | 主戦派 | 南スラヴ同胞の解放。ヴォイヴォディナ獲得 |
| ハンガリー (HUN) | 防衛側 | 現領土の維持。多民族国家の統合 |
| ルーマニア (ROM) | 日和見参戦 | 全トランシルヴァニアの回復（セーケイ地方含む） |
| ドイツ (GER) | 後援者 | バルカンにおけるドイツの影響力維持。ハンガリーを緩衝国として保全 |
| ロシア (RUS) | 後援者 | バルカンにおけるロシアの影響圏拡大。汎スラヴ主義の推進 |

---

## イベントチェーンフロー

```
[1936.10〜12月] .1(HUN) 国境事変 [date trigger, MTTH 14日]
       |
       | 45日後
       v
  .2(YUG) 宣戦布告 → declare_war_on HUN
       |
       +── 1日後 ──→ .3(HUN) 宣戦通知
       +── 1日後 ──→ .100 ニュース「バルカン戦争勃発」
       +── 3日後 ──→ .4(GER) 支援決定 ──→ +2日 → .6(HUN) 独支援到着
       +── 3日後 ──→ .5(RUS) 支援決定 ──→ +2日 → .7(YUG) 露支援到着
       +── 45日後 ─→ .8(ROM) 参戦 ──→ +1日 → .9(HUN) ROM参戦通知
       |                              +1日 → .101 ニュース「ルーマニア参戦」
       |
       +── 30日後 ─→ .10(HUN) 蜂起判定ポーリング開始
                        [hidden, 15日毎ループ, surrender_progress > 0.3]
                        |
                        | 条件達成 → +5日
                        v
                    .11(HUN) 少数民族蜂起
                        ├→ BNT独立 (82,764) → .12通知
                        ├→ SLO独立 (70のみ) → .13通知
                        └→ RUT独立 (73) → .14通知
                        |
                        | +10日
                        v
                    .22(HUN) 講和判定ポーリング開始
                        [hidden, 10日毎ループ, sp>0.7 or Budapest陥落]
                        |
                        | 条件達成 → +3日
                        v
                    .15(HUN) 講和 → tsr_balkan_war_peace_settlement
                        ├→ +1日  → .16(YUG) 勝利通知
                        ├→ +1日  → .17(ROM) トランシルヴァニア回復通知
                        ├→ +1日  → .102 ニュース「バルカン戦争終結」
                        ├→ +30日 → .18(YUG) バナト分割
                        |              └→ .19(ROM) 分割通知
                        |              └→ .103 ニュース「バナト分割」
                        └→ +45日 → .20(HUN) ブルゲンラント割譲
                                       └→ .21(GER) 取得通知
```

---

## 設計判断

### ポーリング2段階制

蜂起（.10, sp>0.3）と講和（.22, sp>0.7 or Budapest）を独立した2つのhiddenイベントで実装。
これにより蜂起と講和の間に最低10日+α の時間差が生まれ、プレイヤーが蜂起の影響を体感できる。

### SLO部分蜂起

蜂起時はstate 70（ブラチスラバ周辺）のみ独立。残り(71, 664)は講和時に移譲。
ゲームプレイ上、全州同時独立だとHUNの崩壊が即時すぎるため。

### 代理戦争の速度制御

両陣営の国民精神に`army_speed_factor = -0.2`を付与。
師団移動速度を下げて戦線が一気に動くのを防ぎ、膠着状態を演出。

### バニラ講和会議の不使用

`white_peace` + 手動`transfer_state`でカスタム講和を実装。
バニラの講和会議はAI判断で結果が不定になるため、スクリプト制御が確実。

### 陣営管理

- .1でバルカン協商を結成、ROMを事前加盟（add_to_warに必要）
- 蜂起時にBNT/SLO/RUTもバルカン協商に加盟
- `DIPLOMACY_LEAVE_FACTION_ENABLE_TRIGGER`を`always = no`で脱退不可

### 戦後の二つの清算

1. **バナト分割**（講和30日後）: BNTをYUG/ROMで分割。764→YUG, 82→ROM。BNT事実上消滅。
2. **ブルゲンラント割譲**（講和45日後）: 戦時借款返済不能のHUNが代償としてstate 975をGERに割譲。

---

## イベント一覧（全25イベント）

### メインチェーン

| ID | 対象 | 種別 | 概要 |
|----|------|------|------|
| .1 | HUN | date trigger | 国境事変。バルカン協商結成。45日後に.2発火 |
| .2 | YUG | triggered | 宣戦布告。全後続イベントを一括予約 |
| .3 | HUN | triggered | 宣戦通知。war_support+15%, stability-10% |
| .4 | GER | triggered | HUN支援。装備送付+国民精神付与 |
| .5 | RUS | triggered | YUG支援。装備送付+国民精神付与 |
| .6 | HUN | triggered | 独支援到着通知 |
| .7 | YUG | triggered | 露支援到着通知 |
| .8 | ROM | triggered | 参戦。add_to_warでYUG側合流 |
| .9 | HUN | triggered | ROM参戦通知。stability-10% |
| .10 | HUN | hidden | 蜂起判定ポーリング（15日毎, sp>0.3） |
| .11 | HUN | triggered | 少数民族蜂起。3カ国同時独立 |
| .12 | BNT | triggered | BNT独立通知 |
| .13 | SLO | triggered | SLO独立通知 |
| .14 | RUT | triggered | RUT独立通知 |
| .22 | HUN | hidden | 講和判定ポーリング（10日毎, sp>0.7 or Budapest） |
| .15 | HUN | triggered | 講和。peace_settlement effect実行 |
| .16 | YUG | triggered | 勝利通知。PP+100 |
| .17 | ROM | triggered | トランシルヴァニア回復通知。PP+100 |

### 戦後イベント

| ID | 対象 | 概要 |
|----|------|------|
| .18 | YUG | バナト分割提案。764→YUG, 82→ROM |
| .19 | ROM | バナト分割通知。PP+50 |
| .20 | HUN | ブルゲンラント割譲。975→GER |
| .21 | GER | ブルゲンラント取得通知。PP+50 |

### ニュースイベント

| ID | 概要 | 備考 |
|----|------|------|
| .100 | バルカン戦争勃発 | major=yes, tag別option 3分岐 |
| .101 | ルーマニア参戦 | major=yes, tag別option 3分岐 |
| .102 | バルカン戦争終結 | major=yes, tag別option 3分岐 |
| .103 | バナト分割 | major=yes, tag別option 2分岐 |

---

## 国民精神

### 初期

| ID | 対象 | 効果 |
|----|------|------|
| `tsr_hun_multiethnic_army` | HUN | non_core_manpower +15%, org -5%, morale -10%, stability -5% |

### 戦中

| ID | 対象 | 効果 |
|----|------|------|
| `tsr_german_proxy_support` | HUN | atk +10%, def +10%, org +5%, supply -10%, **speed -20%** |
| `tsr_russian_war_loan` | YUG | atk +15%, def +15%, org +10%, supply -20%, arms_factory +20%, **speed -20%** |
| `tsr_transylvania_irredentism` | ROM | atk +5%, morale +10%, war_support +10% |

### 戦後

| ID | 対象 | 効果 | 備考 |
|----|------|------|------|
| `tsr_balkan_war_exhaustion` | HUN | stability -10%, war_support -15%, PP -10% | NFで段階除去想定 |
| `tsr_yug_war_debt` | YUG | civ_factory_use +3, PP -15%, stability -5%, consumer +10% | 借款→債務置換 |

---

## 戦後の領土変更

| State | 名称 | 戦前 | 戦後 | 移譲方法 |
|-------|------|------|------|----------|
| 43 | 北ハンガリー（首都） | HUN | HUN | 残留 |
| 155 | 西ハンガリー | HUN | HUN | 残留 |
| 45 | ヴォイヴォディナ | HUN | YUG | peace_settlement |
| 1049 | プレクムリェ | HUN | YUG | peace_settlement |
| 82 | バナト | HUN | BNT→ROM | 蜂起→バナト分割(.18) |
| 764 | 西バナト | HUN | BNT→YUG | 蜂起→バナト分割(.18) |
| 70 | スロヴァキア | HUN | SLO | 蜂起(.11) |
| 71 | 東スロヴァキア | HUN | SLO | peace_settlement |
| 664 | 南スロヴァキア | HUN | SLO | peace_settlement |
| 73 | カルパト・ルテニア | HUN | RUT | 蜂起(.11) |
| 1054 | セーケイ地方 | HUN | ROM | peace_settlement（コア追加） |
| 83 | クリシャナ | HUN | ROM | peace_settlement（コア追加） |
| 975 | ブルゲンラント | HUN | GER | 戦後借款返済(.20) |

HUNはState 43（ブダペスト）と155（西ハンガリー）のみの残存国家となる。

```
戦前                                戦後

  ┌──SLO────────┐                  ┌──SLO──────┐
  │ 70, 71, 664 │                  │ 70,71,664 │
  ├──RUT┬───────┤                  ├──RUT┬─────┤
  │ 73  │       │                  │ 73  │     │
  ├─────┤  HUN  │                  ├─GER─┤ HUN │
  │     │ 43,155│                  │ 975 │43,155│
  │     │  975  │                  ├─────┤     │
  ├─────┼───────┤                  ├──ROM─┼─────┤
  │BNT  │       │                  │82    │1054 │
  │82,764│ 1054 │                  ├──YUG─┤ 83 │
  ├─────┤  83   │                  │764,45│     │
  │  45 │       │                  │ 1049 │     │
  └─────┴───────┘                  └──────┴─────┘
   全てHUN所有
```

---

## 蜂起部隊（OOB）

### SLO_revolt（3個師団）

| 師団名 | 省 | State |
|--------|-----|-------|
| ブラチスラバ義勇連隊 | 9692 (Bratislava) | 70 |
| ジリナ義勇連隊 | 11539 (Žilina) | 70 |
| ニトラ義勇連隊 | 541 (Nitra) | 70 |

### RUT_revolt（2個師団）

| 師団名 | 省 | State |
|--------|-----|-------|
| ウジュホロド義勇連隊 | 11691 (Uzhhorod) | 73 |
| ムカチェヴォ義勇連隊 | 3548 (Mukachevo) | 73 |

---

## 新規国家：バナト共和国 (BNT)

| 項目 | 値 |
|------|-----|
| タグ | BNT |
| 首都 | State 82（バナト） |
| 領土 | State 82, 764 |
| 政体 | 中道 (center, 45%) |
| グラフィック | eastern_european_gfx |
| 色 | rgb { 180 140 90 } |
| 登場 | 蜂起イベント(.11)で独立 |
| 消滅 | バナト分割(.18/.19)で全領土喪失 |

---

## 使用フラグ

| フラグ名 | スコープ | 用途 |
|----------|----------|------|
| `tsr_balkan_war_started` | HUN | .1の重複発火防止 |
| `tsr_balkan_subversion_fired` | HUN | .10蜂起ポーリングの一度きり実行保証 |

---

## ファイル構成

```
events/
└── TR_balkan_war_events.txt              # 全25イベント

common/
├── country_tags/
│   └── 00_countries.txt                  # BNTタグ追加
├── countries/
│   └── Banat.txt                         # BNT色・グラフィック
├── factions/templates/
│   └── Tsareich2_factions.txt            # faction_template_balkan_entente
├── ideas/
│   └── TR_balkan_war_ideas.txt           # 国民精神7種（初期1+戦中3+戦後2+多民族軍1）
├── scripted_effects/
│   └── TR_balkan_war_effects.txt         # 国家解放3+講和処理1
├── scripted_triggers/
│   ├── TR_balkan_war_triggers.txt        # 状態判定7種
│   └── diplomacy_scripted_triggers.txt   # LEAVE_FACTION always=no
└── ...

history/
├── countries/
│   └── BNT - Banat.txt                   # バナト基本設定
├── states/
│   ├── 43-Hungary.txt                    # VP追加: Miskolc
│   ├── 45-Yugoslavia.txt                 # VP追加: Subotica
│   ├── 83-crisana.txt                    # VP強化: Arad 3
│   ├── 154-Southern plain.txt            # VP追加: Kecskemét, Nyíregyháza
│   ├── 155-Western Hungary.txt           # VP追加: Szombathely
│   ├── 973 - Bacs.txt                    # VP強化: Szeged 5
│   ├── 974 - South Transdanubia.txt      # VP追加: Kaposvár
│   ├── 1049-Prekmurje.txt                # VP追加: Murska Sobota
│   └── 1054-Szekely Land.txt             # VP追加: Oradea
└── units/
    ├── SLO_revolt.txt                     # 3個師団 (state 70内)
    └── RUT_revolt.txt                     # 2個師団 (state 73内)

localisation/japanese/
├── countries_l_japanese.yml               # BNT・RUT名称
├── factions_tr_l_japanese.yml             # バルカン協商
├── TR_balkan_war_l_japanese.yml           # イベント・精神テキスト
└── victory_points_l_japanese.yml          # 追加VP名称
```

---

## 検証手順

1. mod起動時に`logs/error.log`でBNTタグ・ローカライゼーション関連エラーがないことを確認
2. コンソール`event tsr_balkan_war.1 HUN`でイベントチェーン開始を確認
3. 1936年10月以降に自然発火することを確認
4. 宣戦→代理支援→ルーマニア参戦→少数民族蜂起→講和の全フローを通し確認
5. 戦後: バナト分割(30日後)とブルゲンラント割譲(45日後)が発火することを確認
6. 戦後の領土配置が上記表の通りか地図上で確認
7. 国民精神の付与・置換が正しく行われているか確認
