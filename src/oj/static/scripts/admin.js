$('#form').delegate('button[data-trigger]', 'click', function() {
    var action = $(this).data('trigger');
    triggers[action]($(this).parent().parent().parent().parent());
}).submit(function() {
    $(this).find('.row[meta-fields]').each(function(idx) {
        $(this).find('input,select').each(function() {
            var field_name = $(this).attr('name').split('-');
            $(this).attr('name', field_name[0] + '-' + idx + '-' + field_name.slice(-1))
        })
    });
});
var triggers = {};
triggers['insert-up'] = function($row) {
    $row.clone().insertBefore($row);
};
triggers['insert-down'] = function($row) {
    $row.clone().insertAfter($row);
};
triggers['exchange-up'] = function($row) {
    var $prev = $row.prev();
    if($prev.attr('meta-fields')) {
        $row.remove();
        $row.insertBefore($prev);
    }
};
triggers['exchange-down'] = function($row) {
    var $next = $row.next();
    if($next.attr('meta-fields')) {
        $row.remove();
        $row.insertAfter($next);
    }
};
triggers['remove'] = function($row) {
    $row.remove();
};
