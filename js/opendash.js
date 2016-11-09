// Only load shit if other shit is ready to be found'n shit
(function ($) {

  /*
  * @description Helper function to toggle an attribute of a dom element.
  *
  * A value for the attribute can be given but is optional, in which case
  * the attribute will be created empty.
  *
  * @param attribute String
  * @param value String optional
  */
  $.fn.toggleAttr = function (attribute, value) {
    value = value || ''
    if (attribute.length > 0) {
      if (($(this).attr(attribute) !== undefined) && ($(this).attr(attribute) !== value)) {
        $(this).removeAttr(attribute)
      } else {
        $(this).attr(attribute, value)
      }
    }
  }
}($))

var agent_list = '.agent-container'
var agent_panel = '#dashboard-agents'
var scan_button = 'button.scan-button'
// var agent_edit_actions_button = 'button#edit_actions'
var agent_change_name_button = 'button#change_name'
var modal_change_name = '#agent_edit_name'
var modal_change_name_form = '#change_name_form'
var modal_change_name_submit = 'a#submit_name_change'
var modal_change_name_input = 'input#new_name'

// Load agents from DB at the beginning
$(document).ready(function () {
  $(agent_list).load('/dashboard/get_mock_agents')
})

// Toggles the "loading" animation of Scan button on Dashboard
function toggleAnimateScanButton () {
  $(scan_button + ' .glyphicon').toggleClass('rotate')
  $(scan_button).toggleClass('btn-default btn-warning')
  $(scan_button).toggleAttr('disabled')
}

// Scan and pair with agents?
$(agent_panel).find(scan_button).on('click', function () {
  toggleAnimateScanButton()
  $(agent_list).load('/dashboard/get_mock_agents', function () {
    toggleAnimateScanButton()
  })
})

// Open change-name modal and get dynamic data from data-attributes to populate
$(agent_list).on('click', agent_change_name_button, function () {
  var agent_id = $(this).attr('data-agent-id').toString()
  var agent_name = $(this).attr('data-current_name')
  $(modal_change_name).find(modal_change_name_input).val(agent_name)
  $(modal_change_name).find(modal_change_name_form).attr('data-agent-id', agent_id)
})

// Substitute href-URL agent name with input and submit
$(modal_change_name).submit(function (event) {
  event.preventDefault()
  var agent_id = $(modal_change_name_form).attr('data-agent-id').toString()
  var new_name = $(modal_change_name).find(modal_change_name_input).val()
  var target_action = '/dashboard/change_name_of/' + agent_id + '/to/' + new_name
  window.location.href = target_action
})
