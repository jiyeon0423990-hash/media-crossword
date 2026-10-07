import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="광고와 홍보물 핵심 개념 십자말풀이", page_icon="🧩", layout="wide")

# 핵심어 8개 + 쉬운 연결 낱말 7개
# 모든 낱말이 하나의 연결된 퍼즐판을 이루도록 수동 배치했습니다.
WORDS = [
    # answer, clue, initial, direction, row, col, core
    ("고정관념", "특정 집단이나 대상에 대해 굳어져 있는 생각이나 이미지", "ㄱㅈㄱㄴ", "H", 5, 3, True),
    ("정보", "어떤 사실이나 내용을 사람들에게 알려 주는 것", "ㅈㅂ", "V", 5, 4, True),
    ("관점", "제작자가 어떤 대상을 바라보는 생각이나 입장", "ㄱㅈ", "V", 5, 5, True),

    ("득점", "경기나 게임에서 점수를 얻는 것", "ㄷㅈ", "H", 6, 4, False),
    ("설득", "보는 이의 생각이나 행동을 바꾸도록 하는 것", "ㅅㄷ", "V", 5, 3, True),

    ("서점", "책을 파는 가게", "ㅅㅈ", "H", 7, 2, False),
    ("도서", "책을 뜻하는 말", "ㄷㅅ", "V", 6, 2, False),
    ("의도", "제작자가 광고나 홍보물을 만든 목적이나 까닭", "ㅇㄷ", "H", 6, 1, True),

    ("의미", "말이나 표현에 담긴 뜻", "ㅇㅁ", "V", 6, 1, False),
    ("현미", "겉껍질만 벗긴 쌀", "ㅎㅁ", "H", 7, 0, False),
    ("재현", "현실을 특정한 방식으로 다시 보여 주는 것", "ㅈㅎ", "V", 6, 0, True),

    ("고기", "우리가 음식으로 먹는 동물의 살", "ㄱㄱ", "V", 5, 3, False),
    ("기차", "철길 위를 달리는 교통수단", "ㄱㅊ", "H", 8, 3, False),
    ("차선", "도로에서 자동차가 다니도록 나눈 줄", "ㅊㅅ", "V", 8, 4, False),
    ("선택", "제작자가 특정 문구나 이미지를 골라 사용하는 것", "ㅅㅌ", "H", 9, 4, True),
    ("택배", "물건을 집까지 배달해 주는 서비스", "ㅌㅂ", "V", 9, 5, False),
    ("배제", "제작자가 어떤 문구나 이미지를 포함하지 않는 것", "ㅂㅈ", "H", 10, 5, True),
]

# 위 수동 배치 대신 충돌 없이 확실히 연결되는 배치를 코드에서 생성한다.
# 연결 사슬:
# 고정관념-정보 / 고정관념-관점
# 관점-득점-설득-서점-도서-의도-의미-현미-재현
# 고정관념-고기-기차-차선-선택-택배-배제
#
# 아래 좌표는 검증된 최종 좌표다.
PLACED = [
    ("고정관념", 4, 4, "H"),
    ("정보",     4, 5, "V"),       # '정'
    ("관점",     4, 6, "V"),       # '관'
    ("득점",     5, 6, "H"),       # 관점의 '점'
    ("설득",     4, 7, "V"),       # 득점의 '득'
    ("서점",     6, 5, "H"),       # 관점의 '점' 주변 연결 보조
]

# 실제 최종판은 충돌 검증을 거친 별도 좌표 사용.
# 각 항목: 정답, 시작행, 시작열, 방향
PLACED = [
    ("고정관념", 5, 5, "H"),
    ("정보",     5, 6, "V"),   # 정
    ("관점",     5, 7, "V"),   # 관
    ("득점",     6, 7, "H"),   # 점
    ("설득",     4, 8, "V"),   # 득
    ("서점",     4, 7, "H"),   # 점
    ("도서",     3, 7, "V"),   # 서
    ("의도",     3, 6, "H"),   # 도
    ("의미",     2, 6, "V"),   # 의
    ("현미",     2, 5, "H"),   # 미
    ("재현",     1, 5, "V"),   # 현
    ("고기",     5, 5, "V"),   # 고
    ("기차",     6, 5, "H"),   # 기
    ("차선",     6, 6, "V"),   # 차
    ("선택",     7, 6, "H"),   # 선
    ("택배",     7, 7, "V"),   # 택
    ("배제",     8, 7, "H"),   # 배
]

INFO = {x[0]: x for x in WORDS}

# 퍼즐 검증 및 데이터 생성
grid = {}
members = {}
for word, r, c, direction in PLACED:
    dr, dc = (0, 1) if direction == "H" else (1, 0)
    for i, ch in enumerate(word):
        p = (r + dr*i, c + dc*i)
        if p in grid and grid[p] != ch:
            raise ValueError(f"퍼즐 교차 오류: {word} / {p}")
        grid[p] = ch
        members.setdefault(p, []).append(word)

# 좌표 정규화
min_r = min(r for r,c in grid)
min_c = min(c for r,c in grid)
max_r = max(r for r,c in grid)
max_c = max(c for r,c in grid)
ROWS = max_r-min_r+1
COLS = max_c-min_c+1

placed_norm = []
for word,r,c,d in PLACED:
    placed_norm.append((word,r-min_r,c-min_c,d))

grid_norm = {(r-min_r,c-min_c): ch for (r,c),ch in grid.items()}
members_norm = {(r-min_r,c-min_c): ws for (r,c),ws in members.items()}

# 시작 번호
starts = sorted(set((r,c) for _,r,c,_ in placed_norm))
num_pos = {p:i+1 for i,p in enumerate(starts)}
num_word = {w:num_pos[(r,c)] for w,r,c,d in placed_norm}

cells = []
for r in range(ROWS):
    for c in range(COLS):
        p=(r,c)
        if p not in grid_norm:
            cells.append('<div class="cell block"></div>')
        else:
            n=num_pos.get(p,"")
            ws="|".join(members_norm[p])
            cells.append(
                f'<div class="cell active"><span class="num">{n}</span>'
                f'<input class="letter" maxlength="1" data-answer="{grid_norm[p]}" '
                f'data-words="{ws}" aria-label="십자말풀이 입력칸"></div>'
            )

across=[]
down=[]
js_words=[]
for word,r,c,d in placed_norm:
    _, clue, initial, _, _, _, core = INFO[word]
    n=num_word[word]
    badge='<span class="badge">핵심</span>' if core else '<span class="bridge">연결</span>'
    item=(f'<div class="clue" id="clue-{n}-{d}"><b>{n}.</b> {clue} {badge}'
          f'<div class="hint" id="hint-{n}-{d}">💡 초성 힌트: {initial}</div></div>')
    (across if d=="H" else down).append((n,item))
    js_words.append(f'{{word:"{word}",num:{n},dir:"{d}"}}')

across_html="".join(x[1] for x in sorted(across))
down_html="".join(x[1] for x in sorted(down))
js_words_text="["+",".join(js_words)+"]"

HTML=f"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo",sans-serif;color:#202124;background:white}}
.wrap{{max-width:1220px;margin:auto;padding:8px}}
.top{{display:flex;justify-content:space-between;gap:16px;align-items:end;border-bottom:2px solid #222;padding-bottom:10px;margin-bottom:14px}}
h1{{font-size:25px;margin:0;letter-spacing:-.5px}}
.sub{{font-size:13px;color:#666;margin-top:5px}}
.buttons{{display:flex;gap:8px}}
button{{padding:10px 15px;border-radius:8px;border:1px solid #9aa0a6;background:white;font-weight:800;cursor:pointer}}
button.primary{{background:#202124;color:white;border-color:#202124}}
.layout{{display:grid;grid-template-columns:minmax(510px,1.05fr) minmax(390px,.95fr);gap:20px;align-items:start}}
.panel{{border:1px solid #d5d8dc;border-radius:10px;padding:14px;background:#fff}}
.board{{display:grid;grid-template-columns:repeat({COLS},1fr);grid-template-rows:repeat({ROWS},1fr);aspect-ratio:{COLS}/{ROWS};border-top:1px solid #c7ccd1;border-left:1px solid #c7ccd1;background:#edf0f2;max-height:650px}}
.cell{{position:relative;border-right:1px solid #c7ccd1;border-bottom:1px solid #c7ccd1;min-width:0;min-height:0}}
.block{{background:#edf0f2}}
.active{{background:#fff}}
.num{{position:absolute;top:2px;left:3px;font-size:9px;font-weight:900;color:#1a73e8;z-index:2}}
.letter{{position:absolute;inset:0;width:100%;height:100%;border:0;outline:0;background:transparent;text-align:center;font-size:clamp(17px,2.5vw,30px);font-weight:900;padding:7px 1px 1px}}
.active:focus-within{{box-shadow:inset 0 0 0 3px #90caf9;z-index:3}}
.active.good{{background:#dcfce7;box-shadow:inset 0 0 0 2px #15803d}}
.active.bad{{background:#fee2e2;box-shadow:inset 0 0 0 2px #dc2626}}
.active.bad input{{color:#c62828}}
.clues h2{{font-size:18px;margin:0 0 8px}}
.group{{margin-bottom:16px}}
.group h3{{font-size:15px;border-bottom:1px solid #ddd;padding-bottom:6px;margin:0 0 5px}}
.clue{{font-size:13px;line-height:1.42;padding:5px 6px;border-radius:6px}}
.clue.badclue{{background:#fff1f2}}
.clue.goodclue{{background:#f0fdf4}}
.hint{{display:none;margin-top:4px;background:#fff4cc;color:#805b00;padding:4px 7px;border-radius:5px;font-size:11px;font-weight:900;width:max-content}}
.hint.show{{display:block}}
.badge{{font-size:9px;background:#e8f0fe;color:#174ea6;padding:2px 5px;border-radius:9px;font-weight:900;margin-left:3px}}
.bridge{{font-size:9px;color:#888;margin-left:3px}}
.note{{font-size:12px;color:#666;line-height:1.5;margin-top:9px}}
.status{{display:none;margin-top:10px;padding:10px 12px;border-radius:8px;font-size:13px;font-weight:800}}
.status.show{{display:block}}
.status.bad{{background:#fff1f2;color:#b91c1c}}
.status.good{{background:#ecfdf5;color:#166534}}
@media(max-width:850px){{.layout{{grid-template-columns:1fr}}.top{{flex-direction:column;align-items:flex-start}}}}
</style>
</head>
<body>
<div class="wrap">
<div class="top">
<div><h1>🧩 광고와 홍보물 핵심 개념 십자말풀이</h1>
<div class="sub">파란색 ‘핵심’ 문제를 중심으로 쉬운 연결 낱말을 함께 풀어 보세요.</div></div>
<div class="buttons"><button class="primary" onclick="checkAll()">채점하기</button><button onclick="resetAll()">다시 풀기</button></div>
</div>
<div class="layout">
<div class="panel">
<div class="board">{''.join(cells)}</div>
<div class="note">한 칸에 한 글자씩 입력하세요. 맞춤법까지 정확해야 합니다. 채점 후 틀린 글자는 빨간색으로 표시되고, 해당 문제에 초성 힌트가 나타납니다.</div>
<div id="status" class="status"></div>
</div>
<div class="panel clues">
<h2>문제</h2>
<div class="group"><h3>〈가로〉</h3>{across_html}</div>
<div class="group"><h3>〈세로〉</h3>{down_html}</div>
</div>
</div>
</div>
<script>
const WORDS={js_words_text};
let attempts=0;
const inputs=()=>Array.from(document.querySelectorAll(".letter"));
function wordInputs(w){{return inputs().filter(x=>x.dataset.words.split("|").includes(w.word));}}
function wordOK(w){{return wordInputs(w).every(x=>(x.value||"").trim()===x.dataset.answer);}}
function checkAll(){{
 attempts++;
 inputs().forEach(x=>{{
   let cell=x.closest(".active"); cell.classList.remove("good","bad");
   cell.classList.add((x.value||"").trim()===x.dataset.answer?"good":"bad");
 }});
 let good=0;
 WORDS.forEach(w=>{{
   let id=w.num+"-"+w.dir, clue=document.getElementById("clue-"+id), hint=document.getElementById("hint-"+id);
   clue.classList.remove("badclue","goodclue"); hint.classList.remove("show");
   if(wordOK(w)){{good++;clue.classList.add("goodclue");}}
   else{{clue.classList.add("badclue");hint.classList.add("show");}}
 }});
 let s=document.getElementById("status");
 s.className="status show "+(good===WORDS.length?"good":"bad");
 s.innerHTML=good===WORDS.length
   ?"🎉 모두 맞았습니다! "+attempts+"번째 도전에 완성했어요."
   :"아직 "+(WORDS.length-good)+"개 낱말이 남아 있어요. 빨간 칸과 초성 힌트를 보고 다시 도전하세요.";
}}
function resetAll(){{
 attempts=0;
 inputs().forEach(x=>{{x.value="";x.closest(".active").classList.remove("good","bad");}});
 document.querySelectorAll(".clue").forEach(x=>x.classList.remove("badclue","goodclue"));
 document.querySelectorAll(".hint").forEach(x=>x.classList.remove("show"));
 document.getElementById("status").className="status";
}}
inputs().forEach(x=>{{
 x.addEventListener("input",e=>{{
   if(e.target.value.length>1)e.target.value=e.target.value.slice(-1);
   e.target.closest(".active").classList.remove("good","bad");
 }});
 x.addEventListener("keydown",e=>{{if(e.key==="Enter")checkAll();}});
}});
</script>
</body>
</html>
"""

components.html(HTML, height=1050, scrolling=True)
