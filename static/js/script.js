document.querySelector(".burger").onclick = function() {
	this.classList.toggle("burger-active");
	document.querySelector("nav").classList.toggle("active");
}

$(function() {
  // при нажатии на кнопку top_up
  $('.top_up').click(function() {
    // переместиться в верхнюю часть страницы
    $("html, body").animate({
      scrollTop:0},1000);
  })
})
// при прокрутке окна (window)
$(window).scroll(function() {
  // если пользователь прокрутил страницу более чем на 700px
  if ($(this).scrollTop()>700) {
    // то сделать кнопку top_up видимой
    $('.top_up').fadeIn();
    $('.top_up').css({display:"flex"});
  }
  // иначе скрыть кнопку top_up
  else {
    $('.top_up').fadeOut();
  }
});

$('#id_service_choice').change(function () {
    var url = $('#form').attr('data-url');
    var service_choice = $(this).val();
    $.ajax ({
        url: url,
        data: {
            'service_choice': service_choice
        },
        success: function (data) {
            $('#id_masters_choice').html(data);
        }
    });
});

$('#id_date_field').change(function() {
    var master = $('#id_masters_choice').val();
    var date = $(this).val();
    $.ajax({
        type: 'GET',
        url: '/ajax/load_time/',
        data: {'date': date, 'master': master},
        success: function(response) {
            $('#id_time_field').html(response);
        }
    });
});

$(document).ready(function () {
    $('#id_client_name').change(function () {
        $.ajax({
            data: $(this).serialize(),
            url: "/ajax/valid_fields/",
            success: function (data) {
                if (/^[а-яА-Я]{2,10}$/.test(data['valid_name']) !=true) {
                    $('#id_client_name').removeClass('valid_field').addClass('invalid_field');
                    $('#id_client_name').after('<p class="errorlist">Имя должно быть от 2-х до 10-ти символов кирилицы</p>');
                } else {
                    $('p.errorlist').remove();
                    $('#id_client_name').removeClass('invalid_field').addClass('valid_field');
                }

            },
        });
        return false;
    });

    $('#id_phone_number').change(function () {
        $.ajax({
            data: $(this).serialize(),
            url: "/ajax/valid_fields/",
            success: function (data) {
                if (/^89[0-9]{9}$/.test(data['valid_phone']) !=true) {
                    $('#id_phone_number').removeClass('valid_field').addClass('invalid_field');
                    $('#id_phone_number').after('<p class="errorlist">Вводить тел. номер нужно без пробелов, скобок и дефисов в виде 89ХХХХХХХХХ</p>');
                } else {
                    $('p.errorlist').remove();
                    $('#id_phone_number').removeClass('invalid_field').addClass('valid_field');
                }
            },
        });
        return false;
    });
});