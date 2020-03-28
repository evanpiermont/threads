

// this code will initilize the screen, font sizes, colors etc. keep colors
// here for easy changing.
//


function clickHist() { 
  d3.selectAll('.fakebutton')
      .on("click", function() {
        d3.selectAll('.fakebutton').classed('clicked', false);
        document.getElementById("new_thread_text").value = "";
        source = this.id;
        ntt = d3.select("#new_thread_text");
        if (source == 'search'){
          ntt.classed('search_form', true);
        } else {
          ntt.classed('search_form', false);
          d3.selectAll('.thread_row').style('display', "block");
        }
        var name_text = ntt.property('value');
        if (ntt.attr("data-big") == 'small'){
          d3.select("#" + source).classed('clicked', true);
          ntt.attr("data-source", source)
          ntt.attr("data-big", 'big')
          ntt.transition()
          .style("width", '100%')
          .style('padding-left', '40px');
           document.getElementById("new_thread_text").focus();
           document.getElementById("new_thread_text").select();
        } else {
          if (ntt.attr("data-source") == source){
          ntt.attr("data-big", 'small')
          ntt.transition()
          .style("width", '0%')
          .style('padding-left', '0px');
          closekws();
          } else {
            ntt.attr("data-source", source)
            d3.selectAll('.fakebutton').classed('clicked', false);
            d3.select("#" + source).classed('clicked', true);
            closekws();
            document.getElementById("new_thread_text").focus();
            document.getElementById("new_thread_text").select();
          }
        };
      
      if (name_text && source == 'new_page') {
        document.getElementById('new_thread_form').submit();
      }
      });

};

document.addEventListener("DOMContentLoaded", clickHist);


function search() { 
  d3.select('#new_thread_text')
      .on("keyup", function() {
        if(d3.select('#new_thread_text').classed('search_form')){
        $q = d3.select('#new_thread_text').property('value').toLowerCase().split(" ");
        d3.selectAll('.thread_row').each( function(d, i){
        kws = d3.select(this).attr("data-keywords-t");
        kws_p = d3.select(this).attr("data-keywords-p");
        kws += kws_p;
        title = d3.select(this).selectAll('.thread_row_title > a').attr("data-title")
        d3.select(this).style('display', "none");
        vis = true
         for (word in $q){
          if ($q[word].length >= 1){
            title = title.replace($q[word], '<span class=bold>'+$q[word]+'</span>')
            if (!(kws.includes($q[word]))){
              vis = false
            };
            title+= "&nbsp;&nbsp;&nbsp;"
            for(kw in kws_p.split(',')){
              if (kws_p.split(',')[kw].includes($q[word])){
                  title+= "<span class=small> // " + kws_p.split(',')[kw] + "</span>"
              }
            };
         };
       };
        if (vis){
          d3.select(this).selectAll('.thread_row_title > a').html(title)
          d3.select(this).style('display', "block");
        }
      });
      };
      });
    };

document.addEventListener("DOMContentLoaded", search);


getThreads = function(filters){

    filtersform = '&user=' + $user;
    $.post('/_get_threads', filtersform, function(json){
        json.thread_index.forEach(function (t, index) {
      
          text = json.threads[t]['title']
          keywords_t = json.threads[t]['keywords_t']
          keywords_p = json.threads[t]['keywords_p']
          flag = !json.threads[t]['read']


          if(text.length > 35){
            text = text.slice(0,35) + '...'
          }

          d3.select("#threads_wrap")
           .append("div")
              .attr("class","thread_row")
              .attr("id","thread" + t)
              .attr("data-keywords-t",keywords_t)
              .attr("data-keywords-p",keywords_p)
              .classed('flag', flag)
          g = d3.select("#thread" + t)
          g.append("div")
              .attr("class","thread_row_title")
              .attr("id","thread_title" + t)
              .append('a')
              .text(text)
              .attr("data-title",text)
              .attr("href","/thread/" + $user + "/" + t)
          g.append("div")
              .attr("class","thread_row_owner")
              .attr("id","thread_owner" + t)
              .text('Created by: ' + json.threads[t]['owner'])
          g.append("div")
              .attr("class","thread_row_date")
              .attr("id","thread_owner_date" + t)
              .text('Created: ' + json.threads[t]['time_start'] + ' // Last Post: ' + json.threads[t]['last_post'])
        });
    })
}

document.addEventListener("DOMContentLoaded", getThreads);


closekws = function(){
  d3.selectAll('.thread_row').each( function(d, i){
    title = d3.select(this).selectAll('.thread_row_title > a').attr("data-title");
    d3.select(this).selectAll('.thread_row_title > a').html(title);
  });
}
