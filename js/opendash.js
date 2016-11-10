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

// Generic Elements
var agent_list = '.agent-container'
var agent_container = agent_list + ' .agents'
// var scan_button = 'button.scan-button'
var agent_change_name_button = 'button#change_name'
var agent_edit_actions_button = 'button#edit_actions'
// Change Name Modal Constants
var modal_change_name = '#agent_edit_name'
var modal_change_name_form = '#change_name_form'
var modal_change_name_input = 'input#new_name'
// Edit Actions Modal Constants
var modal_edit_actions = '#agent_edit_actions'
var modal_edit_actions_table = 'table#action_table'
var modal_add_action_form = '#add_action_form'
var modal_add_action_input = 'input#add_action'
var modal_add_action_submit = '#submit_edit_action'

// Load agents from DB at the beginning
$(document).ready(function () {
  $(agent_container).load('/dashboard/get_mock_agents', function () {
    if ($(agent_container + ' .agent').length <= 0) {
      $(agent_list).find('.empty-message').removeClass('hidden')
    }
    $(agent_list).find('.loading-message').hide()
  })
})

// // Toggles the "loading" animation of Scan button on Dashboard
// function toggleAnimateScanButton () {
//   $(scan_button + ' .glyphicon').toggleClass('rotate')
//   $(scan_button).toggleClass('btn-default btn-warning')
//   $(scan_button).toggleAttr('disabled')
// }

// Scan and pair with agents?
// $(agent_panel).find(scan_button).on('click', function () {
//   toggleAnimateScanButton()
//   $(agent_list).load('/dashboard/get_mock_agents', function () {
//     toggleAnimateScanButton()
//   })
// })

// Dynamically load actions if actions-modal is open
$(agent_list).on('click', agent_edit_actions_button, function () {
  var agent_id = $(this).attr('data-agent-id').toString()
  var target_url = '/dashboard/get_actions_from/' + agent_id
  $(modal_add_action_form).attr('data-agent-id', agent_id)
  $(modal_edit_actions_table).load(target_url)
})

// Send add-action if form is submitted is pressed and action_string is given
$(modal_edit_actions).on('submit', modal_add_action_form, function (event) {
  event.preventDefault()
  var agent_id = $(this).attr('data-agent-id').toString()
  var action_string = $(this).find(modal_add_action_input).val()
  var target_url = 'dashboard/add_mock_action/' + action_string + '/to/' + agent_id
  window.location.href = target_url
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
