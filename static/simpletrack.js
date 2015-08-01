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
    $('tr[data-rowid=' + rowid + ']').removeClass('bg-warning bg-success').addClass('bg-danger');
  });
}

function issue_pending(rowid)
{
  $.post(
    '/pending/' + rowid
  ).done(function(data) {
    $('.alert_field').text(data.message);
    $('tr[data-rowid=' + rowid + ']').removeClass('bg-danger bg-success').addClass('bg-warning');
  });
}

function issue_resolved(rowid)
{
  $.post(
    '/resolved/' + rowid
  ).done(function(data) {
    $('.alert_field').text(data.message);
    $('tr[data-rowid=' + rowid + ']').removeClass('bg-danger bg-warning').addClass('bg-success');
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