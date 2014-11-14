$(document).ready(function(){
  var items = [];

  document.title = project_title + " Article Index";
  $('#main-title').html(project_title + " Article Index");

  $.each( entries, function (key, entry ){
    items.push( "<tr class='entry'>" +
      "<td class='id'>"+ entry.id + "</td>" +
      "<td class='year'>"+ entry.year + "</td>" +
      "<td class='title'>"+ entry.title + "</td>" +
      "<td class='author'>"+ entry.author + "</td>" +
      "<td class='journal'>"+ entry.journal + "</td>" +
      "<td class='keywords'>"+ entry.keywords + "</td>" +
      "<td class='abstract'>"+ entry.abstract + "</td>" +
      "<td class='abstract_toggle'>" + (!entry.abstract.length ? "" :
        "<button type='button' class='toggle-show btn btn-info'>Show Text</button>"+
        "<button type='button' class='toggle-hide btn btn-warning' style='display:none'>Hide Text</button>") + "</td>" +
      "<td class='file'>"+
        "<a href='"+ pdf_root +"\\"+ entry.file.replace(/'/g, "&#39;") +"' target='_blank' class='btn btn-primary'>PDF</a></td>" +
      "</tr>"
    );
  });

  $( "<tbody />", {
    html: items.join( "" )
  }).appendTo( $("#articles") );

  var articles_table = $('#articles').DataTable({
    paging: false,
    columnDefs:[
      {
        targets: [0, 6],
        visible: false
      },
      {
        targets: [7,8],
        searchable: false
      }
    ]
  });

  // date, newspaper, title
  articles_table.order([[1, 'asc'], [4, 'asc'], [2, 'asc']]).draw();

  $('.abstract_toggle button.toggle-show').click(function(event){
    var button = $(this);
    var row = articles_table.row(button.closest('tr'));
    var entry_index = row.data()[0]-1;
    var entry = entries[entry_index];

    row.child("<div>"+ entry.abstract.replace(/\n/g, "<br />") + "</div>").show();

    button.parent().parent().addClass('info');
    button.parent().parent().next().addClass('info');
    button.parent().find('.toggle-hide').show();
    button.hide();

    event.preventDefault();
  });

  $('.abstract_toggle button.toggle-hide').click(function(event){
    var button = $(this);
    var row = articles_table.row(button.closest('tr'));

    row.child.hide();

    button.parent().parent().removeClass('info');
    button.parent().parent().next().removeClass('info');
    button.parent().find('.toggle-show').show();
    button.hide();

    event.preventDefault();
  });

  $('.button-articles-show-all').click(function(event){
    $('.abstract_toggle button.toggle-show').click();
  });

  $('.button-articles-hide-all').click(function(event){
    $('.abstract_toggle button.toggle-hide').click();
  });
});
