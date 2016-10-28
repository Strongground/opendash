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

  var agent_list = '.agent-container ul'
  var agent_panel = '#dashboard-agents'
  var scan_button = 'button.scan-button'

  function toggleAnimateScanButton () {
    jQuery(scan_button + ' .glyphicon').toggleClass('rotate')
    jQuery(scan_button).toggleClass('btn-default btn-warning')
    jQuery(scan_button).toggleAttr('disabled')
  }

  jQuery(agent_panel).find(scan_button).on('click', function () {
    toggleAnimateScanButton()
    jQuery(agent_list).load('/dashboard/get_mock_agents', function () {
      toggleAnimateScanButton()
    })
  })
}(jQuery))
