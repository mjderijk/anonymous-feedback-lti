/*jslint browser: true, plusplus: true */
/*global jQuery, Handlebars, moment */
(function ($) {
    'use strict';

    function format_date(date_str) {
        return moment(date_str).format("MMMM D[,] YYYY [at] h:mm A");
    }

    Handlebars.registerHelper('format_date', function(date_str) {
        return format_date(date_str);
    });

    $(document).ready(function () {
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
                display_loading();
            }
        });

        function display_loading() {
            $('#af-content').html('Loading...');
        }

        function get_form() {
            return $.ajax({
                url: window.anonymous_feedback.form_api,
                dataType: 'json'
            });
        }

        function get_comments() {
            return $.ajax({
                url: window.anonymous_feedback.comments_api,
                dataType: 'json'
            });
        }

        function delete_error(xhr) {
            var data;
            try {
                data = $.parseJSON(xhr.responseText);
            } catch (e) {
                data = {error: xhr.responseText};
            }
            alert('Delete failed: ' + data.error);
        }

        function delete_all_comments() {
            if (confirm('Delete all comments?')) {
                $.ajax({
                    url: window.anonymous_feedback.comments_api,
                    dataType: 'json',
                    type: 'DELETE'
                }).fail(delete_error).done(load_comments);
            }
        }

        function delete_comment() {
            /*jshint validthis: true */
            var comment_id = $(this).attr('id').replace('comment-', '');

            if (comment_id.match(/^[0-9]+$/)) {
                if (confirm('Delete this comment?')) {
                    $.ajax({
                        url: window.anonymous_feedback.comments_api + '/' + comment_id,
                        dataType: 'json',
                        type: 'DELETE'
                    }).fail(delete_error).done(load_comments);
                }
            }
        }

        function add_comment() {
            var content = $.trim($("textarea[name='comments']").val());

            $.ajax({
                url: window.anonymous_feedback.comments_api,
                dataType: 'json',
                contentType: 'application/json',
                type: 'POST',
                data: JSON.stringify({content: content})
            }).fail(load_form).done(load_confirmation);
        }

        function update_form() {
            var description = $.trim($("textarea[name='description']").val()),
                name = $.trim($("input[name='name']").val());

            $.ajax({
                url: window.anonymous_feedback.form_api,
                dataType: 'json',
                contentType: 'application/json',
                type: 'PUT',
                data: JSON.stringify({name: name, description: description})
            }).fail(load_customize).done(load_form);
        }

        function update_comment_count(data) {
            if (data.hasOwnProperty('comment_count')) {
                $('span.af-comment-count').text(data.comment_count);
            }
        }

        function load_confirmation(data) {
            var template = Handlebars.compile($('#confirmation-tmpl').html());
            $('#af-content').html(template(data));
            $('#af-header').html(data.name);
            update_comment_count(data);
        }

        function load_form(data) {
            var template = Handlebars.compile($('#form-tmpl').html());
            data.has_description = (data.description && data.description.length);
            $('#af-content').html(template(data));
            $('#af-header').html(data.name);
            $('button.af-btn-submit').click(add_comment);
            $('#af-form-feedback').focus();
            update_comment_count(data);
        }

        function load_customize(data) {
            var template = Handlebars.compile($('#customize-tmpl').html());
            $('#af-content').html(template(data));
            $('#af-header').html('Customize Form');
            $('button.af-btn-update').click(update_form);
            $('button.af-btn-cancel').click(init_form);
            $('#af-form-name').focus();
            update_comment_count(data);
        }

        function load_comments(data) {
            var template = Handlebars.compile($('#comments-tmpl').html());
            data.comments_file = window.anonymous_feedback.comments_file;
            $('#af-content').html(template(data));
            $('#af-header').html('Comments');
            $('a.af-btn-delete-all').click(delete_all_comments);
            $('a.af-btn-delete').click(delete_comment);
            $('#af-download-all').focus();
            update_comment_count(data);
        }

        function load_error(xhr) {
            var data, template, source;
            try {
                data = $.parseJSON(xhr.responseText);
            } catch (e) {
                data = {error: xhr.responseText};
            }
            source = $("#" + xhr.status + '-tmpl').html();
            if (source) {
                template = Handlebars.compile(source);
                $('#af-content').html(template(data));
            }
        }

        function init_customize() {
            $('#af-form-edit-link').tab('show');
            get_form().fail(load_error).done(load_customize);
        }

        function init_comments() {
            $('#af-form-comments-link').tab('show');
            get_comments().fail(load_error).done(load_comments);
        }

        function init_form() {
            $('#af-form-preview-link').tab('show');
            get_form().fail(load_error).done(load_form);
        }

        function initialize() {
            $('#af-form-preview-link').click(init_form);
            $('#af-form-edit-link').click(init_customize);
            $('#af-form-comments-link').click(init_comments);
            $('#af-accordion').accordion({collapsible: true, active: false});
            init_form();
        }

        initialize();
    });
}(jQuery));
