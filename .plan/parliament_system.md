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
| 議席図方式 | dynamic_list + 並列配列。1テンプレートを100回生成し、propertiesでx/y/frameを動的設定 |
| 議席色方式 | 7フレームスプライトシート + properties/frame（shaderでは不可。詳細は技術メモ参照） |
| ゲーム影響 | Phase 1は表示のみ |
| アクセス | `parent_window_token = politics_tab` で寄生するボタンGUI + 独立した議会ビューGUI（2層構造） |
| 開閉制御 | `parliament_view_open` 変数の有無でトグル |
| 党首 | 既存のイデオロギーリーダー（country_leader）を流用 |
| ローカライズ | token変数（`[?array^i.GetTokenLocalizedKey]`）+ meta_effect + scripted_localisation |
| データ構造 | 同サイズの並列配列を `^i` で共有インデックスアクセスする擬似2次元テーブル |

### ドイツ帝国 1936年初期構成

| # | イデオロギー | 政党名 | 支持率 | 議席数(≈) | 色 RGB |
|---|---|---|---|---|---|
| 0 | far_left | ドイツ共産党 | 4% | 16 | 139, 0, 0 |
| 1 | left | ドイツ社会主義労働者党 | 11% | 44 | 186, 36, 68 |
| 2 | center_left | ドイツ社会民主党 | 21% | 83 | 214, 96, 152 |
| 3 | center | 進歩人民党 | 14% | 56 | 212, 132, 32 |
| 4 | center_right | 中央党 | 16% | 63 | 120, 168, 196 |
| 5 | right | 保守ブロック | 29% | 115 | 92, 118, 148 |
| 6 | far_right | ドイツ民族自由党 | 5% | 20 | 42, 48, 80 |

※ 合計 397席。選挙が発生していない状態（帝政: elections_allowed = no）

---

## ファイル構造

```
common/
├── scripted_guis/
│   └── parliament_gui.txt              # Scripted GUI（ボタン + 議会ビュー）
├── scripted_effects/
│   └── parliament_effects.txt          # 初期化・議席計算・座標配列
├── scripted_localisation/
│   └── parliament_scripted_loc.txt     # 党首名表示用
├── on_actions/
│   └── parliament_on_actions.txt       # on_startupで初期化呼び出し

interface/
├── parliament_view.gui                 # GUI定義（ウィンドウ + テンプレート）
├── parliament_view.gfx                 # スプライト定義

gfx/
├── FX/
│   ├── parliament_bar.shader           # 7色配分バー用shader（作成済み）
│   └── parliament_semicircle.shader    # 半円shader（予備、現時点では不使用）
└── interface/parliament/
    ├── parliament_seat_strip.dds       # 議席アイコン（7フレーム、各色1コマ）
    ├── parliament_party_color.dds      # 政党カラーバー（7フレーム）
    ├── parliament_bg.dds               # ウィンドウ背景
    └── parliament_button.dds           # 政治タブ上のボタン

localisation/japanese/
└── parliament_l_japanese.yml           # UI文字列
```

---

## データ構造設計

同サイズの並列配列を `^i` で共有インデックスアクセスし、擬似2次元テーブルとして運用する。

### スカラー変数（country scope）

```pdx
parliament_total_seats = 397       # 総議席数
parliament_num_parties = 7         # 政党数
parliament_dirty_flag              # GUI更新トリガー用（dirty）
parliament_view_open               # ウィンドウ表示フラグ（有=表示、無=非表示）
```

### 議席テーブル（並列配列、100要素）

`parliament_seat_grid` の dynamic_list 駆動用。

```
parliament_seats        = [0, 1, 2, ..., 99]     # インデックス（駆動用）
parliament_seat_x       = [x0, x1, ..., x99]     # X座標（Python事前計算）
parliament_seat_y       = [y0, y1, ..., y99]     # Y座標（Python事前計算）
parliament_seat_color   = [f0, f1, ..., f99]     # frame値 1-7（政党色）
```

GUI参照: `properties: seat_icon = { x = parliament_seat_x^i; y = parliament_seat_y^i; frame = parliament_seat_color^i }`

### 政党テーブル（並列配列、7要素）

`parliament_party_grid` の dynamic_list 駆動用。

```
parliament_parties          = [0, 1, 2, 3, 4, 5, 6]
parliament_party_seats      = [16, 44, 83, 56, 63, 115, 20]
parliament_party_name       = [token:GER_far_left_party, ..., token:GER_far_right_party]
parliament_party_ideology   = [1, 2, 3, 4, 5, 6, 7]   # frame値（色）
```

GUI参照:
- `properties: party_color_bar = { frame = parliament_party_ideology^i }`
- `text = "[?parliament_party_seats^i]"`
- `text = "[?parliament_party_name^i.GetTokenLocalizedKey]"`

---

## GUI設計

HTMLモックアップ: `.plan/parliament_mockup.html`

### 全体レイアウト

```
┌─────────────────────────────────────────┐
│ REICHSTAG                          [X]  │  ← タイトル + 閉じるボタン
├──────────────────────┬──────────────────┤
│                      │ ■ 政党名    16席 │
│    ○ ○ ○ ○ ○ ○ ○    │   党首名     4% │
│   ○ ○ ○ ○ ○ ○ ○ ○   │ ■ 政党名    44席 │
│  ○ ○ ○ ○ ○ ○ ○ ○ ○  │   党首名    11% │
│                      │ ■ 政党名    83席 │
│     397 議席         │   党首名    21% │
│  ████████████████    │  ... (7政党)     │
│                      │                  │
└──────────────────────┴──────────────────┘
 左: 半円図(480px) + 総議席数 + 配分バー
 右: 政党リスト(260px)
```

### .gui ファイル構造

```gui
# interface/parliament_view.gui
guiTypes = {

    # ===== ① ボタン（政治タブに寄生） =====
    containerWindowType = {
        name = "parliament_button_window"
        position = { x=0 y=0 }  # 目視で調整

        buttonType = {
            name = "parliament_open_button"
            spriteType = "GFX_parliament_button"
            pdx_tooltip = "PARLIAMENT_BUTTON_TT"
        }
    }

    # ===== ② 議会ビューウィンドウ =====
    containerWindowType = {
        name = "parliament_window"
        size = { width=820 height=560 }
        moveable = yes
        orientation = CENTER

        background = {
            name = "bg"
            quadTextureSprite = "GFX_tiled_plain_bg"
        }

        # タイトル
        instantTextBoxType = {
            name = "parliament_title"
            position = { x=16 y=8 }
            text = "PARLIAMENT_TITLE"
            font = "hoi_36header"
            maxWidth = 400
        }

        # 閉じるボタン
        buttonType = {
            name = "parliament_close_button"
            position = { x=-42 y=9 }
            quadTextureSprite = "GFX_closebutton"
            orientation = "UPPER_RIGHT"
            shortcut = "ESCAPE"
            clicksound = click_close
        }

        # --- 半円議席エリア ---
        containerWindowType = {
            name = "parliament_seats_container"
            position = { x=12 y=50 }
            size = { width=480 height=300 }
            clipping = no

            gridBoxType = {
                name = "parliament_seat_grid"
                position = { x=0 y=0 }
                size = { width=480 height=300 }
                slotsize = { width=10 height=10 }
                format = "UPPER_LEFT"
            }
        }

        # --- 総議席数 ---
        instantTextBoxType = {
            name = "total_seats_text"
            position = { x=120 y=360 }
            text = "PARLIAMENT_TOTAL_SEATS"
            font = "hoi_18mbs"
            maxWidth = 240
            format = center
        }

        # --- 議席配分バー（将来: parliament_bar.shader） ---

        # --- 政党リスト ---
        containerWindowType = {
            name = "parliament_party_panel"
            position = { x=510 y=50 }
            size = { width=260 height=460 }

            gridBoxType = {
                name = "parliament_party_grid"
                position = { x=0 y=0 }
                size = { width=260 height=460 }
                slotsize = { width=260 height=60 }
                max_slots_horizontal = 1
                format = "UPPER_LEFT"
            }
        }
    }

    # ===== ③ 議席アイコンテンプレート =====
    containerWindowType = {
        name = "parliament_seat_entry"
        size = { width=10 height=10 }

        iconType = {
            name = "seat_icon"
            spriteType = "GFX_parliament_seat"    # 7フレーム
        }
    }

    # ===== ④ 政党リストエントリテンプレート =====
    containerWindowType = {
        name = "parliament_party_entry"
        size = { width=260 height=55 }

        iconType = {
            name = "party_color_bar"
            position = { x=0 y=5 }
            spriteType = "GFX_parliament_party_color"  # 7フレーム
        }

        instantTextBoxType = {
            name = "party_name_text"
            position = { x=15 y=3 }
            text = "[?parliament_party_name^i.GetTokenLocalizedKey]"
            font = "hoi_16mbs"
            maxWidth = 180
        }

        instantTextBoxType = {
            name = "party_seats_text"
            position = { x=15 y=22 }
            text = "[?parliament_party_seats^i]"
            font = "hoi_18mbs"
            maxWidth = 100
        }

        instantTextBoxType = {
            name = "party_leader_text"
            position = { x=15 y=38 }
            text = ""  # scripted_localisationで設定
            font = "hoi_16mbs"
            maxWidth = 180
        }
    }
}
```

### .gfx スプライト定義

```gfx
# interface/parliament_view.gfx
spriteTypes = {
    spriteType = {
        name = "GFX_parliament_seat"
        texturefile = "gfx/interface/parliament/parliament_seat_strip.dds"
        noOfFrames = 7
    }
    spriteType = {
        name = "GFX_parliament_party_color"
        texturefile = "gfx/interface/parliament/parliament_party_color.dds"
        noOfFrames = 7
    }
    spriteType = {
        name = "GFX_parliament_button"
        texturefile = "gfx/interface/parliament/parliament_button.dds"
    }
}
```

---

## Scripted GUI

```pdx
# common/scripted_guis/parliament_gui.txt
scripted_gui = {

    # ① ボタンGUI — 政治タブに寄生
    parliament_button = {
        context_type = player_context
        window_name = "parliament_button_window"
        parent_window_token = politics_tab

        triggers = {
            parliament_open_button_visible = {
                has_variable = parliament_num_parties
            }
        }
        effects = {
            parliament_open_button_click = {
                if = {
                    limit = { has_variable = parliament_view_open }
                    clear_variable = parliament_view_open
                    else = { set_variable = { parliament_view_open = 1 } }
                }
            }
        }
    }

    # ② 議会ビューGUI — 独立ウィンドウ
    parliament_main = {
        context_type = player_context
        window_name = "parliament_window"
        dirty = parliament_dirty_flag

        visible = { has_variable = parliament_view_open }

        dynamic_lists = {
            parliament_seat_grid = {
                array = parliament_seats
                value = v
                index = i
                change_scope = no
                entry_container = "parliament_seat_entry"
            }
            parliament_party_grid = {
                array = parliament_parties
                value = v
                index = i
                change_scope = no
                entry_container = "parliament_party_entry"
            }
        }

        properties = {
            seat_icon = {
                x = parliament_seat_x^i
                y = parliament_seat_y^i
                frame = parliament_seat_color^i
            }
            party_color_bar = {
                frame = parliament_party_ideology^i
            }
        }

        effects = {
            parliament_close_button_click = {
                clear_variable = parliament_view_open
            }
        }
    }
}
```

---

## Scripted Effects

### 初期化

```pdx
# common/scripted_effects/parliament_effects.txt

initialize_parliament = {
    if = {
        limit = { tag = GER }
        GER_initialize_parliament = yes
    }
}

GER_initialize_parliament = {
    set_variable = { parliament_total_seats = 397 }
    set_variable = { parliament_num_parties = 7 }

    # --- 政党テーブル（並列配列） ---
    clear_array = parliament_parties
    clear_array = parliament_party_name
    clear_array = parliament_party_ideology
    clear_array = parliament_party_seats

    # 各政党: index, name token, frame値, 議席数(後で設定)
    add_to_array = { parliament_parties = 0 }
    add_to_array = { parliament_party_name = token:GER_far_left_party }
    add_to_array = { parliament_party_ideology = 1 }
    add_to_array = { parliament_party_seats = 0 }

    add_to_array = { parliament_parties = 1 }
    add_to_array = { parliament_party_name = token:GER_left_party }
    add_to_array = { parliament_party_ideology = 2 }
    add_to_array = { parliament_party_seats = 0 }

    add_to_array = { parliament_parties = 2 }
    add_to_array = { parliament_party_name = token:GER_center_left_party }
    add_to_array = { parliament_party_ideology = 3 }
    add_to_array = { parliament_party_seats = 0 }

    add_to_array = { parliament_parties = 3 }
    add_to_array = { parliament_party_name = token:GER_center_party }
    add_to_array = { parliament_party_ideology = 4 }
    add_to_array = { parliament_party_seats = 0 }

    add_to_array = { parliament_parties = 4 }
    add_to_array = { parliament_party_name = token:GER_center_right_party }
    add_to_array = { parliament_party_ideology = 5 }
    add_to_array = { parliament_party_seats = 0 }

    add_to_array = { parliament_parties = 5 }
    add_to_array = { parliament_party_name = token:GER_right_party }
    add_to_array = { parliament_party_ideology = 6 }
    add_to_array = { parliament_party_seats = 0 }

    add_to_array = { parliament_parties = 6 }
    add_to_array = { parliament_party_name = token:GER_far_right_party }
    add_to_array = { parliament_party_ideology = 7 }
    add_to_array = { parliament_party_seats = 0 }

    # --- 議席テーブル（Python生成値） ---
    initialize_parliament_seat_positions = yes

    # --- 議席配分 ---
    update_parliament_from_popularity = yes
}
```

### 議席再計算

```pdx
update_parliament_from_popularity = {
    # meta_effectで7政党分を一括処理
    # party_popularity_100@ideology → 0-100の整数 × 3.97 = 議席数

    meta_effect = {
        text = {
            set_temp_variable = { temp_pop = party_popularity_100@[IDEOLOGY] }
            set_temp_variable = { temp_seats = temp_pop }
            multiply_variable = { temp_seats = 3.97 }
            round_variable = temp_seats
            set_variable = { parliament_party_seats^[IDX] = temp_seats }
        }
        IDX = "0"
        IDEOLOGY = "far_left"
    }
    # ... IDX=1/left, 2/center_left, 3/center, 4/center_right, 5/right, 6/far_right

    update_parliament_seat_colors = yes
    add_to_variable = { parliament_dirty_flag = 1 }
}
```

### 議席色計算

```pdx
update_parliament_seat_colors = {
    # cumulative sum方式: 各政党のアイコン数を計算し、parliament_seat_color配列を更新
    # for_each_loopのネスト不可のため、実装は以下のいずれか:
    #   (a) meta_effectで100個分を展開
    #   (b) Python生成のscripted_effect

    set_temp_variable = { seat_idx = 0 }
    for_each_loop = {
        array = parliament_parties
        value = v
        index = pi

        set_temp_variable = { icon_count = parliament_party_seats^pi }
        multiply_variable = { icon_count = 0.252 }   # 100/397
        round_variable = icon_count

        # parliament_seat_color[seat_idx .. seat_idx+icon_count-1] = pi + 1
        # ↑ 内部ループの実装は実装時に確定

        add_to_variable = { seat_idx = icon_count }
    }
}
```

### 座標初期化（Python生成）

```pdx
# Python出力をそのまま貼り付け
initialize_parliament_seat_positions = {
    clear_array = parliament_seats
    clear_array = parliament_seat_x
    clear_array = parliament_seat_y
    clear_array = parliament_seat_color

    # 100個分のadd_to_array（Python生成）
    # add_to_array = { parliament_seats = 0 }
    # add_to_array = { parliament_seat_x = 123 }
    # add_to_array = { parliament_seat_y = 45 }
    # add_to_array = { parliament_seat_color = 1 }
    # ... ×100
}
```

座標生成Python:
```python
import math
rows = [
    {"count": 28, "radius": 105},
    {"count": 33, "radius": 135},
    {"count": 39, "radius": 165},
]
center_x, center_y = 240, 270

for row in rows:
    for i in range(row["count"]):
        angle = math.pi * (i + 0.5) / row["count"]
        x = center_x - row["radius"] * math.cos(angle)
        y = center_y - row["radius"] * math.sin(angle)
        # → add_to_array文として出力
```

---

## 動的ローカライズ

| 手法 | 本システムでの用途 |
|------|---|
| token変数 + `^i` | 政党名: `[?parliament_party_name^i.GetTokenLocalizedKey]` |
| 直接変数参照 + `^i` | 議席数: `[?parliament_party_seats^i]` |
| meta_effect | 議席計算ループの変数名構築 |
| scripted_localisation | 党首名表示（country_leader取得用） |

---

## 実装ステップ

### Phase 1: 表示のみの議会システム
1. Pythonで100座席の半円座標を生成 → scripted_effect出力
2. `interface/parliament_view.gfx` — スプライト定義
3. `gfx/interface/parliament/` — 画像作成（議席アイコン・カラーバー・ボタン）
4. `interface/parliament_view.gui` — GUI定義
5. `common/scripted_effects/parliament_effects.txt` — 初期化・計算
6. `common/scripted_guis/parliament_gui.txt` — GUI接続
7. `common/on_actions/parliament_on_actions.txt` — on_startupで初期化
8. `localisation/japanese/parliament_l_japanese.yml` — UIテキスト

### Phase 2（将来）: 選挙・動的更新
- 選挙イベント作成
- popularity変動 → 議席再配分
- 議席配分バー（parliament_bar.shader）の動的更新対策

### Phase 3（将来）: 他国展開・ゲーム影響
- フランス、イギリス等のプリセット追加
- 議席配分による国民精神・政策への影響

---

## 技術メモ

### shaderの制約（調査済み）
- `progressbartype` がshaderに渡せるのは `color`(4float) + `colortwo`(4float) + `CurrentState`(1float) のみ
- `iconType` の `frame` はスプライトシートのコマ選択に使われ、shaderには渡されない
- `.gfx` の `color`/`colortwo` は起動時固定、scripted GUIから動的変更不可
- **結論**: 個別議席アイコンの色をshaderで動的に変えることは不可 → 7フレームスプライトシート + properties/frame方式を採用
- `parliament_bar.shader`（作成済み）: 7色をハードコード、閾値をcolorパラメータにエンコード
- `parliament_semicircle.shader`（作成済み）: 議席図はdynamic_list方式のため現時点では不使用
- `.lua` 参照（`effectFile = "gfx/FX/xxx.lua"`）は実ファイル不要。エンジンが `xxx.shader` を自動解決

### parent_window_token（調査済み）
- `parent_window_token = politics_tab` でscripted GUIを政治タブに寄生させる
- 参考: `sg_subideologies.txt` の `countrypoliticsview_ideology_info`
- 政治タブ表示中のみボタンが描画される
- ボタン座標は目視で調整（未定）

### token変数（要検証）
- `GER_far_left_party` 等のキーが `token:` で使えるか実機で検証が必要
- 使えない場合は scripted_localisation でフォールバック

### for_each_loopのネスト制約
- HoI4では for_each_loop のネストが不可
- 議席色計算の内部ループ（icon_count回の配列設定）は別手段が必要
- 候補: (a) meta_effectで100個分を展開 (b) Python生成のscripted_effect
