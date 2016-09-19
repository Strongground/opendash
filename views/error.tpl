% showMenu = showMenu
% include('header', showMenu=showMenu)
% error_header = str(error_type+'_header')
% error_description = str(error_type+'_description')
<div class="center-block bg-danger generic-error">
  <h1 class="text-danger">Dammit: {{current_language[error_header]}}</h1>
  <p>{{current_language[error_description]}}</p>
</div>
% include('footer')
