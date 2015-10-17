var editor = ace.edit("editor");
editor.setTheme("ace/theme/iplastic");
editor.getSession().setMode("ace/mode/c_cpp");
editor.setValue(""); 
editor.setShowPrintMargin(false);
document.getElementById('editor').style.fontSize='20px';
editor.getSession().setTabSize(4);
editor.getSession().setUseSoftTabs(true);
$(document).ready(function(){
  var ACE_LANG = {
    "gcc": "c_cpp",
    "g++": "c_cpp",
    "java": "java",
    "pascal": "pascal",
    "go": "golang",
    "lua": "lua",
    "dao": "d",
    "perl": "perl",
    "ruby": "ruby",
    "haskell": "haskell",
    "python2": "python",
    "python3": "python",
  }
  $("#lang").change(function(){
    var lang = $(this).val();
    editor.getSession().setMode("ace/mode/" + ACE_LANG[lang]);
  });

  $("#submit").click(function(){
    var lang = $("#lang").val();
    var code = editor.getValue();
    $("#code").val(code);
    if(confirm("Are you sure submit code?")){
      return true;
    }else{
      return false;
    }
  });
});
