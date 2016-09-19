% showMenu = showMenu
% include('header', showMenu=showMenu)
% setdefault('invalidateField', '')
% print(invalidateField)
<form class="form-signin" method="post">
  <h2 class="form-signin-heading">{{current_language['heading_login']}}</h2>

  % if invalidateField:
  <div class="form-group has-error">
  % else:
  <div class="form-group">
  % end
    <label for="inputUsername" class="sr-only">{{current_language['label_email']}}</label>
    <input type="email" name="username" id="inputUsername" class="form-control" placeholder="{{current_language['label_email']}}" required="" autofocus="">
    <label for="inputPassword" class="sr-only">{{current_language['label_password']}}</label>
    <input type="password" name="password" id="inputPassword" class="form-control" placeholder="{{current_language['label_password']}}" required="" >
  % if invalidateField == 'inputUsername':
    <label for="inputUsername" class="control-label validation-error visible">{{current_language['validation_error_email']}}</label>
  % elif invalidateField == 'inputPassword':
    <label for="inputPassword" class="control-label validation-error">{{current_language['validation_error_password']}}</label>
  % end
  </div>

  <div class="checkbox">
    <label>
      <input type="checkbox" value="remember-me">{{current_language['label_staysignedin']}}
    </label>
  </div>

  <button class="btn btn-lg btn-primary btn-block" type="submit">{{current_language['label_login']}}</button>
</form>
% include('footer')
