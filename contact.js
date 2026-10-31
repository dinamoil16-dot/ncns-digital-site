/* Public configuration only. Never place credentials in contact-config.json. */
(() => {
  "use strict";
  const link=document.getElementById("emailBrief"), status=document.getElementById("contactDelivery");
  if(!link || !status)return;
  fetch("./contact-config.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw new Error("Configuration unavailable");return r.json();}).then(config=>{
    const channels=[["instagramUrl","instagramContact","instagramPending","www.instagram.com"],["whatsappUrl","whatsappContact","whatsappPending","wa.me"]];
    if(config.ownerApproved===true)channels.forEach(([key,id,pending,host])=>{
      try{const url=new URL(config[key]);if(url.protocol!=="https:" || url.hostname!==host || url.username || url.password || url.port || url.pathname==="/")return;
        document.getElementById(id).href=url.href;document.getElementById(id).hidden=false;document.getElementById(pending).hidden=true;
      }catch(_){} });
    const email=typeof config.email==="string"?config.email.trim():"";
    if(config.ownerApproved!==true || !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email))return;
    link.hidden=false;document.getElementById("emailPending").textContent=email;
    const update=()=>{
      const body=["NCNS Digital — project review request","Need: "+document.getElementById("projectType").value,"Outcome: "+document.getElementById("projectDetails").value.trim(),"Current website/process: "+document.getElementById("currentProcess").value.trim(),"Reply channel: "+document.getElementById("replyChannel").value.trim()].join("\n");
      link.href="mailto:"+email+"?subject="+encodeURIComponent("NCNS project review request")+"&body="+encodeURIComponent(body);
    };
    document.getElementById("briefForm").addEventListener("input",update);link.addEventListener("click",e=>{
      if(!document.getElementById("projectDetails").value.trim()){e.preventDefault();status.textContent="Describe your business need and desired outcome first.";document.getElementById("projectDetails").focus();return;}
      update();status.textContent="Opening your email application. Review and send there. This website cannot confirm sending or delivery; keep a copy if no email app opens.";
    });update();
    document.querySelector(".contact-note").textContent="Prepare your brief here, then open your email application to review and send it to "+email+". Copy remains available if no email application is configured.";
    status.textContent=config.deliveryVerified===true?"Owner-configured email draft. Sending happens in your email application; this page does not submit a message.":"Owner-configured recipient; end-to-end delivery has not been verified. Launch remains blocked.";
  }).catch(()=>{status.textContent="Contact configuration could not be loaded. Copy your brief locally; no message has been sent.";});
})();
