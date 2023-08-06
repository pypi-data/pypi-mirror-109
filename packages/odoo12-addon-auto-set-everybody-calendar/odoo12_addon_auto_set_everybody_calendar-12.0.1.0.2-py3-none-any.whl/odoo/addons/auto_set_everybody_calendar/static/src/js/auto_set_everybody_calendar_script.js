odoo.define('auto_set_everybody_calendar.CalendarModel', function (require) {

    "use strict"


var waitFor = function(selector, callback) {

    var element = $(selector);

    if (element.length) {

        callback(element);

    } else {

        setTimeout(function() {

            waitFor(selector, callback);

        }, 100);

    }

};


var CalendarModel = require('web.CalendarModel')


CalendarModel.include({

    /**

     * @override

     */

    init: function (context) {

        this._super.apply(this, arguments)

        // This is a hack to select 'Everything/Everybod's calendars' filters by default (instead of just 'Username [Me]')

        waitFor('.o_calendar_filter_item', function(filters) {

            filters.map(function() {

                var isAll = $(this).data('value') === 'all';

                var checkbox = $(this).find('.custom-control input').get(0);

                if (checkbox && (isAll && !checkbox.checked) || (!isAll && checkbox.checked)) {

                    return checkbox;

                }

            }).click();

        });

    }

})

});
