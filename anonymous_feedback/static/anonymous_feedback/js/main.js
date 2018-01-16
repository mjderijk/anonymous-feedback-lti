/*jslint browser: true, plusplus: true */
/*global jQuery, Handlebars, top */
(function ($) {
    'use strict';
    $(document).ready(function () {
        var API = '/api/v1/form/' + window.anonymous_feedback.canvas_course_id;

        $.ajaxSetup({
            crossDomain: false,
            beforeSend: function (xhr, settings) {
                if (window.anonymous_feedback.session_id) {
                    xhr.setRequestHeader('X-SessionId',
                                         window.anonymous_feedback.session_id);
                }
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken',
                                         window.anonymous_feedback.csrftoken);
                }
            }
        });

        function submit_feedback() {
            var content = $.trim($("textarea[name='comments']").val());

            $.ajax({
                url: API + '/comments',
                dataType: 'json',
                contentType: 'application/json',
                type: 'POST',
                data: JSON.stringify({content: content})
            }).fail(load_form).done(load_form);
        }

        function update_form() {
            var description = $.trim($("textarea[name='description']").val()),
                name = $.trim($("input[name='name']").val());

            $.ajax({
                url: API,
                dataType: 'json',
                contentType: 'application/json',
                type: 'PUT',
                data: JSON.stringify({name: name, description: description})
            }).fail(load_customize).done(load_form);
        }

        function load_form(data) {
            var template = Handlebars.compile($('#form-tmpl').html());
            $('#af-content').html(template(data));
            $('button.af-btn-submit').click(submit_feedback);
        }

        function load_customize(data) {
            var template = Handlebars.compile($('#customize-tmpl').html());
            $('#af-content').html(template(data));
            $('button.af-btn-update').click(update_form);
            $('button.af-btn-cancel').click(load_form);
        }

        function load_comments(data) {
            var template = Handlebars.compile($('#comments-tmpl').html());
            $('#af-content').html(template(data));
        }

        function init_customize() {
            $.ajax({url: API, dataType: 'json'}).fail().done(load_customize);
        }

        function init_comments() {
            $.ajax({url: API, dataType: 'json'}).fail().done(load_comments);
        }

        function initialize() {
            $('button.af-btn-customize').click(init_customize);
            $('button.af-btn-comments').click(init_comments);
            $.ajax({url: API, dataType: 'json'}).fail().done(load_form);
        }

        initialize();
    });
}(jQuery));
