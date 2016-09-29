% showMenu = showMenu
% include('header', showMenu=showMenu)

% setdefault('invalidateField', '')
% setdefault('originalInput', '')

<form class="form-signin" method="post">
  <h2 class="form-signin-heading">{{current_language['heading_login']}}</h2>

  % if invalidateField:
  <div class="form-group has-error">
  % else:
  <div class="form-group">
  % end
    <label for="inputUsername" class="sr-only">{{current_language['label_username']}}</label>
    <input tabindex="1" type="email" name="username" id="inputUsername" class="form-control" placeholder="{{current_language['label_username']}}" required="" autofocus="">
    <label for="inputPassword" class="sr-only">{{current_language['label_password']}}</label>
    <input tabindex="2" type="password" name="password" id="inputPassword" class="form-control" placeholder="{{current_language['label_password']}}" required="" >
  % if invalidateField == 'inputUsername':
    <label for="inputUsername" class="control-label validation-error">{{current_language['validation_error_email']}}</label>
  % elif invalidateField == 'inputPassword':
    <label for="inputPassword" class="control-label validation-error">{{current_language['validation_error_password']}}</label>
  % end
  </div>

  <div class="checkbox">
    <label>
      <input tabindex="3" type="checkbox" name="remember-login" value="true">{{current_language['label_staysignedin']}}
    </label>
  </div>

  <button class="btn btn-lg btn-primary btn-block" type="submit">{{current_language['label_login']}}</button>
</form>
% include('footer')
