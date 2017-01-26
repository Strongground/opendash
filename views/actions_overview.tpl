% include('header', showMenu=showMenu)
% setdefault('open_modal', '')
% if open_modal == 'edit_action':
<script>$(document).ready(function () { $('#actions_edit_action').modal('show') })</script>
% end

<h1>Manage and create actions</h1>

<div class="panel panel-default" id="dashboard-agents">
  <div class="panel-heading">
    <h2 class="panel-title">{{current_language['actions_overview_header']}}</h2>
  </div>
  <div class="panel-body">
    <p>Das ist der Inhalt in der übergebenen Liste der Aktionen:</p>
    <table id="actions_table" class="table table-striped table-hover">
      <thead>
        <tr>
          <th>{{current_language['actions_table_head_number']}}</th>
          <th>{{current_language['actions_table_head_name']}}</th>
          <th>{{current_language['actions_table_head_extended-param']}}</th>
          <th>{{current_language['actions_table_head_plugin']}}</th>
          <th>{{current_language['actions_table_head_uid']}}</th>
          <th>{{current_language['actions_table_head_edit']}}</th>
        </tr>
      </thead>
      <tbody>
        % i = 0
        % for action in list_of_actions:
        %   i += 1
        <tr>
          <td>{{i}}</li>
          <td>{{list_of_actions[action]['custom_name']}}</td>
          <td>{{list_of_actions[action]['extended_parameters']}}</td>
          <td>{{list_of_actions[action]['plugin']}}</td>
          <td>{{action}}</td>
          <td>
            <form index="edit_action_form" method="post">
              <input type="hidden" name="form_type" value="open_modal">
              <input type="hidden" name="action_uid" value="{{action}}">
              <button type="submit" id="edit_action" data-toggle="modal" data-target="#actions_edit_action" data-action-uid="{{action}}" class="btn btn-default" name="edit_action">
                <span class="glyphicon glyphicon-pencil"></span>
              </button>
            </form>
          </td>
        </tr>
        % end
      </tbody>
    </table>
  </div>
</div>

<div class="panel panel-default" id="dashboard-agents">
  <div class="panel-heading">
    <h2 class="panel-title">{{current_language['actions_create_action_header']}}</h2>
  </div>
  <div class="panel-body">
    <form id="create_new_action" method="post">

      <div class="form-group">
        <label for="new_action_name">{{current_language['actions_create_action_description']}}</label>
        <input type="text" name="new_action_name" class="form-control" id="new_action_name" placeholder="{{current_language['actions_create_action_placeholder']}}">
      </div>

      <div class="form-group">
        <label for="plugin">{{current_language['actions_create_action_plugin_description']}}</label>
        <select class="form-control" id="plugin" name="plugin">
          <option>Test-Plugin 1</option>
          <option>Test-Plugin 2</option>
          <option>Test-Plugin 3</option>
          <option>Test-Plugin 4</option>
        </select>
        <p class="help-block">{{current_language['actions_create_action_plugin_help']}}</p>
      </div>

      <div class="form-group">
        <label for="extended-params">{{current_language['actions_create_action_extended_params']}}</label>
        <input type="text" class="form-control" id="extended-params" name="extended-params" placeholder="{{current_language['actions_create_action_extended_params']}}">
      </div>

      <div class="form-group">
        <input type="hidden" name="form_type" value="create_action">
        <button type="submit" id="submit_add_action" class="btn btn-primary pull-right">{{current_language['actions_add_action_submit']}}</button>
      </div>

    </form>
  </div>
</div>

% include('footer')
