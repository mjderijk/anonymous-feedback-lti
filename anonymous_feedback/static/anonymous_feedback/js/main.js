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
            }
        });

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

        function delete_all_comments() {
            if (confirm('Delete all comments?')) {
                $.ajax({
                    url: window.anonymous_feedback.comments_api,
                    dataType: 'json',
                    type: 'DELETE'
                }).fail().done(load_comments);
            }
        }

        function delete_comment() {
            /*jshint validthis: true */
            var comment_id = $(this).attr('id').replace('comment-', '');

            if (!comment_id.match(/^[0-9]+$/)) {
                alert('Invalid');
                return;
            }

            $.ajax({
                url: window.anonymous_feedback.comments_api + '/' + comment_id,
                dataType: 'json',
                type: 'DELETE'
            }).fail().done(load_comments);
        }

        function add_comment() {
            var content = $.trim($("textarea[name='comments']").val());

            $.ajax({
                url: window.anonymous_feedback.comments_api,
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
                url: window.anonymous_feedback.form_api,
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
            $('button.af-btn-submit').click(add_comment);
            $('a.af-btn-customize').click(init_customize);
            $('a.af-btn-comments').click(init_comments);
            $('a.af-btn-preview').click(init_form);
            update_comment_count(data);
        }

        function load_customize(data) {
            var template = Handlebars.compile($('#customize-tmpl').html());
            $('#af-content').html(template(data));
            $('#af-header').html('Customize Form');
            $('button.af-btn-update').click(update_form);
            $('button.af-btn-cancel').click(init_form);
            $('a.af-btn-customize').click(init_customize);
            $('a.af-btn-comments').click(init_comments);
            $('a.af-btn-preview').click(init_form);
            update_comment_count(data);
        }

        function load_comments(data) {
            var template = Handlebars.compile($('#comments-tmpl').html());
            data.comments_file = window.anonymous_feedback.comments_file;
            $('#af-content').html(template(data));
            $('#af-header').html('Comments');
            $('.af-btn-delete-all').click(delete_all_comments);
            $('.af-btn-delete').click(delete_comment);
            $('a.af-btn-customize').click(init_customize);
            $('a.af-btn-comments').click(init_comments);
            $('a.af-btn-preview').click(init_form);
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
            init_form();
        }

        initialize();
    });
}(jQuery));

$( function() {
            $( "#accordion" ).accordion({
              collapsible: true, active: false
            });
          } );