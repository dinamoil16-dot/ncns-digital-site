/* NCNS Growth OS · client-side interactive demo
   All data in this file is synthetic. No external services, storage or tracking. */
(function () {
  "use strict";
  const DATA = {
    current: {
      organic: { leads: 100, qualified: 34, won: 8, revenue: 12720, spend: 950 },
      paid: { leads: 90, qualified: 26, won: 6, revenue: 9540, spend: 5050 },
      referral: { leads: 40, qualified: 19, won: 5, revenue: 7950, spend: 350 },
      outbound: { leads: 58, qualified: 7, won: 1, revenue: 1590, spend: 1250 }
    },
    previous: {
      organic: { leads: 82, qualified: 26, won: 6, revenue: 9600, spend: 950 },
      paid: { leads: 77, qualified: 20, won: 4, revenue: 6400, spend: 4680 },
      referral: { leads: 34, qualified: 15, won: 3, revenue: 4800, spend: 300 },
      outbound: { leads: 43, qualified: 7, won: 1, revenue: 1200, spend: 970 }
    },
    quarter: {
      organic: { leads: 351, qualified: 118, won: 30, revenue: 48000, spend: 3200 },
      paid: { leads: 308, qualified: 89, won: 20, revenue: 31800, spend: 17400 },
      referral: { leads: 143, qualified: 66, won: 17, revenue: 27000, spend: 1100 },
      outbound: { leads: 178, qualified: 29, won: 4, revenue: 5800, spend: 2900 }
    }
  };
  const labels = {organic:"Organic search",paid:"Paid campaigns",referral:"Referrals",outbound:"B2B outreach"};
  const periodLabels={current:"This month",previous:"Previous month",quarter:"This quarter"};
  const currency = new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",maximumFractionDigits:0});
  const number = new Intl.NumberFormat("en-US",{maximumFractionDigits:0});
  const dollar = v => currency.format(v);
  const pct = v => (v*100).toFixed(1)+"%";
  const $ = id => document.getElementById(id);
  const state = {period:"current",channel:"all"};
  const initialOpportunities = [
    {id:"DEMO-101",name:"Sample Atelier A",source:"Organic search",stage:"New",due:-2,done:false,policy:"Allowed"},
    {id:"DEMO-102",name:"Sample Engineering B",source:"Paid campaigns",stage:"Qualification",due:0,done:false,policy:"Allowed"},
    {id:"DEMO-103",name:"Sample Services C",source:"Referrals",stage:"Proposal",due:2,done:false,policy:"Allowed"},
    {id:"DEMO-104",name:"Sample Supply D",source:"B2B outreach",stage:"Qualification",due:-1,done:false,policy:"Opted out"},
    {id:"DEMO-105",name:"Sample Studio E",source:"Organic search",stage:"Won",due:0,done:true,policy:"Allowed"}
  ];
  let opportunities=initialOpportunities.map(x=>({...x}));
  let flowStage=0;
  function renderFlow(){
    const d=selected();$("flowLeads").textContent=number.format(d.leads);$("flowQualified").textContent=number.format(d.qualified);$("flowWon").textContent=number.format(d.won);
    const details=["ACQUIRE — "+(state.channel==="all"?"All sample channels":labels[state.channel])+": "+d.leads+" enquiries. Before connecting real sources, agree attribution and permission rules.","QUALIFY — "+d.qualified+" of "+d.leads+" sample enquiries meet the fictional definition ("+pct(percent(d.qualified,d.leads))+"). A real team must agree the qualification criteria.","SELL — "+d.won+" won / "+d.qualified+" qualified ("+pct(percent(d.won,d.qualified))+"). Inspect the separate operator queue for permitted next actions; no messages are sent.","IMPROVE — Export an action plan with assumptions and next experiments. Sample sales revenue is not net profit, and a forecast is not a result."];
    $("flowDetail").textContent=details[flowStage];
    const target=$("flowTarget");target.href=["#overview","#overview","#pipeline","#plan"][flowStage];target.textContent=["Inspect acquisition","Inspect qualification","Open operator queue","Open action plan"][flowStage];
    document.querySelectorAll("[data-flow]").forEach((b,i)=>b.setAttribute("aria-pressed",String(i===flowStage)));
  }
  function selected() {
    const values=state.channel==="all" ? Object.values(DATA[state.period]) : [DATA[state.period][state.channel]];
    return values.reduce((a,x)=>({leads:a.leads+x.leads,qualified:a.qualified+x.qualified,won:a.won+x.won,revenue:a.revenue+x.revenue,spend:a.spend+x.spend}),{leads:0,qualified:0,won:0,revenue:0,spend:0});
  }
  function percent(n,d){return d===0?0:n/d;}
  function make(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e;}
  function renderMetrics() {
    const d=selected();
    $("kpiLeads").textContent=number.format(d.leads);
    $("kpiQualified").textContent=number.format(d.qualified);
    $("kpiWon").textContent=number.format(d.won);
    $("kpiRevenue").textContent=dollar(d.revenue);
    $("kpiQualification").textContent=pct(percent(d.qualified,d.leads))+" qualified from incoming";
    $("kpiClose").textContent=pct(percent(d.won,d.qualified))+" of qualified leads closed";
    const bar=$("funnel");bar.replaceChildren();
    [["Incoming leads",d.leads,"100%"],["Qualified",d.qualified,pct(percent(d.qualified,d.leads))],["Won",d.won,pct(percent(d.won,d.leads))]].forEach(a=>{
      const row=make("div","funnel-step"), label=make("span","",a[0]),track=make("div","track"),fill=make("div","fill"),total=make("strong","",number.format(a[1]));
      fill.style.width=String(percent(a[1],d.leads)*100)+"%";
      track.appendChild(fill);row.append(label,track,total);bar.appendChild(row);
    });
    renderInsights(d);renderScenario();renderActions();renderFlow();
  }
  function dueCount(){return opportunities.filter(x=>!x.done && x.due<=0 && x.policy==="Allowed" && x.stage!=="Won" && x.stage!=="Lost").length;}
  function renderInsights(d){
    const list=$("insights");list.replaceChildren();
    const messages=[];
    if(d.leads>0 && d.qualified/d.leads<.32) messages.push(["Qualification gap","A substantial share of sample enquiries lacks qualification. Test clearer entry forms and a human-reviewed lead score."]);
    else messages.push(["Lead quality checkpoint","Qualification is a useful early signal. Verify whether your definition correlates with actual signed customers."]);
    if(d.qualified>0 && d.won/d.qualified<.24)messages.push(["Sales handoff","Review response times, quote quality and stage-specific follow-ups before buying more traffic."]);
    else messages.push(["Sales consistency","Compare won deals across channels before making budget decisions."]);
    if(d.spend>0)messages.push(["Acquisition efficiency","Illustrative media and sourcing spend: "+dollar(d.spend)+". Attribution does not establish incremental impact or net profit."]);
    const due=dueCount();messages.push(["Operator workload",due+" fictional, permitted follow-up"+(due===1?" is":"s are")+" due or overdue in the separate mini-pipeline."]);
    messages.forEach((m,i)=>{
      const item=make("div","insight"),marker=make("span","mark","0"+(i+1)),content=make("div"),title=make("h4","",m[0]),desc=make("p","",m[1]);
      content.append(title,desc);item.append(marker,content);list.appendChild(item);
    });
  }
  function relativeDate(n){
    const d=new Date();d.setHours(12,0,0,0);d.setDate(d.getDate()+n);
    return new Intl.DateTimeFormat("en-US",{month:"short",day:"numeric"}).format(d);
  }
  function renderPipeline(){
    const table=$("leadRows");table.replaceChildren();
    opportunities.forEach(item=>{
      const tr=document.createElement("tr");
      const name=make("td","",item.name);name.appendChild(make("small","",item.id));
      const channel=make("td","",item.source);
      const stage=make("td");
      const selector=document.createElement("select");selector.setAttribute("aria-label","Stage for "+item.name);
      ["New","Qualification","Proposal","Won","Lost"].forEach(s=>{const opt=document.createElement("option");opt.value=s;opt.textContent=s;selector.appendChild(opt);});
      selector.value=item.stage;selector.addEventListener("change",()=>{item.stage=selector.value; if(item.stage==="Won"||item.stage==="Lost")item.done=true;else item.done=false;renderPipeline();document.querySelector('[aria-label="Stage for '+item.name+'"]').focus();$("pipelineStatus").textContent=item.name+": "+item.stage;renderInsights(selected());renderActions();});
      stage.appendChild(selector);
      const due=make("td");
      const active=!item.done && item.stage!=="Won" && item.stage!=="Lost";
      const msg=item.done?"Completed / closed":item.due<0?"Overdue · "+relativeDate(item.due):item.due===0?"Due today": "Due "+relativeDate(item.due);
      due.appendChild(make("span","due"+(active&&item.due<0?" overdue":""),msg));
      if(active&&item.policy==="Allowed"){
        const done=make("button","tiny-button","Mark completed");done.type="button";done.setAttribute("aria-label","Mark follow-up completed for "+item.name);
        done.addEventListener("click",()=>{item.done=true;renderPipeline();$("resetPipeline").focus();$("pipelineStatus").textContent="Local follow-up marked completed. No message sent.";renderInsights(selected());renderActions();});due.appendChild(done);
      }
      const policy=make("td");policy.appendChild(make("span","policy"+(item.policy!=="Allowed"?" optout":""),item.policy==="Allowed"?"Contact permitted (sample)":"Do not contact"));
      tr.append(name,channel,stage,due,policy);table.appendChild(tr);
    });
    const due=dueCount();$("followupCount").textContent=String(due)+" actionable follow-up"+(due===1?"":"s");
  }
  function inputNumber(id){return Number($(id).value);}
  function renderScenario() {
    const d=selected(),q=inputNumber("qualifiedRate")/100,c=inputNumber("closeRate")/100,av=inputNumber("dealValue"),margin=inputNumber("marginRate")/100;
    const expectedQualified=d.leads*q,expectedWon=expectedQualified*c,forecast=expectedWon*av,contribution=forecast*margin-d.spend;
    $("qualifiedValue").textContent=number.format(q*100)+"%";$("closeValue").textContent=number.format(c*100)+"%";
    $("dealValueOutput").textContent=dollar(av);$("marginValue").textContent=number.format(margin*100)+"%";
    $("forecastRevenue").textContent=dollar(forecast);$("forecastWon").textContent=expectedWon.toFixed(1);
    $("forecastContribution").textContent=dollar(contribution);
    $("scenarioFormula").textContent=number.format(d.leads)+" sample leads × "+number.format(q*100)+"% qualification × "+number.format(c*100)+"% close × "+dollar(av)+" average revenue = "+dollar(forecast)+". Estimated contribution = revenue × "+number.format(margin*100)+"% gross margin − "+dollar(d.spend)+" acquisition spend.";
  }
  function recommended(){
    const d=selected(),qualifiedRate=percent(d.qualified,d.leads),closeRate=percent(d.won,d.qualified);
    const actions=[];
    if(qualifiedRate<.32)actions.push("BUILD — Review lead-source quality and improve qualification fields before buying more traffic.");
    else actions.push("BUILD — Connect qualified-lead definitions and channel attribution to the real CRM.");
    if(closeRate<.24)actions.push("OPERATE — Audit quote turnaround and stage-level loss reasons; add a manager-reviewed follow-up queue.");
    else actions.push("OPERATE — Track response time, opportunity ownership and sales-stage hygiene weekly.");
    if(dueCount()>0)actions.push("OPERATE — Resolve "+dueCount()+" permitted due/overdue fictional follow-up task(s); honor all opt-outs.");
    actions.push("GROW — Test one targeted landing-page or channel hypothesis, with a real baseline and a defined success metric.");
    actions.push("GROW — Review gross margin and actual customer acquisition cost before concluding whether extra sales are profitable.");
    return actions;
  }
  function renderActions(){
    const root=$("actions");root.replaceChildren();
    recommended().forEach(a=>root.appendChild(make("li","",a)));
  }
  function getPlan(){
    const d=selected();
    return [
      "NCNS GROWTH OS — SAMPLE ACTION PLAN / FICTIONAL DATA",
      "Reporting window: "+periodLabels[state.period],
      "Channel: "+(state.channel==="all"?"All channels":labels[state.channel]),
      "Incoming leads: "+d.leads+" | Qualified: "+d.qualified+" | Won: "+d.won,
      "Sample sales revenue: "+dollar(d.revenue)+" | Sample acquisition spend: "+dollar(d.spend),
      "Illustrative scenario: "+$("scenarioFormula").textContent,
      "Note: contribution is not net profit. Forecasts use fictional adjustable assumptions.",
      "",
      ...recommended().map((a,i)=>String(i+1)+". "+a),
      "",
      "Next: assess real business process, connect consented data, agree on scope and measurements.",
      "No customer results, real contacts, API transmissions or ROI guarantees are represented here."
    ].join("\n");
  }
  function setupControls() {
    document.body.classList.add("enhanced");
    document.querySelectorAll("[data-flow]").forEach(b=>b.addEventListener("click",()=>{flowStage=Number(b.dataset.flow);renderFlow();}));
    const motion=window.matchMedia("(prefers-reduced-motion: reduce)");
    let paused=motion.matches;
    const updateMotion=()=>{document.body.classList.toggle("flow-paused",paused);$("pauseFlow").textContent=paused?"Resume flow motion":"Pause flow motion";$("pauseFlow").setAttribute("aria-pressed",String(paused));};
    motion.addEventListener("change",()=>{paused=motion.matches;updateMotion();});
    $("pauseFlow").addEventListener("click",()=>{paused=!paused;updateMotion();});updateMotion();
    $("resetPipeline").addEventListener("click",()=>{opportunities=initialOpportunities.map(x=>({...x}));renderPipeline();renderInsights(selected());renderActions();$("pipelineStatus").textContent="Fictional queue reset. No data sent.";});
    $("period").addEventListener("change",e=>{state.period=e.target.value;renderMetrics();});
    $("channel").addEventListener("change",e=>{state.channel=e.target.value;renderMetrics();});
    ["qualifiedRate","closeRate","dealValue","marginRate"].forEach(id=>$(id).addEventListener("input",renderScenario));
    $("resetScenario").addEventListener("click",()=>{["qualifiedRate","closeRate","dealValue","marginRate"].forEach((id,i)=>$(id).value=[30,23,1590,40][i]);renderScenario();});
    $("copyPlan").addEventListener("click",async()=>{
      const value=getPlan(),status=$("copyStatus"),fallback=$("manualPlan");status.textContent="";fallback.hidden=true;
      try{if(!navigator.clipboard||!navigator.clipboard.writeText)throw new Error("Clipboard unavailable");await navigator.clipboard.writeText(value);status.textContent="Sample action plan copied. Review the assumptions before reusing.";}
      catch(_){fallback.hidden=false;fallback.value=value;fallback.focus();fallback.select();status.textContent="Automatic clipboard access is unavailable. The plan is selected below for manual copying.";}
    });
    $("downloadPlan").addEventListener("click",()=>{
      const content=JSON.stringify({demo:true,syntheticData:true,period:state.period,channel:state.channel,metrics:selected(),scenario:{qualificationRate:inputNumber("qualifiedRate"),closeRate:inputNumber("closeRate"),averageRevenue:inputNumber("dealValue"),grossMarginPercent:inputNumber("marginRate"),formula:$("scenarioFormula").textContent},sampleOpenOpportunities:opportunities.map(x=>({id:x.id,stage:x.stage,followUpCompleted:x.done,policy:x.policy})),recommendedActions:recommended(),disclaimer:"Illustrative fictional data and modeled assumptions, not actual customers, revenue results or net profit."},null,2);
      const url=URL.createObjectURL(new Blob([content],{type:"application/json"}));const a=document.createElement("a");a.href=url;a.download="ncns-growth-os-demo-plan.json";document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);
      $("copyStatus").textContent="A JSON sample plan was prepared locally in your browser. No data was sent.";
    });
    const links=Array.from(document.querySelectorAll(".side-nav a"));
    if("IntersectionObserver" in window){
      const sections=links.map(a=>document.querySelector(a.getAttribute("href"))).filter(Boolean);
      const observer=new IntersectionObserver(entries=>{
        const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
        if(visible.length){const id=visible[0].target.id;links.forEach(a=>a.classList.toggle("active",a.getAttribute("href")==="#"+id));}
      },{rootMargin:"-10% 0px -50% 0px",threshold:[0,.1,.4]});
      sections.forEach(s=>observer.observe(s));
    }
  }
  function init(){setupControls();renderPipeline();renderMetrics();}
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});else init();
})();
