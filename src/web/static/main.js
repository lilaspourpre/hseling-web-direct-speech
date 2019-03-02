$(document).ready(() => {
  //$().on('click', () => {
   // $('.download-button').show();
  //});

  $(".said-tag").on("click", () => {
  	$(".said").toggleClass("said-active");

  });


  $(".author-tag").on("click", () => {
  	$(".author-comment").toggleClass("author-active");

  });


  $(".verb-tag").on("click", () => {
  	$(".speech-verb").toggleClass("verb-active");

  });


  $(".who-tag").on("click", () => {
  	$(".who").toggleClass("who-active");

  });




});

function download_file()
{
    var vars = getUrlVars(),
      file_id = vars["file_id"];
    window.open('/download_processed/?file_id=' + file_id);
}

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

$(function () {
  var vars = getUrlVars(),
      task_id = vars["task_id"];

  if(task_id) {
    var get_status = function () {
      $.get("/web/status?task_id=" + task_id, function(data) {
        if (data.ready) {
		  $("i").hide();
		  $(location).attr('href', '/web/download?file_id='+data["file_id"])
        } else {
		  $("i").show();
          setTimeout(get_status, 20);
        }
      });
    };

    get_status();
  }
});
