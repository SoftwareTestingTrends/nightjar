import json
def el(t,id,at,**k): d={"type":t,"id":id,"at":at}; d.update(k); return d
def box(id,text,at,**k): return el("box",id,at,text=text,**k)
def txt(id,text,at,**k): return el("text",id,at,text=text,**k)
def ico(id,name,label,at,**k): return el("icon",id,at,name=name,label=label,**k)
def arr(id,f,t,at,**k): return el("arrow",id,at,**{"from":f,"to":t},**k)
def ann(kind,id,target,at,**k): return el(kind,id,at,target=target,**k)
def torque(id,pose,at,h=420,wave=False,**k): return el("custom",id,at,component="custom/Torque.tsx",props={"pose":pose,"height":h,"wave":wave},size=[round(h*400/440)+40,h+20],**k)
def grp(id,layout,children,**k): d={"type":"group","id":id,"layout":layout,"children":children}; d.update(k); return d
R=lambda id,g=100: {"rightOf":id,"gap":g}
B=lambda id,g=100: {"below":id,"gap":g}
beats=[]
beats.append({"id":"b1","board":"title","add":[el("custom","tt","b1:welcome",component="custom/TorqueTitle.tsx",props={"eyebrow":"COURSE INTRODUCTION","title":"Who Tests the Tests?"},size=[1800,330],pos=[3000,1500]),el("custom","ts","b1:quality",component="custom/TorqueTitle.tsx",props={"subtitle":"Quality Engineering in the AI-Native SDLC"},size=[1800,100],place={"below":"tt","gap":30}),torque("t1","happy","b1:welcome",h=520,wave=True,place={"leftOf":"tt","gap":80})],"camera":[{"at":"b1:start","focus":["tt","ts","t1"],"duration":0.5},{"at":"b1:native+0.4s","focus":["tt","t1"],"duration":3}]})
# b2: agents write fast, checking piles up
beats.append({"id":"b2","board":"problem","add":[
  ico("ia","ai","agents write code","b2:agents",color="flow",pos=[2400,1300]),
  txt("wf","fast","b2:fast",color="flow",place=B("ia",60)),
  ico("it","tester_shield","checking it","b2:checking",place=R("ia",300)),
  arr("wc","ia","it","b2:right"),
  txt("cf","no faster","b2:faster",color="warn",place=B("it",60)),
  el("stack","pile","b2:piles",items=["PR waiting for review","PR waiting for review","PR waiting for review","PR waiting for review"],color="warn",place=B("cf",80)),
 ],"camera":[{"at":"b2:start","focus":["ia","it"]},{"at":"b2:piles","focus":["ia","it","pile"]}]})
# b3: who it's for
beats.append({"id":"b3","board":"who","add":[
  ico("you","tester_shield","you know testing","b3:testers",color="group",pos=[2880,1200]),
  ico("k1","ai","agents","b3:agents"),
  ico("k2","tool","harnesses","b3:harnesses"),
  ico("k3","score","evals","b3:evaluations"),
  grp("gk","row",["k1","k2","k3"],gap=200,place=B("you",200)),
  txt("bu","built up from the start","b3:builds",color="flow",place=B("gk",100)),
 ],"camera":[{"at":"b3:start","focus":["you"]},{"at":"b3:agents","focus":["you","gk","bu"]}]})
# b4: real app capture
beats.append({"id":"b4","screen":{"kind":"capture","src":"captures/nightjar-home.png","regions":{"nudge":[352,210,1216,195],"nudgetime":[375,232,470,52],"usual":[375,345,360,40]}},
 "camera":[{"at":"b4:diary","zoomTo":"nudge","duration":0.9}],
 "add":[ann("circle","c-usual","usual","b4:bedtime"),ann("highlight","h-nudge","nudgetime","b4:nudge")]})
# b5: the coach and three risks, with icons
beats.append({"id":"b5","board":"why","add":[
  box("app","NightJar + an AI sleep coach","b5:coach",size="lg",color="flow",pos=[2880,1150]),
  ico("r1","elsewhere","clocks that change","b5:clocks",color="warn"),
  ico("r2","firstaid","no health claims","b5:health",color="warn"),
  ico("r3","language","a different answer every time","b5:differently",color="warn"),
  grp("gr","row",["r1","r2","r3"],gap=260,place=B("app",200)),
  torque("t5a","sleepy","b5:coach",h=380,place={"leftOf":"app","gap":120}),
 ],"camera":[{"at":"b5:start","focus":["app","t5a"]},{"at":"b5:bugs","focus":["app","gr","t5a"]}]})
# b6: a real recorded run, with the real gap circled
beats.append({"id":"b6","screen":{"kind":"terminal","title":"a recorded agent run · the capstone build","lines":[
   {"text":"NIGHTJAR_LOCK_TESTS=1 claude -p \"Build the wind-down lead time…\"","kind":"cmd","at":"b6:runs"},
   {"text":"I didn't edit any test files, and nothing is committed.","kind":"out","at":"b6:record"},
   {"text":"make test: 122 passed, 2 deselected in 2.17s","kind":"out","at":"b6:specs"},
   {"text":"make lint: All checks passed!","kind":"out","at":"b6:tests"},
   {"text":"make evals: 8/8 cases at or above 100% pass rate","kind":"out","at":"b6:code"},
   {"text":"This was 66 passed before the committed lead-time tests.","kind":"out","at":"b6:nightjar"},
 ]},
 "add":[ann("circle","c66","line:6","b6:gap"),
        {"type":"note","id":"n66","text":"it was 68: a real slip a reviewer caught","at":"b6:happened","place":{"below":"line:6","gap":60},"color":"warn"},
        {"type":"note","id":"nfic","text":"the company and its people are fictional","at":"b6:company","place":{"below":"line:6","gap":170},"color":"aside"}]})
# b7-b8: the chain with icons, checks below
steps=[("need","target","business need","b7:need"),("spec","statement","spec","b7:spec"),("plan","planning","plan","b7:plan"),
       ("tests","sanity","tests","b7:tests"),("code","whitebox","code","b7:code"),("merge","branch","merged commit","b7:commit")]
add=[txt("nt","the bedtime nudge, followed in the capstone","b7:nudge",color="group",pos=[2880,1050])]
for i,(id,icon,label,at) in enumerate(steps):
  d=ico(id,icon,label,at,color="flow" if id=="merge" else "ink")
  if i==0: d["pos"]=[1500,1400]
  else: d["place"]=R(steps[i-1][0],200)
  add.append(d)
  if i: add.append(arr("a"+id,steps[i-1][0],id,at))
beats.append({"id":"b7","board":"main","add":add,"camera":[{"at":"b7:start","focus":["nt","need","plan"]},{"at":"b7:tests","focus":["nt","need","merge"]}]})
checks=[("ck1","spec","decisions routed","b8:agent",80),("ck2","plan","tests moved first","b8:writing",200),("ck3","tests","fail for the right reason","b8:design",80),("ck4","code","tests locked","b8:check",200),("ck5","merge","a gate with an owner","b8:trust",80)]
b8=[txt(c,t,at,color="group",place=B(s,g)) for c,s,t,at,g in checks]
beats.append({"id":"b8","board":"main","add":b8,"camera":[{"at":"b8:start","focus":["nt","need","merge","ck2"]}]})
# b9-b11: the map as six icons
parts=[("p1","ai","Foundations: what changed","b9:changed"),("p2","statement","From need to spec","b9:spec"),("p3","tester_shield","Testing agent-written work","b9:testing"),
       ("p4","score","Evals","b10:evaluations"),("p5","permissions","Gates, review and security","b10:gates"),("p6","pulse","Running it, and the tester's job","b11:part")]
pos={"p1":[2110,1300],"p2":[2880,1300],"p3":[3650,1300],"p4":[2110,1760],"p5":[2880,1760],"p6":[3650,1760]}
pb={"b9":[],"b10":[],"b11":[]}
for id,icon,label,at in parts: pb[at.split(":")[0]].append(ico(id,icon,label,at,pos=pos[id]))
pb["b9"].insert(0,txt("six","six parts","b9:six",color="group",pos=[2880,950]))
beats.append({"id":"b9","board":"map","hold":True,"add":pb["b9"],"camera":[{"at":"b9:start","focus":["six","p1","p3","p4","p6"]}]})
beats.append({"id":"b10","board":"map","hold":True,"add":pb["b10"]})
beats.append({"id":"b11","board":"map","hold":True,"add":pb["b11"]})
# b12: each lesson
L=[("l1","execute","a short video","b12:video"),("l2","cheatsheet","a written lesson","b12:written"),("l3","whitebox","a try-it","b12:try-it"),("l4","guessing","recap questions","b12:recap")]
add=[txt("eh","each lesson","b12:each",color="group",pos=[2880,1150])]+[ico(i,n,l,a) for i,n,l,a in L]
add.append(grp("gl","row",["l1","l2","l3","l4"],gap=220,place=B("eh",160)))
beats.append({"id":"b12","board":"lesson","add":add,"camera":[{"at":"b12:start","focus":["eh","gl"]}]})
# b13: what you need
N=[("n1","whitebox","a terminal","b13:terminal"),("n2","branch","git","b13:git"),("n3","tool","uv: about 15 minutes to set up","b13:fifteen"),("n4","ai","a coding agent","b13:exercises")]
add=[txt("nh","what you need","b13:need",color="group",pos=[2880,1150])]+[ico(i,n,l,a) for i,n,l,a in N]
add.append(grp("gn","row",["n1","n2","n3","n4"],gap=220,place=B("nh",160)))
add.append(txt("any","shown with Claude Code; the ideas work with any agent","b13:videos",color="flow",place=B("gn",120)))
beats.append({"id":"b13","board":"need","add":add,"camera":[{"at":"b13:start","focus":["nh","gn","any"]}],"hold":True})
beats.append({"id":"b14","board":"start","add":[
  txt("sh","start here","b14:start#1",color="group",pos=[2880,1150]),
  box("s1","Code got cheap. Checking it didn't.","b14:first",size="lg",color="flow",place=B("sh",60)),
  box("s2","Meet NightJar","b14:meet",place=B("s1",120)),
  arr("sa","s1","s2","b14:then"),
 ],"camera":[{"at":"b14:start","focus":["sh","s1","s2"]}]})
v={"meta":{"slug":"01-course-intro","title":"Who Tests the Tests?","mode":"concept","targets":["stream"],"course":{"title":"Who Tests the Tests?","lesson":1,"next":"Code got cheap. Checking it didn't."}},"beats":beats}
json.dump(v,open("/Users/you/ai-projects/video-generator-ai/courses/ai-native-sdlc/lessons/01-course-intro/video.json","w"),indent=1,ensure_ascii=False)
