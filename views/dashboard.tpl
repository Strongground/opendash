% include('header', showMenu=showMenu)
<div class="jumbotron">
  <h1>{{current_language['welcome_header']}}</h1>
  <p class="lead">{{current_language['welcome_paragraph1']}}</p>
  <p>{{current_language['welcome_paragraph2']}}</p>
</div>

<div class="panel panel-default" id="dashboard-agents">
  <div class="panel-heading">
    <h2 class="panel-title">{{current_language['agents_header']}}</h2>
  </div>
  <div class="panel-body">

    <div class="row">
      <div class="agent-container col-md-10">
        <ul>
          <h3>{{current_language['agents_empty_header']}}</h3>
          <p>{{current_language['agents_empty_description']}}</p>
        </ul>
      </div>
      <div class="col-md-2">
        <button class="btn btn-primary btn-lg pull-right scan-button" type="button" name="scan_for_devices">
          <span class="glyphicon glyphicon-refresh"></span>
          {{current_language['agents_scan_button']}}
        </button>
      </div>
    </div>

  </div>
</div>

% include('footer')
