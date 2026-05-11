# 議会システム設計計画

## 概要
半円形の議席図を表示し、各政党の議席数・党首を可視化する汎用議会システム。
ドイツ帝国を最初の実装対象とするが、他国にも展開可能な構造とする。

---

## 確定仕様

| 項目 | 決定 |
|------|------|
| 政党構造 | 1イデオロギーグループ = 1政党（7政党） |
| 総議席数 | 397席（史実帝国議会） |
| 議席計算 | 選挙イベント時にpopularityベースで再配分。選挙間は固定 |
| GUI議席数 | 100個のアイコン（1アイコン ≈ 4席） |
| ゲーム影響 | Phase 1は表示のみ |
| アクセス | 政治タブ上にボタンを配置 → オーバーレイとして表示 |
| 党首 | 既存のイデオロギーリーダー（country_leader）を流用 |
| ローカライズ | token変数 + meta_effect 方式 |

### ドイツ帝国 1936年初期構成

| # | イデオロギー | 政党名 | 支持率 | 議席数(≈) |
|---|---|---|---|---|
| 0 | far_left | ドイツ共産党 | 4% | 16 |
| 1 | left | ドイツ社会主義労働者党 | 11% | 44 |
| 2 | center_left | ドイツ社会民主党 | 21% | 83 |
| 3 | center | 進歩人民党 | 14% | 56 |
| 4 | center_right | 中央党 | 16% | 63 |
| 5 | right | 保守ブロック | 29% | 115 |
| 6 | far_right | ドイツ民族自由党 | 5% | 20 |

※ 合計 397席。選挙が発生していない状態（帝政: elections_allowed = no）

---

## ファイル構造

```
common/
├── scripted_guis/
│   └── parliament_gui.txt              # Scripted GUI ロジック
├── scripted_effects/
│   └── parliament_effects.txt          # 初期化・選挙時更新effect
├── scripted_localisation/
│   └── parliament_scripted_loc.txt     # token変数表示用
├── on_actions/
│   └── parliament_on_actions.txt       # on_startup等で初期化呼び出し
│
interface/
│   └── parliament_view.gui             # GUI定義（半円+政党リスト+ボタン）
│
gfx/
│   ├── FX/
│   │   └── parliament_bar.shader      # 7色議席配分バー用shader（作成済み）
│   └── interface/parliament/
│       ├── parliament_seat_strip.dds   # 議席アイコン（7フレーム、各色1コマ）
│       ├── parliament_bg.dds           # 半円図の背景
│       ├── parliament_bar.dds          # 配分バー用テクスチャ
│       └── parliament_button.dds       # 政治タブ上のボタン
│
localisation/japanese/
│   └── parliament_l_japanese.yml       # 固定UI文字列
```

---

## データ構造設計

### 1. 変数一覧（country scope）

```pdx
# --- 基本情報 ---
parliament_total_seats = 397            # 総議席数
parliament_num_parties = 7              # 政党数（= イデオロギー数）
parliament_dirty_flag                   # GUI更新トリガー用

# --- 政党別データ（0～6） ---
# 議席数
parliament_seats_0 = 16                 # far_left
parliament_seats_1 = 44                 # left
parliament_seats_2 = 83                 # center_left
parliament_seats_3 = 56                 # center
parliament_seats_4 = 63                 # center_right
parliament_seats_5 = 115               # right
parliament_seats_6 = 20                # far_right

# 政党名token（ローカライズキーとして使用）
parliament_party_name_0 = token:GER_far_left_party
parliament_party_name_1 = token:GER_left_party
parliament_party_name_2 = token:GER_center_left_party
parliament_party_name_3 = token:GER_center_party
parliament_party_name_4 = token:GER_center_right_party
parliament_party_name_5 = token:GER_right_party
parliament_party_name_6 = token:GER_far_right_party

# イデオロギーtoken（色の決定に使用）
parliament_party_ideology_0 = token:far_left
parliament_party_ideology_1 = token:left
parliament_party_ideology_2 = token:center_left
parliament_party_ideology_3 = token:center
parliament_party_ideology_4 = token:center_right
parliament_party_ideology_5 = token:right
parliament_party_ideology_6 = token:far_right

# --- 配列 ---
parliament_parties = [ 0, 1, 2, 3, 4, 5, 6 ]  # 政党インデックス配列
```

### 2. 議席アイコンの色制御方式

#### 検討: shaderによる動的色変更
バニラの `progress.shader` を元に、7色対応shaderを作成することを検討した。
しかし、HoI4のshaderシステムには以下の制約がある:

- `progressbartype` がshaderに渡せるパラメータは `vFirstColor`(float4), `vSecondColor`(float4), `CurrentState`(float) の計9値のみ
- `iconType` の場合、`frame` はスプライトシートのコマ選択に使われ、shaderの `CurrentState` には渡されない
- `.gfx` で定義する `color`/`colortwo` は起動時に固定され、scripted GUIから実行時に変更不可

**結論: 個別の議席アイコンの色を変数によってshaderで変えることはできない。**

#### 採用方式: 7フレームスプライトシート + properties

代わりに、7色分のコマを持つスプライトシート（`noOfFrames = 7`）を用意し、
scripted GUIの `properties` で `frame` を変数から設定する方式を採用する。

```gfx
spriteType = {
    name = "GFX_parliament_seat"
    texturefile = "gfx/interface/parliament/parliament_seat_strip.dds"
    noOfFrames = 7   # 1=far_left, 2=left, 3=center_left, 4=center, 5=center_right, 6=right, 7=far_right
}
```

100個のアイコンへの色割り当て方法:
```
議席0～3   → far_left (16席 / 397 * 100 ≈ 4個)  → frame 1
議席4～14  → left (44席 / 397 * 100 ≈ 11個)      → frame 2
議席15～35 → center_left (83席 / 397 * 100 ≈ 21個) → frame 3
議席36～49 → center (56席 / 397 * 100 ≈ 14個)    → frame 4
議席50～65 → center_right (63席 / 397 * 100 ≈ 16個) → frame 5
議席66～94 → right (115席 / 397 * 100 ≈ 29個)    → frame 6
議席95～99 → far_right (20席 / 397 * 100 ≈ 5個)  → frame 7
```

scripted GUIのpropertiesでframe値を動的設定:
```pdx
properties = {
    seat_0 = { frame = parliament_seat_color_0 }
    seat_1 = { frame = parliament_seat_color_1 }
    # ... seat_2 ～ seat_99
}
```

各 `parliament_seat_color_N` 変数（1～7のframe値）は選挙時にcumulative sumで再計算。

#### 補助: 議席配分バー（parliament_bar.shader）

半円図の下に議席配分の水平バーを配置する。これにはカスタムshaderを使用:
- `gfx/FX/parliament_bar.shader`（作成済み）
- 7色をshaderにハードコード（イデオロギー色は固定のため）
- 6つの累積閾値を `color`(RGBA=4値) + `colortwo`(RG=2値) にエンコード
- ドイツ1936年初期値: `color = { 0.04 0.15 0.36 0.50 }` `colortwo = { 0.66 0.95 0.0 1.0 }`
- 制約: `.gfx`定義は起動時固定のため、選挙による動的更新には非対応（Phase 2で対策検討）

各イデオロギーグループの色（`common/ideologies/00_ideologies.txt` より）:

| # | イデオロギー | RGB (0-255) | shader値 (0-1) |
|---|---|---|---|
| 0 | far_left | 139, 0, 0 | 0.545, 0.000, 0.000 |
| 1 | left | 186, 36, 68 | 0.729, 0.141, 0.267 |
| 2 | center_left | 214, 96, 152 | 0.839, 0.376, 0.596 |
| 3 | center | 212, 132, 32 | 0.831, 0.518, 0.125 |
| 4 | center_right | 120, 168, 196 | 0.471, 0.659, 0.769 |
| 5 | right | 92, 118, 148 | 0.361, 0.463, 0.580 |
| 6 | far_right | 42, 48, 80 | 0.165, 0.188, 0.314 |

---

## scripted_effect 詳細

### 初期化

```pdx
# common/scripted_effects/parliament_effects.txt

# マスター初期化（on_startupから呼ぶ）
initialize_parliament = {
    if = {
        limit = { tag = GER }
        GER_initialize_parliament = yes
    }
    # 将来: FRA, ENG 等を追加
}

GER_initialize_parliament = {
    set_variable = { parliament_total_seats = 397 }
    set_variable = { parliament_num_parties = 7 }
    
    # 配列初期化
    clear_array = parliament_parties
    add_to_array = { parliament_parties = 0 }
    add_to_array = { parliament_parties = 1 }
    add_to_array = { parliament_parties = 2 }
    add_to_array = { parliament_parties = 3 }
    add_to_array = { parliament_parties = 4 }
    add_to_array = { parliament_parties = 5 }
    add_to_array = { parliament_parties = 6 }
    
    # 政党名token
    set_variable = { parliament_party_name_0 = token:GER_far_left_party }
    set_variable = { parliament_party_name_1 = token:GER_left_party }
    set_variable = { parliament_party_name_2 = token:GER_center_left_party }
    set_variable = { parliament_party_name_3 = token:GER_center_party }
    set_variable = { parliament_party_name_4 = token:GER_center_right_party }
    set_variable = { parliament_party_name_5 = token:GER_right_party }
    set_variable = { parliament_party_name_6 = token:GER_far_right_party }
    
    # イデオロギーtoken
    set_variable = { parliament_party_ideology_0 = token:far_left }
    set_variable = { parliament_party_ideology_1 = token:left }
    set_variable = { parliament_party_ideology_2 = token:center_left }
    set_variable = { parliament_party_ideology_3 = token:center }
    set_variable = { parliament_party_ideology_4 = token:center_right }
    set_variable = { parliament_party_ideology_5 = token:right }
    set_variable = { parliament_party_ideology_6 = token:far_right }
    
    # 初期議席配分（popularityベース）
    update_parliament_from_popularity = yes
}
```

### 選挙時の議席再計算

```pdx
update_parliament_from_popularity = {
    # 各イデオロギーのpopularityを取得し、397席で比例配分
    # HoI4ではparty_popularity_100を使って整数値(0-100)を取得可能
    
    # far_left
    set_temp_variable = { temp_pop = party_popularity_100@far_left }
    set_temp_variable = { temp_seats = temp_pop }
    multiply_variable = { temp_seats = 3.97 }  # 397/100
    round_variable = temp_seats
    set_variable = { parliament_seats_0 = temp_seats }
    
    # left
    set_temp_variable = { temp_pop = party_popularity_100@left }
    set_temp_variable = { temp_seats = temp_pop }
    multiply_variable = { temp_seats = 3.97 }
    round_variable = temp_seats
    set_variable = { parliament_seats_1 = temp_seats }
    
    # ... 同様に 2～6
    # (meta_effectでループ化可能)
    
    # GUI議席色の再計算
    update_parliament_seat_colors = yes
    
    # dirty flagを変更してGUI更新をトリガー
    add_to_variable = { parliament_dirty_flag = 1 }
}
```

### meta_effectによるループ化

```pdx
# 7政党分をmeta_effectで一括処理
update_parliament_from_popularity_meta = {
    # イデオロギー名の配列を用意
    set_temp_variable = { iter = 0 }
    
    # 各政党について実行
    meta_effect = {
        text = {
            set_temp_variable = { temp_pop = party_popularity_100@[IDEOLOGY] }
            set_temp_variable = { temp_seats = temp_pop }
            multiply_variable = { temp_seats = 3.97 }
            round_variable = temp_seats
            set_variable = { parliament_seats_[IDX] = temp_seats }
        }
        IDX = "0"
        IDEOLOGY = "far_left"
    }
    meta_effect = {
        text = {
            set_temp_variable = { temp_pop = party_popularity_100@[IDEOLOGY] }
            set_temp_variable = { temp_seats = temp_pop }
            multiply_variable = { temp_seats = 3.97 }
            round_variable = temp_seats
            set_variable = { parliament_seats_[IDX] = temp_seats }
        }
        IDX = "1"
        IDEOLOGY = "left"
    }
    # ... 2～6 同様
}
```

### 100個の議席色を計算

```pdx
update_parliament_seat_colors = {
    # cumulative sum方式で各座席がどの政党に属するか判定
    # 100アイコンに対して比例配分
    
    set_temp_variable = { cum = 0 }
    set_temp_variable = { party_idx = 1 }  # frame値（1始まり）
    
    # seat_color_Nを1～7のframe値で設定
    # 計算: アイコンN番目 → (N * 397 / 100) が何議席目か → その議席の政党
    
    # meta_effectで100個分を生成するか、
    # 外部スクリプトで生成したscripted_effectとして埋め込む
    
    # 簡易版: 各政党の100アイコン中の割当数を計算
    set_temp_variable = { icons_0 = parliament_seats_0 }
    multiply_variable = { icons_0 = 0.252 }  # 100/397
    round_variable = icons_0
    # ... 同様に icons_1 ～ icons_6
    
    # ここからmeta_effectまたは手動でseat_color_0～99を設定
}
```

---

## GUI設計

### 政治タブ上のボタン

```gui
# countrypoliticsview.gui に追加（またはオーバーレイ）
# 政治タブのcontainerの上にScripted GUIのcontainerを重ねる

containerWindowType = {
    name = "parliament_button_container"
    position = { x=0 y=0 }
    
    buttonType = {
        name = "parliament_open_button"
        position = { x=520 y=80 }
        spriteType = "GFX_parliament_button"
        tooltip = "PARLIAMENT_BUTTON_TT"
    }
}
```

### 半円議席図（100個のアイコン）

座標はPythonで事前計算:
```python
import math
# 3列の半円配置（内側33個、中間33個、外側34個）
rows = [
    {"count": 28, "radius": 100},  # 内側
    {"count": 33, "radius": 130},  # 中間
    {"count": 39, "radius": 160},  # 外側
]
# 合計100個

center_x, center_y = 300, 280  # 半円の中心（下端）

for row in rows:
    for i in range(row["count"]):
        angle = math.pi * (i + 0.5) / row["count"]  # 0～π
        x = center_x - row["radius"] * math.cos(angle)
        y = center_y - row["radius"] * math.sin(angle)
        # → .guiファイルのposition値として出力
```

```gui
# interface/parliament_view.gui
containerWindowType = {
    name = "parliament_window"
    position = { x=100 y=50 }
    size = { width=700 height=500 }
    moveable = yes
    
    background = {
        name = "bg"
        spriteType = "GFX_parliament_bg"
    }
    
    # 閉じるボタン
    buttonType = {
        name = "parliament_close_button"
        position = { x=660 y=10 }
        spriteType = "GFX_closebutton"
    }
    
    # === 半円議席エリア ===
    containerWindowType = {
        name = "parliament_seats_container"
        position = { x=50 y=20 }
        size = { width=400 height=300 }
        
        # 100個の議席アイコン（座標はPythonで生成）
        iconType = { name = "seat_0"  position = { x=... y=... } spriteType = "GFX_parliament_seat" }
        iconType = { name = "seat_1"  position = { x=... y=... } spriteType = "GFX_parliament_seat" }
        # ... seat_2 ～ seat_99
    }
    
    # === 政党リスト ===
    containerWindowType = {
        name = "parliament_party_panel"
        position = { x=470 y=20 }
        size = { width=220 height=450 }
        
        gridBoxType = {
            name = "parliament_party_grid"
            position = { x=0 y=0 }
            size = { width=220 height=450 }
            slotsize = { width=220 height=60 }
            max_slots_horizontal = 1
            format = "UPPER_LEFT"
        }
    }
    
    # === 総議席数テキスト ===
    instantTextBoxType = {
        name = "total_seats_text"
        position = { x=150 y=310 }
        text = "[?parliament_total_seats] 議席"
        font = "hoi_18mbs"
        maxWidth = 200
        format = center
    }
}

# 政党リスト1エントリのテンプレート
containerWindowType = {
    name = "parliament_party_entry"
    size = { width=220 height=55 }
    
    # 政党カラーバー
    iconType = {
        name = "party_color_bar"
        position = { x=0 y=5 }
        spriteType = "GFX_parliament_party_color"  # 7フレーム
    }
    
    # 政党名（token変数から取得）
    instantTextBoxType = {
        name = "party_name_text"
        position = { x=15 y=3 }
        text = "[?parliament_party_name_0.GetTokenLocalizedKey]"  # ← scripted_locで動的に
        font = "hoi_16mbs"
        maxWidth = 200
    }
    
    # 議席数
    instantTextBoxType = {
        name = "party_seats_text"
        position = { x=15 y=22 }
        text = "[?parliament_seats_0] 席"
        font = "hoi_18mbs"
        maxWidth = 100
    }
    
    # 党首名（イデオロギーリーダー）
    instantTextBoxType = {
        name = "party_leader_text"
        position = { x=15 y=40 }
        font = "hoi_16mbs"
        maxWidth = 200
    }
}
```

### Scripted GUI定義

```pdx
# common/scripted_guis/parliament_gui.txt
scripted_gui = {
    parliament_main = {
        window_name = "parliament_window"
        context_type = player_context
        dirty = parliament_dirty_flag
        
        # ウィンドウ表示条件
        visible = {
            has_variable = parliament_num_parties
        }
        
        # 政党リストのdynamic_list
        dynamic_lists = {
            parliament_party_grid = {
                array = parliament_parties
                value = v
                index = i
                change_scope = no
                entry_container = "parliament_party_entry"
            }
        }
        
        # 各議席アイコンのframe（色）を動的設定
        properties = {
            seat_0 = { frame = parliament_seat_color_0 }
            seat_1 = { frame = parliament_seat_color_1 }
            seat_2 = { frame = parliament_seat_color_2 }
            # ... seat_3 ～ seat_99
        }
        
        # ボタン操作
        effects = {
            parliament_open_button_click = {
                # ウィンドウ表示/非表示トグル
            }
            parliament_close_button_click = {
                # ウィンドウを閉じる
            }
        }
        
        triggers = {
            parliament_open_button_visible = {
                has_variable = parliament_num_parties
            }
        }
    }
}
```

---

## 動的ローカライズの3手法

### a) Scripted Localisation — 条件分岐でテキストを切り替え
```pdx
# common/scripted_localisation/parliament_scripted_loc.txt
defined_text = {
    name = GetPartyName
    text = {
        trigger = { check_variable = { v = 0 } }
        localization_key = "GER_party_spd"
    }
    text = {
        trigger = { check_variable = { v = 1 } }
        localization_key = "GER_party_zentrum"
    }
}
# GUI上では [ROOT.GetPartyName] で表示
```

### b) Token変数 — ゲーム定義のローカライズキーを直接取得
```pdx
# 初期化時にtokenを格納
set_variable = { parliament_party_name_0 = token:GER_far_left_party }

# GUIローカライズで: [?parliament_party_name_0.GetTokenLocalizedKey]
# → 「ドイツ共産党」が表示される

# 政党名変更時:
set_variable = { parliament_party_name_0 = token:GER_far_left_party_reformed }
# → GUI表示が自動的に新しいキーの値に切り替わる
```

### c) meta_effect — 変数名・文字列を動的に組み立て
```pdx
# for_each_loopと組み合わせて、変数名のインデックス部分を動的生成
meta_effect = {
    text = {
        set_variable = { parliament_seats_[IDX] = temp_seats }
    }
    IDX = "[?v]"
}
# → ループ中にIDXが展開され、政党ごとに個別の変数を設定できる
```

### 使い分け
| 手法 | 本システムでの用途 |
|------|---|
| token変数 | 政党名表示、イデオロギー名表示 |
| meta_effect | 議席計算ループ、座席色計算の変数名構築 |
| scripted_localisation | 党首名表示（country_leader取得用） |

---

## 実装ステップ

### Phase 1: 表示のみの議会システム
1. Pythonで100座席の半円座標を生成
2. `interface/parliament_view.gui` — GUI定義
3. `gfx/` — 議席アイコン・背景・ボタン画像作成
4. `common/scripted_effects/parliament_effects.txt` — 初期化・座席色計算
5. `common/scripted_guis/parliament_gui.txt` — GUI接続
6. `common/on_actions/` — on_startupでinitialize_parliament呼び出し
7. `localisation/` — UIテキスト
8. GER historyファイルまたはon_startupで初期化実行

### Phase 2（将来）: 選挙・動的更新
- 選挙イベント作成
- popularity変動 → 議席再配分
- 帝政 → 民主化への遷移時に選挙を解禁

### Phase 3（将来）: 他国展開・ゲーム影響
- フランス、イギリス等のプリセット追加
- 議席配分による国民精神・政策への影響

---

## 技術的課題・検討事項

1. **半円座標の事前計算**
   - Pythonで3列×100個の座標を生成 → .guiに直接埋め込み
   - 列構成: 内側28個、中間33個、外側39個（合計100）

2. **100個のpropertiesの記述量**
   - seat_0 ～ seat_99 のproperties定義が必要
   - Pythonで生成するか、手動で書くか → Python生成が現実的

3. **議席色変数100個の計算**
   - `parliament_seat_color_0` ～ `parliament_seat_color_99`
   - cumulative sumでどの政党の範囲かを判定しframe値を設定
   - meta_effectでループ生成可能

4. **政治タブとの連携**
   - 政治タブはハードコーディングされている
   - `countrypoliticsview.gui` の上にScripted GUIのcontainerをオーバーレイ
   - context_type = player_context で政治タブ表示中に重ねて描画

5. **token変数の有効性確認**
   - `GER_far_left_party` 等のキーがtokenとして使えるか要検証
   - 使えない場合は scripted_localisation でフォールバック

6. **meta_effect / token変数の活用範囲**
   - 変数名の動的構築: `parliament_seats_[IDX]` のインデックス展開
   - GUIテキスト: `[?var.GetTokenLocalizedKey]` で直接ローカライズ表示
   - 汎用化の鍵: 政党数が国ごとに異なっても対応可能

7. **shaderの制約と使い分け（調査済み）**
   - HoI4の `progressbartype` がshaderに渡せるのは `color`(4float) + `colortwo`(4float) + `CurrentState`(1float) のみ
   - `iconType` では `frame` がスプライトシートのコマ選択に使われ、shader変数には渡されない
   - `.gfx` の `color`/`colortwo` は起動時固定、scripted GUIから動的変更不可
   - **議席アイコン**: shaderによる動的色変更は不可 → 7フレームスプライトシート + properties/frame方式を採用
   - **配分バー**: `parliament_bar.shader`（作成済み）で7色表示。閾値はcolorパラメータにエンコード。動的更新は将来課題
   - `parliament_semicircle.shader` も作成済みだが、議席図はgridbox方式で実装するため現時点では不使用
   - `.lua` 参照（`effectFile = "gfx/FX/xxx.lua"`）は実ファイル不要。エンジンが自動的に `xxx.shader` を解決する
