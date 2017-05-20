function add_issue()
{
  $.post(
      '/add',
      { 'description': $('#description').val() },
      function(data) {
        location.reload();
      }
    );
}

function delete_issue(rowid)
{
  $.post(
    '/delete/' + rowid
    ).done(function(data) {
      $('.alert_field').text(data.message);
    });
  $('tr[data-rowid=' + rowid + ']').remove();
}

// obviously can be done better
function issue_open(rowid)
{
  $.post(
    '/open/' + rowid
  ).done(function(data) {
    $('.alert_field').text(data.message);
    $('tr[data-rowid=' + rowid + ']').removeClass('bg-danger bg-success bg-info').addClass('bg-warning');
  });
}

function issue_pending(rowid)
{
  $.post(
    '/pending/' + rowid
  ).done(function(data) {
    $('.alert_field').text(data.message);
    $('tr[data-rowid=' + rowid + ']').removeClass('bg-danger bg-success bg-warning').addClass('bg-info');
  });
}

function issue_resolved(rowid)
{
  $.post(
    '/resolved/' + rowid
  ).done(function(data) {
    $('.alert_field').text(data.message);
    $('tr[data-rowid=' + rowid + ']').removeClass('bg-danger bg-warning bg-info').addClass('bg-success');
  });
}

function issue_rejected(rowid)
{
    $.post(
	'/rejected/' + rowid
    ).done(function(data) {
	$('.alert_field').text(data.message);
	$('tr[data-rowid=' + rowid + ']').removeClass('bg-warning bg-info bg-success').addClass('bg-danger');
    });
}

// function update_issue(rowid, status)
// {
//   $.post(
//     '/' + status + '/' + rowid
//   ).done(function(data) {
//     $('.alert_field').text(data.message);
//   });
// }
