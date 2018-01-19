/*jslint browser: true, plusplus: true */
/*global jQuery, Handlebars, top */
(function ($) {
    'use strict';
    $(document).ready(function () {
        var API = 'api/v1/form/' + window.anonymous_feedback.canvas_course_id;

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

        function get_form() {
            return $.ajax({url: API, dataType: 'json'});
        }

        function get_comments(ev) {
            var params = {url: API + '/comments'};

            if (ev.data.hasOwnProperty('accept')) {
                params.accept = ev.data.accept;
            } else {
                params.dataType = 'json';
            }
            return $.ajax(params);
        }

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

        function update_comment_count(data) {
            if (data.hasOwnProperty('comment_count')) {
                $('.af-comment-count').text(data.comment_count);
            }
        }

        function load_form(data) {
            var template = Handlebars.compile($('#form-tmpl').html());
            data.has_description = (data.description && data.description.length);

            $('#af-content').html(template(data));
            $('#af-header').html(data.name);
            $('button.af-btn-submit').click(submit_feedback);
            update_comment_count(data);
        }

        function load_customize(data) {
            var template = Handlebars.compile($('#customize-tmpl').html());
            $('#af-content').html(template(data));
            $('#af-header').html('Customize Form');
            $('button.af-btn-update').click(update_form);
            $('button.af-btn-cancel').click(init_form);
            update_comment_count(data);
        }

        function load_comments(data) {
            var template = Handlebars.compile($('#comments-tmpl').html());
            $('#af-content').html(template(data));
            $('#af-header').html('Comments');
            $('af-btn-download-all').click({accept: 'text/csv'}, get_comments);
            //$('af-btn-delete-all').click();
            //$('af-btn-delete').click();
            update_comment_count(data);
        }

        function init_customize() {
            get_form().fail().done(load_customize);
        }

        function init_comments() {
            get_comments().fail().done(load_comments);
        }

        function init_form() {
            get_form().fail().done(load_form);
        }

        function initialize() {
            $('.af-btn-customize').click(init_customize);
            $('.af-btn-comments').click(init_comments);
            init_form();
        }

        initialize();
    });
}(jQuery));
