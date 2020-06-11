$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();

  $('.mosaico').click(function () {
    const prodPk = $(this).attr('prod-id');
    const imgPk = $(this).attr('img-id');
    const path = `/recursos/imagen/${prodPk}/${imgPk}/`;
    $.ajax({
      url: path,
      success: (result) => $("#img-zoom").html(result)
    })
  })
});