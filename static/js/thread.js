
function clickHist() { 
  d3.selectAll('.fakebutton')
      .on("click", function() {
        });
      };

document.addEventListener("DOMContentLoaded", clickHist);


$croll = true;


textAreaResize = function(){
  $('textarea').each(function () {
  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
  });
  
  $(document).on('input', 'textarea', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
  scrollBottom()
});
};

var mq = window.matchMedia( "only screen and (max-width : 500px)" );
if (!mq.matches) {
    document.addEventListener("DOMContentLoaded", textAreaResize);
}





function click_postPara() { 
      $(document).on('click',  '.post', function(){
        postPara()
      });
};

function postPara() { 
        para_text = d3.select('#para_input_0').node().value 
        if(para_text){
        formdata = '&owner=' + $user;
        formdata += '&text=' + para_text; 
        formdata += '&para_num=' + 0; //deal with this!
        formdata += '&thread_id=' + $thread_id; 

        $.post('/_post_para', formdata, function(json){
          getParas()
          renderKatex();
          $croll = true;
        });
      } else {
        return false
      };

};


document.addEventListener("DOMContentLoaded", click_postPara);
//document.addEventListener("DOMContentLoaded", hideInput);

var map = {17: false, 13: false};

function post_enter() { 
  $(document).on('keydown', '#para_input_0', function (e) {
    k = e.originalEvent.keyCode
    if(k in map)
      map[k] = true;
      if (map[17] && map[13]) { 
        map[17] = false;
        map[13] = false;
        postPara()
      }
    });
  $(document).on('keyup', '#para_input_0', function () {
    for (key in map) {
        map[key] = false;
      };
    });
};


document.addEventListener("DOMContentLoaded", post_enter);



getParas = function(){

    formdata = '&thread_id=' + $thread_id; 
    $.post('/_get_paras', formdata, function(json){
    d3.select("#para_wrap").selectAll("*").remove();
        l = Object.keys(json.paras).length
         for (var p in json.paras){
        //   t = l+1- t

           text = json.paras[p]['text']
           owner = json.paras[p]['owner']
           date_start = json.paras[p]['date_start']
           time_start = json.paras[p]['time_start']


           g= d3.select("#para_wrap").append("div")
            .attr("class","para")
            
            g.append("div")
              .attr("class","para_text") //fix!!
              .attr("id","para_text_" + p)
              .html(text)
            g.append("div")
              .attr("class","para_owner")
              .attr("id","para_owner_" + p)
              .text(owner) 
            g.append("div")
              .attr("class","para_time")
              .attr("id","para_time_" + p)
              .html(date_start + '<br>' + time_start)            
        };

        g = d3.select("#para_wrap").append("div")
              g.attr("class","para")
              
            g.append('textarea')
                .attr("class","para_input")
                .attr("id","para_input_0")
            g.append('div')
                .classed("post", true)             
                .classed("fake_button", true)             
                .attr("id","post_0")
                .text('Post')

    renderKatex();
    })
}

scrollBottom = function(){
    if ($croll){
    $("#para_wrap").animate({
         scrollTop: 100000000 
     }, 1000);
    $croll = false;
    document.getElementById("para_input_0").focus();
    document.getElementById("para_input_0").select();
  };
  };

document.addEventListener("DOMContentLoaded", getParas);


renderKatex = function(){
  d3.selectAll('.math').each( function(d, i){
    var texTxt = d3.select(this).text();
    try {
      if(this.tagName == 'DIV'){
        el = d3.select(this).node()
        katex.render(texTxt, el, { displayMode: true, throwOnError: false});
      }else{
        el = d3.select(this).node()
        katex.render(texTxt, el, {throwOnError: false});
      }
    }
    catch(err) {
        d3.select(this).html("<span class=err>" + texTxt + "</span>");
    }
  }); 
  scrollBottom();
};



