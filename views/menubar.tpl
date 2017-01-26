% setdefault('currentpage', '')

<nav class="navbar navbar-default navbar-fixed-top">
  <div class="container">

    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">OpenDash</a>
    </div>

    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        <li
        % if currentpage == 'dashboard':
        class="active"
        % end
        ><a href="./dashboard">Dashboard</a></li>
        <li
        % if currentpage == 'actions':
        class="active"
        % end
        ><a href="./actions_overview">Action Manager</a></li>
        <li><a href="./preferences">Preferences</a></li>
        <li><a href="./support">Support</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li class="active logout"><a href="./logout">Log out</a></li>
      </ul>
    </div>

  </div>
</nav>
