(this.webpackJsonpreactapp=this.webpackJsonpreactapp||[]).push([[0],{102:function(e,t,n){},127:function(e,t,n){},130:function(e,t,n){},131:function(e,t,n){},133:function(e,t,n){},136:function(e,t,n){"use strict";n.r(t);var r=n(0),c=n.n(r),a=(n(102),n(141)),i=n(142),s=n(143),o=n(160),l=n(145),d=n(146),u=n(147),j=n(148),h=n(149),b=n(150),p=n(161),f=n(151),O=n(152),x=n(153),g=n(154),m=n(36),y=n(4),v=function(){return Object(y.jsx)(a.a,{render:function(e){var t=e.isSideNavExpanded,n=e.onClickSideNavExpand;return Object(y.jsxs)(i.a,{"aria-label":"guiaMe",children:[Object(y.jsx)(s.a,{}),Object(y.jsx)(o.a,{"aria-label":"Open menu",onClick:n,isActive:t}),Object(y.jsx)(l.a,{element:m.b,to:"/",prefix:"AGR",children:"guiaMe"}),Object(y.jsxs)(d.a,{"aria-label":"guiaMe",children:[Object(y.jsx)(u.a,{element:m.b,to:"/room",children:"Room Page"}),Object(y.jsx)(u.a,{element:m.b,to:"/mapdev",children:"Map Editor"}),Object(y.jsx)(u.a,{element:m.b,to:"/stats",children:"Estad\xedsticas"})]}),Object(y.jsx)(j.a,{"aria-label":"Side navigation",expanded:t,isPersistent:!1,children:Object(y.jsx)(h.a,{children:Object(y.jsxs)(b.a,{children:[Object(y.jsx)(u.a,{element:m.b,to:"/room",children:"Room Page"}),Object(y.jsx)(u.a,{element:m.b,to:"/mapdev",children:"Map Editor"}),Object(y.jsx)(u.a,{element:m.b,to:"/stats",children:"Estad\xedsticas"})]})})}),Object(y.jsxs)(p.a,{children:[Object(y.jsx)(f.a,{"aria-label":"Notifications",children:Object(y.jsx)(O.a,{})}),Object(y.jsx)(f.a,{"aria-label":"User Avatar",children:Object(y.jsx)(x.a,{})}),Object(y.jsx)(f.a,{"aria-label":"App Switcher",children:Object(y.jsx)(g.a,{})})]})]})}})},w=n(21),S=n(156),k=n(23),C=n.n(k),R=n(38),N=n(17),T=n.p+"static/media/robot.5e2091c7.png",_=new WebSocket("ws://guiame.ddns.net:8000/ws/robot/R01/");_.onmessage=function(e){var t=JSON.parse(e.data);console.log("RobotSocket Received: ",t)},new WebSocket("ws://guiame.ddns.net:8000/ws/ui/R01/").onmessage=function(e){var t=JSON.parse(e.data);console.log("UISocket Received: ",t)};var E=n(137),B=n(158),P=n(159),I=n(51),H=n.n(I),D=function(){var e=Object(R.a)(C.a.mark((function e(){var t;return C.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,H.a.get("".concat("http://guiame.ddns.net:8000/api/","routes"));case 2:return t=e.sent,e.abrupt("return",t.data);case 4:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}(),W=(n(127),function(e){var t=e.onSubmit,n=e.onChange,r=e.value;return Object(y.jsxs)("div",{className:"room-page__keyboard",children:[Object(y.jsxs)("div",{className:"room-page__keyboard-row",children:[Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"1")},children:"1"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"2")},children:"2"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"3")},children:"3"})]}),Object(y.jsxs)("div",{className:"room-page__keyboard-row",children:[Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"4")},children:"4"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"5")},children:"5"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"6")},children:"6"})]}),Object(y.jsxs)("div",{className:"room-page__keyboard-row",children:[Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"7")},children:"7"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"8")},children:"8"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"9")},children:"9"})]}),Object(y.jsxs)("div",{className:"room-page__keyboard-row",children:[Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n("")},children:"Reset"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return n(r+"0")},children:"0"}),Object(y.jsx)(E.a,{className:"room-page__keyboard-button",onClick:function(){return t()},children:"OK"})]})]})}),A=n(58),F=function(){var e=c.a.useState(""),t=Object(N.a)(e,2),n=t[0],r=t[1],a=c.a.useState(!1),i=Object(N.a)(a,2),s=i[0],o=i[1],l=c.a.useState(!1),d=Object(N.a)(l,2),u=d[0],j=d[1],h=c.a.useState(),b=Object(N.a)(h,2),p=b[0],f=b[1],O=c.a.useState(!1),x=Object(N.a)(O,2),g=x[0],m=x[1],v=c.a.useState(""),w=Object(N.a)(v,2),S=w[0],k=w[1],_=c.a.useState(new WebSocket("ws://guiame.ddns.net:8000/ws/ui/"+"PiCar"+"/")),E=Object(N.a)(_,1)[0];E.onmessage=function(e){var t=JSON.parse(e.data),n=t.message;if(console.log("RoomPage Received: ",t),void 0!==n&&void 0!==n.type)if("next_direction"===n.type){for(var r=0;r<p.route.length;r++)if(p.route[r].includes("CRUCE")){k(p.route[r]);break}}else"finished_route"===n.type&&k("stop")};var I=function(){var e=Object(R.a)(C.a.mark((function e(){var t,r;return C.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,D();case 2:t=e.sent,(r=t.find((function(e){return e.dest_room===n&&"hall"===e.origin_room})))?(console.log("Route:",r),f(r),o(!0)):j(!0);case 5:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return Object(y.jsxs)("div",{className:"room-page",children:[!1,s&&Object(y.jsx)(B.a,{open:s,onRequestClose:function(){return o(!1)},onRequestSubmit:function(){return function(){m(!0),k(p.route[0]);var e={type:"to.robot",message:{type:"start",room:n,route:p}};E.send(JSON.stringify(e)),o(!1)}()},modalHeading:"Confirmar destino",primaryButtonText:"Submit",children:Object(y.jsxs)("div",{children:[Object(y.jsxs)("h1",{children:["Ir a la habitaci\xf3n ",n,"?"]}),Object(y.jsx)("img",{src:"https://i.etsystatic.com/17441626/r/il/362050/1469060776/il_fullxfull.1469060776_e867.jpg",alt:"room"})]})}),Object(y.jsxs)(P.a,{className:"room-page__content",children:[""===n?Object(y.jsx)("h3",{children:"Introduce o n\xfamero da habitaci\xf3n"}):Object(y.jsxs)("h3",{children:["Habitaci\xf3n: ",n]}),u&&Object(y.jsx)("h3",{style:{color:"red"},children:"Non existe a habitaci\xf3n"}),g?Object(y.jsxs)("div",{children:["stop"===S?Object(y.jsxs)(y.Fragment,{children:[Object(y.jsx)("h4",{children:"Has chegado ao destino"}),Object(y.jsx)(A.a,{style:{width:"70%",height:"70%",fill:"green"},onClick:function(){return window.location.reload()}})]}):Object(y.jsxs)("h4",{children:["No pr\xf3ximo cruce: ",Object(y.jsx)("strong",{children:S.split(".")[0]})]}),S.startsWith("recto")&&Object(y.jsx)(A.e,{style:{width:"70%",height:"70%",fill:"green"}}),S.startsWith("derecha")&&Object(y.jsx)(A.d,{style:{width:"70%",height:"70%",fill:"green"}}),S.startsWith("vuelta")&&Object(y.jsx)(A.b,{style:{width:"70%",height:"70%",fill:"green"}}),S.startsWith("izquierda")&&Object(y.jsx)(A.c,{style:{width:"70%",height:"70%",fill:"green"}})]}):Object(y.jsx)(W,{onSubmit:function(){return I()},onChange:function(e){r(e),j(!1)},value:n})]}),Object(y.jsx)("img",{src:T,alt:"robot"})]})},M=n(14),J=n(80),L=n(75),z=n.p+"static/media/background.3b8b1600.png",U=n(25),G=(n(130),{running:!1,currentTime:0,lastTime:0});function q(e,t){switch(t.type){case"reset":return{running:!1,currentTime:0,lastTime:0};case"start":return Object(M.a)(Object(M.a)({},e),{},{running:!0,lastTime:Date.now()});case"stop":return Object(M.a)(Object(M.a)({},e),{},{running:!1});case"tick":return e.running?Object(M.a)(Object(M.a)({},e),{},{currentTime:e.currentTime+(Date.now()-e.lastTime),lastTime:Date.now()}):e;default:return e}}function X(){var e=Object(r.useReducer)(q,G),t=Object(N.a)(e,2),n=t[0],c=t[1],a=function(e){var t=new Date(e),n=t.getHours()+t.getTimezoneOffset()/60,r=t.getMinutes(),c=t.getSeconds(),a=t.getMilliseconds();return n=n.toString().padStart(2,"0"),r=r.toString().padStart(2,"0"),{seconds:c=c.toString().padStart(2,"0"),minutes:r,hours:n,milliseconds:a=a.toString().padStart(3,"0")}}(n.currentTime);return Object(r.useEffect)((function(){var e;return e=requestAnimationFrame((function t(){c({type:"tick"}),e=requestAnimationFrame(t)})),function(){return cancelAnimationFrame(e)}}),[]),Object(y.jsxs)("div",{className:"ppal",children:[Object(y.jsx)("div",{className:"textt",children:" Tempo en ruta : "}),Object(y.jsxs)("span",{className:"timer",id:"timer",children:[a.hours,":",a.minutes,":",a.seconds,".",a.milliseconds]}),Object(y.jsxs)("div",{children:[Object(y.jsxs)("button",{id:"restart",hidden:!0,onClick:function(){return c({type:"reset"})},children:["Reset"," "]}),Object(y.jsxs)("button",{id:"start",hidden:!0,onClick:function(){return c({type:"start"})},children:["start"," "]}),Object(y.jsxs)("button",{id:"stop",hidden:!0,onClick:function(){return c({type:"stop"})},children:["stop"," "]})]})]})}var Y=[],V=function(){var e=c.a.useState("BASE"),t=Object(N.a)(e,2),n=t[0],r=t[1],a=c.a.useState(!1),i=Object(N.a)(a,2),s=i[0],o=i[1],l=c.a.useRef(null),d=c.a.useRef(null),u=c.a.useState(new WebSocket("ws://guiame.ddns.net:8000/ws/dashboard/")),j=Object(N.a)(u,1)[0],h=new window.Image;h.src=z;var b=[],p=[];return j.onmessage=function(e){var t=JSON.parse(e.data);if(console.log("Dashboard Received: ",t),void 0!==t.hall&&(d.current.opacity(1),Y.push(t.hall),r(t.hall)),void 0!==t.active&&t.active&&!s)document.getElementById("restart").click(),document.getElementById("start").click(),o(!0);else if(void 0!==t.active&&!t.active&&s){Y=[],document.getElementById("stop").click();var n=document.getElementById("timer").textContent;b=n.split(":"),p=b[2].split("."),o(!1),r("BASE");var c={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({robot_id:"R01",destiny:t.route.dest_room,minutes:b[1],seconds:p[0],miliseconds:p[1]})};try{fetch("http://guiame.ddns.net:8000/api/stats/",c).then((function(e){e.json()}))}catch(a){console.error(a)}}},c.a.useEffect((function(){if(console.log(d),null!==d.current){var e=new J.a.Animation((function(e){null!==d.current&&d.current.opacity((Math.sin(e.time/300)+1)/2)}),d.current.getLayer());return e.start(),function(){e.stop()}}}),[]),Object(y.jsxs)(y.Fragment,{children:[Object(y.jsx)(X,{id:"crono"}),Object(y.jsx)(U.d,{width:L.stageWidth,height:L.stageHeight,ref:l,children:L.layers.map((function(e,t){return Object(y.jsxs)(U.b,{children:[0===t&&Object(y.jsx)(U.a,{image:h,width:1280,height:720}),e.elements.map((function(e,t){if("Rect"===e.type){var r=!1;return r=(r=!!Y.find((function(t){return e.attrs.id===t})))||e.attrs.id===n,"BASE"===e.attrs.id&&(r=!1),"BASE"===n&&0!==Y.length&&(Y.splice(0,Y.length),Y.splice(0,Y.length)),Object(y.jsx)(U.c,Object(M.a)(Object(M.a)({},e.attrs),{},{fill:!0===r?"green":e.attrs.fill,ref:e.attrs.id===n?d:null}),t)}return"Text"===e.type?Object(y.jsx)(U.e,Object(M.a)({},e.attrs),t):null}))]},t)}))})]})},K=n(48),Q=(n(131),n(157)),Z=n(155),$=function(e){var t=e.shapeProps,n=e.isSelected,r=e.onSelect,a=e.onChange,i=c.a.useRef(),s=c.a.useRef();return c.a.useEffect((function(){n&&(s.current.nodes([i.current]),s.current.getLayer().batchDraw())}),[n]),Object(y.jsxs)(c.a.Fragment,{children:[Object(y.jsx)(U.c,Object(M.a)(Object(M.a)({onClick:r,onTap:r,ref:i},t),{},{draggable:!0,onDragEnd:function(e){a(Object(M.a)(Object(M.a)({},t),{},{x:e.target.x()>0?e.target.x():0,y:e.target.y()>0?e.target.y():0}))},onTransformEnd:function(e){var n=i.current,r=n.scaleX(),c=n.scaleY();n.scaleX(1),n.scaleY(1),a(Object(M.a)(Object(M.a)({},t),{},{x:n.x(),y:n.y(),width:Math.max(5,n.width()*r),height:Math.max(n.height()*c)}))}})),n&&Object(y.jsx)(U.f,{ref:s,boundBoxFunc:function(e,t){return t.width<5||t.height<5?e:t}})]})},ee={type:"Text",x:100,y:100,text:"Hello World",fontSize:16,fill:"black"},te={type:"Rect",x:100,y:100,width:100,height:100,fill:"purple"},ne={type:"Rect",x:100,y:100,width:30,height:100,fill:"black"},re={type:"Rect",x:100,y:100,width:30,height:30,fill:"blue"},ce=function(){var e=c.a.useRef(),t=new window.Image;t.src=z;var n=c.a.useState([]),r=Object(N.a)(n,2),a=r[0],i=r[1],s=c.a.useState(null),o=Object(N.a)(s,2),l=o[0],d=o[1],u=c.a.useState(""),j=Object(N.a)(u,2),h=j[0],b=j[1],p=c.a.useState("blue"),f=Object(N.a)(p,2),O=f[0],x=f[1],g=c.a.useState("vertical"),m=Object(N.a)(g,2),v=m[0],w=m[1];var S=function(){var t=e.current,n=t.children.map((function(e,t){return{layer:"layer"+t,elements:e.children.filter((function(e){return"Transformer"!==e.className})).map((function(e){return"Rect"===e.className?{type:e.className,attrs:{id:e.id(),x:e.x(),y:e.y(),width:e.width(),height:e.height(),fill:e.fill()}}:"Text"===e.className?{type:e.className,attrs:{id:e.id(),x:e.x(),y:e.y(),text:e.text(),fontSize:e.fontSize(),fill:e.fill()}}:null}))}}));!function(e,t){var n="data:text/json;charset=utf-8,"+encodeURIComponent(JSON.stringify(e,null,2)),r=document.createElement("a");r.download=t,r.href=n,document.body.appendChild(r),r.click(),document.body.removeChild(r)}({stageWidth:t.width(),stageHeight:t.height(),layers:n},"stage.json")};function k(e){if("room"===e){var t=Object(M.a)({id:"room"+a.filter((function(e){return e.id.startsWith("room")})).length},te);i([].concat(Object(K.a)(a),[t]))}else if("text"===e){var n=Object(M.a)({id:"text"+a.filter((function(e){return e.id.startsWith("text")})).length},ee);""!==h&&(n.text=h,b("")),i([].concat(Object(K.a)(a),[n]))}else if("hall"===e){var r=Object(M.a)({id:"hall"+a.filter((function(e){return e.id.startsWith("hall")})).length},ne);if("vertical"===v);else{var c=r.width;r.width=r.height,r.height=c}i([].concat(Object(K.a)(a),[r]))}else if("sticker"===e){var s=Object(M.a)({id:"sticker"+a.filter((function(e){return e.id.startsWith("sticker")})).length},re);s.fill=O,i([].concat(Object(K.a)(a),[s]))}}return Object(y.jsxs)("div",{children:[Object(y.jsx)("div",{style:{display:"flex",flexDirection:"row",marginTop:"1rem",textAlign:"center",justifyContent:"space-around"},children:null!==l&&"Rect"===a.find((function(e){return e.id===l})).type?Object(y.jsxs)(y.Fragment,{children:[Object(y.jsxs)("div",{children:[Object(y.jsx)("strong",{children:"Shape ID"})," ",Object(y.jsx)(Q.a,{id:"change-id",labelText:"",placeholder:a.find((function(e){return e.id===l})).id.toString()})]}),Object(y.jsxs)("div",{children:[Object(y.jsx)("strong",{children:"Shape Width"})," ",Object(y.jsx)(Q.a,{id:"change-width",labelText:"",placeholder:a.find((function(e){return e.id===l})).width.toString()})]}),Object(y.jsxs)("div",{children:[Object(y.jsx)("strong",{children:"Shape Height"})," ",Object(y.jsx)(Q.a,{id:"change-height",labelText:"",placeholder:a.find((function(e){return e.id===l})).height.toString()})]}),Object(y.jsxs)("div",{children:[Object(y.jsx)("strong",{children:"Shape X-Position"})," ",Object(y.jsx)(Q.a,{id:"change-x-pos",labelText:"",placeholder:a.find((function(e){return e.id===l})).x.toString()})]}),Object(y.jsxs)("div",{children:[Object(y.jsx)("strong",{children:"Shape Y-Position"})," ",Object(y.jsx)(Q.a,{id:"change-y-pos",labelText:"",placeholder:a.find((function(e){return e.id===l})).y.toString()})]}),Object(y.jsxs)("div",{children:[Object(y.jsx)("strong",{children:"Shape Color"})," ",Object(y.jsx)(Q.a,{id:"change-color",labelText:"",placeholder:a.find((function(e){return e.id===l})).fill})]}),Object(y.jsx)(E.a,{onClick:function(){var e=document.getElementById("change-id").value,t=document.getElementById("change-width").value,n=document.getElementById("change-height").value,r=document.getElementById("change-x-pos").value,c=document.getElementById("change-y-pos").value,s=document.getElementById("change-color").value,o=a.map((function(a){return a.id===l&&(a.id=""!==e?e:a.id,a.width=""!==t?parseInt(t):a.width,a.height=""!==n?parseInt(n):a.height,a.x=""!==r?parseInt(r):a.x,a.y=""!==c?parseInt(c):a.y,a.fill=""!==s?s:a.fill),a}));i(o),d(""!==e?e:l)},style:{marginLeft:"1rem",padding:"1rem"},children:"Save Shape"}),Object(y.jsx)(E.a,{onClick:function(){return d(null)},style:{marginLeft:"10px",padding:"1rem"},children:"Unselect"})]}):Object(y.jsx)(y.Fragment,{})}),Object(y.jsxs)("div",{style:{display:"flex",flexDirection:"row",marginTop:"1rem"},children:[Object(y.jsxs)("div",{style:{display:"flex",flexDirection:"column",marginRight:"1rem"},children:[Object(y.jsx)(E.a,{onClick:function(){return k("room")},style:{margin:"1px"},children:"New Room"}),Object(y.jsx)(E.a,{onClick:function(){return k("hall")},style:{margin:"1px"},children:"New Hall"}),Object(y.jsxs)("div",{children:[Object(y.jsx)(Z.a,{id:"cb-vertical",labelText:"Vertical",onChange:function(){return w("vertical")},checked:"vertical"===v}),Object(y.jsx)(Z.a,{id:"cb-horizontal",labelText:"Horizontal",onChange:function(){return w("horizontal")},checked:"horizontal"===v})]}),Object(y.jsx)(E.a,{onClick:function(){return k("sticker")},style:{margin:"1px"},children:"New Sticker"}),Object(y.jsxs)("div",{children:[Object(y.jsx)(Z.a,{id:"cb-blue",labelText:"Blue",onClick:function(){return x("blue")},checked:"blue"===O}),Object(y.jsx)(Z.a,{id:"cb-red",labelText:"Red",onClick:function(){return x("red")},checked:"red"===O})]}),Object(y.jsx)(E.a,{onClick:function(){return k("text")},style:{margin:"1px"},children:"New Text"}),Object(y.jsx)("div",{children:Object(y.jsx)(Q.a,{id:"text-input",labelText:"",placeholder:"Hello World",onChange:function(e){return b(e.target.value)},value:h})}),Object(y.jsx)(E.a,{onClick:function(){l===a[a.length-1].id&&d(null),i(a.slice(0,a.length-1))},style:{margin:"1px"},children:"Del Last"}),Object(y.jsx)(E.a,{onClick:function(){return S()},style:{margin:"1px"},children:"Export"}),e.current&&Object(y.jsxs)(y.Fragment,{children:[Object(y.jsxs)("div",{children:["Stage width: ",e.current.width()]}),Object(y.jsxs)("div",{children:["Stage height: ",e.current.height()]})]})]}),Object(y.jsx)("div",{style:{border:"1px solid"},children:Object(y.jsxs)(U.d,{width:1280,height:720,ref:e,children:[Object(y.jsxs)(U.b,{children:[Object(y.jsx)(U.a,{image:t,width:1280,height:720}),a.map((function(e,t){var n=l===e.id;return"Rect"===e.type?Object(y.jsx)($,{shapeProps:e,onSelect:function(){l===e.id?d(null):d(e.id)},onChange:function(t){i(a.map((function(n){return n.id===e.id?t:n})))},isSelected:n},e.id):null}))]}),Object(y.jsx)(U.b,{children:a.map((function(e,t){var n=l===e.id;return"Text"===e.type?Object(y.jsx)(U.e,Object(M.a)(Object(M.a)({draggable:!0},e),{},{isSelected:n,onClick:function(){if(l===e.id){var t=["red","black","white"],n=(t.indexOf(e.fill)+1)%t.length;e.fill=t[n],d(null)}else d(e.id)}}),e.id):null}))})]})})]})]})},ae=n(55);n(79);function ie(){var e=Object(r.useState)(!0),t=Object(N.a)(e,2),n=t[0],c=t[1],a=Object(r.useState)([]),i=Object(N.a)(a,2),s=i[0],o=i[1];Object(r.useEffect)((function(){function e(){return(e=Object(R.a)(C.a.mark((function e(){return C.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,H.a.get("http://guiame.ddns.net:8000/api/statsHalls/?format=json").then((function(e){o(e.data),c(!1)}));case 2:case"end":return e.stop()}}),e)})))).apply(this,arguments)}n&&function(){e.apply(this,arguments)}()}),[n]);var l=Object(r.useMemo)((function(){return[{Header:"PASILLO",accessor:"hall"},{Header:"DET\xcdVOSE",accessor:"stopped"}]}),[]),d=Object(ae.useTable)({columns:l,data:s},ae.useSortBy),u=d.getTableProps,j=d.getTableBodyProps,h=d.headerGroups,b=d.rows,p=d.prepareRow;return Object(y.jsx)("div",{className:"container",children:Object(y.jsxs)("table",Object(M.a)(Object(M.a)({},u()),{},{children:[Object(y.jsx)("thead",{children:h.map((function(e){return Object(y.jsx)("tr",Object(M.a)(Object(M.a)({},e.getHeaderGroupProps()),{},{children:e.headers.map((function(e){return Object(y.jsx)("th",Object(M.a)(Object(M.a)({},e.getHeaderProps(e.getSortByToggleProps())),{},{className:e.isSorted?e.isSortedDesc?"desc":"asc":"",children:e.render("Header")}))}))}))}))}),Object(y.jsx)("tbody",Object(M.a)(Object(M.a)({},j()),{},{children:b.map((function(e){return p(e),Object(y.jsx)("tr",Object(M.a)(Object(M.a)({},e.getRowProps()),{},{children:e.cells.map((function(e){return Object(y.jsx)("td",Object(M.a)(Object(M.a)({},e.getCellProps()),{},{children:e.render("Cell")}))}))}))}))}))]}))})}function se(){var e=Object(r.useState)(!0),t=Object(N.a)(e,2),n=t[0],c=t[1],a=Object(r.useState)([]),i=Object(N.a)(a,2),s=i[0],o=i[1];Object(r.useEffect)((function(){function e(){return(e=Object(R.a)(C.a.mark((function e(){return C.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,H.a.get("http://guiame.ddns.net:8000/api/stats/?format=json").then((function(e){o(e.data),c(!1)}));case 2:case"end":return e.stop()}}),e)})))).apply(this,arguments)}n&&function(){e.apply(this,arguments)}()}),[n]);var l=Object(r.useMemo)((function(){return[{Header:"ROBOT",accessor:"robot_id"},{Header:"DESTINO",accessor:"destiny"},{Header:"MINUTOS",accessor:"minutes"},{Header:"SEGUNDOS",accessor:"seconds"},{Header:"MILISEGUNDOS",accessor:"miliseconds"}]}),[]),d=Object(ae.useTable)({columns:l,data:s},ae.useSortBy),u=d.getTableProps,j=d.getTableBodyProps,h=d.headerGroups,b=d.rows,p=d.prepareRow;return Object(y.jsx)("div",{className:"container",children:Object(y.jsxs)("table",Object(M.a)(Object(M.a)({},u()),{},{children:[Object(y.jsx)("thead",{children:h.map((function(e){return Object(y.jsx)("tr",Object(M.a)(Object(M.a)({},e.getHeaderGroupProps()),{},{children:e.headers.map((function(e){return Object(y.jsx)("th",Object(M.a)(Object(M.a)({},e.getHeaderProps(e.getSortByToggleProps())),{},{className:e.isSorted?e.isSortedDesc?"desc":"asc":"",children:e.render("Header")}))}))}))}))}),Object(y.jsx)("tbody",Object(M.a)(Object(M.a)({},j()),{},{children:b.map((function(e){return p(e),Object(y.jsx)("tr",Object(M.a)(Object(M.a)({},e.getRowProps()),{},{children:e.cells.map((function(e){return Object(y.jsx)("td",Object(M.a)(Object(M.a)({},e.getCellProps()),{},{children:e.render("Cell")}))}))}))}))}))]}))})}function oe(){return Object(y.jsxs)(y.Fragment,{children:[Object(y.jsx)("div",{}),Object(y.jsx)("div",{className:"text",children:"Estad\xedsticas das rutas"}),Object(y.jsx)(se,{}),Object(y.jsx)("div",{className:"text",children:"Pasillos noss que se parou debido a obst\xe1culos"}),Object(y.jsx)(ie,{})]})}var le=n.p+"static/media/logo_guiame.447031dc.jpg";var de=function(){return Object(y.jsxs)(y.Fragment,{children:[!window.location.href.includes("room")&&Object(y.jsx)(v,{}),Object(y.jsxs)(S.a,{children:[Object(y.jsx)("div",{className:"room-page__header",children:Object(y.jsx)("h1",{children:Object(y.jsx)("img",{src:le,alt:"descripcion",style:{maxWidth:"100%"}})})}),Object(y.jsxs)(w.c,{children:[Object(y.jsx)(w.a,{exact:!0,path:"/",component:V}),Object(y.jsx)(w.a,{exact:!0,path:"/mapdev",component:ce}),Object(y.jsx)(w.a,{exact:!0,path:"/room",component:F}),Object(y.jsx)(w.a,{exact:!0,path:"/stats",component:oe})]})]})]})},ue=(n(133),n(68)),je=n.n(ue),he=n(96),be=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,162)).then((function(t){var n=t.getCLS,r=t.getFID,c=t.getFCP,a=t.getLCP,i=t.getTTFB;n(e),r(e),c(e),a(e),i(e)}))},pe=n(56),fe=(n(135),n(63)),Oe=function(e){return function(t,n,r){return e((function(e,n){var r,c=performance.now(),a=t(e,n),i=performance.now(),s=(r=i-c,Math.round(100*r)/100);return console.log("Reducer process time:",s),a}),n,r)}},xe=function(e){return function(t){return function(n){console.group(n.type),console.info("Dispatching",n);var r=t(n);return console.log("Next state",e.getState()),console.groupEnd(),r}}},ge=n(82);function me(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1;return new Promise((function(t){return setTimeout((function(){return t({data:e})}),500)}))}var ye=Object(ge.a)("counter/fetchCount",function(){var e=Object(R.a)(C.a.mark((function e(t){var n;return C.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,me(t);case 2:return n=e.sent,e.abrupt("return",n.data);case 4:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()),ve=Object(ge.b)({name:"counter",initialState:{value:0,status:"idle"},reducers:{increment:function(e){e.value+=1},decrement:function(e){e.value-=1},incrementByAmount:function(e,t){e.value+=t.payload}},extraReducers:function(e){e.addCase(ye.pending,(function(e){e.status="loading"})).addCase(ye.fulfilled,(function(e,t){e.status="idle",e.value+=t.payload}))}}),we=ve.actions,Se=(we.increment,we.decrement,we.incrementByAmount,ve.reducer),ke=Object(pe.combineReducers)({counter:Se});var Ce=function(e){var t=[xe,fe.a],n=[pe.applyMiddleware.apply(void 0,t),Oe],r=null;return r=pe.compose.apply(void 0,n),Object(pe.createStore)(ke,e,r)}();je.a.render(Object(y.jsx)(he.a,{store:Ce,children:Object(y.jsx)(m.a,{children:Object(y.jsx)(de,{})})}),document.getElementById("root")),be()},75:function(e){e.exports=JSON.parse('{"stageWidth":1280,"stageHeight":720,"layers":[{"layer":"layer0","elements":[{"type":"Rect","attrs":{"id":"BASE","x":447,"y":531,"width":50,"height":50,"fill":"blue"}},{"type":"Rect","attrs":{"id":"pasillo01","x":455.00000000000006,"y":421,"width":32.00000000000017,"height":108.99999999999964,"fill":"black"}},{"type":"Rect","attrs":{"id":"nodo1","x":455.0000000000001,"y":389.99999999999983,"width":32.000000000000064,"height":31.000000000000043,"fill":"red"}},{"type":"Rect","attrs":{"id":"pasillo12","x":486.99999999999983,"y":389.9999999999986,"width":256.00000000000006,"height":32.99999999999986,"fill":"black"}},{"type":"Rect","attrs":{"id":"nodo2","x":743,"y":390,"width":33,"height":33,"fill":"red"}},{"type":"Rect","attrs":{"id":"pasillo23","x":775.9999999999998,"y":389.9999999152273,"width":351.9999999999998,"height":32.99999974568673,"fill":"black"}},{"type":"Rect","attrs":{"id":"nodo3","x":1128.0000000000002,"y":389.9999754163975,"width":33.50396791794098,"height":33.50396774839885,"fill":"red"}},{"type":"Rect","attrs":{"id":"pasillo14","x":455.0000000000009,"y":258.999986521404,"width":32.00000000000006,"height":130.99999737209774,"fill":"black"}},{"type":"Rect","attrs":{"id":"nodo4","x":455.00000000000006,"y":228.0000000000001,"width":31.999999999999947,"height":31.00000000000005,"fill":"red"}},{"type":"Rect","attrs":{"id":"pasillo15","x":455.0000000000001,"y":180.00000000000003,"width":30.999999999999872,"height":50.00000000000009,"fill":"black"}},{"type":"Rect","attrs":{"id":"nodo5","x":454.9999999999999,"y":149.99999999999994,"width":31.00000000000011,"height":30.999999999999996,"fill":"green"}},{"type":"Rect","attrs":{"id":"pasillo56","x":454.99999999999926,"y":74.99999999999997,"width":31.999999999999847,"height":74.99999999999982,"fill":"black"}},{"type":"Rect","attrs":{"id":"nodo6","x":455.0000000000001,"y":43.999999999999986,"width":32.00000000000008,"height":31.00000000000001,"fill":"red"}},{"type":"Rect","attrs":{"id":"pasillo17","x":339,"y":390.0000000000009,"width":116.00000000000009,"height":31.000000000000032,"fill":"black"}},{"type":"Rect","attrs":{"id":"nodo7","x":307.99999999999994,"y":389.99997541639766,"width":30.999999999999996,"height":30.999999999999844,"fill":"red"}}]},{"layer":"layer1","elements":[]}]}')},79:function(e,t,n){}},[[136,1,2]]]);
//# sourceMappingURL=main.7e513d15.chunk.js.map