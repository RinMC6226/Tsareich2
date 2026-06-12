# 旧マップ削除state一覧 (BSR 3.0移植前の history/states)

2026-06-12 の BSR Public Beta 3.0 マップ移植 (`feature/_map_bsr_import`, 1532be68) で削除・置換された旧 `history/states/` 全 1068 州の記録。

- 旧データ実体: `../Tsareich2_map_backup_20260612/history_states/` および git 履歴 (8ffcab23 以前)
- 新マップも state ID 1〜2044 を連番使用するため、ID 自体は全て新定義に引き継がれている。本表の「削除」は旧定義(領域・名称・所有者)の置換を意味する
- 区分の内訳: 維持(日本語訳継続) 451 / 名称同一(訳なし) 0 / 再編・改名 617
- 注意: 旧日本語名には移植前から新マップ名称へ先行対応していたものが混在する (例: ID 2「ラツィオ」= 新 Lazio、ID 4「ニーダーエスターライヒ」= 新 Niederösterreich)。区分が「再編・改名」でも旧日本語名が新 state 名の訳としてそのまま有効な場合がある
- そのため本表は日本語訳の復元ワークシートを兼ねる。「旧日本語名」が「新state名(同ID)」の訳として正しい行は、`localisation/japanese/state_names_l_japanese.yml` の該当キーへ戻せばよい

| ID | 旧英語名 | 旧日本語名 | 旧owner | 新state名(同ID) | 区分 |
|---:|---|---|---|---|---|
| 1 | Corsica | コルシカ | ITA | Corse | 再編・改名 |
| 2 | Italy | ラツィオ | ITA | Lazio | 再編・改名 |
| 3 | Swiss Plateau | スイス高原 | SWI | Berne | 再編・改名 |
| 4 | Austria | ニーダーエスターライヒ | GER | Niederösterreich | 再編・改名 |
| 5 | Germany | エルムラント＝マズーレン | GER | Ortelsburg | 再編・改名 |
| 6 | Flanders | フランデレン | BEL | Vlaanderen | 再編・改名 |
| 7 | Holland | ホラント | HOL | Holland | 維持(日本語訳継続) |
| 8 | Luxemburg | ルクセンブルク | GER | Lëtzebuerg | 再編・改名 |
| 9 | Bohemia | ボヘミア | CZE | Čechy | 再編・改名 |
| 10 | Warsaw | ワルシャワ | RUS | Warszawa | 再編・改名 |
| 11 | Kaunas | カウナス | RUS | Kaunas | 維持(日本語訳継続) |
| 12 | Vidzeme | ヴィドゼメ | RUS | Rīga | 再編・改名 |
| 13 | Estonia | ハリュ | RUS | Harju | 再編・改名 |
| 14 | Brittany | ブルターニュ | FRA | Brittany | 維持(日本語訳継続) |
| 15 | Normandy | ノルマンディー | FRA | Normandy | 維持(日本語訳継続) |
| 16 | Ile de France | イル・ド・フランス | FRA | Île-de-France | 再編・改名 |
| 17 | Alcase Lorraine | フランシュ＝コンテ | FRA | Épinal | 再編・改名 |
| 18 | Champagne | シャンパーニュ | FRA | Champagne | 維持(日本語訳継続) |
| 19 | Aquitaine | アキテーヌ | FRA | Aquitaine | 維持(日本語訳継続) |
| 20 | Rhone | ローヌ | FRA | Saint-Étienne | 再編・改名 |
| 21 | Bouches-du-Rhone | ブーシュ・デュ・ローヌ | FRA | Marseille | 再編・改名 |
| 22 | Languedoc | ラングドック | FRA | Languedoc | 維持(日本語訳継続) |
| 23 | Poitou | ポワトゥー | FRA | Poitou | 維持(日本語訳継続) |
| 24 | Centre | サントル | FRA | Centre | 維持(日本語訳継続) |
| 25 | Limousin | リムーザン | FRA | Limousin | 維持(日本語訳継続) |
| 26 | Auvergne | オーヴェルニュ | FRA | Auvergne | 維持(日本語訳継続) |
| 27 | Bourgogne | ブルゴーニュ | FRA | Bourgogne | 維持(日本語訳継続) |
| 28 | Alcase | エルザス＝ロートリンゲン | GER | Alsace | 再編・改名 |
| 29 | Pas de Calais | ノール＝パ・ド・カレー | BEL | Arras | 再編・改名 |
| 30 | Loire | ロワール | FRA | Centre-Val de Loire | 再編・改名 |
| 31 | Midi Pyrenees | ミディ・ピレネー | FRA | Midi Pyrenees | 維持(日本語訳継続) |
| 32 | Alpes | アルプス | FRA | Alpes | 維持(日本語訳継続) |
| 33 | Centre-Sud | サントル＝スュド | FRA | Centre-Sud | 維持(日本語訳継続) |
| 34 | Wallonia | ワロン | BEL | Roman Payis | 再編・改名 |
| 35 | Brabant | ブラバント | HOL | Noord-Brabant | 再編・改名 |
| 36 | Friesland | フリースラント | HOL | Friesland | 維持(日本語訳継続) |
| 37 | Sjaelland | シェラン | DEN | Sjælland | 再編・改名 |
| 38 | Gävleborg | イェヴレボリ | SWE | Norrland | 再編・改名 |
| 39 | South Tyrol | アルト・アディジェ | GER | Alto Adige | 再編・改名 |
| 40 | USSR | バルナウル | RUS | Barnaul | 再編・改名 |
| 41 | Madrid | マドリード | SPR | Madrid | 維持(日本語訳継続) |
| 42 | Moselland | モーゼルラント | GER | Pfalz | 再編・改名 |
| 43 | Northern Hungary | ハンガリー北部 | HUN | Észak-Magyarország | 再編・改名 |
| 44 | Central Albania | 中央アルバニア | ALB | Tirana | 再編・改名 |
| 45 | Vojvodina | バーチュカ | HUN | Vojvodina | 維持(日本語訳継続) |
| 46 | Muntenia | ムンテニア | ROM | Muntenia | 維持(日本語訳継続) |
| 47 | Attica | アッティカ | GRE | Athína | 再編・改名 |
| 48 | Sofia | ソフィア | BUL | Sofia | 維持(日本語訳継続) |
| 49 | Ankara | アンカラ | TUR | Ankara | 維持(日本語訳継続) |
| 50 | Württemberg | ヴュルテンベルク | GER | Württemberg | 維持(日本語訳継続) |
| 51 | Rhineland | ラインラント | GER | Westrheinland | 再編・改名 |
| 52 | Oberbayern | オーバーバイエルン | GER | Oberbayern | 維持(日本語訳継続) |
| 53 | Niederbayern | ニーダーバイエルン | GER | Niederbayern | 維持(日本語訳継続) |
| 54 | Franken | フランケン | GER | Franken | 維持(日本語訳継続) |
| 55 | Hessen | ヘッセン | GER | Hessen | 維持(日本語訳継続) |
| 56 | Weser-Ems | ヴェーザー＝エムス | GER | Weser-Ems | 維持(日本語訳継続) |
| 57 | Westfalen | ヴェストファーレン | GER | Westfalen | 維持(日本語訳継続) |
| 58 | Schleswig - Holstein | ホルシュタイン | GER | Holstein | 再編・改名 |
| 59 | Hannover | ハノーファー | GER | Hamburg | 再編・改名 |
| 60 | Thüringen | テューリンゲン | GER | Thüringen | 維持(日本語訳継続) |
| 61 | Mecklenburg | メクレンブルク | GER | Mecklenburg | 維持(日本語訳継続) |
| 62 | Pommern | フォアポンメルン | GER | Vorpommern | 再編・改名 |
| 63 | Hinterpommern | ヒンターポンメルン | GER | Greifenberg | 再編・改名 |
| 64 | Brandenburg | ブランデンブルク | GER | Reichstag | 再編・改名 |
| 65 | Sachsen | ザクセン | GER | Sachsen | 維持(日本語訳継続) |
| 66 | Niederschlesien | ニーダーシュレージェン | GER | Breslau | 再編・改名 |
| 67 | Oberschlesien | オーバーシュレージェン | GER | Oppeln | 再編・改名 |
| 68 | Ostmark | オストマルク | GER | Ostmark | 維持(日本語訳継続) |
| 69 | Sudatenland | 北ズデーテンラント | GER | Karlovy Vary | 再編・改名 |
| 70 | Western Slovakia | スロヴァキア西部 | HUN | Bratislava | 再編・改名 |
| 71 | Eastern Slovakia | スロヴァキア東部 | HUN | Východné Slovensko | 再編・改名 |
| 72 | Trans-Olza | チェシンスコ | CZE | Zaolší | 再編・改名 |
| 73 | Carpathian Ruthenia | ポドカルパツカー・ルス | HUN | Podkarpatská Rus | 再編・改名 |
| 74 | Sudeten Silesia | ズデーテン シレジア | GER | Východní Sudety | 再編・改名 |
| 75 | Moravia | モラヴィア | CZE | Morava | 再編・改名 |
| 76 | North Transylvania | 北トランシルヴァニア | ROM | Transilvania de Nord | 再編・改名 |
| 77 | Dobrudja | ドブルジャ | ROM | Dobrogea | 再編・改名 |
| 78 | Bessarabia | ベッサラビア | RUS | Basarabia | 再編・改名 |
| 79 | Moldova | モルドヴァ | ROM | Moldova | 維持(日本語訳継続) |
| 80 | Bucovina | ブコヴィナ | RUS | Bucovina de Nord | 再編・改名 |
| 81 | Oltenia | オルテニア | ROM | Oltenia | 維持(日本語訳継続) |
| 82 | Banat | バナト | HUN | Banat | 維持(日本語訳継続) |
| 83 | Crisana | クリシャナ | HUN | Crișana de Sud | 再編・改名 |
| 84 | Transylvania | トランシルヴァニア | ROM | Transilvania | 再編・改名 |
| 85 | Danzig | ダンツィヒ | GER | Danzig | 維持(日本語訳継続) |
| 86 | Poznań | ポズナニ | GER | Poznań | 維持(日本語訳継続) |
| 87 | Lodz | ウーチ | RUS | Łódź | 再編・改名 |
| 88 | Kielce | クラクフ | RUS | Zakopane | 再編・改名 |
| 89 | Stanisławów | スタニスワヴフ | RUS | Stanisławów | 維持(日本語訳継続) |
| 90 | Kielce | キェルツェ | RUS | Kielce | 維持(日本語訳継続) |
| 91 | Lwów | ルヴフ | RUS | Lwów | 維持(日本語訳継続) |
| 92 | Lublin | ルブリン | RUS | Puławy | 再編・改名 |
| 93 | Wołyn | ヴォウィニ | RUS | Wołyn | 維持(日本語訳継続) |
| 94 | Polesie | ポレシェ | RUS | Polesie | 維持(日本語訳継続) |
| 95 | Nowogródek | ノヴォグルデク | RUS | Nowogródek | 維持(日本語訳継続) |
| 96 | Wilejka | ヴィリェイカ | RUS | Wilejka | 維持(日本語訳継続) |
| 97 | Białystok | ビャウィストク | RUS | Białystok | 維持(日本語訳継続) |
| 98 | Płock | プウォツク | RUS | Płock | 維持(日本語訳継続) |
| 99 | Jutland | 北シュレースヴィヒ | DEN | Jylland | 再編・改名 |
| 100 | Iceland | アイスランド | ICE | Reykjavík | 再編・改名 |
| 101 | Greenland | グリーンランド | DEN | Godthåb | 再編・改名 |
| 102 | North-Eastern Slovenia | 北スロベニア | YUG | Dolenjska | 再編・改名 |
| 103 | Dalmatia | ダルマチア | YUG | Dalmatia | 維持(日本語訳継続) |
| 104 | Bosnia | ボスニア | YUG | Zenica | 再編・改名 |
| 105 | Montenegro | モンテネグロ | YUG | Podgorica | 再編・改名 |
| 106 | Macedonia | マケドニア | YUG | Severna Makedonija | 再編・改名 |
| 107 | Serbia | セルビア | YUG | Beograd | 再編・改名 |
| 108 | Morava | モラヴァ | YUG | Morava | 維持(日本語訳継続) |
| 109 | Croatia | クロアチア | YUG | Zagreb | 再編・改名 |
| 110 | Norway | オスロ・フィヨルド | NOR | Oslo | 再編・改名 |
| 111 | Uusimaa | ウーシマー | RUS | Uusimaa | 維持(日本語訳継続) |
| 112 | Lisbon | リスボン | POR | Lisbon | 維持(日本語訳継続) |
| 113 | Leinster | レンスター | IRE | Leinster | 維持(日本語訳継続) |
| 114 | Sardinia | サルデーニャ | ITA | Sardegna | 再編・改名 |
| 115 | Sicily | シチリア | ITA | Sicilia | 再編・改名 |
| 116 | Malta | マルタ | ITA | Malta | 維持(日本語訳継続) |
| 117 | Campania | カンパニア | ITA | Campania | 維持(日本語訳継続) |
| 118 | Gibraltar | ジブラルタル | GER | Gibraltar | 維持(日本語訳継続) |
| 119 | Northern Ireland | アイルランド北部 | IRE | Belfast | 再編・改名 |
| 120 | Scottish Highlands | 高地スコットランド | ENG | Scottish Highlands | 維持(日本語訳継続) |
| 121 | Lothian | ロージアン | ENG | Lothian | 維持(日本語訳継続) |
| 122 | Wales | ウェールズ | ENG | Wales | 維持(日本語訳継続) |
| 123 | Cornwall | イングランド南西部 | ENG | Devon | 再編・改名 |
| 124 | Gotland | ゴットランド | SWE | Gotland | 維持(日本語訳継続) |
| 125 | East Anglia | イースト・アングリア | ENG | East Anglia | 維持(日本語訳継続) |
| 126 | Greater London Area | グレーター・ロンドン | ENG | Greater London Area | 維持(日本語訳継続) |
| 127 | Sussex | サセックス | ENG | Sussex | 維持(日本語訳継続) |
| 128 | West Midlands | ウェスト・ミッドランズ | ENG | West Midlands | 維持(日本語訳継続) |
| 129 | East Midlands | イースト・ミッドランズ | ENG | East Midlands | 維持(日本語訳継続) |
| 130 | Yorkshire | ヨークシャー | ENG | Yorkshire | 維持(日本語訳継続) |
| 131 | Northern England | ノーサンバーランド | ENG | Durham | 再編・改名 |
| 132 | Lancashire | ランカシャー | ENG | Lancashire | 維持(日本語訳継続) |
| 133 | Lanark | ラナーク | ENG | Lanark | 維持(日本語訳継続) |
| 134 | Connaught | コノート | IRE | Connaught | 維持(日本語訳継続) |
| 135 | Munster | マンスター | IRE | Munster | 維持(日本語訳継続) |
| 136 | Aberdeenshire | アバディーンシャー | ENG | Aberdeenshire | 維持(日本語訳継続) |
| 137 | Crimea | クリミア | RUS | Yalta | 再編・改名 |
| 138 | Skane | スコーネ | SWE | Skåne | 再編・改名 |
| 139 | Småland | スモーランド | SWE | Småland | 維持(日本語訳継続) |
| 140 | Västergötland | ヴェステルイェートランド | SWE | Västergötland | 維持(日本語訳継続) |
| 141 | Sodermanland | セーデルマンランド | SWE | Stockholm | 再編・改名 |
| 142 | Vestlandet | ヴェストラン | NOR | Vestlandet | 維持(日本語訳継続) |
| 143 | Midt-Noreg | トロンデラーグ | NOR | Trøndelag | 再編・改名 |
| 144 | Nordland | ヌールラン | NOR | Finnmark | 再編・改名 |
| 145 | Åland | オーランド | RUS | Åland | 維持(日本語訳継続) |
| 146 | Karjala | カレリア | RUS | Karjala | 維持(日本語訳継続) |
| 147 | Salla | サッラ | RUS | Kuolajärvi | 再編・改名 |
| 148 | Lappi | ラッピ | RUS | Lappi | 維持(日本語訳継続) |
| 149 | Vaasa | ヴァーサ | RUS | Etelä-Pohjanmaa | 再編・改名 |
| 150 | Kuopio | クオピオ | RUS | Savo | 再編・改名 |
| 151 | Eastern Swiss Alps | 東スイスアルプス | SWI | Eastern Switzerland | 再編・改名 |
| 152 | Upper Austria | オーバーエスターライヒ | GER | Oberösterreich | 再編・改名 |
| 153 | Tyrol | チロル | GER | Tirol | 再編・改名 |
| 154 | Transtisza | ティスザントゥル | HUN | Alföld | 再編・改名 |
| 155 | Western Hungary | ドナウ川西岸北部 | HUN | Dunántúl | 再編・改名 |
| 156 | Calabria | カラブリア | ITA | Calabria | 維持(日本語訳継続) |
| 157 | Abruzzo | アブルッツォ | ITA | Umbria e Marche | 再編・改名 |
| 158 | Piedmont | ピエモンテ | ITA | Piemonte | 再編・改名 |
| 159 | Lombardy | ロンバルディア | ITA | Lombardy | 維持(日本語訳継続) |
| 160 | Veneto | ヴェネト | ITA | Veneto | 維持(日本語訳継続) |
| 161 | Emilia Romagna | エミリア・ロマーニャ | ITA | Romagna | 再編・改名 |
| 162 | Tuscany | トスカーナ | ITA | Toscana | 再編・改名 |
| 163 | Dalmatia | ザラ | ITA | Zara | 再編・改名 |
| 164 | Dodecanese | ドデカネス | ITA | Dodekanisa | 再編・改名 |
| 165 | Catalonia | カタルーニャ | SPR | Cataluña | 再編・改名 |
| 166 | Western Aragon | アラゴン西部 | SPR | Western Aragón | 再編・改名 |
| 167 | Valencia | バレンシア | SPR | Valencia | 維持(日本語訳継続) |
| 168 | Murcia | ムルシア | SPR | Murcia | 維持(日本語訳継続) |
| 169 | Sevilla | セビリア | SPR | Sevilla | 維持(日本語訳継続) |
| 170 | Extremadura | エストレマドゥーラ | SPR | Extremadura | 維持(日本語訳継続) |
| 171 | Galicia | ガリシア | SPR | Galicia | 維持(日本語訳継続) |
| 172 | Navarre | ナバラ | SPR | Navarra | 再編・改名 |
| 173 | Granada | グラナダ | SPR | Granada | 維持(日本語訳継続) |
| 174 | Leon | レオン | SPR | León | 再編・改名 |
| 175 | Ciudad Real | シウダー・レアル | SPR | Ciudad Real | 維持(日本語訳継続) |
| 176 | Burgos | ブルゴス | SPR | Burgos | 維持(日本語訳継続) |
| 177 | Balearic Islands | イスラス・バレアレス | SPR | Islas Baleares | 再編・改名 |
| 178 | Canary islands | イスラス・カナリアス | SPR | Islas Canarias | 再編・改名 |
| 179 | Beja | ベージャ | POR | Beja | 維持(日本語訳継続) |
| 180 | Porto | ポルト | POR | Porto | 維持(日本語訳継続) |
| 181 | Guarda | グアルダ | POR | Guarda | 維持(日本語訳継続) |
| 182 | Crete | クレタ | GRE | Kríti | 再編・改名 |
| 183 | Cyprus | キプロス | GRE | Cyprus | 維持(日本語訳継続) |
| 184 | Thrace | トラキア | GRE | Thraki | 再編・改名 |
| 185 | Epirus | エピロス | GRE | Anatolikí Ípeiros | 再編・改名 |
| 186 | Peloponnese | ペロポネソス | GRE | Peloponnese | 維持(日本語訳継続) |
| 187 | Aegean Islands | エーゲ海諸島 | GRE | Nisiá Ton Kykládon | 再編・改名 |
| 188 | Memel | メーメル | GER | Klaipėda | 再編・改名 |
| 189 | Kaunas | シャウレイ | RUS | Šiauliai | 再編・改名 |
| 190 | Kurzeme | クルゼメ | RUS | Kurzeme | 維持(日本語訳継続) |
| 191 | Tartu | タルトゥ | RUS | Tartu | 維持(日本語訳継続) |
| 192 | Odessa | オデッサ | RUS | Odessa | 維持(日本語訳継続) |
| 193 | Chernigov | チェルニゴフ | RUS | Kozelets | 再編・改名 |
| 194 | Mozyr | モーズィリ | RUS | Rechytsa | 再編・改名 |
| 195 | Leningrad | サンクトペテルブルク | RUS | Leningrad | 維持(日本語訳継続) |
| 196 | Kherson | ヘルソン | RUS | Kherson | 維持(日本語訳継続) |
| 197 | Mykolaiv | ムィコラーイウ | RUS | Mykolaiv | 維持(日本語訳継続) |
| 198 | Vinnytsia | ヴィーンヌィツャ | RUS | Yampil | 再編・改名 |
| 199 | Khmelnytskyi | プロスクリフ | RUS | Proskurov | 再編・改名 |
| 200 | Zaporozhe | ザポロージェ | RUS | Zaporozhe | 維持(日本語訳継続) |
| 201 | Zhytomyr | ジトームィル | RUS | Zhytomyr | 維持(日本語訳継続) |
| 202 | Kiev | キエフ | RUS | Kyiv | 再編・改名 |
| 203 | Cherkasy | チェルカースィ | RUS | Cherkasy | 維持(日本語訳継続) |
| 204 | Bobruysk | ボブルイスク | RUS | Salihorsk | 再編・改名 |
| 205 | Kaluga | カルーガ | RUS | Kaluga | 維持(日本語訳継続) |
| 206 | Minsk | ミンスク | RUS | Minsk | 維持(日本語訳継続) |
| 207 | Vitebsk | ヴィーチェプスク | RUS | Vitebsk | 維持(日本語訳継続) |
| 208 | Luga | ルーガ | RUS | Luga | 維持(日本語訳継続) |
| 209 | Pskov | プスコフ | RUS | Pskov | 維持(日本語訳継続) |
| 210 | Nevel | ネヴェリ | RUS | Nevel | 維持(日本語訳継続) |
| 211 | Burgas | ブルガス | BUL | Burgas | 維持(日本語訳継続) |
| 212 | Plovdiv | プロヴディフ | BUL | Plovdiv | 維持(日本語訳継続) |
| 213 | Murmansk | ムルマンスク | RUS | Kolsky Poluostrov | 再編・改名 |
| 214 | Arkhangelsk | アルハンゲリスク | RUS | Vostochnyy Arkhangelsk | 再編・改名 |
| 215 | Onega | オネガ | RUS | Onega | 維持(日本語訳継続) |
| 216 | Olonets | オロネツ | RUS | Olonets | 維持(日本語訳継続) |
| 217 | Stalingrad | ツァリーツィン | RUS | Stalingrád | 再編・改名 |
| 218 | Rostov | ロストフ | RUS | Rostov-na-Donu | 再編・改名 |
| 219 | Moscow | モスクワ | RUS | Moskva | 再編・改名 |
| 220 | Kursk | クルスク | RUS | Kursk | 維持(日本語訳継続) |
| 221 | Kharkov | ハリコフ | RUS | Kharkiv | 再編・改名 |
| 222 | Orel | オリョール | RUS | Orel | 維持(日本語訳継続) |
| 223 | Tula | トゥーラ | RUS | Tula | 維持(日本語訳継続) |
| 224 | Bryansk | ブリャンスク | RUS | Bryansk | 維持(日本語訳継続) |
| 225 | Sumy | スームィ | RUS | Sumy | 維持(日本語訳継続) |
| 226 | Dnipropetrovsk | ドニプロペトロウシク | RUS | Dnipropetrovsk | 維持(日本語訳継続) |
| 227 | Stalino | スターリノ | RUS | Stalïno | 再編・改名 |
| 228 | Voroshilovgrad | ヴォロシロフグラード | RUS | Voroshilovgrad | 維持(日本語訳継続) |
| 229 | baku | アゼルバイジャン | RUS | Zubovka | 再編・改名 |
| 230 | Armenia | アルメニア | RUS | Yerevan | 再編・改名 |
| 231 | Georgia | グルジア | RUS | Tbilisi | 再編・改名 |
| 232 | Grozny | グロズヌイ | RUS | Chechnya | 再編・改名 |
| 233 | Caucasus Mountains | コーカサス山脈 | RUS | Arkhyz | 再編・改名 |
| 234 | Krasodar | クラスノダール | RUS | Krasnodar | 再編・改名 |
| 235 | Stavropol | スタヴロポリ | RUS | Voroshilovsk | 再編・改名 |
| 236 | Astrakhan | アストラハン | RUS | Astrakhan | 維持(日本語訳継続) |
| 237 | Elista | エリスタ | RUS | Elista | 維持(日本語訳継続) |
| 238 | Volgodonsk | ヴォルゴドンスク | RUS | Volgodonsk | 維持(日本語訳継続) |
| 239 | Saratov | サラトフ | RUS | Saratov | 維持(日本語訳継続) |
| 240 | Belgorod | ベルゴロド | RUS | Belgorod | 維持(日本語訳継続) |
| 241 | Gomel | ゴーメリ | RUS | Gomel | 維持(日本語訳継続) |
| 242 | Smolensk | スモレンスク | RUS | Roslavl | 再編・改名 |
| 243 | Roslavl | ロスラヴリ | RUS | Smolensk | 再編・改名 |
| 244 | Volkhov | ヴォルホフ | RUS | Volkhov | 維持(日本語訳継続) |
| 245 | Millerovo | ミレロヴォ | RUS | Surovikino | 再編・改名 |
| 246 | Rzhev | ルジェフ | RUS | Rzhev | 維持(日本語訳継続) |
| 247 | Kalinin | カリーニン | RUS | Kalinin | 維持(日本語訳継続) |
| 248 | Yaroslavl | ヤロスラヴリ | RUS | Yaroslavl | 維持(日本語訳継続) |
| 249 | Kazan | カザン | RUS | Kazan | 維持(日本語訳継続) |
| 250 | Ulyanovsky | ウリヤノフスク | RUS | Ulyanovsky | 維持(日本語訳継続) |
| 251 | Samara | クイブィシェフ | RUS | Kuibyshev | 再編・改名 |
| 252 | Nizhny Novogrod | ゴーリキー | RUS | Gorki | 再編・改名 |
| 253 | Ivanovo | イヴァノヴォ | RUS | Ivanovo | 維持(日本語訳継続) |
| 254 | Ryazan | リャザン | RUS | Ryazan | 維持(日本語訳継続) |
| 255 | Penza | ペンザ | RUS | Penza | 維持(日本語訳継続) |
| 256 | Cheboksary | チェボクサルィ | RUS | Cheboksary | 維持(日本語訳継続) |
| 257 | Tambov | タンボフ | RUS | Tambov | 維持(日本語訳継続) |
| 258 | Lipetsk | リペツク | RUS | Lipetsk | 維持(日本語訳継続) |
| 259 | Poltava | ポルタヴァ | RUS | Poltava | 維持(日本語訳継続) |
| 260 | Voronezh | ヴォロネジ | RUS | Voronezh | 維持(日本語訳継続) |
| 261 | Ohio | オハイオ | USA | Ohio | 維持(日本語訳継続) |
| 262 | Pechora | ペチョラ | RUS | Pechora | 維持(日本語訳継続) |
| 263 | Novgorod | ノヴゴロド | RUS | Novgorod | 維持(日本語訳継続) |
| 264 | Tikhvin | チフヴィン | RUS | Tikhvin | 維持(日本語訳継続) |
| 265 | Mikhaylovka | ミハイロフカ | RUS | Mikhaylovka | 維持(日本語訳継続) |
| 266 | Tehran | テヘラン | PER | Tehran | 維持(日本語訳継続) |
| 267 | Kabul | カーブル | AFG | Ghazni | 再編・改名 |
| 268 | French Somaliland | フランス領ソマリランド | SOM | Djibouti | 再編・改名 |
| 269 | British Somaliland | イギリス領ソマリランド | SOM | Somaliland | 再編・改名 |
| 270 | Pitcairn Island | ピトケアン島 | ENG | Pitcairn Island | 維持(日本語訳継続) |
| 271 | ethiopia | シェワ | ETH | Addis Ababa | 再編・改名 |
| 272 | Senegal | セネガル | AOC | Senegal | 維持(日本語訳継続) |
| 273 | Libyan Desert (impassable) | リビア砂漠 | LBA | Tabaqah | 再編・改名 |
| 274 | Ghana | ガーナ | DWA | Ghana | 維持(日本語訳継続) |
| 275 | Transvaal | トランスヴァール | SAF | Transvaal | 維持(日本語訳継続) |
| 276 | Southern Ontario | オンタリオ南部 | CAN | Ottawa | 再編・改名 |
| 277 | Mexico City | メキシコシティ | MEX | Ciudad de México | 再編・改名 |
| 278 | Buenos Aires | ブエノスアイレス | ARG | Buenos Aires | 維持(日本語訳継続) |
| 279 | Santiago | サンティアゴ | CHL | Santiago | 維持(日本語訳継続) |
| 280 | Mato Grosso | マットグロッソ | BRA | Mato Grosso | 維持(日本語訳継続) |
| 281 | Maldives | モルディブ | ENG | Maldives | 維持(日本語訳継続) |
| 282 | Kanto | 関東 | JAP | Minami Kantō | 再編・改名 |
| 283 | Gansu | 甘粛 | XIC | Tianshui | 再編・改名 |
| 284 | North Island | 北島 | AST | North Island | 維持(日本語訳継続) |
| 285 | New South Wales | ニューサウスウェールズ | AST | New South Wales | 維持(日本語訳継続) |
| 286 | Champa | チャンパ | DAS | Southern Indochina | 再編・改名 |
| 287 | Taklamakan (impassable) | タクラマカン | SIK | Taklamakan | 維持(日本語訳継続) |
| 288 | Magwe | マグウェ | BRM | Rangoon | 再編・改名 |
| 289 | Siam | シャム | SIA | Siam | 維持(日本語訳継続) |
| 290 | Spanish Africa | スペイン領アフリカ | RIF | ar-Rīf | 再編・改名 |
| 291 | Baghdad | バグダード | IRQ | Baghdad | 維持(日本語訳継続) |
| 292 | Nejd | ナジュド | SAU | Ha'il | 再編・改名 |
| 293 | North Yemen | 北イエメン | YEM | Yemen | 再編・改名 |
| 294 | Muscat | マスカット | OMA | Muscat | 維持(日本語訳継続) |
| 295 | Léopoldville | レオポルドヴィル | BEL | Leopoldville | 再編・改名 |
| 296 | Portuguese Guinea | ポルトガル領ギニア | POR | Guiné-Bissau | 再編・改名 |
| 297 | Equatorial Guinea | 赤道ギニア | DWA | Malabo | 再編・改名 |
| 298 | Liberia | リベリア | LIB | Liberia | 維持(日本語訳継続) |
| 299 | Falkland Islands | フォークランド諸島 | ENG | Falkland Islands | 維持(日本語訳継続) |
| 300 | Montevideo | モンテビデオ | URG | Uruguay | 再編・改名 |
| 301 | Paraguay | パラグアイ | PAR | Paraguay | 維持(日本語訳継続) |
| 302 | La Paz | ラパス | BOL | La Paz | 維持(日本語訳継続) |
| 303 | Lima | リマ | PRU | Lima | 維持(日本語訳継続) |
| 304 | Panama | パナマ | PAN | Panamá Oriental | 再編・改名 |
| 305 | Ecuador | エクアドル | ECU | Ecuador | 維持(日本語訳継続) |
| 306 | Cundinamarca | クンディナマルカ | COL | Cundinamarca | 維持(日本語訳継続) |
| 307 | Miranda | ミランダ | VEN | Miranda | 維持(日本語訳継続) |
| 308 | Leeward Islands | リーワード諸島 | ENG | Leeward Islands | 維持(日本語訳継続) |
| 309 | Suriname | スリナム | HOL | Suriname | 維持(日本語訳継続) |
| 310 | French Guiana | フランス領ギアナ | USA | Guyane | 再編・改名 |
| 311 | BritMex | イギリス領ホンジュラス | ENG | Belize | 再編・改名 |
| 312 | Honduras | ホンジュラス | HON | Honduras | 維持(日本語訳継続) |
| 313 | Guatemala | グアテマラ | GUA | Ciudad de Guatemala | 再編・改名 |
| 314 | El Salvador | エルサルバドル | ELS | El Salvador | 維持(日本語訳継続) |
| 315 | Cuba | キューバ | CUB | Cuba | 維持(日本語訳継続) |
| 316 | Costa Rica | コスタリカ | COS | Costa Rica | 維持(日本語訳継続) |
| 317 | Nicaragua | ニカラグア | NIC | Managua | 再編・改名 |
| 318 | Haiti | ハイチ | HAI | Haiti | 維持(日本語訳継続) |
| 319 | Dominican Republic | ドミニカ | DOM | Dominican Republic | 維持(日本語訳継続) |
| 320 | French India | フランス領インド | DRV | Pondichéry | 再編・改名 |
| 321 | Goa | ゴア | POR | Goa | 維持(日本語訳継続) |
| 322 | Tibet | ナクチュ | TIB | Nagqu | 再編・改名 |
| 323 | Nepal | ネパール | NEP | Nepal | 維持(日本語訳継続) |
| 324 | Bhutan | ブータン | BHU | Bhutan | 維持(日本語訳継続) |
| 325 | Yunnan | 雲南 | YUN | Kunming | 再編・改名 |
| 326 | Hong Kong | 香港 | GER | Hong Kong | 維持(日本語訳継続) |
| 327 | Manila | マニラ | PHI | Manila | 維持(日本語訳継続) |
| 328 | Kirin | 吉林 | MAN | Binkiang | 再編・改名 |
| 329 | Tannu Tuva | タンヌ・トゥヴァ | RUS | Tannú Tyva | 再編・改名 |
| 330 | Mongolia | モンゴル | MON | Ulaanbaatar | 再編・改名 |
| 331 | Newfoundland | ニューファンドランド | ENG | Newfoundland | 維持(日本語訳継続) |
| 332 | Labrador | ラブラドール | ENG | Labrador | 維持(日本語訳継続) |
| 333 | Sarawak | サラワク | DAS | Sarawak | 維持(日本語訳継続) |
| 334 | Dutch Borneo | カリマンタン | INS | East Kalimantan | 再編・改名 |
| 335 | Java | ジャワ | INS | West Java | 再編・改名 |
| 336 | Malaya | マラヤ | DAS | Malay | 再編・改名 |
| 337 | Faroe Islands | フェロー諸島 | DEN | Færøerne | 再編・改名 |
| 338 | Gloucestershire | グロスタシャー | ENG | Gloucestershire | 維持(日本語訳継続) |
| 339 | Izmir | イズミル | TUR | Balıkesir | 再編・改名 |
| 340 | Bursa | ブルサ | TUR | Biga | 再編・改名 |
| 341 | Edirne | エディルネ | GRE | İstanbul | 再編・改名 |
| 342 | Antalya | アンタルヤ | TUR | Mugla | 再編・改名 |
| 343 | Afyon | アフィヨン | TUR | Afyon | 維持(日本語訳継続) |
| 344 | Malatya | マラティヤ | TUR | Adana | 再編・改名 |
| 345 | Mersin | メルスィン | TUR | Silifke | 再編・改名 |
| 346 | Konya | コンヤ | TUR | Konya | 維持(日本語訳継続) |
| 347 | Izmit | イズミット | TUR | Zonguldak | 再編・改名 |
| 348 | Kayseri | カイセリ | TUR | Aksaray | 再編・改名 |
| 349 | Sivas | スィヴァス | TUR | Sivas | 維持(日本語訳継続) |
| 350 | Diyarbakır | ディヤルバクル | KUR | Cizre | 再編・改名 |
| 351 | Vologda | ヴォログダ | RUS | Totma | 再編・改名 |
| 352 | Hakkari | ハッキャリ | KUR | Hakkari | 維持(日本語訳継続) |
| 353 | Erzurum | トゥンジェリ | KUR | Van | 再編・改名 |
| 354 | Trabzon | トラブゾン | ARM | Trabzon | 維持(日本語訳継続) |
| 355 | Samsun | サムスン | TUR | Samsun | 維持(日本語訳継続) |
| 356 | Kastamonu | カスタモヌ | TUR | Kastamonu | 維持(日本語訳継続) |
| 357 | New England | ニューイングランド | USA | Massachusetts | 再編・改名 |
| 358 | New York | ニューヨーク | USA | Albany | 再編・改名 |
| 359 | New Jersey | ニュージャージー | USA | Newark | 再編・改名 |
| 360 | Pennsylvania | ペンシルべニア | USA | Harrisburg | 再編・改名 |
| 361 | Maryland | メリーランド | USA | District of Columbia | 再編・改名 |
| 362 | Virginia | バージニア | USA | Virginia | 維持(日本語訳継続) |
| 363 | North Carolina | ノースカロライナ | USA | North Carolina | 維持(日本語訳継続) |
| 364 | South Carolina | サウスカロライナ | USA | South Carolina | 維持(日本語訳継続) |
| 365 | Georgia | ジョージア | USA | Georgia | 維持(日本語訳継続) |
| 366 | Florida | フロリダ | USA | Florida | 維持(日本語訳継続) |
| 367 | Alabama | アラバマ | USA | Montgomery | 再編・改名 |
| 368 | Tennessee | テネシー | USA | Tennessee | 維持(日本語訳継続) |
| 369 | Kentucky | ケンタッキー | USA | Kentucky | 維持(日本語訳継続) |
| 370 | Mississippi | ミシシッピ | USA | Jackson | 再編・改名 |
| 371 | Louisiana | ルイジアナ | USA | Monroe | 再編・改名 |
| 372 | Arkansas | アーカンソー | USA | Arkansas | 維持(日本語訳継続) |
| 373 | Missouri | ミズーリ | USA | Missouri | 維持(日本語訳継続) |
| 374 | Oklahoma | オクラホマ | USA | Oklahoma | 維持(日本語訳継続) |
| 375 | Texas | テキサス | USA | Houston | 再編・改名 |
| 376 | New Mexico | ニューメキシコ | USA | Albuquerque | 再編・改名 |
| 377 | Arizona | アリゾナ | USA | Northern Arizona | 再編・改名 |
| 378 | California | カリフォルニア | USA | Santa Maria | 再編・改名 |
| 379 | Nevada | ネバダ | USA | Western Nevada | 再編・改名 |
| 380 | Utah | ユタ | USA | Utah | 維持(日本語訳継続) |
| 381 | Wyoming | ワイオミング | USA | Northern Wyoming | 再編・改名 |
| 382 | Colorado | コロラド | USA | Grand Junction | 再編・改名 |
| 383 | Kansas | カンザス | USA | Kansas | 維持(日本語訳継続) |
| 384 | Nebraska | ネブラスカ | USA | Nebraska | 維持(日本語訳継続) |
| 385 | Oregon | オレゴン | USA | Oregon | 維持(日本語訳継続) |
| 386 | Washington | ワシントン | USA | Washington | 維持(日本語訳継続) |
| 387 | Idaho | アイダホ | USA | Idaho | 維持(日本語訳継続) |
| 388 | Montana | モンタナ | USA | Montana | 維持(日本語訳継続) |
| 389 | North Dakota | ノースダコタ | USA | North Dakota | 維持(日本語訳継続) |
| 390 | South Dakota | サウスダコタ | USA | South Dakota | 維持(日本語訳継続) |
| 391 | Minnesota | ミネソタ | USA | Minnesota | 維持(日本語訳継続) |
| 392 | Iowa | アイオワ | USA | Iowa | 維持(日本語訳継続) |
| 393 | Michigan | ミシガン | USA | Michigan | 維持(日本語訳継続) |
| 394 | Wisconsin | ウィスコンシン | USA | Wisconsin | 維持(日本語訳継続) |
| 395 | Illinois | イリノイ | USA | Illinois | 維持(日本語訳継続) |
| 396 | Indiana | インディアナ | USA | Indiana | 維持(日本語訳継続) |
| 397 | Syktyvkar | スィクトィフカル | RUS | Syktyvkar | 維持(日本語訳継続) |
| 398 | Perm | ペルミ | RUS | Perm | 維持(日本語訳継続) |
| 399 | Izhevsk | イジェフスク | RUS | Izhevsk | 維持(日本語訳継続) |
| 400 | Kirov | キーロフ | RUS | Kirov | 維持(日本語訳継続) |
| 401 | Engels | エンゲリス | RUS | Engels | 維持(日本語訳継続) |
| 402 | Akhtubinsk | アクチュビンスク | RUS | Akhtubinsk | 維持(日本語訳継続) |
| 403 | Tyumen | チュメニ | RUS | Tyumen | 維持(日本語訳継続) |
| 404 | Kyzyl Orda | クズロルダ | RUS | Mirzoyan | 再編・改名 |
| 405 | Tashkent | タシュケント | RUS | Toshkent | 再編・改名 |
| 406 | Krasnyy Yar | グリエフ | RUS | Guryev | 再編・改名 |
| 407 | Uralsk | ウラリスク | RUS | Ural'sk | 再編・改名 |
| 408 | Vladivostok | ウラジオストク | RUS | Vladivostok | 維持(日本語訳継続) |
| 409 | Khabarovsk | ハバロフスク | RUS | Khabarovsk | 維持(日本語訳継続) |
| 410 | Sistan | スィースターン | PER | Sistan | 維持(日本語訳継続) |
| 411 | Isfahan | エスファハーン | PER | Isfahan | 維持(日本語訳継続) |
| 412 | Fars | ファールス | PER | Fars | 維持(日本語訳継続) |
| 413 | Khuzestan | フーゼスターン | PER | Khuzestan | 維持(日本語訳継続) |
| 414 | Kerman | ケルマーン | PER | Kerman | 維持(日本語訳継続) |
| 415 | Herat | ヘラート | AFG | Farah | 再編・改名 |
| 416 | Khorasan | ホラーサーン | PER | Khorasan | 維持(日本語訳継続) |
| 417 | Hamadan | ハマダーン | PER | Hamadan | 維持(日本語訳継続) |
| 418 | Semnan | サムナーン | PER | Semnan | 維持(日本語訳継続) |
| 419 | Azerbaijan | 西アゼルバイジャン | PER | Tibriz | 再編・改名 |
| 420 | Gilan | ギーラーン | PER | Gilan | 維持(日本語訳継続) |
| 421 | Ilam | イラム | PER | Kurdistan | 再編・改名 |
| 422 | Ceylon | セイロン | ENG | Ceylon | 維持(日本語訳継続) |
| 423 | Southern Madras | 南マドラス | DRV | Madras | 再編・改名 |
| 424 | Northern Madras | 北マドラス | DRV | Andhra | 再編・改名 |
| 425 | Mysore | マイソール | DRV | Karnataka | 再編・改名 |
| 426 | Orissa | オリッサ | IND | Orissa | 維持(日本語訳継続) |
| 427 | Hyderabad | ハイデラバード | HYD | Hyderabad | 維持(日本語訳継続) |
| 428 | Gujarat | グジャラート | IND | Gujarat | 維持(日本語訳継続) |
| 429 | Bombay | ボンベイ | MRA | Bombay | 維持(日本語訳継続) |
| 430 | East Bengal | 東ベンガル | BAN | Dacca | 再編・改名 |
| 431 | West Bengal | 西ベンガル | BAN | Calcutta | 再編・改名 |
| 432 | Assam | アッサム | BAN | Assam | 維持(日本語訳継続) |
| 433 | Rajahsthan | ラージャスターン | IND | Rajahsthan | 維持(日本語訳継続) |
| 434 | Arunachal Pradesh | アルナーチャル・プラデーシュ | TIB | Tawang | 再編・改名 |
| 435 | Bihar | ビハール | IND | Bihar | 維持(日本語訳継続) |
| 436 | Central Provinces | 中央州 | IND | Jabalpur | 再編・改名 |
| 437 | Central India | 中央インド | IND | Indore | 再編・改名 |
| 438 | United Provinces | 連合州 | IND | Lucknow | 再編・改名 |
| 439 | Delhi | デリー | IND | Delhi | 維持(日本語訳継続) |
| 440 | West Punjab | 西パンジャブ | PAK | Punjab | 再編・改名 |
| 441 | Kashmir | カシミール | KAS | Kashmir | 維持(日本語訳継続) |
| 442 | Peshawar | ペシャーワル | AFG | Peshawar | 維持(日本語訳継続) |
| 443 | Sind | シンド | PAK | Sind | 維持(日本語訳継続) |
| 444 | South Baluchistan | 南バルチスタン | KLT | Baluchistan | 再編・改名 |
| 445 | Sibi | シビ | PAK | Quetta | 再編・改名 |
| 446 | Cairo | スエズ | EGY | Cairo | 維持(日本語訳継続) |
| 447 | Alexandria | アレクサンドリア | EGY | Alexandria | 維持(日本語訳継続) |
| 448 | Tripoli | トリポリ | LBA | Tripoli | 維持(日本語訳継続) |
| 449 | El Agheila | エル・アゲイラ | LBA | El Agheila | 維持(日本語訳継続) |
| 450 | Benghasi | ベンガジ | LBA | Benghasi | 維持(日本語訳継続) |
| 451 | Derna | デルナ | LBA | Derna | 維持(日本語訳継続) |
| 452 | Matrouh | マトルーフ | EGY | Matrouh | 維持(日本語訳継続) |
| 453 | Sinai | シナイ | EGY | el-ʻArīsh | 再編・改名 |
| 454 | Palestine | パレスチナ | SYR | Tel Aviv | 再編・改名 |
| 455 | Jordan | ヨルダン | SYR | Jordan | 維持(日本語訳継続) |
| 456 | Aswan | アスワン | EGY | Aswan | 維持(日本語訳継続) |
| 457 | Aswan | 東部砂漠 | EGY | Hurghada | 再編・改名 |
| 458 | Tunisia | チュニジア | TUN | Tunis | 再編・改名 |
| 459 | Algiers | アルジェ | ALG | Algiers | 維持(日本語訳継続) |
| 460 | Constantine | コンスタンティーヌ | ALG | Constantine | 維持(日本語訳継続) |
| 461 | Casablanca | カサブランカ | MOR | Morocco | 再編・改名 |
| 462 | Marrakech | マラケシュ | MOR | Marrakech | 維持(日本語訳継続) |
| 463 | Alaska | アラスカ | USA | Anchorage | 再編・改名 |
| 464 | Nova Scotia | ノバスコシア | CAN | Nova Scotia | 維持(日本語訳継続) |
| 465 | New Brunswick | ニューブランズウィック | CAN | New Brunswick | 維持(日本語訳継続) |
| 466 | Quebec | ノール・デュ・ケベック | CAN | Quebec | 維持(日本語訳継続) |
| 467 | Manitoba | マニトバ | CAN | Manitoba | 維持(日本語訳継続) |
| 468 | Saint Lawrence | セント・ローレンス | CAN | Montréal | 再編・改名 |
| 469 | Saskatchewan | サスカチュワン | CAN | Saskatchewan | 維持(日本語訳継続) |
| 470 | Alberta | アルバータ | CAN | Alberta | 維持(日本語訳継続) |
| 471 | Prince Rupert | ルパート王子 | CAN | Yukon | 再編・改名 |
| 472 | N.W Territories | 北西部領土 | CAN | Northwestern Territories | 再編・改名 |
| 473 | British Columbia | ブリティッシュコロンビア | CAN | British Columbia | 維持(日本語訳継続) |
| 474 | Yucatan | ユカタン | MEX | Yucatan | 維持(日本語訳継続) |
| 475 | Chiapas | チアパス | MEX | Chiapas | 維持(日本語訳継続) |
| 476 | Oaxaca | オアハカ | MEX | Villahermosa | 再編・改名 |
| 477 | Veracruz | ベラクルス | MEX | Veracruz | 維持(日本語訳継続) |
| 478 | Jalisco | ハリスコ | MEX | Jalisco | 維持(日本語訳継続) |
| 479 | Tamaulipas | タマウリパス | MEX | Tamaulipas | 維持(日本語訳継続) |
| 480 | Coahuila | コアウリア | MEX | Coahuila | 維持(日本語訳継続) |
| 481 | Durango | ドゥランゴ | MEX | Durango | 維持(日本語訳継続) |
| 482 | Chihuahua | チワワ | MEX | Chihuahua | 維持(日本語訳継続) |
| 483 | Sonora | ソノラ | MEX | Sonora | 維持(日本語訳継続) |
| 484 | Baja California | バハ・カリフォルニア | MEX | Baja California | 維持(日本語訳継続) |
| 485 | Guerrero | ゲレロ | MEX | Guerrero | 維持(日本語訳継続) |
| 486 | Meta | メタ | COL | Meta | 維持(日本語訳継続) |
| 487 | Santa Cruz | サンタクルス | BOL | Santa Cruz | 維持(日本語訳継続) |
| 488 | Bolivar | ボリバル | VEN | Bolivar | 維持(日本語訳継続) |
| 489 | Zulia | スリア | VEN | Zulia | 維持(日本語訳継続) |
| 490 | Pastaza | パスタサ | ECU | Pastaza | 維持(日本語訳継続) |
| 491 | Loreto | ロレト | PRU | Loreto | 維持(日本語訳継続) |
| 492 | Arequipa | アレキパ | PRU | Arequipa | 維持(日本語訳継続) |
| 493 | La Libertad | ラ・リベルタ | COL | La Libertad | 維持(日本語訳継続) |
| 494 | Ucayali | ウカヤリ | PRU | Ucayali | 維持(日本語訳継続) |
| 495 | Amazonas | アマゾナス | BRA | Manaus | 再編・改名 |
| 496 | Para | ミナスジェライス | BRA | Minas Gerais | 再編・改名 |
| 497 | Maranhao | マラニョン | BRA | Para | 再編・改名 |
| 498 | Rio Grande | リオ・グランデ・ド・ノルテ | BRA | Rio Grande do Norte | 再編・改名 |
| 499 | Bahia | バイーア | BRA | Bahia | 維持(日本語訳継続) |
| 500 | Rio de Janeiro | リオデジャネイロ | BRA | Rio de Janeiro | 維持(日本語訳継続) |
| 501 | Saol Paulo | サンパウロ | BRA | Sao Paulo | 再編・改名 |
| 502 | Rio Grande Sul | リオ・グランデ・ド・スル | BRA | Rio Grande do Sul | 再編・改名 |
| 503 | Santa Catarina | サンタ・カタリーナ | BRA | Parana | 再編・改名 |
| 504 | Iguacu | ポンタ・ポラン | BRA | Iguacu | 維持(日本語訳継続) |
| 505 | Goias | ゴイアス | BRA | Goias | 維持(日本語訳継続) |
| 506 | Antofagasta | アントファガスタ | CHL | Atacama | 再編・改名 |
| 507 | Magallanes | マガリャーネス | CHL | Aisén | 再編・改名 |
| 508 | Tucumán | トゥクマン | ARG | Tucuman | 再編・改名 |
| 509 | Chaco Austral | 南方チャコ | ARG | Chaco Austral | 維持(日本語訳継続) |
| 510 | Región Mesopotámica | メソポタミア地域 | ARG | Entre Rios | 再編・改名 |
| 511 | Mendoza | メンドーサ | ARG | Mendoza | 維持(日本語訳継続) |
| 512 | Río Negro | リオ・ネグロ | ARG | Patagonia | 再編・改名 |
| 513 | Tlemcen | トレムセン | ALG | Tlemcen | 維持(日本語訳継続) |
| 514 | Algerian Desert (impassable) | アルジェリア砂漠 | ALG | Algerian Desert | 維持(日本語訳継続) |
| 515 | Southern Sahara (impassable) | サハラ砂漠南部 | AOC | Agadez | 再編・改名 |
| 516 | Northern Siberia | ドゥディンカ | RUS | Central Siberia | 再編・改名 |
| 517 | Victoria | ビクトリア | AST | Victoria | 維持(日本語訳継続) |
| 518 | Tasmania | タスマニア | AST | Tasmania | 維持(日本語訳継続) |
| 519 | South Australia | 南オーストラリア | AST | South Australia | 維持(日本語訳継続) |
| 520 | Northern Territory | ノーザンテリトリー | AST | Northern Territory | 維持(日本語訳継続) |
| 521 | Queensland | クイーンズランド | AST | Queensland | 維持(日本語訳継続) |
| 522 | Western Australia | オーストラリア西部 | AST | Western Australia | 維持(日本語訳継続) |
| 523 | New Guinea | パプア | AST | Papua | 再編・改名 |
| 524 | Taiwan | 台湾 | FOR | Taiwan | 維持(日本語訳継続) |
| 525 | Gyeonggi | 京畿 | KOR | Keiki-dō | 再編・改名 |
| 526 | Okinawa | 沖縄 | JAP | Okinawa | 維持(日本語訳継続) |
| 527 | Pyongan-Hwanghae | 平安・黄海 | KOR | Pyon'ando | 再編・改名 |
| 528 | Kitakyūshū | 北九州 | JAP | Kita Kyūshū | 再編・改名 |
| 529 | San'yo | 山陽 | JAP | Chūgokuchihō | 再編・改名 |
| 530 | Shikoku | 四国 | JAP | Shikoku | 維持(日本語訳継続) |
| 531 | Kansai | 関西 | JAP | Kansai | 維持(日本語訳継続) |
| 532 | Tokai | 東海 | JAP | Tōkai | 再編・改名 |
| 533 | Kita-Tohoku | 北東北 | JAP | Tōhoku | 再編・改名 |
| 534 | Koshinetsu | 甲信越 | JAP | Niigata | 再編・改名 |
| 535 | Hokuriku | 北陸 | JAP | Hokuriku | 維持(日本語訳継続) |
| 536 | Hokkaido | 北海道 | JAP | Hokkaidō | 再編・改名 |
| 537 | South Sakhalin | 樺太 | RUS | Minami Karafuto | 再編・改名 |
| 538 | Cameroun | コキラービル | BEL | Central Congo | 再編・改名 |
| 539 | Gabon | ガボン | DWA | Gabon | 維持(日本語訳継続) |
| 540 | Angola | ルアンダ | POR | Luanda | 再編・改名 |
| 541 | South West Africa | ホマス | DSW | Windhoek | 再編・改名 |
| 542 | Bechuanaland | ベチュアナランド | BOT | Bechuanaland | 維持(日本語訳継続) |
| 543 | Madagascar | マダガスカル | GER | Madagascar | 維持(日本語訳継続) |
| 544 | East Africa | ロレンソ・マルケス | POR | Lourenco Marques | 再編・改名 |
| 545 | Rhodesia | ローデシア | FRN | Salisbury | 再編・改名 |
| 546 | Tanganyika | タンガニーカ | DOA | Dodoma | 再編・改名 |
| 547 | East Africa | ナイロビ | DOA | Nairobi | 再編・改名 |
| 548 | Uganda | ウガンダ | DOA | Uganda | 維持(日本語訳継続) |
| 549 | Sudan | クルドファン | EGY | Kordofan | 再編・改名 |
| 550 | Eritrea | エリトリア | ERI | Eritrea | 維持(日本語訳継続) |
| 551 | Khartoum | ハルツーム | EGY | Khartoum | 維持(日本語訳継続) |
| 552 | Western Desert (impassable) | 西部砂漠 | EGY | Western Desert | 維持(日本語訳継続) |
| 553 | Lebanon | レバノン | SYR | Lebanon | 維持(日本語訳継続) |
| 554 | Damascus | ダマスカス | SYR | Damascus | 維持(日本語訳継続) |
| 555 | Kuril Islands | 千島列島 | RUS | Chishima Rettō | 再編・改名 |
| 556 | Mali | バマコ | AOC | Bamako | 再編・改名 |
| 557 | Mauritania | モーリタニア | AOC | Noukachott | 再編・改名 |
| 558 | Nigeria | ラゴス | DWA | Kaduna | 再編・改名 |
| 559 | Somaliland | ソマリランド | SOM | Somalia | 再編・改名 |
| 560 | Nikolayevsk | ニコラエフスク | RUS | Nikolayevsk-na-Amure | 再編・改名 |
| 561 | Amur | アムール | RUS | Severnyy Amur | 再編・改名 |
| 562 | Okhotsk | オホーツク | RUS | Okhotsk | 維持(日本語訳継続) |
| 563 | Chita | チタ | RUS | Chita | 維持(日本語訳継続) |
| 564 | TS 6 | ウラン・ウデ | RUS | Ulan Ude | 再編・改名 |
| 565 | Bodaybo | ボダイボ | RUS | Bodaybo | 維持(日本語訳継続) |
| 566 | Irkutsk | イルクーツク | RUS | Irkutsk | 維持(日本語訳継続) |
| 567 | Bratsk | ブラーツク | RUS | Bratsk | 維持(日本語訳継続) |
| 568 | Krasnoyarsk | クラスノヤルスク | RUS | Krasnoyarsk | 維持(日本語訳継続) |
| 569 | TS 11 | ハカシア | RUS | Kemerovo | 再編・改名 |
| 570 | Novosibirsk | ノヴォシビルスク | RUS | Novosibirsk | 維持(日本語訳継続) |
| 571 | Omsk | オムスク | RUS | Omsk | 維持(日本語訳継続) |
| 572 | Chelyabinsk | チェリャビンスク | RUS | Chelyabinsk | 維持(日本語訳継続) |
| 573 | Zlatoust | ズラトウースト | RUS | Zlatoust | 維持(日本語訳継続) |
| 574 | Yakutsk | ヤクーツク | RUS | Yakutsk | 維持(日本語訳継続) |
| 575 | Kirensk | キレンスク | RUS | Kirensk | 維持(日本語訳継続) |
| 576 | Yeniseisk | エニセイスク | RUS | Yeniseisk | 維持(日本語訳継続) |
| 577 | Surgut | スルグート | RUS | Surgut | 維持(日本語訳継続) |
| 578 | Tomsk | トムスク | RUS | Tomsk | 維持(日本語訳継続) |
| 579 | Salekhard | サレハルド | RUS | Salekhard | 維持(日本語訳継続) |
| 580 | Tobolsk | トボリスク | RUS | Tobolsk | 維持(日本語訳継続) |
| 581 | Northern Urals | ウラル北部 | RUS | Severnyy Ural | 再編・改名 |
| 582 | Magnitogorsk | マグニトゴルスク | RUS | Beloretsk | 再編・改名 |
| 583 | Kazakhstan | クスタナイ | RUS | Kustanay | 再編・改名 |
| 584 | Ashkhabad | アシハバード | RUS | Ashkhabad | 維持(日本語訳継続) |
| 585 | Uzbekistan | ウルゲンチ | RUS | Urganch | 再編・改名 |
| 586 | Alma-Ata | アルマ・アタ | RUS | Alma-Ata | 維持(日本語訳継続) |
| 587 | Ust Urt | ウスチウルト | RUS | Ust Urt | 維持(日本語訳継続) |
| 588 | Semipalatinsk | セミパラチンスク | RUS | Semipalatinsk | 維持(日本語訳継続) |
| 589 | Ayaguz | アヤグーズ | RUS | Balkhash | 再編・改名 |
| 590 | Akmolinsk | アクモリンスク | RUS | Akmolinsk | 維持(日本語訳継続) |
| 591 | Hainan | 海南 | GXC | Hainan | 維持(日本語訳継続) |
| 592 | Guangzhou | 広州 | GXC | Jiangmen | 再編・改名 |
| 593 | Guangdong | 広東 | GXC | Yootung | 再編・改名 |
| 594 | Nanning | 南寧 | GXC | Yamchow | 再編・改名 |
| 595 | Fujian | 福建 | KMT | Hokkien | 再編・改名 |
| 596 | Zhejiang | 浙江 | KMT | Chekiang | 再編・改名 |
| 597 | Shandong | 山東 | BYG | Shantung | 再編・改名 |
| 598 | Jiangsu | 江蘇 | BYG | Kiangsu | 再編・改名 |
| 599 | Guangxi | 広西 | GXC | Kwanghsi | 再編・改名 |
| 600 | Jiangxi | 江西 | KMT | Kiangsi | 再編・改名 |
| 601 | Chamdo | カム | TIB | Kham | 再編・改名 |
| 602 | Hunan | 湖南 | KMT | Hunan | 維持(日本語訳継続) |
| 603 | Guizhou | 貴州 | GUI | Kweichow | 再編・改名 |
| 604 | Qinghai | 青海 | XSM | Tsinghai | 再編・改名 |
| 605 | Sichuan | 四川 | KMT | Szechwan | 再編・改名 |
| 606 | Anhui | 安徽 | BYG | Anhwei | 再編・改名 |
| 607 | Henan | 河南 | BYG | Honan | 再編・改名 |
| 608 | Beiping | 北平 | BYG | Beiping | 維持(日本語訳継続) |
| 609 | East Hebei | 冀東 | BYG | Hopeh Dongbu | 再編・改名 |
| 610 | Jehol | 熱河 | BYG | Jehol | 維持(日本語訳継続) |
| 611 | Chahar | チャハル | MON | Nanchahar | 再編・改名 |
| 612 | Xilingol | シリンゴル | MON | Chahar | 再編・改名 |
| 613 | China 12 | 上海 | KMT | Shanghai | 再編・改名 |
| 614 | Hebei | 河北 | BYG | Hopeh | 再編・改名 |
| 615 | Shanxi | 山西 | SHX | Shansi | 再編・改名 |
| 616 | Ningxia | 寧夏 | XSM | Ningsia | 再編・改名 |
| 617 | Urumqi | ウルムチ | SIK | Tihwa | 再編・改名 |
| 618 | Dzungaria | ジュンガル盆地 | ETR | Pekiang | 再編・改名 |
| 619 | Yarkand | ヤルカンド | SIK | Shache | 再編・改名 |
| 620 | Hubei | 湖北 | BYG | Hupeh | 再編・改名 |
| 621 | Suiyuan | 綏遠 | MON | Suiyuan | 維持(日本語訳継続) |
| 622 | Shaanbei | 陝北 | XIC | Shensi | 再編・改名 |
| 623 | Luzon | ルソン | PHI | Luzon | 維持(日本語訳継続) |
| 624 | Central Islands | 中央諸島 | PHI | Central Islands | 維持(日本語訳継続) |
| 625 | Eastern Visayas | 東ビサヤ | PHI | Samar | 再編・改名 |
| 626 | Palawan | パラワン | PHI | Palawan | 維持(日本語訳継続) |
| 627 | Davao | ダバオ | PHI | Mindanao | 再編・改名 |
| 628 | Western Visayas | 西ビサヤ | PHI | Cebu | 再編・改名 |
| 629 | Hawaii | ハワイ | USA | Hawaii | 維持(日本語訳継続) |
| 630 | Johnston Atoll | ジョンストン環礁 | USA | Johnston Atoll | 維持(日本語訳継続) |
| 631 | Midway Island | ミッドウェー島 | USA | Midway Island | 維持(日本語訳継続) |
| 632 | Wake Island | ウェーク島 | USA | Wake Island | 維持(日本語訳継続) |
| 633 | Marshall Islands | マーシャル諸島 | DAS | Marshall Islands | 維持(日本語訳継続) |
| 634 | Solomon Islands | ソロモン諸島 | DAS | Solomon Islands | 維持(日本語訳継続) |
| 635 | New Caledonia | ニューカレドニア | AST | New Caledonia | 維持(日本語訳継続) |
| 636 | Fiji | フィジー | AST | Fiji | 維持(日本語訳継続) |
| 637 | Kamchatka | カムチャツカ | RUS | Kamchatka | 維持(日本語訳継続) |
| 638 | Guam | グアム | USA | Guam | 維持(日本語訳継続) |
| 639 | Gilbert Islands | ギルバート諸島 | DAS | Gilbert Islands | 維持(日本語訳継続) |
| 640 | Mandalay | マンダレー | BRM | Mandalay | 維持(日本語訳継続) |
| 641 | Tahiti | タヒチ | AST | Tahiti | 維持(日本語訳継続) |
| 642 | Phoenix Island | フェニックス島 | USA | Phoenix Island | 維持(日本語訳継続) |
| 643 | Ellice Islands | エリス諸島 | DAS | Ellice Islands | 維持(日本語訳継続) |
| 644 | state 3 | コルィマ | RUS | Northeast Siberia | 再編・改名 |
| 645 | Iwo Jima | 硫黄島 | JAP | Iōtō | 再編・改名 |
| 646 | Saipan | サイパン | DAS | Saipan | 維持(日本語訳継続) |
| 647 | Palau | パラオ | DAS | Palau | 維持(日本語訳継続) |
| 648 | Marcus Island | 南鳥島 | JAP | Minami-Tori-shima | 再編・改名 |
| 649 | Galapagos Islands | ガラパゴス諸島 | ECU | Galapagos Islands | 維持(日本語訳継続) |
| 650 | Attu Island | アッツ島 | USA | Attu Island | 維持(日本語訳継続) |
| 651 | Ufa | ウファ | RUS | Ufa | 維持(日本語訳継続) |
| 652 | Orenburg | オレンブルク | RUS | Orenburg | 維持(日本語訳継続) |
| 653 | Sverdlovsk | スヴェルドロフスク | RUS | Sverdlovsk | 維持(日本語訳継続) |
| 654 | sov state 8 | ゴルノ＝アルタイスク | RUS | Oyrot-Tura | 再編・改名 |
| 655 | North Sakhalin | 北サハリン | RUS | Severnyy Sakhalin | 再編・改名 |
| 656 | Kuwait | クウェート | IRQ | Kuwait | 維持(日本語訳継続) |
| 657 | Birobidzhan | ビロビジャン | RUS | Birobidzhan | 維持(日本語訳継続) |
| 658 | Abu Dhabi | アブダビ | UAE | Abu Dhabi | 維持(日本語訳継続) |
| 659 | South Yemen | 南イエメン | YEM | Aden | 再編・改名 |
| 660 | Equatorial Africa | 赤道アフリカ | DWA | Equatorial Africa | 維持(日本語訳継続) |
| 661 | Tripolitania | トリポリタニア | LBA | Tripolitania | 維持(日本語訳継続) |
| 662 | Sirte | スルト | LBA | Sirte | 維持(日本語訳継続) |
| 663 | Cyrenaica | キレナイカ | LBA | Cyrenaica | 維持(日本語訳継続) |
| 664 | Southern Slovakia | スロヴァキア南部 | HUN | Južné Slovensko | 再編・改名 |
| 665 | Gabes | ガベス | TUN | Gabès | 再編・改名 |
| 666 | Norrnorrland | ノールボッテン | SWE | Lappland | 再編・改名 |
| 667 | Lesser Sunda Islands | 小スンダ列島 | INS | Lesser Sunda Islands | 維持(日本語訳継続) |
| 668 | The Moluccas | モルッカ諸島 | INS | North Maluku | 再編・改名 |
| 669 | Dutch New Guinea | 西パプア | INS | West Papua | 再編・改名 |
| 670 | Laos | ラオス | DAS | Laos | 維持(日本語訳継続) |
| 671 | Tonkin | トンキン | DAS | Tonkin | 維持(日本語訳継続) |
| 672 | Sumatra | スマトラ | INS | Northwest Sumatra | 再編・改名 |
| 673 | Sulawesi | スラウェシ | INS | South Sulawesi | 再編・改名 |
| 674 | Central Australia (impassable) | 中央オーストラリア | AST | Central Australia | 維持(日本語訳継続) |
| 675 | Al Hajara | アル・ハジャラ | SAU | Al Hajara | 維持(日本語訳継続) |
| 676 | Mosul | モースル | IRQ | Mosul | 維持(日本語訳継続) |
| 677 | Aleppo | アレッポ | SYR | Halab | 再編・改名 |
| 678 | Rub al Khali | ルブアルハリ | SAU | Rub al Khali | 維持(日本語訳継続) |
| 679 | Hejaz | マディーナ | SAU | Hejaz | 維持(日本語訳継続) |
| 680 | Deir-az-Zur | デリゾール | SYR | Deir-az-Zur | 維持(日本語訳継続) |
| 681 | Cape | ケープ | SAF | Cape | 維持(日本語訳継続) |
| 682 | Northern Ontario | オンタリオ北部 | CAN | Northern Ontario | 維持(日本語訳継続) |
| 683 | Northeastern Canada | ヌナブト | CAN | Keewatin | 再編・改名 |
| 684 | Caroline Islands | カロリン諸島 | DAS | Caroline Islands | 維持(日本語訳継続) |
| 685 | Panama Canal | パナマ運河 | USA | Panamá Canal | 再編・改名 |
| 686 | Puerto Rico | プエルトリコ | USA | Puerto Rico | 維持(日本語訳継続) |
| 687 | British Guyana | イギリス領ガイアナ | ENG | British Guyana | 維持(日本語訳継続) |
| 688 | Chaco Boreal | 北方チャコ | PAR | Chaco Boreal | 維持(日本語訳継続) |
| 689 | Jamaica | ジャマイカ | ENG | Jamaica | 維持(日本語訳継続) |
| 690 | Northern Bahamas | バハマ北部 | ENG | Northern Bahamas | 維持(日本語訳継続) |
| 691 | Trinidad | トリニダード | ENG | Trinidad | 維持(日本語訳継続) |
| 692 | Windward Islands | ウィンドワード諸島 | ENG | Windward Islands | 維持(日本語訳継続) |
| 693 | Southern Bahamas | バハマ南部 | ENG | Southern Bahamas | 維持(日本語訳継続) |
| 694 | French Caribbean | フランス領アンティル | USA | Antilles Françaises | 再編・改名 |
| 695 | Curaçao | キュラソー | HOL | Curaçao | 維持(日本語訳継続) |
| 696 | Bermuda | バミューダ | ENG | Bermuda | 維持(日本語訳継続) |
| 697 | Madeira | マデイラ | POR | Madeira | 維持(日本語訳継続) |
| 698 | Azores | アゾレス | POR | Azores | 維持(日本語訳継続) |
| 699 | Rio de Oro | リオ・デ・オロ | MOR | Río de Oro | 再編・改名 |
| 700 | Sierra Leone | シエラレオネ | ENG | Sierra Leone | 維持(日本語訳継続) |
| 701 | Gambia | ガンビア | ENG | Gambia | 維持(日本語訳継続) |
| 702 | Cape Verde | カーボベルデ | POR | Cape Verde | 維持(日本語訳継続) |
| 703 | Ascension | アセンション | ENG | Ascension | 維持(日本語訳継続) |
| 704 | Saint Helena | セントヘレナ | ENG | Saint Helena | 維持(日本語訳継続) |
| 705 | Sao Tome | サントメ | POR | Sao Tome | 維持(日本語訳継続) |
| 706 | Reunion | レユニオン | GER | Reunion | 維持(日本語訳継続) |
| 707 | Mauritius | モーリシャス | ENG | Mauritius | 維持(日本語訳継続) |
| 708 | Comoro Islands | コモロ諸島 | GER | Comoro Islands | 維持(日本語訳継続) |
| 709 | Seychelles | セーシェル | ENG | Seychelles | 維持(日本語訳継続) |
| 710 | Diego Garcia | ディエゴ・ガルシア | ENG | Diego Garcia | 維持(日本語訳継続) |
| 711 | Christmas Island | クリスマス島 | ENG | Christmas Island | 維持(日本語訳継続) |
| 712 | Cocos Islands | ココス諸島 | ENG | Cocos Islands | 維持(日本語訳継続) |
| 713 | Kerguelen | ケルゲレン | GER | Kerguelen | 維持(日本語訳継続) |
| 714 | Heilungkiang | 黒竜江 | MAN | Heilungkiang | 維持(日本語訳継続) |
| 715 | Liaobei | 遼北 | BYG | Liaopeh | 再編・改名 |
| 716 | Liaoning | 遼寧 | MAN | Ishangga Gašan Hoton | 再編・改名 |
| 717 | Sungkiang | 松江 | MAN | Sankiang | 再編・改名 |
| 718 | Stanleyville | スタンリーヴィル | BEL | Stanleyville | 維持(日本語訳継続) |
| 719 | Natal | ナタール | SAF | Natal | 維持(日本語訳継続) |
| 720 | South Georgia | サウスジョージア | ENG | South Georgia | 維持(日本語訳継続) |
| 721 | East Timor | ポルトガル領ティモール | POR | Portuguese Timor | 再編・改名 |
| 722 | Petsamo | ペツァモ | RUS | Petsamo | 維持(日本語訳継続) |
| 723 | South Island | 南島 | AST | South Island | 維持(日本語訳継続) |
| 724 | Northern Malay | マレー北部 | SIA | Northern Malay | 維持(日本語訳継続) |
| 725 | Nauru | ナウル | DAS | Nauru | 維持(日本語訳継続) |
| 726 | Samoa | サモア | DAS | Samoa | 維持(日本語訳継続) |
| 727 | Line Islands | ライン諸島 | USA | Line Islands | 維持(日本語訳継続) |
| 728 | Guangzhouwan | 広州湾 | GER | Guangzhouwan | 維持(日本語訳継続) |
| 729 | Macau | マカオ | POR | Macau | 維持(日本語訳継続) |
| 730 | St Pierre and Miquelon | サンピエール島・ミクロン島 | ENG | St Pierre and Miquelon | 維持(日本語訳継続) |
| 731 | Central Macedonia | 中央マケドニア | GRE | Kentrikí Makedonía | 再編・改名 |
| 732 | Pamir | パミール | RUS | Frunze | 再編・改名 |
| 733 | Andaman | アンダマン | ENG | Andaman and Nicobar | 再編・改名 |
| 734 | Nendo | ネンド | DAS | Nendo | 維持(日本語訳継続) |
| 735 | Savoy | サヴォイ | FRA | Haute-Savoie | 再編・改名 |
| 736 | Litorale | リトラーレ | ITA | Istria | 再編・改名 |
| 737 | Bismarck | ビスマルク | DAS | Bismarck | 維持(日本語訳継続) |
| 738 | Aru Islands | アルー諸島 | INS | Aru Islands | 維持(日本語訳継続) |
| 739 | Haida Gwaii | ハイダグアイ | CAN | Haida Gwaii | 維持(日本語訳継続) |
| 740 | Vancouver Island | バンクーバー島 | CAN | Vancouver Island | 維持(日本語訳継続) |
| 741 | Cambodia | カンボジア | DAS | Cambodia | 維持(日本語訳継続) |
| 742 | Stalinabad | スタリナバード | RUS | Stalinabad | 維持(日本語訳継続) |
| 743 | Qingdao | 青島 | GER | Tsingtao | 再編・改名 |
| 744 | Xian | 西安 | XIC | Sianyang | 再編・改名 |
| 745 | Dalian | 大連 | RUS | Dalian | 維持(日本語訳継続) |
| 746 | Ordos | オルドス | XIC | Ordos | 維持(日本語訳継続) |
| 747 | Dali | 大理 | YUN | Tali | 再編・改名 |
| 748 | Zunyi | 遵義 | GUI | Tsunyi | 再編・改名 |
| 749 | Huangshan | 黄山 | KMT | Suanshan | 再編・改名 |
| 750 | Changde | 常徳 | KMT | Changde | 維持(日本語訳継続) |
| 751 | Liangshan | 涼山 | KMT | Liangshan | 維持(日本語訳継続) |
| 752 | Chamdo | 甘孜 | KMT | Ganzi | 再編・改名 |
| 753 | Gannan | 甘南 | XSM | Gannan | 維持(日本語訳継続) |
| 754 | Golog | ゴロク | XSM | Golog | 維持(日本語訳継続) |
| 755 | Haixi | 海西 | XSM | Dulan | 再編・改名 |
| 756 | Jiuquan | 酒泉 | XSM | Lanchow | 再編・改名 |
| 757 | Shigatse | シガツェ | TIB | Shigatse | 維持(日本語訳継続) |
| 758 | Ngari | ガリ | TIB | Ngari | 維持(日本語訳継続) |
| 759 | Kunlun | 崑崙山 | SIK | Kunlun | 維持(日本語訳継続) |
| 760 | Dabancheng | 達坂城 | SIK | Hami | 再編・改名 |
| 761 | Hulunbuir | フルンボイル | MAN | Xingan | 再編・改名 |
| 762 | Katowice | カトヴィツェ | GER | Katowice | 維持(日本語訳継続) |
| 763 | Königsberg | ケーニヒスベルク | GER | Königsberg | 維持(日本語訳継続) |
| 764 | West Banat | 西バナト | HUN | Srednji Banat | 再編・改名 |
| 765 | Qatar | カタール | QAT | Qatar | 維持(日本語訳継続) |
| 766 | Southern Bessarabia | ベッサラビア南部 | RUS | Basarabia de Sud | 再編・改名 |
| 767 | North Darfur (impassable) | 北ダルフール | EGY | Sudanese Sahara | 再編・改名 |
| 768 | Rwanda | ルワンダ | BEL | Rwanda | 維持(日本語訳継続) |
| 769 | Burundi | ブルンジ | BEL | Burundi | 維持(日本語訳継続) |
| 770 | Malawi | マラウイ | FRN | Malawi | 維持(日本語訳継続) |
| 771 | Zambia | ローデシア北東部 | FRN | Lusaka | 再編・改名 |
| 772 | Middle Congo | 中央コンゴ | COG | Middle Congo | 維持(日本語訳継続) |
| 773 | Cameroon | カメルーン | DWA | Yaoundé | 再編・改名 |
| 774 | Chad | チャド | DWA | N'Djamena | 再編・改名 |
| 775 | B.E.T. (impassable) | ボルク・エネディ・ティベスティ | DWA | Borkou-Ennedi-Tibesti | 再編・改名 |
| 776 | Dahomey | ダホメ | DWA | Dahomey | 維持(日本語訳継続) |
| 777 | Togo | トーゴ | DWA | Togo | 維持(日本語訳継続) |
| 778 | Upper Volta | オートボルタ | AOC | Upper Volta | 維持(日本語訳継続) |
| 779 | Ivory Coast | 象牙海岸 | AOC | Ivory Coast | 維持(日本語訳継続) |
| 780 | Guinea | ギニア | AOC | Guinea | 維持(日本語訳継続) |
| 781 | Niger | ニジェール | AOC | Niamey | 再編・改名 |
| 782 | Tombouctou (impassable) | トンブクトゥ | AOC | Azawad | 再編・改名 |
| 783 | Sidi Ifni | シディ・イフニー | MOR | Sidi Ifni | 維持(日本語訳継続) |
| 784 | Ermland-Masuren | ヴィルナ | RUS | Wilno | 再編・改名 |
| 785 | Picardy | ピカルディ | FRA | Picardie | 再編・改名 |
| 786 | Mauritanian Desert (impassable) | モーリタニア砂漠 | AOC | Northeastern Mauritania | 再編・改名 |
| 787 | Northern Kashmir | カシミール北部 | KAS | Northern Kashmir | 維持(日本語訳継続) |
| 788 | Salamanca | サラマンカ | SPR | Ostrheinland | 再編・改名 |
| 789 | Córdoba | コルドバ | SPR | Saarland | 再編・改名 |
| 790 | Asturias | アストゥリアス | SPR | Frankfurt | 再編・改名 |
| 791 | Valladolid | バリャドリド | SPR | Nordbaden | 再編・改名 |
| 792 | País Vasco | パイス・バスコ | SPR | Trier | 再編・改名 |
| 793 | Guadalajara | グアダラハラ | SPR | Magdeburg-Anhalt | 再編・改名 |
| 794 | Eastern Aragón | アラゴン東部 | SPR | Brandenburg | 再編・改名 |
| 795 | Santarém | サンタレン | POR | Leipzig | 再編・改名 |
| 796 | Cabinda | カビンダ | POR | Schleswig | 再編・改名 |
| 797 | Istanbul | コンスタンティノープル西岸 | STC | Stettin | 再編・改名 |
| 798 | Amasya | アマスィヤ | TUR | Traunstein | 再編・改名 |
| 799 | Hatay | アレクサンドレッタ | SYR | Südbaden | 再編・改名 |
| 800 | Van | ヴァン | ARM | Burghausen | 再編・改名 |
| 801 | Moesia | モエシア | BUL | Ostniederschlesien | 再編・改名 |
| 802 | Kosovo | コソボ | YUG | Glatz | 再編・改名 |
| 803 | Southern Serbia | セルビア南部 | YUG | Ratibor | 再編・改名 |
| 804 | Herzegovina | ヘルツェゴビナ | YUG | Sønderjylland | 再編・改名 |
| 805 | Northern Epirus | エピロス北部 | ALB | Bornholm | 再編・改名 |
| 806 | Pyrénées-Atlantiques | ピレネー＝アトランティク | FRA | Salzburg | 再編・改名 |
| 807 | Gdynia | グディニャ | GER | Horn | 再編・改名 |
| 808 | Riga | リガ | RUS | Somogy | 再編・改名 |
| 809 | Latgale | ゼムガレ | RUS | Bács-Kiskun | 再編・改名 |
| 810 | Zemgale | ラトガレ | RUS | Burgenland | 再編・改名 |
| 811 | Saaremaa | サーレマー | RUS | Eismitte | 再編・改名 |
| 812 | Tallinn | ハリュ | RUS | Eupen-Malmedy | 再編・改名 |
| 813 | Rakvere | ヴィルマー | RUS | Waloneye de l'Est | 再編・改名 |
| 814 | Suduva | スードゥヴァ | RUS | Nancy | 再編・改名 |
| 815 | Aukštaitija | アウクシュタイティヤ | RUS | Hirson | 再編・改名 |
| 816 | West Virginia | ウェストバージニア | USA | Foggia | 再編・改名 |
| 817 | Gobi | ゴビ | MON | Meuse | 再編・改名 |
| 818 | Khovd | ホブド | MON | Upper Normandy | 再編・改名 |
| 819 | Dornod | ドルノド | MON | Bourges | 再編・改名 |
| 820 | Khövsgöl | フブスグル | MON | Roussillon | 再編・改名 |
| 821 | Chechnya-Ingushetia | チェチェン＝イングーシ | RUS | Nice | 再編・改名 |
| 822 | Chukotka | チュコト | RUS | Toulon | 再編・改名 |
| 823 | Karakalpakstan | カラカルパクスタン | RUS | Savoie | 再編・改名 |
| 824 | Yamalia | ヤマル | RUS | Andorra | 再編・改名 |
| 825 | Nenets | ネネツ | RUS | Monaco | 再編・改名 |
| 826 | Abkhazia | アブハジア | RUS | Liechtenstein | 再編・改名 |
| 827 | Kabardino-Balkaria | カバルダ＝バルカル | RUS | San Marino | 再編・改名 |
| 828 | North Ossetia | 北オセチア | RUS | Vaticano | 再編・改名 |
| 829 | Engels-Marxstadt | エンゲリス＝マルクスシュタット | RUS | Transnistria | 再編・改名 |
| 830 | Bukhara | ブハラ | RUS | Bucovina de Sud | 再編・改名 |
| 831 | Khiva | ヒヴァ | RUS | Sulina | 再編・改名 |
| 832 | Tashauz | タシャウズ | RUS | Constanta | 再編・改名 |
| 833 | Mari El | マリ・エル | RUS | Mutenia de Est | 再編・改名 |
| 834 | Balta-Tiraspol | バルタ＝ティラスポリ | RUS | Anticosti Island | 再編・改名 |
| 835 | Hararghe | ハラルゲ | ETH | Upper Maine | 再編・改名 |
| 836 | Bale | バレ | ETH | Maine | 再編・改名 |
| 837 | Sidamo | シダモ | ETH | New Hampshire | 再編・改名 |
| 838 | Illubabor-Kaffa | イルバボール・カッファ | ETH | Vermont | 再編・改名 |
| 839 | Welega | ウェレガ | ETH | Connecticut | 再編・改名 |
| 840 | Gojjam | ゴジャム | ETH | Rhode Island | 再編・改名 |
| 841 | Begemder | ベゲムデル | ETH | Delaware | 再編・改名 |
| 842 | Tigray | ティグライ | ETH | Saint Lawrence | 再編・改名 |
| 843 | Wello | ウォロ | ETH | West Virginia | 再編・改名 |
| 844 | Jubaland | ジュバランド | SOM | Maryland | 再編・改名 |
| 845 | Jura Mountains | ジュラ山脈 | SWI | Baton Rouge | 再編・改名 |
| 846 | Ticino | ティチーノ | SWI | Evanston | 再編・改名 |
| 847 | Western Swiss Alps | 西スイスアルプス | SWI | Denver | 再編・改名 |
| 848 | Voralberg | フォアアールベルク | GER | Elkhart | 再編・改名 |
| 849 | Puglia | プーリア | ITA | Guymon | 再編・改名 |
| 850 | Trentino | トレンティーノ | ITA | Amarillo | 再編・改名 |
| 851 | Var | ヴァール | FRA | Big Bend | 再編・改名 |
| 852 | Istria | イストリア | ITA | San Antonio | 再編・改名 |
| 853 | Ljubljana | リュブリャナ | YUG | Eastern Nevada | 再編・改名 |
| 854 | Jawf | ジャウフ | SAU | Northern California | 再編・改名 |
| 855 | Tabuk | タブーク | SAU | Bakersfield | 再編・改名 |
| 856 | Asir-Makkah | アシール・マッカ | SAU | Superior | 再編・改名 |
| 857 | Ha'il | アル・カーシム | SAU | Grand Rapids | 再編・改名 |
| 858 | Najiran | ナジュラーン | SAU | Acadiana | 再編・改名 |
| 859 | Dammam | ダンマーム | SAU | Missoula | 再編・改名 |
| 860 | Côte-Nord | コート・ノール | CAN | Guantanamo Bay | 再編・改名 |
| 861 | Saguenay | サグネ | CAN | Orkney Islands | 再編・改名 |
| 862 | ouest du quebec | ウエスト・デュ・ケベック | CAN | Shetland | 再編・改名 |
| 863 | Maurice | モーリス | CAN | Oświęcim | 再編・改名 |
| 864 | Yukon | ユーコン準州 | CAN | Yasuní | 再編・改名 |
| 865 | N. Saskatchewan | 北サスカチュワン | CAN | Starogard | 再編・改名 |
| 866 | Districts of Ontario | オンタリオ州 | CAN | Idria | 再編・改名 |
| 867 | Northern Manitoba | 北マニトバ | CAN | Trentino | 再編・改名 |
| 868 | Isan | イサーン | SIA | Baranja | 再編・改名 |
| 869 | Lanna | ランナー | SIA | Syrmia | 再編・改名 |
| 870 | North West Australia | 北西オーストラリア | AST | Pirot | 再編・改名 |
| 871 | South West Australia | 南西オーストラリア | AST | Devar | 再編・改名 |
| 872 | North Queensland | 北クイーンズランド | AST | Niš | 再編・改名 |
| 873 | South West Queensland | 南西クイーンズランド | AST | Hala'ib | 再編・改名 |
| 874 | Magadan | マガダン | RUS | Bir Tawil | 再編・改名 |
| 875 | Chukchi Peninsula | チュクチ半島 | RUS | Bahrain | 再編・改名 |
| 876 | Udachny | ウダーチヌイ | RUS | Musandam | 再編・改名 |
| 877 | Verkhoyansk | ベルホヤンスク | RUS | Hatay | 再編・改名 |
| 878 | Khatangsky | ハタンスキー | RUS | Priština | 再編・改名 |
| 879 | Kargopol | カルゴポリ | RUS | Marijampole | 再編・改名 |
| 880 | Kotlas | コトラス | RUS | Latgale | 再編・改名 |
| 881 | Karagandy | カラガンディ | RUS | Zemgale | 再編・改名 |
| 882 | Pavlodar | パブロダル | RUS | Saaremaa-Hiiumaa | 再編・改名 |
| 883 | Kassala | カッサラ | EGY | Jaanilinn | 再編・改名 |
| 884 | Upper Nile | 上ナイル | EGY | Hlučínsko | 再編・改名 |
| 885 | Bahr al Ghazal | バハル・アル・ガザール | EGY | Hewa | 再編・改名 |
| 886 | Blue Nile | 青ナイル | EGY | Jižní Sudety | 再編・改名 |
| 887 | South Darfur | 南ダルフール | EGY | Liberec | 再編・改名 |
| 888 | Lusambo | ルサンボ | BEL | Moravské Sudety | 再編・改名 |
| 889 | Elisabethville | エリザベートヴィル | BEL | Trenčín | 再編・改名 |
| 890 | Costermansville | コステルマンスビル | BEL | Petseri | 再編・改名 |
| 891 | Zambesi | ザンベジ | POR | Abrene | 再編・改名 |
| 892 | South West Angola | 南西アンゴラ | POR | Vaud | 再編・改名 |
| 893 | Karas | カラス | DSW | Ticino | 再編・改名 |
| 894 | Kuneme | クネーネ | DSW | Graubünden | 再編・改名 |
| 895 | Kavango | オチョソンデュパ | DSW | Likouala | 再編・改名 |
| 896 | Manica e Sofala | マニカ・エ・ソファラ | POR | Sangha | 再編・改名 |
| 897 | Zambezia-Moçambique | ザンベジア・モサンビーク | POR | Oyem | 再編・改名 |
| 898 | Gao | ガオ | AOC | Moundou | 再編・改名 |
| 899 | Kayes-Koulikoro | ケーズ・クリコロ | AOC | Neukamerun | 再編・改名 |
| 900 | Benue | ベヌエ | DWA | Southern Cameroon | 再編・改名 |
| 901 | Borno | ボルノ | DWA | Northern Cameroon | 再編・改名 |
| 902 | Sokoto | ソコト | DWA | Weihaiwei | 再編・改名 |
| 903 | Garissa | ガリッサ | DOA | Tadakiyo michi | 再編・改名 |
| 904 | Nyanza-Rift Valley | ニャンザ・リフトバレー | DOA | Zenradō | 再編・改名 |
| 905 | Mombasa | モンバサ | DOA | Gyonsan | 再編・改名 |
| 906 | Socotra | ソコトラ | SOM | Eharadō | 再編・改名 |
| 907 | Cairo | カイロ | EGY | Kita Eharadō | 再編・改名 |
| 908 | Afar | アファール | ETH | Kōkai michi | 再編・改名 |
| 909 | Schleswig | シュレースヴィヒ | GER | Kankyōdō | 再編・改名 |
| 910 | Bornholm | ボーンホルム | DEN | Utsuryōtō | 再編・改名 |
| 911 | Fyn | フュン | DEN | Saishū | 再編・改名 |
| 912 | Southern Jutland | ユトランド南部 | GER | Acre | 再編・改名 |
| 913 | Östergötland | エステルイェータランド | SWE | Acre do Norte | 再編・改名 |
| 914 | Jan Mayen | ヤンマイエン | NOR | Corumbá | 再編・改名 |
| 915 | Bohuslän | ブーヒュースレーン | SWE | Iquique | 再編・改名 |
| 916 | Dalarna | ダーラナ | SWE | Antofagasta | 再編・改名 |
| 917 | Jämtland | イェムトランド | SWE | Panamá Occidental | 再編・改名 |
| 918 | Västerbotten | ヴェステルボッテン | SWE | New Guinea | 再編・改名 |
| 919 | Värmland | ヴェルムランド | SWE | Great Victoria Desert | 再編・改名 |
| 920 | Opplandene | オップランデン | NOR | Kimberley | 再編・改名 |
| 921 | Telemark | テレマルク | NOR | South Austrailia Desert | 再編・改名 |
| 922 | Agder | アグデル | NOR | White Cliffs | 再編・改名 |
| 923 | Helgeland | ヘルゲラン | NOR | Channel Country | 再編・改名 |
| 924 | Troms | トロムス | NOR | Simpson Desert | 再編・改名 |
| 925 | Finnmark | フィンマルク | NOR | Hotin | 再編・改名 |
| 926 | Turku | トゥルク | RUS | Pryluky | 再編・改名 |
| 927 | Häme | ハメ | RUS | Klintsy | 再編・改名 |
| 928 | Kymi | キュミ | RUS | Kem | 再編・改名 |
| 929 | Oulu | オウル | RUS | Belaja Karelija | 再編・改名 |
| 930 | Mikkeli | ミッケリ | RUS | Volzhsky | 再編・改名 |
| 931 | Cumbria | カンブリア | ENG | Dagestan | 再編・改名 |
| 932 | Isle of Man | マン島 | ENG | Derbent | 再編・改名 |
| 933 | Shetland Islands | シェットランド諸島 | ENG | Świsłocz | 再編・改名 |
| 934 | Shkodër | シュコーデル | ALB | Gorenjska | 再編・改名 |
| 935 | Ceará | セアラー | BRA | Bled | 再編・改名 |
| 936 | Pernambuco | ペルナンブーコ | BRA | Murska Sobota | 再編・改名 |
| 937 | Piauí | ピアウイ | BRA | Sisak-Moslavina | 再編・改名 |
| 938 | Pará | パラ | BRA | Neum | 再編・改名 |
| 939 | Amapa | アマパ | BRA | Lika | 再編・改名 |
| 940 | Acre | アクレ | BRA | Budva | 再編・改名 |
| 941 | Tocantins | トカンティンス | BRA | Mitrovica | 再編・改名 |
| 942 | Guaporé | グアポレ | BRA | Pleven | 再編・改名 |
| 943 | Espírito Santo | エスピリトサント | BRA | Shumen | 再編・改名 |
| 944 | Paraná | パラナ | BRA | Al Ahsa | 再編・改名 |
| 945 | Cerro Largo | セロ・ラルゴ | URG | Al Anbar | 再編・改名 |
| 946 | Paysandú | パイサンドゥ | URG | Al Muthanna | 再編・改名 |
| 947 | Tacna-Moquegua | タクナ・モケグア | PRU | Eastern Jordan | 再編・改名 |
| 948 | Easter Island | イースター島 | CHL | Malborghetto Valbruna | 再編・改名 |
| 949 | Aysén | アイセン | CHL | Sheba | 再編・改名 |
| 950 | Araucanía | アラウカニア | CHL | Izmit | 再編・改名 |
| 951 | Arica y Tarapacá | アリカ・イ・タラパカ | CHL | Antalya | 再編・改名 |
| 952 | Atacama | アタカマ | CHL | Northern Cyprus | 再編・改名 |
| 953 | Tierra del Fuego | ティエラ・デル・フエゴ | ARG | Eskisehir | 再編・改名 |
| 954 | Santa Cruz | サンタクルス | ARG | Denizli | 再編・改名 |
| 955 | Chubut | チュブ | ARG | Giresun | 再編・改名 |
| 956 | Santa Fe | サンタフェ | ARG | Corum | 再編・改名 |
| 957 | Formosa | フォルモサ | ARG | Yozgat | 再編・改名 |
| 958 | San Luis y La Pampa | サン・ルイス・ラ・パンパ | ARG | Amasya | 再編・改名 |
| 959 | Los Andes | ロスアンデス | ARG | Tunceli | 再編・改名 |
| 960 | San Juan y La Rioja | サン・フアン・イ・ラ・リオハ | ARG | Şırnak | 再編・改名 |
| 961 | Amazon (impassable) | アマゾン | BRA | Antep | 再編・改名 |
| 962 | Amazon (impassable) | アマゾン | BRA | Tsushima Island | 再編・改名 |
| 963 | Amazon (impassable) | アマゾン | BRA | Fukushima | 再編・改名 |
| 964 | Amazon (impassable) | アマゾン | BRA | Kita Kantō | 再編・改名 |
| 965 | Amazon (impassable) | アマゾン | BRA | Wakayama | 再編・改名 |
| 966 | Amazon (impassable) | アマゾン | BRA | Osumi Islands | 再編・改名 |
| 967 | Amazon (impassable) | アマゾン | BRA | Kumamoto-Miyazaki | 再編・改名 |
| 968 | Amazon (impassable) | アマゾン | BRA | Kagoshima | 再編・改名 |
| 969 | Rio Branco | リオ・ブランコ | BRA | Kōchi | 再編・改名 |
| 970 | Debar | デバル | YUG | Lazarev | 再編・改名 |
| 971 | Northern Dobruja | 北ドブロジャ | ROM | Senkaku Islands | 再編・改名 |
| 972 | South Sudetenland | 南ズデーテンラント | GER | American Virgin Islands | 再編・改名 |
| 973 | Bács-Kiskun | バーチュ・キシュクン | HUN | British Virgin Islands | 再編・改名 |
| 974 | South Transdanubia | ドナウ川西岸南部 | HUN | Channel Islands | 再編・改名 |
| 975 | Burgenland | ブルゲンラント | HUN | Nisiá Anatolikoú Aigaíou | 再編・改名 |
| 976 | Steiermark-Kärnten | シュタイアーマルク・ケルンテン | GER | Kentrikí Ípeiros | 再編・改名 |
| 977 | Antwerp | アントワープ | BEL | Corfu | 再編・改名 |
| 978 | Baden | バーデン | GER | Évvoia | 再編・改名 |
| 979 | Kaiser-Wilhelmsland | カイザー・ヴィルヘルムス・ラント | DAS | Ostfriesland | 再編・改名 |
| 980 | Ardennes | アルデンヌ | BEL | Singapore | 再編・改名 |
| 981 | Barotseland | バロツェランド | FRN | Kedah | 再編・改名 |
| 982 | Madras States | マドラス州 | DRV | Brunei | 再編・改名 |
| 983 | Kolhapur and Deccan | コールハープルとデカン | MRA | Sikkim | 再編・改名 |
| 984 | Bastar | バスタル | IND | North Aksai Chin | 再編・改名 |
| 985 | Sikkim | シッキム | TIB | Himachal | 再編・改名 |
| 986 | East Punjab | 東パンジャブ | IND | Friuli-Venezia Giulia | 再編・改名 |
| 987 | Waziristan | ワジリスタン | AFG | Milano | 再編・改名 |
| 988 | North Baluchistan | 北バルチスタン | KLT | Cuneo-Alessandria | 再編・改名 |
| 989 | Bahawalpur | バハワルプール | IND | Liguria | 再編・改名 |
| 990 | Manipur | マニプール | BAN | Viterbo | 再編・改名 |
| 991 | Gwalior | グワリオル | IND | Basilicata | 再編・改名 |
| 992 | Province of Aden | アデン州 | YEM | Puglia | 再編・改名 |
| 993 | Kentung and Yawnghwe | ケントゥンとヤウンシェ | BRM | Trieste | 再編・改名 |
| 994 | Tenasserim | テナセリム | BRM | Sopron | 再編・改名 |
| 995 | Pegu | ペグー | BRM | Suez Canal | 再編・改名 |
| 996 | Irrawaddy | イラワジ | BRM | Przemyśl | 再編・改名 |
| 997 | Arakan | アラカン | BRM | Suwałki | 再編・改名 |
| 998 | Sagaing | サガイン | BRM | Aouzou | 再編・改名 |
| 999 | Federated Shan | シャン連合州 | BRM | Aktobe | 再編・改名 |
| 1000 | East Azerbaijan | 東アゼルバイジャン | PER | Magnitogorsk | 再編・改名 |
| 1001 | Kurdistan | クルディスタン | PER | Kars | 再編・改名 |
| 1002 | Yazd | ヤズド | PER | Apkhazeti | 再編・改名 |
| 1003 | South Khorasan | 南ホラーサーン | PER | Dağlıq Qarabağ | 再編・改名 |
| 1004 | North Khorasan | 北ホラーサーン | PER | Naxçıvan | 再編・改名 |
| 1005 | Qataghan | カタガン | AFG | Masallı | 再編・改名 |
| 1006 | Khyber Pass | カイバル峠 | AFG | Halland | 再編・改名 |
| 1007 | Maymanah | メイマナ | AFG | Västmanland | 再編・改名 |
| 1008 | Qandahar | カンダハール | AFG | Dalarna | 再編・改名 |
| 1009 | Farah | ファラー | AFG | Jämtland | 再編・改名 |
| 1010 | Al Anbar | アル・アンバール | IRQ | Telemark | 再編・改名 |
| 1011 | Al Basrah | アル・バスラ | IRQ | Østlandet | 再編・改名 |
| 1012 | Kalat | カラート | KLT | Buskerud | 再編・改名 |
| 1013 | Musandam | ムサンダム | OMA | Nordland | 再編・改名 |
| 1014 | Bahrain | バーレーン | BHR | Troms | 再編・改名 |
| 1015 | Oman | オマーン | OMA | Khovd | 再編・改名 |
| 1016 | Dhofar | ドファール | OMA | Khovsgol | 再編・改名 |
| 1017 | Trung Bo | チュンボ | DAS | Arkhangai | 再編・改名 |
| 1018 | Minami Kyūshū | 南九州 | JAP | Khentii | 再編・改名 |
| 1019 | Minami Tohoku | 南東北 | JAP | Dornod | 再編・改名 |
| 1020 | San'in | 山陰 | JAP | Dornogovi | 再編・改名 |
| 1021 | Singapore | シンガポール | DAS | Nanking | 再編・改名 |
| 1022 | Interior Borneo (impassable) | ボルネオ内陸部 | INS | Tonghua | 再編・改名 |
| 1023 | Brunei | ブルネイ | DAS | Dandong | 再編・改名 |
| 1024 | Sabah | サバ | DAS | Jiandao | 再編・改名 |
| 1025 | Zamboanga | サンボアンガ | PHI | Chinchow | 再編・改名 |
| 1026 | Northern Mindanao | 北ミンダナオ | PHI | Fengtian | 再編・改名 |
| 1027 | Bataan | バターン | PHI | Liaocheng | 再編・改名 |
| 1028 | Hamgyong | 咸鏡 | KOR | Nantung | 再編・改名 |
| 1029 | Gangwon | 江原 | KOR | Sinsiang | 再編・改名 |
| 1030 | Gyeongsang | 慶尚 | KOR | Siangyang | 再編・改名 |
| 1031 | Chungcheong-Jeolla | 忠清・全羅 | KOR | Wuhan | 再編・改名 |
| 1032 | Yan'an | 延安 | XIC | Guayana Esequiba del Sur | 再編・改名 |
| 1033 | Nanlu | 南路 | GXC | Boa Vista | 再編・改名 |
| 1034 | Suzhou | 蘇州 | KMT | Alto Rio Negro | 再編・改名 |
| 1035 | Nanjing | 南京 | KMT | Bougainville Island | 再編・改名 |
| 1036 | Wuhan | 武漢 | KMT | Cabinda | 再編・改名 |
| 1037 | Chongqing | 重慶 | KMT | Swaziland | 再編・改名 |
| 1038 | Jinan | 済南 | BYG | Lesotho | 再編・改名 |
| 1039 | Hebei-Chahar | 河北チャハル | BYG | Socotra | 再編・改名 |
| 1040 | Alxa | アルシャー | XSM | Al-Hasakah | 再編・改名 |
| 1041 | Chengdu | 成都 | KMT | Kengtung | 再編・改名 |
| 1042 | Khotan | ホータン | SIK | Tenasserim | 再編・改名 |
| 1043 | Pailingmiao | パイリンミャオ | MON | Ceuta | 再編・改名 |
| 1044 | Wuwei | 武威 | XSM | Melilla | 再編・改名 |
| 1045 | Guyuan | 固原 | XIC | Epiri i Veriut | 再編・改名 |
| 1046 | Yulin | 楡林 | XIC | Hercegovine | 再編・改名 |
| 1047 | Eupen - Malmedy | キール | GER | Visegrad | 再編・改名 |
| 1048 | Moselgebiet |  | GER | Banja Luka | 再編・改名 |
| 1049 | Prekmurje |  | HUN | Volta | 再編・改名 |
| 1050 | South Jordan |  | SAU | Salamanca | 再編・改名 |
| 1051 | East Jordan |  | SAU | Córdoba | 再編・改名 |
| 1052 | West Euphrates |  | SAU | Asturias | 再編・改名 |
| 1053 | Syrian Desert South |  | IRQ | Valladolid | 再編・改名 |
| 1054 | Szekely Land |  | HUN | País Vasco | 再編・改名 |
| 1055 | Straits Commission Anatolia |  | STC | Guadalajara | 再編・改名 |
| 1056 | Straits Commission Thrace |  | STC | Walvis Bay | 再編・改名 |
| 1057 | Straits Commission Bosphorus | コンスタンティノープル東岸 | STC | Caprivi Strip | 再編・改名 |
| 1058 | Armenian SSR Borderlands |  | RUS | Zeeuws-Vlaanderen | 再編・改名 |
| 1059 | German Syria Cilicia |  | SYR | Gelderland | 再編・改名 |
| 1060 | German Syria Upper Mesopotamia |  | IRQ | Limburg | 再編・改名 |
| 1061 | German Levant Euphrates |  | SAU | Maasdelta | 再編・改名 |
| 1062 | Northern Champagne | シャンパーニュ南部 | FRA | Kleve | 再編・改名 |
| 1063 | Western Ile de France | イル・ド・フランス東部 | FRA | Dytiki Thraki | 再編・改名 |
| 1064 | Eastern Ile de France | イル・ド・フランス南部 | FRA | Gallup | 再編・改名 |
| 1065 | Western Normandy | ノルマンディー東部 | FRA | Pueblo | 再編・改名 |
| 1066 | Savoy Counties | サヴォア | ITA | Fiume | 再編・改名 |
| 1067 | Nice | ニース | ITA | Hanko | 再編・改名 |
| 1068 | Bavarian Imperial State | アルトシュタット | BAY | Porkkalanniemi | 再編・改名 |

## 付録: 削除せず新 localisation へ引き継いだ動的キー

旧 state_names loc には通常の `STATE_<ID>` 以外に以下の動的キーがあり、これらは削除せず新しい `state_names_l_japanese.yml` / `state_names_l_english.yml` の末尾へそのまま引き継いだ (いずれも旧 map の state ID 基準のため、国家セットアップ再構築時に新 ID への読み替えが必要)。

- **owner 別 state 名 `TAG_STATE_<ID>`: 200 キー** — 所有国による表示名の使い分け (例: STATE_6 を BEL「フランデレン」/ GER「フランデアン」/ FRA「フランドル」)
- **スクリプト用動的 state 名: 17 キー** — `28_german_name`「アルザス＝ロレーヌ」、`330_monarchist_name`「ウルガ」/`330_non_monarchist_name`「イヘ・フレー」、ザイール公定名 `*_autenticite_name` 6件 など。2026-06-12 時点で events/・common/ からの参照なし (将来用)
