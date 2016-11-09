% setdefault('old_name_of_agent', '')

<div class="modal fade" id="agent_edit_actions">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">{{current_language['modal_edit_actions_title']}}</h4>
      </div>
      <div class="modal-body">
        <table class="table table-striped">
          <tr>
            <th>Action</th>
              % #for item in actions: {{item}}
              <li></li>
              #% end
          </tr>
        </table>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">{{current_language['modal_close']}}</button>
        <button type="button" class="btn btn-primary">{{current_language['modal_save_changes']}}</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="agent_edit_name">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">{{current_language['modal_change_name_title']}}</h4>
      </div>
      <form id="change_name_form" action="" data-agent-id="">
        <div class="modal-body">
            <div class="form-group">
              <label for="new_name">{{current_language['modal_change_name_description']}}</label>
              <input type="text" class="form-control" id="new_name">
              <p class="help-block">{{current_language['modal_change_name_helptext']}}</p>
            </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">{{current_language['modal_close']}}</button>
          <button type="submit" id="submit_name_change" class="btn btn-primary">{{current_language['modal_save_changes']}}</a>
        </div>
      </form>
    </div>
  </div>
</div>
