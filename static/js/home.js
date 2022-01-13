$(document).ready(function () {
  (function () {
    class Message {
      constructor(arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
          return function () {
            var $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.message_side).find('.text').html(_this.text);
            $('.messages').append($message);
            return setTimeout(function () {
              return $message.addClass('appeared');
            }, 0);
          };
        } (this);
        return this;
      }
    }
    $(function () {
      var getMessageText, message_side, sendMessage;
      message_side = 'left';
      getMessageText = function () {
        var $message_input;
        $message_input = $('.message_input');
        return $message_input.val();
      };
      sendMessage = function (text, sender='bot') {
        var $messages, message;
        if (text.trim() === '') {
          return;
        }
        $('.message_input').val('');
        $messages = $('.messages');
        message_side = sender === 'people' ? 'right' : 'left';
        message = new Message({
          text: text,
          message_side: message_side
        });
        message.draw();
        return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
      };

      var api = e => {
        sendMessage(e, 'people')
        $('.message_input').focus()
        $.ajax({
          url:'/chatbot/',
          method:'post',
          datatype:'json',
          data: {
            msg: e
          },
          success: data => {
            if(data.success){
              sendMessage(data.data, 'bot')
            }else{
              alert('something wrong!')
            }
          },
          error: data => {

          },
        })

      }

      setTimeout(() => {
        sendMessage('Xin chào, tôi có thể giúp gì cho bạn!', 'bot')
      }, 500)
      $('.send_message').click(function (e) {
        return api(getMessageText());
      });
      $('.message_input').keyup(function (e) {
        if (e.which === 13) {
          return api(getMessageText());
        }
      });






      // sendMessage('Hello Philip! :)');
      // setTimeout(function () {
      //   return sendMessage('Hi Sandy! How are you?');
      // }, 1000);
      // return setTimeout(function () {
      //   return sendMessage('I\'m fine, thank you!');
      // }, 2000);
    });
  }.call(this));
})