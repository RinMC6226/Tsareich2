# 議会システム統合設計 v2

## 設計方針

旧計画（独自GUI・dynamic_list・汎用構造）と既存実装（ディシジョン内蔵・bps支持率・9党・工作体系）の長所を統合する。

| 方針 | 採用元 | 理由 |
|------|--------|------|
| 独立ウィンドウGUI | 旧計画 | 表示スペース確保、将来拡張（党首・配分バー等） |
| dynamic_list + properties | 旧計画 | コード量を抑え、政党数変更に構造変更不要 |
| 独自bps支持率 | 実装 | ゲーム内ideology popularityとの干渉回避 |
| 国ごとの政党数自由 | 実装 | 7固定ではなく、YAMLで任意の数を定義 |
| 選挙・工作を初期搭載 | 実装 | Phase分けせず最初から遊べる状態にする |
| 操作UIはウィンドウ内ボタン | 新規 | ディシジョン大量生成を回避し、汎用性を高める |
| 変数名に国タグを含めない | 新規 | country scopeで自然に分離。他国追加時にコード複製不要 |

---

## データ構造

### スカラー変数（country scope）

変数名にタグを含めず、country scopeの自然な分離を利用する。
GERで `parliament_total_seats = 397` をセットし、FRAで `parliament_total_seats = 615` をセットしても衝突しない。

```
parliament_total_seats        # 総議席数
parliament_num_parties        # 政党数
parliament_display_seats      # GUIに表示する代表アイコン数（例: 100）
parliament_dirty              # GUI更新トリガー
parliament_view_open          # ウィンドウ表示フラグ
parliament_selected_party     # 操作対象の政党インデックス（-1 = 未選択）
parliament_government_seats   # 与党連立の合計議席
parliament_opposition_seats   # 野党合計議席
parliament_election_interval  # 選挙間隔（日数）
```

### 政党テーブル（並列配列、N要素）

```
parliament_parties            = [0, 1, 2, ..., N-1]   # インデックス（dynamic_list駆動用）
parliament_party_name         = [token:..., ...]       # 政党名トークン
parliament_party_seats        = [12, 36, 71, ...]      # 実議席数
parliament_party_support_bps  = [302, 906, 1788, ...]  # 支持率（basis points、合計10000）
parliament_party_support_pct  = [0.0302, ...]          # 表示用（bps / 10000）
parliament_party_color_frame  = [1, 2, 3, ...]         # スプライトシートのframe番号
parliament_party_is_governing = [0, 0, 0, 0, 1, 1, 1, 1, 0]  # 与党=1
```

### 議席テーブル（並列配列、display_seats要素）

```
parliament_seats              = [0, 1, 2, ..., 99]     # インデックス（dynamic_list駆動用）
parliament_seat_x             = [x0, x1, ..., x99]     # X座標（Python事前計算）
parliament_seat_y             = [y0, y1, ..., y99]     # Y座標（Python事前計算）
parliament_seat_color         = [f0, f1, ..., f99]     # frame値（政党色）
```

### 累積議席しきい値（議席色計算用）

```
parliament_party_seat_threshold = [12, 48, 119, ...]   # 各政党の累積議席数
```

seat_color計算時に使用:
- 代表アイコンi (0-99) が表す実議席番号 = `i * total_seats / display_seats`
- その実議席番号がどの政党の累積範囲に入るかで frame を決定

---

## GUI設計

### ウィンドウ構成

```
┌─────────────────────────────────────────────────────┐
│ REICHSTAG                                      [X]  │
├──────────────────────────┬──────────────────────────┤
│                          │ ■ 政党名    16席  3.0%   │
│      ○ ○ ○ ○ ○ ○ ○      │   [党首名]               │
│     ○ ○ ○ ○ ○ ○ ○ ○     │ ■ 政党名    44席 11.0%   │
│    ○ ○ ○ ○ ○ ○ ○ ○ ○    │   [党首名]               │
│                          │ ■ 政党名    83席 21.0%   │
│       397 議席           │   ... (N政党、スクロール) │
│    ████████████████      │                          │
│                          ├──────────────────────────┤
│  与党: 207  野党: 190    │ [ロビー] [反対] [工作]   │
│                          │ ← 選択中の政党に対して → │
└──────────────────────────┴──────────────────────────┘
 左: 半円図(~480px) + 総議席 + 配分バー + 与野党数
 右上: 政党リスト（dynamic_list、クリックで政党選択）
 右下: 操作パネル（選択中の政党への工作ボタン）
```

**サイズ**: 820×560（旧計画準拠）。ディシジョン埋め込みの700×250より大幅に広い。

### .gui ファイル構造

```gui
# interface/parliament_view.gui
guiTypes = {

    # ===== ボタン（政治タブに寄生） =====
    containerWindowType = {
        name = "parliament_button_window"
        # parent_window_tokenで政治タブに配置

        buttonType = {
            name = "parliament_open_button"
            spriteType = "GFX_parliament_button"
        }
    }

    # ===== 議会ビューウィンドウ =====
    containerWindowType = {
        name = "parliament_window"
        size = { width=820 height=560 }
        moveable = yes
        orientation = CENTER

        background = { ... }

        # タイトル（scripted_localisationで国ごとに変える）
        instantTextBoxType = {
            name = "parliament_title"
            text = "[GetParliamentTitle]"
        }

        # 閉じるボタン
        buttonType = {
            name = "parliament_close_button"
            shortcut = "ESCAPE"
        }

        # --- 半円議席エリア ---
        containerWindowType = {
            name = "parliament_seats_container"
            size = { width=480 height=340 }
            clipping = no

            gridBoxType = {
                name = "parliament_seat_grid"
                slotsize = { width=10 height=10 }
            }
        }

        # --- 総議席数 ---
        instantTextBoxType = {
            name = "parliament_total_seats_text"
            text = "[?parliament_total_seats] PARLIAMENT_SEATS"
        }

        # --- 与野党数 ---
        instantTextBoxType = {
            name = "parliament_gov_opp_text"
            text = "PARLIAMENT_GOV_OPP_SUMMARY"
        }

        # --- 政党リスト ---
        containerWindowType = {
            name = "parliament_party_panel"
            position = { x=510 y=50 }
            size = { width=280 height=380 }
            verticalScrollbar = "right_vertical_slider"

            gridBoxType = {
                name = "parliament_party_grid"
                slotsize = { width=280 height=55 }
                max_slots_horizontal = 1
            }
        }

        # --- 操作パネル ---
        containerWindowType = {
            name = "parliament_action_panel"
            position = { x=510 y=440 }
            size = { width=280 height=100 }

            buttonType = {
                name = "parliament_btn_lobby"
                # 選択中の政党にロビー活動
            }
            buttonType = {
                name = "parliament_btn_counter"
                # 選択中の政党に反対集会
            }
            buttonType = {
                name = "parliament_btn_operation"
                # 選択中の政党に工作
            }
        }
    }

    # ===== 議席アイコンテンプレート =====
    containerWindowType = {
        name = "parliament_seat_entry"
        size = { width=10 height=10 }

        iconType = {
            name = "seat_icon"
            spriteType = "GFX_parliament_seat"  # 最大15フレーム
        }
    }

    # ===== 政党リストエントリテンプレート =====
    containerWindowType = {
        name = "parliament_party_entry"
        size = { width=280 height=55 }

        buttonType = {
            name = "party_select_button"
            # クリックで parliament_selected_party = ^i
        }

        iconType = {
            name = "party_color_bar"
            spriteType = "GFX_parliament_party_color"
        }

        # 与党マーカー
        iconType = {
            name = "party_gov_marker"
            spriteType = "GFX_parliament_gov_marker"
        }

        instantTextBoxType = {
            name = "party_name_text"
            text = "[?parliament_party_name^i.GetTokenLocalizedKey]"
        }

        instantTextBoxType = {
            name = "party_seats_text"
            text = "[?parliament_party_seats^i]"
        }

        instantTextBoxType = {
            name = "party_support_text"
            text = "[?parliament_party_support_pct^i|%1]"
        }

        # 党首名（scripted_localisation）
        instantTextBoxType = {
            name = "party_leader_text"
            text = "[GetPartyLeader]"
        }
    }
}
```

### .gfx スプライト定義

```gfx
spriteTypes = {
    # 議席アイコン: 最大15フレーム（各色1コマ）
    spriteType = {
        name = "GFX_parliament_seat"
        texturefile = "gfx/interface/parliament/parliament_seat_strip.dds"
        noOfFrames = 15
    }
    # 政党カラーバー
    spriteType = {
        name = "GFX_parliament_party_color"
        texturefile = "gfx/interface/parliament/parliament_party_color.dds"
        noOfFrames = 15
    }
    # 与党マーカー
    spriteType = {
        name = "GFX_parliament_gov_marker"
        texturefile = "gfx/interface/parliament/parliament_gov_marker.dds"
    }
    # 政治タブボタン
    spriteType = {
        name = "GFX_parliament_button"
        texturefile = "gfx/interface/parliament/parliament_button.dds"
    }
}
```

画像はPythonジェネレーターがYAMLの色定義から自動生成する。
15フレームスプライトシートに各政党の色を左から順に焼き込む。政党数がフレーム数未満の場合、余りは透明。

---

## Scripted GUI

```pdx
# common/scripted_guis/parliament_gui.txt
scripted_gui = {

    # ボタン — 政治タブに寄生
    parliament_button = {
        context_type = player_context
        window_name = "parliament_button_window"
        parent_window_token = politics_tab

        triggers = {
            parliament_open_button_visible = {
                has_country_flag = parliament_initialized
            }
        }
        effects = {
            parliament_open_button_click = {
                if = {
                    limit = { has_variable = parliament_view_open }
                    clear_variable = parliament_view_open
                }
                else = {
                    set_variable = { parliament_view_open = 1 }
                }
            }
        }
    }

    # 議会ビュー — 独立ウィンドウ
    parliament_main = {
        context_type = player_context
        window_name = "parliament_window"
        dirty = parliament_dirty

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
                frame = parliament_party_color_frame^i
            }
        }

        triggers = {
            # 与党マーカーは与党政党のみ表示
            party_gov_marker_visible = {
                check_variable = { parliament_party_is_governing^i = 1 }
            }

            # 操作パネルは政党選択時のみ表示
            parliament_action_panel_visible = {
                check_variable = { parliament_selected_party > -1 }
            }

            # ロビーボタンの有効条件
            parliament_btn_lobby_click_enabled = {
                check_variable = { parliament_selected_party > -1 }
                NOT = { has_country_flag = parliament_action_cooldown }
                has_political_power > 49
            }
            parliament_btn_counter_click_enabled = {
                check_variable = { parliament_selected_party > -1 }
                NOT = { has_country_flag = parliament_action_cooldown }
                has_political_power > 24
            }
            parliament_btn_operation_click_enabled = {
                check_variable = { parliament_selected_party > -1 }
                NOT = { has_country_flag = parliament_action_cooldown }
                has_political_power > 74
                # 対象政党が3議席以上
            }
        }

        effects = {
            parliament_close_button_click = {
                clear_variable = parliament_view_open
            }

            party_select_button_click = {
                set_variable = { parliament_selected_party = i }
            }

            parliament_btn_lobby_click = {
                add_political_power = -50
                parliament_lobby_selected = yes
            }

            parliament_btn_counter_click = {
                add_political_power = -25
                parliament_counter_selected = yes
            }

            parliament_btn_operation_click = {
                add_political_power = -75
                parliament_operation_selected = yes
            }
        }
    }
}
```

### ディシジョンとの共存（選挙タイマー）

選挙タイマーはミッション型ディシジョンとして残す（GUI内ボタンではタイマー表示が難しいため）。
ただし国タグ非依存にする。

```pdx
# common/decisions/parliament_decisions.txt
parliament_decisions = {
    parliament_election_mission = {
        activation = {
            has_country_flag = parliament_initialized
        }
        available = { hidden_trigger = { always = no } }
        is_good = yes
        fire_only_once = no
        selectable_mission = no
        days_mission_timeout = 180    # on_startupで国ごとに上書き可能
        timeout_effect = {
            parliament_hold_election = yes
        }
        ai_will_do = { factor = 0 }
    }
}
```

---

## Scripted Effects

### 初期化（国ごとに呼ぶ）

```pdx
# common/scripted_effects/parliament_effects.txt

# 汎用: 全国共通の初期化後処理
parliament_post_initialize = {
    set_variable = { parliament_selected_party = -1 }
    set_variable = { parliament_dirty = 0 }
    set_country_flag = parliament_initialized
    parliament_update_seat_colors = yes
    parliament_recalc_government = yes
    add_to_variable = { parliament_dirty = 1 }
}
```

国別初期化は別ファイルで定義し、末尾で `parliament_post_initialize` を呼ぶ。

```pdx
# common/scripted_effects/GER_parliament_init.txt
GER_parliament_initialize = {
    set_variable = { parliament_total_seats = 397 }
    set_variable = { parliament_num_parties = 9 }
    set_variable = { parliament_display_seats = 100 }
    set_variable = { parliament_election_interval = 180 }

    # 政党配列（Python生成 or 手書き）
    clear_array = parliament_parties
    clear_array = parliament_party_name
    clear_array = parliament_party_seats
    clear_array = parliament_party_support_bps
    clear_array = parliament_party_color_frame
    clear_array = parliament_party_is_governing

    # 0: KPD
    add_to_array = { parliament_parties = 0 }
    add_to_array = { parliament_party_name = token:GER_party_kpd }
    add_to_array = { parliament_party_seats = 12 }
    add_to_array = { parliament_party_support_bps = 302 }
    add_to_array = { parliament_party_color_frame = 1 }
    add_to_array = { parliament_party_is_governing = 0 }
    # ... 1-8 も同様

    # 議席座標（Python生成）
    GER_parliament_init_seat_positions = yes

    parliament_post_initialize = yes
}
```

### 議席色計算（汎用）

```pdx
parliament_update_seat_colors = {
    # 1. 累積しきい値を計算
    set_variable = { parliament_cumulative = 0 }
    for_each_loop = {
        array = parliament_parties
        value = v
        index = pi

        add_to_variable = { parliament_cumulative = parliament_party_seats^pi }
        set_variable = { parliament_party_seat_threshold^pi = parliament_cumulative }
    }

    # 2. 各代表アイコンの色を決定
    #    for_each_loopのネスト不可のため、
    #    seat_color配列は meta_effect または Python生成の展開コードで更新
    parliament_assign_seat_colors = yes
}
```

`parliament_assign_seat_colors` の実装:
display_seats（例: 100）個分のロジックをPythonで生成する。
各アイコン i に対し、`real_seat = i * total_seats / display_seats` を計算し、
累積しきい値と比較して frame を決定する。

```pdx
# Python生成される展開コード（概念）
parliament_assign_seat_colors = {
    # seat 0: real_seat ≈ 0 * 397 / 100 = 0
    set_temp_variable = { _rs = 0 }
    set_variable = { parliament_seat_color^0 = 1 }  # デフォルト: 第1政党
    for_each_loop = {
        array = parliament_parties
        value = _pv
        index = _pi
        if = {
            limit = {
                check_variable = { _pi > 0 }
                set_temp_variable = { _prev = _pi }
                subtract_from_temp_variable = { _prev = 1 }
                check_variable = { parliament_party_seat_threshold^_prev > _rs }
            }
            # この政党ではない → スキップ
        }
    }
    # ... ×100
    # 実際にはPythonが効率的なトリガーチェーンを生成
}
```

**注**: `for_each_loop` のネスト不可制約により、この部分はPythonジェネレーターが
display_seats個分のif/else_ifチェーンを静的に展開する。
これは旧実装の397×9=3573トリガーと比較して、100×N（N=政党数）程度で済む。

### 選挙処理（汎用）

```pdx
parliament_hold_election = {
    for_each_loop = {
        array = parliament_parties
        value = v
        index = pi

        set_temp_variable = { _tmp = parliament_party_support_bps^pi }
        divide_temp_variable = { _tmp = 10000 }
        multiply_temp_variable = { _tmp = parliament_total_seats }
        # floor は暗黙（HoI4の変数は整数部のみ保持する場面もあるが、
        # 安全のため round_temp_variable を使用）
        round_temp_variable = _tmp
        set_variable = { parliament_party_seats^pi = _tmp }
    }

    parliament_recalc_government = yes
    parliament_update_seat_colors = yes
    add_to_variable = { parliament_dirty = 1 }
}
```

### 与野党計算（汎用）

```pdx
parliament_recalc_government = {
    set_variable = { parliament_government_seats = 0 }
    for_each_loop = {
        array = parliament_parties
        value = v
        index = pi

        if = {
            limit = {
                check_variable = { parliament_party_is_governing^pi = 1 }
            }
            add_to_variable = { parliament_government_seats = parliament_party_seats^pi }
        }
    }
    set_variable = { parliament_opposition_seats = parliament_total_seats }
    subtract_from_variable = { parliament_opposition_seats = parliament_government_seats }
}
```

### 操作エフェクト（汎用）

```pdx
parliament_lobby_selected = {
    # parliament_selected_party の支持率を +200bps
    set_temp_variable = { _idx = parliament_selected_party }
    add_to_variable = { parliament_party_support_bps^_idx = 200 }
    parliament_normalize_support = yes
    parliament_update_display = yes

    set_country_flag = { flag = parliament_action_cooldown days = 30 value = 1 }
}

parliament_counter_selected = {
    set_temp_variable = { _idx = parliament_selected_party }
    subtract_from_variable = { parliament_party_support_bps^_idx = 200 }
    parliament_normalize_support = yes
    parliament_update_display = yes

    set_country_flag = { flag = parliament_action_cooldown days = 30 value = 1 }
}

parliament_operation_selected = {
    set_temp_variable = { _idx = parliament_selected_party }
    random_list = {
        60 = {
            # 対象から2議席を与党最大政党へ移す
            subtract_from_variable = { parliament_party_seats^_idx = 2 }
            # 与党内の最大政党を探す処理（別途）
            parliament_add_seats_to_governing = yes
            parliament_recalc_government = yes
            parliament_update_seat_colors = yes
        }
        40 = {
            add_political_power = -10
        }
    }

    set_country_flag = { flag = parliament_action_cooldown days = 60 value = 1 }
}

parliament_normalize_support = {
    for_each_loop = {
        array = parliament_parties
        value = v
        index = pi

        if = {
            limit = { check_variable = { parliament_party_support_bps^pi < 0 } }
            set_variable = { parliament_party_support_bps^pi = 0 }
        }
    }
}

parliament_update_display = {
    for_each_loop = {
        array = parliament_parties
        value = v
        index = pi

        set_temp_variable = { _tmp = parliament_party_support_bps^pi }
        divide_temp_variable = { _tmp = 10000 }
        set_variable = { parliament_party_support_pct^pi = _tmp }
    }
    add_to_variable = { parliament_dirty = 1 }
}
```

---

## Scripted Localisation

```pdx
# common/scripted_localisation/parliament_loc.txt
defined_text = {
    name = GetParliamentTitle
    text = {
        trigger = { tag = GER }
        localization_key = GER_PARLIAMENT_TITLE
    }
    text = {
        trigger = { tag = FRA }
        localization_key = FRA_PARLIAMENT_TITLE
    }
    # 他国追加時にここに1ブロック追加
}
```

---

## Pythonジェネレーター

既存の `generate_parliament.py` を拡張する。

### 入力: YAML設定ファイル（国別）

```yaml
# tools/parliament_diagram/parliaments/GER.yml
tag: GER
total_seats: 397
display_seats: 100
election_interval: 180

parties:
  - id: kpd
    name_token: GER_party_kpd
    seats: 12
    support_bps: 302
    governing: false
    color: [139, 30, 30]
  - id: sapd
    name_token: GER_party_sapd
    seats: 36
    support_bps: 906
    governing: false
    color: [196, 72, 58]
  # ... 以下同様

diagram:
  rows: 4
  cx: 240
  cy: 270
  r_inner: 105
  r_outer: 195
  layout_engine: parliamentarch
```

### 出力ファイル

| 出力 | 内容 |
|------|------|
| `common/scripted_effects/{TAG}_parliament_init.txt` | 国別初期化（配列セットアップ + 座標データ） |
| `common/scripted_effects/parliament_assign_seat_colors.txt` | 座席色計算の展開コード（display_seats分） |
| `gfx/interface/parliament/parliament_seat_strip.dds` | 政党色スプライトシート（全国共通、最大15フレーム） |
| `gfx/interface/parliament/parliament_party_color.dds` | 政党カラーバー（同上） |
| `gfx/interface/parliament/parliament_gov_marker.dds` | 与党マーカー |

以下は**生成しない**（手書き、全国共通）:

| ファイル | 理由 |
|------|------|
| `interface/parliament_view.gui` | 汎用テンプレート。国ごとに変わらない |
| `interface/parliament_view.gfx` | 同上 |
| `common/scripted_guis/parliament_gui.txt` | 同上 |
| `common/scripted_effects/parliament_effects.txt` | 汎用ロジック |
| `common/decisions/parliament_decisions.txt` | 選挙ミッション（汎用） |

### 座標生成

display_seats（100）個分の半円座標を計算し、`add_to_array` 文として出力する。
既存の `compute_seat_positions` 関数を流用。

---

## ファイル構造

```
common/
├── scripted_guis/
│   └── parliament_gui.txt                 # 汎用（手書き）
├── scripted_effects/
│   ├── parliament_effects.txt             # 汎用ロジック（手書き）
│   ├── parliament_assign_seat_colors.txt  # 座席色展開（Python生成）
│   ├── GER_parliament_init.txt            # GER初期化（Python生成）
│   └── FRA_parliament_init.txt            # FRA初期化（Python生成、将来）
├── scripted_localisation/
│   └── parliament_loc.txt                 # 国名分岐（手書き、国追加時に1行追加）
├── decisions/
│   └── parliament_decisions.txt           # 選挙ミッション（汎用、手書き）
├── on_actions/
│   └── parliament_on_actions.txt          # on_startup（手書き、国追加時に1行追加）

interface/
├── parliament_view.gui                    # GUI定義（汎用、手書き）
├── parliament_view.gfx                    # スプライト定義（汎用、手書き）

gfx/interface/parliament/
├── parliament_seat_strip.dds              # 議席色スプライトシート（Python生成）
├── parliament_party_color.dds             # 政党カラーバー（Python生成）
├── parliament_gov_marker.dds              # 与党マーカー（Python生成）
├── parliament_button.dds                  # 政治タブボタン（手作成）

localisation/japanese/
├── parliament_l_japanese.yml              # 共通UI文字列（手書き）
├── GER_parliament_l_japanese.yml          # GER政党名等（手書き or Python生成）

tools/parliament_diagram/
├── generate_parliament.py                 # ジェネレーター
├── parliaments/
│   ├── GER.yml                            # GER設定
│   └── FRA.yml                            # FRA設定（将来）
```

### 他国追加時の作業

1. `parliaments/{TAG}.yml` を作成
2. `python generate_parliament.py parliaments/{TAG}.yml` を実行
3. `on_actions` に `{TAG} = { {TAG}_parliament_initialize = yes }` を1行追加
4. `scripted_localisation` に `GetParliamentTitle` のブロックを1つ追加
5. ローカライズファイルに政党名を追加

GUIファイル・scripted_gui・汎用effectの変更は不要。

---

## 旧実装からの移行ポイント

| 旧実装の要素 | 統合版での扱い |
|---|---|
| `GER_parliament_kpd_seats` 等の個別変数 | `parliament_party_seats^i` 配列に統合 |
| 27個のNOT排他制御 | ウィンドウ内ボタン化により不要（クールダウンフラグ1つで制御） |
| 397×9=3573個のvisibleトリガー | 100×N個に削減（display_seats=100） |
| 45,296行のscripted_gui | 数百行の汎用scripted_gui + 生成展開コード |
| ディシジョンの表示/非表示トグル | 不要（独立ウィンドウ内で完結） |
| `countrydecisionview.gui` の上書き | 不要（ディシジョンUI非使用） |

---

## 未確定事項・要検証

| 項目 | 状態 | 対策 |
|------|------|------|
| `token:` による政党名の動的参照 | 未検証 | 不可の場合は scripted_localisation でフォールバック |
| `parliament_party_is_governing^i` の配列triggerでの参照 | 未検証 | 不可の場合は累積しきい値方式で代替 |
| `properties` での `^i` 参照 | 旧計画で想定済み、未検証 | 公式modの `sg_subideologies.txt` に類似例あり |
| `set_variable = { array^temp_var = value }` の動的インデックス | 未検証 | 不可の場合は meta_effect で展開 |
| `set_country_flag` の `days` パラメータでのクールダウン | 要確認 | 代替: timed mission |
| 15フレームスプライトシートの上限 | 動作するはずだが要確認 | 実機テスト |

---

## 実装ステップ

### Step 1: 汎用フレームワーク（GER表示のみ）
1. `parliament_view.gui` — ウィンドウ + テンプレート定義
2. `parliament_view.gfx` — スプライト定義
3. `parliament_gui.txt` — scripted GUI（ボタン + ウィンドウ + dynamic_list）
4. `parliament_effects.txt` — 汎用effect（選挙・与野党計算・正規化）
5. Pythonジェネレーターで `GER_parliament_init.txt` + 座席色展開 + 画像を生成
6. `parliament_on_actions.txt` — on_startup
7. ローカライズ
8. **実機テスト**: dynamic_list表示、properties動作、token参照

### Step 2: 操作機能
1. 操作パネル（ロビー・反対・工作ボタン）のGUI追加
2. `parliament_effects.txt` に操作effect追加
3. クールダウン制御
4. 操作結果の反映確認

### Step 3: 選挙サイクル
1. 選挙ミッションディシジョン
2. `parliament_hold_election` の動作確認
3. 支持率→議席変換の精度確認

### Step 4: 他国展開テスト
1. FRA（テスト用最小構成: 3政党）のYAMLを作成
2. ジェネレーター実行
3. on_actions + scripted_localisation に追加
4. 汎用コードの変更なしで動くことを確認
