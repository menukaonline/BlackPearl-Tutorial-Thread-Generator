styles=\
'''
<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css'><link rel="stylesheet" href="./style.css"><style>@import url(https://fonts.googleapis.com/css?family=Lora:400,700|Roboto&display=swap);body,html{height:100%}body{font-family:Roboto,sans-serif;padding:1rem 1rem 12rem;background-color:#efefef}.btn{background-color:#fff}#copy_button{position:relative;overflow:visible}#copy_tooltip{display:block;font-size:80%;position:absolute;background:#1a3ca2;color:#fff;padding:.5rem 1rem;border-radius:4px;top:0;left:20px;right:20px;margin:auto;opacity:0}#copy_tooltip.active{-webkit-animation:slide-up .15s cubic-bezier(.51,.92,.265,1.55) both;animation:slide-up .15s cubic-bezier(.51,.92,.265,1.55) both}#copy_tooltip.inactive{-webkit-animation:slide-up .1s cubic-bezier(.25,.46,.45,.94) reverse both;animation:slide-up .1s cubic-bezier(.25,.46,.45,.94) reverse both}#copy_tooltip:after{content:"";position:absolute;top:98%;left:50%;margin-left:-8px;width:0;height:0;border-top:8px solid #1a3ca2;border-right:8px solid transparent;border-left:8px solid transparent}@-webkit-keyframes slide-up{0%{transform:translateY(0) scale(.8);opacity:0}100%{transform:translateY(-35px) scale(1);opacity:1}}@keyframes slide-up{0%{transform:translateY(0) scale(.8);opacity:0}100%{transform:translateY(-35px) scale(1);opacity:1}}</style>
'''
body=\
'''
<form class="col-m-8"><label for="copy_textarea" tabindex="-1">Copy text in the textarea with the button below.</label><pre><textarea readonly id="copy_textarea" class="form-control form-control-lg" style="height: 300px; font-size: 15px" row="3">{bbCode}</textarea></p><p><button data-clipboard-target="#copy_textarea" class="btn btn-outline-primary btn-lg" type="button" id="copy_button">Copy to Clipboard<span id="copy_tooltip" aria-live="assertive" role="tooltip"></span></button></p></form>
'''
scripts=\
'''
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script><script src='https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.4/clipboard.min.js'></script><script>var active=!1;function copyMessageTooltip(o,t){active=!0;$("#copy_tooltip").text(t).addClass("active"),o.attr("aria-describedby","copy_tooltip"),setTimeout(function(){$("#copy_tooltip").removeClass("active").addClass("inactive"),$("#copy_tooltip").replaceWith($("#copy_tooltip").clone(!0)),o.removeAttr("aria-describedby"),setTimeout(function(){$("#copy_tooltip").removeClass("inactive").text(""),active=!1},100)},2e3)}$(document).ready(function(){$("#copy_textarea");var o=$("#copy_button"),t=new ClipboardJS("#copy_button");t.on("success",function(t){t.clearSelection(),o.focus(),active||copyMessageTooltip(o,"Text Copied!")}),t.on("error",function(t){active||copyMessageTooltip(o,"Press Ctrl+C to copy")})});</script></body>
'''